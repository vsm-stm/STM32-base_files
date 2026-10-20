#!/usr/bin/env python3
"""
flash_sectors.py — one-shot rewrite of the cmake/STM32<F>-map.cmake files so
the flash erase-sector layout is fully explicit data, computed by nothing at
project-configure time.

The FLASH_LAYOUT column in each device row selects a shared Flash geometry.
Missing columns are filled once from the model; existing selections are kept.
For each layout/density/mode the generated block contains one list of erase
records (address, size, bank, hardware number), in layout format 3. The presence
of a single/dual list defines the supported modes. No separate device aliases,
mode tables or duplicate address/size lists are generated.

Layout model, one shape for every family:  (fixed_runs, repeat_size)
    fixed_runs   leading non-uniform sectors, as (count, size_bytes) runs
    repeat_size  the uniform sector size that fills the rest
Uniform-page families have fixed_runs == [].

Fixed dual-bank devices select dual automatically. Switchable devices default
to single; project.json may explicitly select dual. Bank address gaps are
preserved in the records, never presented as writable Flash.

    flash_sectors.py                 rewrite every cmake/STM32<F>-map.cmake
    flash_sectors.py --dry-run       print the new files, write nothing
    flash_sectors.py --verify        check the model vs the old *_flash_config*.h.in
    flash_sectors.py --cmake-dir DIR  default: ./cmake next to this script

Run it by hand when a layout needs fixing; it is idempotent.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FLASH_BASE = 0x08000000
K = 1024

# family ("F4", "G0", ...) -> (fixed_runs, repeat_size)
#   fixed_runs    leading non-uniform sectors, as (count, size_bytes) runs
#   repeat_size   int, or a callable(flash_kb) -> int when the uniform sector
#                 size depends on the device's flash density
FAMILIES: dict[str, tuple[list[tuple[int, int]], object]] = {
    # F0: <=64K parts use 1 KB pages, 128K+ parts use 2 KB (no F0 in between)
    "F0": ([], lambda kb: 1 * K if kb <= 64 else 2 * K),
    # F1: LD/MD (<=128K) 1 KB pages, HD/XL (256K+) 2 KB
    "F1": ([], lambda kb: 1 * K if kb <= 128 else 2 * K),
    "F2": ([(4, 16 * K), (1, 64 * K)], 128 * K),
    "F3": ([], 2 * K),
    "F4": ([(4, 16 * K), (1, 64 * K)], 128 * K),
    "F7": ([(4, 32 * K), (1, 128 * K)], 256 * K),
    "G0": ([], 2 * K),
    "G4": ([], 2 * K),
    "H7": ([], 128 * K),        # 128 KB sectors (H7A3/B3 are 8 KB)
    "L0": ([], 128),
    "L1": ([], 256),
    "C0": ([], 2 * K),
}

F7_SMALL_MODELS = {"stm32f722xx", "stm32f723xx", "stm32f730xx", "stm32f732xx", "stm32f733xx"}
G4_WIDE_MODELS = {"stm32g471xx", "stm32g473xx", "stm32g474xx", "stm32g483xx", "stm32g484xx"}
F4_BANKED_MODELS = {f"stm32f{part}xx" for part in (427, 429, 437, 439, 469, 479)}
F7_BANKED_MODELS = {f"stm32f{part}xx" for part in (765, 767, 769, 777, 779)}
L0_BANKED_MODELS = {f"stm32l{part:03d}xx" for part in (71, 72, 73, 81, 82, 83)}

BEGIN = "# >>> flash_sectors.py: BEGIN generated"
END = "# <<< flash_sectors.py: END generated"

# Device row: NAME cmsis <flash>K <ram>K <extra> [FLASH_LAYOUT].
ROW_RE = re.compile(r"^\s*STM32\w+\s+\S+\s+(\d+)K\s+\d+\S*\s+\S+(?:\s+\S+)?\s*$")


def sectors(family: str, flash_kb: int, *, small_f7: bool = False, wide_g4: bool = False) -> list[tuple[int, int]]:
    """-> [(address, size_bytes), ...] : the complete erase map for this size."""
    fixed, repeat = FAMILIES["F4" if small_f7 else family]
    if wide_g4:
        fixed, repeat = [], 4 * K
    if callable(repeat):
        repeat = repeat(flash_kb)
    flash = flash_kb * K
    sizes: list[int] = []
    used = 0
    for count, size in fixed:
        for _ in range(count):
            if used + size > flash:
                break
            sizes.append(size)
            used += size
    while used + repeat <= flash:
        sizes.append(repeat)
        used += repeat
    if used != flash:
        print(f"  WARNING {family} {flash_kb}K: covered {used}/{flash} B", file=sys.stderr)

    addr, out = FLASH_BASE, []
    for size in sizes:
        out.append((addr, size))
        addr += size
    return out


def find_block(text: str, name: str) -> tuple[int, int] | None:
    """(start, end) char offsets of `set(<name> ... )`, incl. the closing line."""
    m = re.search(rf"^set\(\s*{re.escape(name)}\b", text, re.MULTILINE)
    if not m:
        return None
    close = re.compile(r"^\)\s*$", re.MULTILINE)
    c = close.search(text, m.end())
    if not c:
        sys.exit(f"flash_sectors: no closing ) for set({name})")
    return m.start(), c.end()


def drop_sector_map(text: str, family: str) -> str:
    """Remove set(STM32<F>_SECTOR_MAP ...) and the comment banner above it."""
    span = find_block(text, f"STM32{family}_SECTOR_MAP")
    if span is None:
        return text
    start = span[0]
    # walk back over contiguous comment / blank lines
    lines_before = text[:start].splitlines(keepends=True)
    while lines_before and (lines_before[-1].lstrip().startswith("#")
                            or not lines_before[-1].strip()):
        start -= len(lines_before.pop())
    return text[:start].rstrip("\n") + "\n" + text[span[1]:].lstrip("\n")


def layout_name(family: str, model: str, kb: int) -> str:
    if family == "F4" and model in F4_BANKED_MODELS:
        return "STM32F4_BANKED"
    if family == "F7":
        if model in F7_SMALL_MODELS:
            return "STM32F7_SMALL"
        if model in F7_BANKED_MODELS:
            return "STM32F7_BANKED"
    if family == "G4" and model in G4_WIDE_MODELS:
        return "STM32G4_BANKED"
    if family == "G0" and model in {"stm32g0b1xx", "stm32g0c1xx"}:
        return "STM32G0_BANKED"
    if family == "G0" and model == "stm32g0b0xx":
        return "STM32G0_FIXED_DUAL"
    if family == "H7" and model in {"stm32h7a3xx", "stm32h7b3xx", "stm32h7b0xx"}:
        return "STM32H7_SMALL_PAGE"
    if family == "L0" and model in L0_BANKED_MODELS and kb >= 128:
        return "STM32L0_BANKED"
    return f"STM32{family}"


# Return supported modes only. A fixed dual layout has no synthetic single mode;
# switchable layouts emit both lists and let the base choose the requested/default.
def bank_modes(layout: str, kb: int) -> tuple[str, ...]:
    if layout == "STM32F4_BANKED":
        return ("dual",) if kb == 2048 else (("single", "dual") if kb == 1024 else ("single",))
    if layout == "STM32F7_BANKED" or layout == "STM32G4_BANKED":
        return ("single", "dual")
    if layout == "STM32G0_BANKED":
        return ("dual",) if kb == 512 else (("single", "dual") if kb == 256 else ("single",))
    if layout == "STM32G0_FIXED_DUAL":
        return ("dual",)
    if layout.startswith("STM32H7") and kb == 2048:
        return ("dual",)
    if layout == "STM32F1" and kb > 512:
        return ("dual",)
    if layout == "STM32L1" and kb >= 384:
        return ("dual",)
    if layout == "STM32L0_BANKED":
        return ("dual",)
    return ("single",)


# Physical bank numbering and register selector are retained independently of the
# array index. G4 bank 2 starts at its hardware window even when bank 1 is smaller,
# preserving the unmapped gap instead of inventing writable addresses.
def erase_records(layout: str, kb: int, mode: str) -> list[tuple[int, int, int, int]]:
    """Records are in address order; number is the register's erase selector."""
    family = layout[5:7]
    if mode == "single":
        pairs = sectors(family, kb, small_f7=layout == "STM32F7_SMALL",
                        wide_g4=layout == "STM32G4_BANKED")
        if layout == "STM32H7_SMALL_PAGE":
            pairs = [(FLASH_BASE + i * 8 * K, 8 * K) for i in range(kb // 8)]
        return [(a, s, 1, i + (4 if family == "F4" and i >= 12 else 0))
                for i, (a, s) in enumerate(pairs)]

    bank1_kb = 512 if family == "F1" else kb // 2
    bank2_kb = kb - bank1_kb
    bank2_base = FLASH_BASE + (256 * K if layout == "STM32G4_BANKED" else bank1_kb * K)
    records = []
    for bank, base, capacity in ((1, FLASH_BASE, bank1_kb), (2, bank2_base, bank2_kb)):
        if family in {"F4", "F7"}:
            pairs = sectors("F4", capacity)
        elif layout == "STM32G4_BANKED":
            pairs = sectors("G4", capacity)
        elif layout == "STM32H7_SMALL_PAGE":
            pairs = [(FLASH_BASE + i * 8 * K, 8 * K) for i in range(capacity // 8)]
        else:
            pairs = sectors(family, capacity)
        for number, (address, size) in enumerate(pairs):
            hardware = number + (16 if bank == 2 and family in {"F4", "F7"} else 0)
            records.append((base + address - FLASH_BASE, size, bank, hardware))
    return records


def build_generated(layouts: set[tuple[str, int]]) -> str:
    lines = [
        BEGIN,
        "set(STM32_FLASH_LAYOUT_VERSION 3)",
        "# Mode-specific erase records: <address> <size> <bank> <hardware number>.",
        "# Generated by flash_sectors.py - do not edit by hand.",
    ]
    for layout, kb in sorted(layouts):
        modes = bank_modes(layout, kb)
        for mode in modes:
            records = " ".join(f"0x{a:08X} {s} {bank} {number}"
                               for a, s, bank, number in erase_records(layout, kb, mode))
            lines.append(f"set({layout}_ERASE_{mode}_{kb}K {records})")
    lines.append(END)
    return "\n".join(lines) + "\n"


# Preserve an existing row's explicit FLASH_LAYOUT and rebuild only the generated
# erase-record block. The row and generated lists are the sole lookup inputs;
# do not restore separate per-model alias/mode tables.
def rewrite(mapfile: Path, family: str) -> str | None:
    text = mapfile.read_text(encoding="utf-8")
    text = drop_sector_map(text, family)
    span = find_block(text, f"STM32{family}_MAP")
    if span is None:
        return None
    rows = text[span[0]:span[1]].splitlines()
    layouts = set()
    for index, row in enumerate(rows):
        if not ROW_RE.match(row):
            continue
        fields = row.split()
        kb = int(fields[2][:-1])
        layout = fields[5] if len(fields) == 6 else layout_name(family, fields[1], kb)
        if len(fields) == 5:
            rows[index] = row.rstrip() + "  " + layout
        layouts.add((layout, kb))
    if not layouts:
        return None
    text = text[:span[0]] + "\n".join(rows) + text[span[1]:]
    text = re.sub(r"^(# STM32_FULL_NAME[^\n]*?)(?:\s+FLASH_LAYOUT)?$",
                  r"\1  FLASH_LAYOUT", text, flags=re.MULTILINE)
    gen = build_generated(layouts)
    if BEGIN in text and END in text:
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?",
                      gen, text, flags=re.DOTALL)
    else:
        text = text.rstrip("\n") + "\n\n" + gen
    return text


# Legacy comparison tool: only compares old per-device templates that still exist.
# With no such templates it does not validate the current generated map corpus.
def verify(cmake_dir: Path) -> int:
    rx = re.compile(r"\{\s*0x([0-9A-Fa-f]+)UL\s*,\s*(\d+)UL\s*\}")
    bad = 0
    for tmpl in sorted(cmake_dir.glob("STM32*_flash_config*.h.in")):
        if "_dual" in tmpl.name:
            print(f"  [skip] {tmpl.name:<34} dual-bank - deferred")
            continue
        pairs = [(int(a, 16), int(s)) for a, s in rx.findall(tmpl.read_text(encoding="utf-8"))]
        if not pairs:
            continue
        fam = tmpl.name[5:7]
        total_kb = sum(s for _, s in pairs) // K
        got = sectors(fam, total_kb)
        ok = got == pairs
        bad += 0 if ok else 1
        print(f"  [{'ok  ' if ok else 'DIFF'}] {tmpl.name:<34} {fam} {total_kb}K")
        if not ok:
            print(f"          template: {pairs}\n          computed: {got}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cmake-dir", type=Path)
    args = ap.parse_args()

    cmake_dir = args.cmake_dir or (Path(__file__).resolve().parent / "cmake")
    if not cmake_dir.is_dir():
        sys.exit(f"flash_sectors: {cmake_dir} not found")

    if args.verify:
        print(f"verifying vs {cmake_dir}/*_flash_config*.h.in ...")
        n = verify(cmake_dir)
        print("all match" if n == 0 else f"{n} mismatch(es)")
        return 1 if n else 0

    for fam in FAMILIES:
        mapfile = cmake_dir / f"STM32{fam}-map.cmake"
        if not mapfile.is_file():
            print(f"  skip STM32{fam}: no map file")
            continue
        new = rewrite(mapfile, fam)
        if new is None:
            print(f"  skip STM32{fam}: no STM32{fam}_MAP rows")
            continue
        if args.dry_run:
            print(f"\n================ {mapfile.name} ================\n{new}")
            continue
        if new != mapfile.read_text(encoding="utf-8"):
            mapfile.write_text(new, encoding="utf-8")
            print(f"  updated {mapfile.name}")
        else:
            print(f"  unchanged {mapfile.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
