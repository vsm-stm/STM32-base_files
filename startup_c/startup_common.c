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

#if defined(SCB_VTOR_TBLOFF_Msk)
	SCB->VTOR = (uint32_t)(uintptr_t)vector_table;
#elif defined(STM32_IMAGE_FLASH_ORIGIN) && (STM32_IMAGE_FLASH_ORIGIN != 0x08000000U)
#error "Relocated firmware needs VTOR or a board-specific vector remap startup"
#endif
#if (__CORTEX_M >= 3U)
	__set_BASEPRI(0);
	__set_FAULTMASK(0);
#endif
	__DSB();
	__ISB();
	/* FPU stays disabled. No FP operations in global/static constructors;
	 * explicitly enable the FPU from main before using float/double.
	 */
	__libc_init_array();
	__enable_irq();
	main();
	for (;;) {}
}

