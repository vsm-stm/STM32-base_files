# STM32-base_files

*[English](#english) · [Русский](#русский)*

---

## English

Data for building STM32 firmware without HAL: downloaded into a project by
`download_one()` from `stm32_cmake_base` (by path name, from this repository).

## Contents

| Directory | What's inside | Used by |
|---|---|---|
| `Device/<series>/Include`, `Source` | CMSIS device headers and `system_*.c/.h` (ST) | the compiler |
| `SVD/<series>/` | peripheral descriptions for the debugger (ST) | `cortex-debug` |
| `startup_c/startup_common.c` | shared startup (copy/zero tables, VTOR/IRQ, C++ constructors) | linking |
| `startup_c/<series>/vector_<chip>.c` | the chip's interrupt vector table | linking, driver IRQ-stub generation |
| `linker/` | linker script templates: `simple`, `ccm`, `f7` | `stm32_add_firmware()` |
| `cmake/STM32<F>-map.cmake` | chip table (flash/RAM/CCM), `main_cpu_PARAMS`, erase-sector lists `STM32<F>_SECTORS_<n>K` | `cmsis-download.cmake` |
| `cmake/flash_config.h.in`, `irq_registry_config.h.in` | shared templates the drivers generate their own headers from | `STM32_Drivers_CPP` |

## Maintenance

`flash_sectors.py` rewrites `cmake/STM32<F>-map.cmake`: it drops the stale
`STM32<F>_SECTOR_MAP` and appends ready-made erase-sector lists for every
flash size. Run manually when the layout changes; idempotent. `--dry-run`
only prints the result.

## Licenses

The repository's own files are MIT (`LICENSE`). ST's files (`Device/`, `SVD/`)
keep their STMicroelectronics license (Apache-2.0). Details, exceptions, and
the list of files without an explicit license are in `THIRD_PARTY.md`.

---

## Русский

Данные для сборки прошивок STM32 без HAL: скачиваются в проект командой
`download_one()` из `stm32_cmake_base` (по имени пути в этом репозитории).

## Состав

| Каталог | Что внутри | Кто использует |
|---|---|---|
| `Device/<серия>/Include`, `Source` | CMSIS-заголовки устройств и `system_*.c/.h` (ST) | компилятор |
| `SVD/<серия>/` | описания периферии для отладчика (ST) | `cortex-debug` |
| `startup_c/startup_common.c` | общий стартап (copy/zero tables, VTOR/IRQ, C++-конструкторы) | линковка |
| `startup_c/<серия>/vector_<чип>.c` | таблица векторов прерываний чипа | линковка, генерация IRQ-заглушек драйверов |
| `linker/` | шаблоны линкер-скриптов: `simple`, `ccm`, `f7` | `stm32_add_firmware()` |
| `cmake/STM32<F>-map.cmake` | таблица чипов (flash/RAM/CCM), `main_cpu_PARAMS`, списки секторов `STM32<F>_SECTORS_<n>K` | `cmsis-download.cmake` |
| `cmake/flash_config.h.in`, `irq_registry_config.h.in` | общие шаблоны, из которых драйверы генерируют свои заголовки | `STM32_Drivers_CPP` |

## Обслуживание

`flash_sectors.py` переписывает `cmake/STM32<F>-map.cmake`: убирает устаревшую
`STM32<F>_SECTOR_MAP` и дописывает готовые списки секторов стирания по каждому
объёму флеша. Запускается вручную при изменении раскладки, идемпотентен;
`--dry-run` только печатает результат.

## Лицензии

Собственные файлы репозитория — MIT (`LICENSE`). Файлы ST (`Device/`, `SVD/`)
сохраняют лицензии STMicroelectronics (Apache-2.0). Подробности, исключения и
список файлов без явной лицензии — в `THIRD_PARTY.md`.

## Runtime/layout format 2 / Формат runtime/layout 2

- Startup and all three linker templates use matching copy/zero tables with
  byte lengths and `__stm32_` symbol names. CCM/ITCM/DTCM/SRAM2 initialize
  automatically before constructors; .ccmram_bss is NOLOAD.
- With `__FPU_PRESENT == 1` and `__FPU_USED == 1`, startup enables CP10/CP11
  access through `SCB->CPACR` after RAM initialization. One shared `DSB`/`ISB`
  pair follows FPU/VTOR/core mask configuration before constructors.
  Constructors may use float/double. Devices/builds without
  hardware FPU use omit this block.
- Single-bank only: F72/F73 geometry is 16/64/128 KiB, other supported F7
  layouts 32/128/256 KiB. G4 category 3 single-bank pages are 4 KiB. Actual
  option bytes must match this mode. F4 2 MiB has no supported single-bank list.
- Update startup/linker/maps together; run flash_sectors.py to regenerate
  format-2 maps. Regeneration does not rewrite files whose contents match.
- Vendor system_*.c stays in this data repository but is not downloaded or
  linked by the platform. system_*.h is a required dependency of device headers.

Общий startup обслуживает таблицы копирования и обнуления всех RAM-секций до
конструкторов, выставляет VTOR и восстанавливает IRQ перед main. При наличии
и использовании аппаратного FPU startup включает его после инициализации RAM,
до конструкторов. Одна общая пара DSB/ISB завершает настройку FPU, VTOR и масок
ядра; float/double в конструкторах разрешены.
Dual-bank не реализован. Startup, linker и maps обновляются совместно.
Подробности — в BASE_FIXES.md репозитория [stm32_cmake_base](https://github.com/vsm-stm/stm32_cmake_base).
