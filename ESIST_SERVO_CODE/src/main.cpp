#include <stdio.h>
#include <stdlib.h>
#include "hardware/pwm.h"

// Pin definition (using GPIO 0)
#define SERVO_PIN 0

// Servo pulse width constants (in microseconds)
#define SERVO_MIN_PULSE 500   // 0 degrees
#define SERVO_MAX_PULSE 2500  // 180 degrees
#define SERVO_FREQ 50         // 50Hz = 20ms period

void set_servo_angle(uint pin, float angle) {
    // Ensure angle is between 0 and 180
    if (angle < 0) angle = 0;
    if (angle > 180) angle = 180;

    // Calculate pulse width for given angle
    uint32_t pulse_width = SERVO_MIN_PULSE + ((SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle) / 180.0;
    
    // Get PWM slice and channel for the pin
    uint slice_num = pwm_gpio_to_slice_num(pin);
    uint channel = pwm_gpio_to_channel(pin);

    // Set frequency (20ms period = 50Hz)
    pwm_set_clkdiv(slice_num, 125.0f);  // 125MHz / 125 = 1MHz clock
    pwm_set_wrap(slice_num, 20000);     // 1MHz / 20000 = 50Hz
    
    // Set duty cycle
    pwm_set_chan_level(slice_num, channel, pulse_width);
    
    // Enable PWM
    pwm_set_enabled(slice_num, true);
}

int main() {
    // Initialize chosen pin as PWM
    gpio_set_function(SERVO_PIN, GPIO_FUNC_PWM);

    // Initialize stdio
    stdio_init_all();

    while (true) {
        printf("Moving to 0 degrees\n");
        set_servo_angle(SERVO_PIN, 0);
        sleep_ms(2000);  // Wait 2 seconds

        printf("Moving to 90 degrees\n");
        set_servo_angle(SERVO_PIN, 90);
        sleep_ms(2000);  // Wait 2 seconds
    }

    return 0;
}