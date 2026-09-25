# ============================================================
# STM32F4 full MCU map (ST.com / datasheets)
# STM32_FULL_NAME  NAME         FLASH_KB  RAM_KB  CCMRAM_KB
# ============================================================

set(main_cpu_PARAMS
	-mcpu=cortex-m4
	-mthumb
	-mfpu=fpv4-sp-d16
	-mfloat-abi=hard
)

set(STM32F4_MAP

  # ----------------------------------------------------------
  # STM32F401 (0 CCM)
  # Up to 256KB Flash / 64KB SRAM (no CCM) :contentReference[oaicite:0]{index=0}
  # ----------------------------------------------------------
  STM32F401CB  stm32f401xc    128K   64K   0K
  STM32F401RB  stm32f401xc    128K   64K   0K
  STM32F401VB  stm32f401xc    128K   64K   0K

  STM32F401CC  stm32f401xc    256K   64K   0K
  STM32F401RC  stm32f401xc    256K   64K   0K
  STM32F401VC  stm32f401xc    256K   64K   0K

  STM32F401CD  stm32f401xe    384K   96K   0K
  STM32F401RD  stm32f401xe    384K   96K   0K
  STM32F401VD  stm32f401xe    384K   96K   0K

  STM32F401CE  stm32f401xe    512K   96K   0K
  STM32F401RE  stm32f401xe    512K   96K   0K
  STM32F401VE  stm32f401xe    512K   96K   0K

  # ----------------------------------------------------------
  # STM32F405 (64K CCM)
  # Up to 192+4KB SRAM including 64KB CCM :contentReference[oaicite:1]{index=1}
  # ----------------------------------------------------------
  STM32F405OE  stm32f405xx    512K  192K  64K

  STM32F405RG  stm32f405xx   1024K  192K  64K
  STM32F405OG  stm32f405xx   1024K  192K  64K
  STM32F405VG  stm32f405xx   1024K  192K  64K
  STM32F405ZG  stm32f405xx   1024K  192K  64K

  # ----------------------------------------------------------
  # STM32F407 (64K CCM)
  # Up to 192+4KB SRAM including 64KB CCM :contentReference[oaicite:2]{index=2}
  # ----------------------------------------------------------
  STM32F407VE  stm32f407xx    512K  192K  64K
  STM32F407ZE  stm32f407xx    512K  192K  64K
  STM32F407IE  stm32f407xx    512K  192K  64K

  STM32F407VG  stm32f407xx   1024K  192K  64K
  STM32F407ZG  stm32f407xx   1024K  192K  64K
  STM32F407IG  stm32f407xx   1024K  192K  64K

  # ----------------------------------------------------------
  # STM32F410 (0 CCM)
  # STM32F410x8/xB: up to 128KB Flash / 32KB RAM :contentReference[oaicite:3]{index=3}
  # ----------------------------------------------------------
  STM32F410C8  stm32f410cx     64K   32K   0K
  STM32F410R8  stm32f410rx     64K   32K   0K
  STM32F410T8  stm32f410tx     64K   32K   0K

  STM32F410CB  stm32f410cx    128K   32K   0K
  STM32F410RB  stm32f410rx    128K   32K   0K
  STM32F410TB  stm32f410tx    128K   32K   0K

  # ----------------------------------------------------------
  # STM32F411 (0 CCM)
  # Up to 512KB Flash / 128KB SRAM :contentReference[oaicite:4]{index=4}
  # ----------------------------------------------------------
  STM32F411CC  stm32f411xc    256K  128K   0K
  STM32F411RC  stm32f411xc    256K  128K   0K
  STM32F411VC  stm32f411xc    256K  128K   0K

  STM32F411CE  stm32f411xe    512K  128K   0K
  STM32F411RE  stm32f411xe    512K  128K   0K
  STM32F411VE  stm32f411xe    512K  128K   0K

  # ----------------------------------------------------------
  # STM32F412 (0 CCM)
  # Up to 1MB Flash / 256KB SRAM :contentReference[oaicite:5]{index=5}
  # ----------------------------------------------------------
  STM32F412CE  stm32f412cx    512K  256K   0K
  STM32F412RE  stm32f412rx    512K  256K   0K
  STM32F412VE  stm32f412vx    512K  256K   0K
  STM32F412ZE  stm32f412zx    512K  256K   0K

  STM32F412CG  stm32f412cx   1024K  256K   0K
  STM32F412RG  stm32f412rx   1024K  256K   0K
  STM32F412VG  stm32f412vx   1024K  256K   0K
  STM32F412ZG  stm32f412zx   1024K  256K   0K

  # ----------------------------------------------------------
  # STM32F413 / STM32F423 (64K CCM)
  # SRAM system 320 (256 + 64) → 64KB CCM :contentReference[oaicite:6]{index=6}
  # ----------------------------------------------------------
  STM32F413CG  stm32f413xx   1024K  320K  64K
  STM32F413RG  stm32f413xx   1024K  320K  64K
  STM32F413MG  stm32f413xx   1024K  320K  64K
  STM32F413VG  stm32f413xx   1024K  320K  64K
  STM32F413ZG  stm32f413xx   1024K  320K  64K

  STM32F413CH  stm32f413xx   1536K  320K  64K
  STM32F413RH  stm32f413xx   1536K  320K  64K
  STM32F413MH  stm32f413xx   1536K  320K  64K
  STM32F413VH  stm32f413xx   1536K  320K  64K
  STM32F413ZH  stm32f413xx   1536K  320K  64K

  STM32F423CH  stm32f423xx   1536K  320K  64K
  STM32F423RH  stm32f423xx   1536K  320K  64K
  STM32F423MH  stm32f423xx   1536K  320K  64K
  STM32F423VH  stm32f423xx   1536K  320K  64K
  STM32F423ZH  stm32f423xx   1536K  320K  64K

  # ----------------------------------------------------------
  # STM32F415 (64K CCM)  — same memory class as F405/407 :contentReference[oaicite:7]{index=7}
  # ----------------------------------------------------------
  STM32F415RG  stm32f415xx   1024K  192K  64K
  STM32F415OG  stm32f415xx   1024K  192K  64K
  STM32F415VG  stm32f415xx   1024K  192K  64K
  STM32F415ZG  stm32f415xx   1024K  192K  64K

  # ----------------------------------------------------------
  # STM32F417 (64K CCM)  — same memory class as F405/407 :contentReference[oaicite:8]{index=8}
  # ----------------------------------------------------------
  STM32F417VE  stm32f417xx    512K  192K  64K
  STM32F417ZE  stm32f417xx    512K  192K  64K
  STM32F417IE  stm32f417xx    512K  192K  64K

  STM32F417VG  stm32f417xx   1024K  192K  64K
  STM32F417ZG  stm32f417xx   1024K  192K  64K
  STM32F417IG  stm32f417xx   1024K  192K  64K

  # ----------------------------------------------------------
  # STM32F427 (64K CCM)
  # Up to 256+4KB SRAM including 64KB CCM :contentReference[oaicite:9]{index=9}
  # ----------------------------------------------------------
  STM32F427VG  stm32f427xx   1024K  256K  64K
  STM32F427ZG  stm32f427xx   1024K  256K  64K
  STM32F427AG  stm32f427xx   1024K  256K  64K
  STM32F427IG  stm32f427xx   1024K  256K  64K

  STM32F427VI  stm32f427xx   2048K  256K  64K
  STM32F427ZI  stm32f427xx   2048K  256K  64K
  STM32F427AI  stm32f427xx   2048K  256K  64K
  STM32F427II  stm32f427xx   2048K  256K  64K

  # ----------------------------------------------------------
  # STM32F429 (64K CCM)
  # Up to 256+4KB SRAM including 64KB CCM :contentReference[oaicite:10]{index=10}
  # ----------------------------------------------------------
  STM32F429VE  stm32f429xx   1024K  256K  64K
  STM32F429ZE  stm32f429xx   1024K  256K  64K
  STM32F429IE  stm32f429xx   1024K  256K  64K
  STM32F429BE  stm32f429xx   1024K  256K  64K
  STM32F429NE  stm32f429xx   1024K  256K  64K

  STM32F429VG  stm32f429xx   1024K  256K  64K
  STM32F429ZG  stm32f429xx   1024K  256K  64K
  STM32F429AG  stm32f429xx   1024K  256K  64K
  STM32F429IG  stm32f429xx   1024K  256K  64K
  STM32F429BG  stm32f429xx   1024K  256K  64K
  STM32F429NG  stm32f429xx   1024K  256K  64K

  STM32F429VI  stm32f429xx   2048K  256K  64K
  STM32F429ZI  stm32f429xx   2048K  256K  64K
  STM32F429AI  stm32f429xx   2048K  256K  64K
  STM32F429II  stm32f429xx   2048K  256K  64K
  STM32F429BI  stm32f429xx   2048K  256K  64K
  STM32F429NI  stm32f429xx   2048K  256K  64K

  # ----------------------------------------------------------
  # STM32F437 (64K CCM) — same memory class as F427/F429 :contentReference[oaicite:11]{index=11}
  # ----------------------------------------------------------
  STM32F437VG  stm32f437xx   1024K  256K  64K
  STM32F437ZG  stm32f437xx   1024K  256K  64K
  STM32F437IG  stm32f437xx   1024K  256K  64K

  STM32F437VI  stm32f437xx   2048K  256K  64K
  STM32F437ZI  stm32f437xx   2048K  256K  64K
  STM32F437AI  stm32f437xx   2048K  256K  64K
  STM32F437II  stm32f437xx   2048K  256K  64K

  # ----------------------------------------------------------
  # STM32F439 (64K CCM) — same memory class as F427/F429 :contentReference[oaicite:12]{index=12}
  # ----------------------------------------------------------
  STM32F439VG  stm32f439xx   1024K  256K  64K
  STM32F439ZG  stm32f439xx   1024K  256K  64K
  STM32F439IG  stm32f439xx   1024K  256K  64K
  STM32F439NG  stm32f439xx   1024K  256K  64K
  STM32F439BG  stm32f439xx   1024K  256K  64K

  STM32F439VI  stm32f439xx   2048K  256K  64K
  STM32F439ZI  stm32f439xx   2048K  256K  64K
  STM32F439AI  stm32f439xx   2048K  256K  64K
  STM32F439II  stm32f439xx   2048K  256K  64K
  STM32F439BI  stm32f439xx   2048K  256K  64K
  STM32F439NI  stm32f439xx   2048K  256K  64K

  # ----------------------------------------------------------
  # STM32F446 (0 CCM)
  # Up to 512KB Flash / 128+4KB RAM (no CCM) :contentReference[oaicite:13]{index=13}
  # ----------------------------------------------------------
  STM32F446RC  stm32f446xx    256K  128K   0K
  STM32F446MC  stm32f446xx    256K  128K   0K
  STM32F446VC  stm32f446xx    256K  128K   0K
  STM32F446ZC  stm32f446xx    256K  128K   0K

  STM32F446RE  stm32f446xx    512K  128K   0K
  STM32F446ME  stm32f446xx    512K  128K   0K
  STM32F446VE  stm32f446xx    512K  128K   0K
  STM32F446ZE  stm32f446xx    512K  128K   0K

  # ----------------------------------------------------------
  # STM32F469 (64K CCM)
  # Up to 384+4KB SRAM including 64KB CCM :contentReference[oaicite:14]{index=14}
  # ----------------------------------------------------------
  STM32F469AE  stm32f469xx    512K  384K  64K
  STM32F469AG  stm32f469xx   1024K  384K  64K
  STM32F469AI  stm32f469xx   2048K  384K  64K

  STM32F469BE  stm32f469xx    512K  384K  64K
  STM32F469BG  stm32f469xx   1024K  384K  64K
  STM32F469BI  stm32f469xx   2048K  384K  64K

  STM32F469IE  stm32f469xx    512K  384K  64K
  STM32F469IG  stm32f469xx   1024K  384K  64K
  STM32F469II  stm32f469xx   2048K  384K  64K

  STM32F469NE  stm32f469xx    512K  384K  64K
  STM32F469NG  stm32f469xx   1024K  384K  64K
  STM32F469NI  stm32f469xx   2048K  384K  64K

  STM32F469VE  stm32f469xx    512K  384K  64K
  STM32F469VG  stm32f469xx   1024K  384K  64K
  STM32F469VI  stm32f469xx   2048K  384K  64K

  STM32F469ZE  stm32f469xx    512K  384K  64K
  STM32F469ZG  stm32f469xx   1024K  384K  64K
  STM32F469ZI  stm32f469xx   2048K  384K  64K

  # ----------------------------------------------------------
  # STM32F479 (64K CCM) — same memory class as F469 :contentReference[oaicite:15]{index=15}
  # ----------------------------------------------------------
  STM32F479AG  stm32f479xx   1024K  384K  64K
  STM32F479BG  stm32f479xx   1024K  384K  64K
  STM32F479IG  stm32f479xx   1024K  384K  64K
  STM32F479NG  stm32f479xx   1024K  384K  64K
  STM32F479VG  stm32f479xx   1024K  384K  64K
  STM32F479ZG  stm32f479xx   1024K  384K  64K

  STM32F479AI  stm32f479xx   2048K  384K  64K
  STM32F479BI  stm32f479xx   2048K  384K  64K
  STM32F479II  stm32f479xx   2048K  384K  64K
  STM32F479NI  stm32f479xx   2048K  384K  64K
  STM32F479VI  stm32f479xx   2048K  384K  64K
  STM32F479ZI  stm32f479xx   2048K  384K  64K
)

