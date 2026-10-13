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
| `cmake/STM32<F>-map.cmake` | chip table (flash/RAM/CCM/Flash layout), `main_cpu_PARAMS`, shared erase maps for each layout/density/mode | `cmsis-download.cmake` |
| `cmake/flash_config.h.in`, `irq_registry_config.h.in` | shared templates the drivers generate their own headers from | `STM32_Drivers_CPP` |

## Maintenance

`flash_sectors.py` rewrites `cmake/STM32<F>-map.cmake`. Each device row contains
six fields: part name, CMSIS selector, Flash size, RAM size, extra RAM size and
`FLASH_LAYOUT`. Devices with the same geometry share a layout. The generated
block contains one erase list per layout/density/mode; the presence of a
single/dual list defines the supported modes. Separate device aliases, mode
tables, sector-count tables and duplicate address/size lists are removed.
Run manually when the layout changes; idempotent. `--dry-run` only prints the result.

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
| `cmake/STM32<F>-map.cmake` | таблица чипов (flash/RAM/CCM/вариант Flash), `main_cpu_PARAMS`, общие карты стирания по варианту/объёму/режиму | `cmsis-download.cmake` |
| `cmake/flash_config.h.in`, `irq_registry_config.h.in` | общие шаблоны, из которых драйверы генерируют свои заголовки | `STM32_Drivers_CPP` |

## Обслуживание

`flash_sectors.py` переписывает `cmake/STM32<F>-map.cmake`. В строке устройства
шесть полей: имя МК, CMSIS-селектор, объём Flash, объём RAM, дополнительная RAM
и `FLASH_LAYOUT`. Устройства с одинаковой геометрией используют общий вариант.
Генерируемый блок содержит одну карту стирания по варианту/объёму/режиму;
наличие карты single/dual определяет допустимые режимы. Отдельные соответствия
устройств, таблицы режимов, количества секторов и дубли адресов/размеров удаляются.
Запускается вручную при изменении раскладки, идемпотентен; `--dry-run` только
печатает результат.

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
- The device row's FLASH_LAYOUT column selects shared format-3 records containing
  address, size, bank and hardware erase selector. Fixed dual-bank parts use
  dual; switchable parts default to single unless project.json selects dual.
- F4/F7 second-bank erase selectors start at 16. G0 uses a bank-local page
  number and BKER. G4 category-3 dual layouts preserve the address gap on
  128/256 KiB parts. H7A3/B3 use 8 KiB pages, other mapped H7 use 128 KiB sectors.
- Regenerate maps with flash_sectors.py. Use matching platform/driver versions
  and flash_config.h.in; startup's existing runtime tables remain format 2.
- Vendor system_*.c stays in this data repository but is not downloaded or
  linked by the platform. system_*.h is a required dependency of device headers.

Общий startup обслуживает таблицы копирования и обнуления всех RAM-секций до
конструкторов, выставляет VTOR и восстанавливает IRQ перед main. При наличии
и использовании аппаратного FPU startup включает его после инициализации RAM,
до конструкторов. Одна общая пара DSB/ISB завершает настройку FPU, VTOR и масок
ядра; float/double в конструкторах разрешены.
Столбец FLASH_LAYOUT в строке МК выбирает общие карты Flash формата 3: адрес, размер,
банк, аппаратный селектор стирания. У фиксированных dual-bank выбирается dual;
переключаемые по умолчанию single, явный dual задаётся в project.json.
Нумерация стирания второго банка F4/F7 начинается с 16; G0 использует локальный
номер страницы и BKER. Разрывы G4 category 3 сохранены. H7A3/B3 используют
страницы 8 КиБ, остальные H7 в карте — сектора 128 КиБ. Карты H7 не означают
реализацию его платформы. Генератор, карты, flash_config-шаблон, linker и база
обновляются совместно; существующие startup-таблицы остаются runtime формата 2.
Подробности — в BASE_FIXES.md репозитория [stm32_cmake_base](https://github.com/vsm-stm/stm32_cmake_base).
