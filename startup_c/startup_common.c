/**
 * @file startup_common.c
 * @brief Shared reset runtime driven by linker copy/zero tables.
 *
 * With IRQs masked: copy initialized RAM sections byte-for-byte, zero BSS and
 * project DMA buffers, grant FPU CP10/11 when present/used, install VTOR when
 * supported, clear applicable core masks, then execute C/C++ init arrays.
 * Shared DSB/ISB complete RAM/core setup before constructors; no duplicate FPU
 * barriers are needed. Finally enable IRQs and call main; returning main spins.
 *
 * Does not call CMSIS SystemInit/system_stm32*. Peripheral clocks and F7 DMA MPU
 * attributes belong to System::Init in main (or to the plain-CMSIS application).
 * Constructors must not depend on those later peripheral/cache configurations.
 * An image relocated without VTOR requires a board-specific vector remap startup.
 */
#include <stdint.h>
#include STM32_DEVICE_HEADER

/* Linker tables contain (source, destination, byte count) and
 * (destination, byte count) records. No family-specific memory loops.
 */
extern const uint32_t __stm32_copy_table_start__[], __stm32_copy_table_end__[];
extern const uint32_t __stm32_zero_table_start__[], __stm32_zero_table_end__[];
extern uint32_t vector_table[];

/* declaration main function */
int main(void);

void __libc_init_array(void);

__attribute__((noreturn)) void Reset_Handler(void) {
	__disable_irq();
	for (const uint32_t *p = __stm32_copy_table_start__; p < __stm32_copy_table_end__; p += 3) {
		const uint8_t *src = (const uint8_t *)(uintptr_t)p[0];
		uint8_t *dst = (uint8_t *)(uintptr_t)p[1];
		for (uint32_t i = 0; i < p[2]; ++i) dst[i] = src[i];
	}
	for (const uint32_t *p = __stm32_zero_table_start__; p < __stm32_zero_table_end__; p += 2) {
		uint8_t *dst = (uint8_t *)(uintptr_t)p[0];
		for (uint32_t i = 0; i < p[1]; ++i) dst[i] = 0;
	}

#if defined(__FPU_PRESENT) && (__FPU_PRESENT == 1U) && defined(__FPU_USED) && (__FPU_USED == 1U)
	/* Enable CP10/CP11 before constructors. */
	SCB->CPACR |= (3UL << 20U) | (3UL << 22U);
#endif
#if defined(SCB_VTOR_TBLOFF_Msk)
	SCB->VTOR = (uint32_t)(uintptr_t)vector_table;
#elif defined(STM32_IMAGE_FLASH_ORIGIN) && (STM32_IMAGE_FLASH_ORIGIN != 0x08000000U)
#error "Relocated firmware needs VTOR or a board-specific vector remap startup"
#endif
#if (__CORTEX_M >= 3U)
	__set_BASEPRI(0);
	__set_FAULTMASK(0);
#endif
	/* Complete RAM initialization and core configuration before constructors. */
	__DSB();
	__ISB();
	__libc_init_array();
	__enable_irq();
	main();
	for (;;) {}
}

