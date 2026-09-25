#include <stdint.h>

void Default_Handler(void) {
	while(1) {}
}

extern uint32_t _estack;

void Reset_Handler(void)						__attribute__ ((weak, alias("Default_Handler")));
void NMI_Handler(void)						__attribute__ ((weak, alias("Default_Handler")));
void HardFault_Handler(void)						__attribute__ ((weak, alias("Default_Handler")));
void SVC_Handler(void)						__attribute__ ((weak, alias("Default_Handler")));
void PendSV_Handler(void)						__attribute__ ((weak, alias("Default_Handler")));
void SysTick_Handler(void)						__attribute__ ((weak, alias("Default_Handler")));
void WWDG_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void RTC_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void FLASH_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void RCC_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void EXTI0_1_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void EXTI2_3_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void EXTI4_15_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void DMA1_Channel1_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void DMA1_Channel2_3_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void DMA1_Channel4_5_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void ADC1_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void TIM1_BRK_UP_TRG_COM_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void TIM1_CC_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void TIM3_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void TIM14_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void TIM16_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void TIM17_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void I2C1_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void SPI1_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));
void USART1_IRQHandler(void)						__attribute__ ((weak, alias("Default_Handler")));

__attribute__ ((section(".isr_vector")))
uint32_t vector_table[] = {
	(uint32_t) &_estack,
	(uint32_t) Reset_Handler,
	(uint32_t) NMI_Handler,
	(uint32_t) HardFault_Handler,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) SVC_Handler,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) PendSV_Handler,
	(uint32_t) SysTick_Handler,
	(uint32_t) WWDG_IRQHandler,
	(uint32_t) 0,
	(uint32_t) RTC_IRQHandler,
	(uint32_t) FLASH_IRQHandler,
	(uint32_t) RCC_IRQHandler,
	(uint32_t) EXTI0_1_IRQHandler,
	(uint32_t) EXTI2_3_IRQHandler,
	(uint32_t) EXTI4_15_IRQHandler,
	(uint32_t) 0,
	(uint32_t) DMA1_Channel1_IRQHandler,
	(uint32_t) DMA1_Channel2_3_IRQHandler,
	(uint32_t) DMA1_Channel4_5_IRQHandler,
	(uint32_t) ADC1_IRQHandler,
	(uint32_t) TIM1_BRK_UP_TRG_COM_IRQHandler,
	(uint32_t) TIM1_CC_IRQHandler,
	(uint32_t) 0,
	(uint32_t) TIM3_IRQHandler,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) TIM14_IRQHandler,
	(uint32_t) 0,
	(uint32_t) TIM16_IRQHandler,
	(uint32_t) TIM17_IRQHandler,
	(uint32_t) I2C1_IRQHandler,
	(uint32_t) 0,
	(uint32_t) SPI1_IRQHandler,
	(uint32_t) 0,
	(uint32_t) USART1_IRQHandler,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) 0,
	(uint32_t) 0,
};
