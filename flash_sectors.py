#!/usr/bin/env python3
"""
flash_sectors.py — one-shot rewrite of the cmake/STM32<F>-map.cmake files so
the flash erase-sector layout is fully explicit data, computed by nothing at
project-configure time.

For every cmake/STM32<F>-map.cmake it:

  1. keeps the legacy STM32<F>_SECTOR_MAP (FLASH_KB -> COUNT lookup) for backward
     compatibility; --drop-legacy deletes it together with its banner.

  2. appends, between markers at the end of the file, one full sector list per
     flash density found in STM32<F>_MAP - <address> <size_bytes> pairs, one
     pair per erase sector, even for uniform-page parts (F0/G0/...) where every
     size is equal:

         # >>> flash_sectors.py: BEGIN generated
         set(STM32F4_SECTORS_128K  0x08000000 16384 0x08004000 16384 ...)
         set(STM32F4_SECTORS_512K  ...)
         # <<< flash_sectors.py: END generated

The device rows are NOT touched - the flash size is already there (column 3),
so CMake just does STM32<F>_SECTORS_${STM32_FLASH} to get the ready list. No
math, nothing appended. (Dual-bank later: a STM32_DUAL_BANK-driven "_DUAL"
suffix, still not a per-row column.)

Layout model, one shape for every family:  (fixed_runs, repeat_size)
    fixed_runs   leading non-uniform sectors, as (count, size_bytes) runs
    repeat_size  the uniform sector size that fills the rest
Uniform-page families have fixed_runs == [].

Dual-bank layouts are NOT generated yet (deferred): densities above a family's
single-bank max are still emitted but flagged with a warning comment.

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

# largest single-bank flash (KB); above this a device is dual-bank only
SINGLE_BANK_MAX_KB = {"F4": 1024, "F7": 1024, "H7": 1024, "G4": 512}

BEGIN = "# >>> flash_sectors.py: BEGIN generated"
END = "# <<< flash_sectors.py: END generated"

# a device row inside set(STM32<F>_MAP ...):  NAME  cmsis  <flash>K  <ram>K  <extra>
ROW_RE = re.compile(r"^\s*STM32\w+\s+\S+\s+(\d+)K\s+\d+\S*\s+\S+\s*$")


def sectors(family: str, flash_kb: int) -> list[tuple[int, int]]:
    """-> [(address, size_bytes), ...] : the complete erase map for this size."""
    fixed, repeat = FAMILIES[family]
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


def map_densities(text: str, family: str) -> list[int]:
    """Distinct flash-KB values in STM32<F>_MAP. Rows are not modified."""
    span = find_block(text, f"STM32{family}_MAP")
    if span is None:
        return []
    block = text[span[0]:span[1]]
    return sorted({int(m.group(1)) for line in block.splitlines()
                   if (m := ROW_RE.match(line))})


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


def build_generated(family: str, densities: list[int]) -> str:
    cap = SINGLE_BANK_MAX_KB.get(family)
    lines = [
        BEGIN,
        f"# STM32{family} erase-sector maps: <address> <size> pairs, one per",
        f"# sector. Pick STM32{family}_SECTORS_${{STM32_FLASH}} for the device.",
        "# Generated by flash_sectors.py - do not edit by hand.",
    ]
    for kb in densities:
        if cap and kb > cap:
            lines.append(f"# {kb}K is dual-bank (deferred) - the list below is the "
                         f"single-bank layout and is NOT correct for it.")
        pairs = " ".join(f"0x{a:08X} {s}" for a, s in sectors(family, kb))
        lines.append(f"set(STM32{family}_SECTORS_{kb}K  {pairs})")
    lines.append(END)
    return "\n".join(lines) + "\n"


def rewrite(mapfile: Path, family: str, drop_legacy: bool = False) -> str | None:
    text = mapfile.read_text()
    densities = map_densities(text, family)
    if not densities:
        return None
    if drop_legacy:
        text = drop_sector_map(text, family)
    gen = build_generated(family, densities)
    if BEGIN in text and END in text:
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?",
                      gen, text, flags=re.DOTALL)
    else:
        text = text.rstrip("\n") + "\n\n" + gen
    return text


def verify(cmake_dir: Path) -> int:
    rx = re.compile(r"\{\s*0x([0-9A-Fa-f]+)UL\s*,\s*(\d+)UL\s*\}")
    bad = 0
    for tmpl in sorted(cmake_dir.glob("STM32*_flash_config*.h.in")):
        if "_dual" in tmpl.name:
            print(f"  [skip] {tmpl.name:<34} dual-bank - deferred")
            continue
        pairs = [(int(a, 16), int(s)) for a, s in rx.findall(tmpl.read_text())]
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
    ap.add_argument("--drop-legacy", action="store_true",
                    help="удалить устаревшие STM32<F>_SECTOR_MAP (по умолчанию остаются)")
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
        new = rewrite(mapfile, fam, args.drop_legacy)
        if new is None:
            print(f"  skip STM32{fam}: no STM32{fam}_MAP rows")
            continue
        if args.dry_run:
            print(f"\n================ {mapfile.name} ================\n{new}")
            continue
        mapfile.write_text(new)
        print(f"  updated {mapfile.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
