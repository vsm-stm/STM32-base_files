# STM32-base_files

Данные для сборки прошивок STM32 без HAL: скачиваются в проект командой
`download_one()` из `stm32_cmake_base` (по имени пути в этом репозитории).

## Состав

| Каталог | Что внутри | Кто использует |
|---|---|---|
| `Device/<серия>/Include`, `Source` | CMSIS-заголовки устройств и `system_*.c/.h` (ST) | компилятор |
| `SVD/<серия>/` | описания периферии для отладчика (ST) | `cortex-debug` |
| `startup_c/startup_common.c` | общий стартап (Reset_Handler: .data/.bss, C++-конструкторы) | линковка |
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
