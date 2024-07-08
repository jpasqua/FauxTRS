import RPi.GPIO as GPIO
import time
import random
from threading import Thread, Event
import argparse
import signal
import sys

# Set up the GPIO pins
LED_PIN_1 = 17  # GPIO pin for the first LED
LED_PIN_2 = 27  # GPIO pin for the second LED

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)

# Function to blink an LED at random intervals
def blink_led(led_pin, start_delay, min_time, max_time, stop_event):
    time.sleep(start_delay)
    GPIO.output(led_pin, GPIO.LOW)
    
    while not stop_event.is_set():
        sleep_time = random.uniform(min_time, max_time)
        while sleep_time > 0 and not stop_event.is_set():
            time.sleep(1)
            sleep_time = sleep_time - 1
        for _ in range(10):
            if stop_event.is_set():
                break
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(0.1)  # LED on for 0.1 seconds
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(0.1)  # LED off for 0.1 seconds

# Clean up GPIO and stop threads on exit
def cleanup(threads):
    stop_event.set()
    for thread in threads:
        thread.join()
    GPIO.cleanup()

# Signal handler for graceful exit
def signal_handler(sig, frame):
    global cleaned_up
    if not cleaned_up:
        cleanup(threads)
        cleaned_up = True
    sys.exit(0)

# Main function
def main(min_time, max_time):
    global stop_event
    global threads
    global cleaned_up

    cleaned_up = False
    stop_event = Event()

    # Turn both LEDs on
    GPIO.output(LED_PIN_1, GPIO.HIGH)
    GPIO.output(LED_PIN_2, GPIO.HIGH)

    # Start threads to blink the LEDs independently
    threads = [
        Thread(target=blink_led, args=(LED_PIN_1, 2, min_time, max_time, stop_event)),
        Thread(target=blink_led, args=(LED_PIN_2, 2, min_time, max_time, stop_event))
    ]

    for thread in threads:
        thread.start()

    try:
        # Keep the main thread alive
        for thread in threads:
            thread.join()
    finally:
        if not cleaned_up:
            cleanup(threads)
            cleaned_up = True

# Argument parser for command line arguments
if __name__ == '__main__':
    # Register signal handler for SIGINT and SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser(description='LED Blinker')
    parser.add_argument('--min-time', type=float, default=5.0, help='Minimum time between blinks in seconds')
    parser.add_argument('--max-time', type=float, default=20.0, help='Maximum time between blinks in seconds')
    args = parser.parse_args()

    # Run the main function
    main(args.min_time, args.max_time)