# ============================================================
# LEGACY, will be removed in future releases
# STM32F4 flash sector count lookup
#
# Single-bank sector counts (dual-bank = count * 2).
# Set STM32_DUAL_BANK=ON in base-setup.cmake to enable dual.
#
# Lookup table: FLASH_KB  SECTOR_COUNT
# ============================================================
set(STM32F4_SECTOR_MAP
  #  FLASH_KB  SECTOR_COUNT
      64        4
      128       5
      256       6
      512       8
      1024      12
      2048      12
)

# >>> flash_sectors.py: BEGIN generated
# STM32F4 erase-sector maps: <address> <size> pairs, one per
# sector. Pick STM32F4_SECTORS_${STM32_FLASH} for the device.
# Generated by flash_sectors.py - do not edit by hand.
set(STM32F4_SECTORS_64K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384)
set(STM32F4_SECTORS_128K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384 0x08010000 65536)
set(STM32F4_SECTORS_256K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384 0x08010000 65536 0x08020000 131072)
set(STM32F4_SECTORS_384K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384 0x08010000 65536 0x08020000 131072 0x08040000 131072)
set(STM32F4_SECTORS_512K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384 0x08010000 65536 0x08020000 131072 0x08040000 131072 0x08060000 131072)
set(STM32F4_SECTORS_1024K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384 0x08010000 65536 0x08020000 131072 0x08040000 131072 0x08060000 131072 0x08080000 131072 0x080A0000 131072 0x080C0000 131072 0x080E0000 131072)
# 1536K is dual-bank (deferred) - the list below is the single-bank layout and is NOT correct for it.
set(STM32F4_SECTORS_1536K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384 0x08010000 65536 0x08020000 131072 0x08040000 131072 0x08060000 131072 0x08080000 131072 0x080A0000 131072 0x080C0000 131072 0x080E0000 131072 0x08100000 131072 0x08120000 131072 0x08140000 131072 0x08160000 131072)
# 2048K is dual-bank (deferred) - the list below is the single-bank layout and is NOT correct for it.
set(STM32F4_SECTORS_2048K  0x08000000 16384 0x08004000 16384 0x08008000 16384 0x0800C000 16384 0x08010000 65536 0x08020000 131072 0x08040000 131072 0x08060000 131072 0x08080000 131072 0x080A0000 131072 0x080C0000 131072 0x080E0000 131072 0x08100000 131072 0x08120000 131072 0x08140000 131072 0x08160000 131072 0x08180000 131072 0x081A0000 131072 0x081C0000 131072 0x081E0000 131072)
# <<< flash_sectors.py: END generated
