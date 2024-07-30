import RPi.GPIO as GPIO
import tkinter as tk
from time import sleep
import threading

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for RGB
RED_PIN = 5
GREEN_PIN = 6
BLUE_PIN = 13

# Set up GPIO pins for PWM
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Initialize PWM on the pins
r = GPIO.PWM(RED_PIN, 1000)  # 1000 Hz frequency
g = GPIO.PWM(GREEN_PIN, 1000)
b = GPIO.PWM(BLUE_PIN, 1000)

# Start PWM with 0 duty cycle
r.start(0)
g.start(0)
b.start(0)

def update_rgb(value):
    """Update the RGB values based on the sliders and apply to LEDs."""
    red_value = scale_red.get()
    green_value = scale_green.get()
    blue_value = scale_blue.get()

    # Update the PWM duty cycle
    r.ChangeDutyCycle(red_value * 100 / 255)
    g.ChangeDutyCycle(green_value * 100 / 255)
    b.ChangeDutyCycle(blue_value * 100 / 255)
    
    # Update RGB display label
    rgb_display.set(f'RGB: ({red_value}, {green_value}, {blue_value})')

def flash_effect():
    """Flashing effect function."""
    global flashing, flash_on
    if flashing:
        # Get the current RGB values
        red_value = scale_red.get()
        green_value = scale_green.get()
        blue_value = scale_blue.get()

        # Toggle LED state
        if flash_on:
            r.ChangeDutyCycle(0)
            g.ChangeDutyCycle(0)
            b.ChangeDutyCycle(0)
        else:
            r.ChangeDutyCycle(red_value * 100 / 255)
            g.ChangeDutyCycle(green_value * 100 / 255)
            b.ChangeDutyCycle(blue_value * 100 / 255)
        
        # Toggle the flash_on state
        flash_on = not flash_on
        
        # Schedule the next flash
        threading.Timer(flash_interval, flash_effect).start()

# Flashing effect parameters
flash_interval = 0.5  # Interval between flashes in seconds
flashing = True  # Whether the flashing effect is active
flash_on = True  # State of the flashing effect (LED on/off)

# Set up the main Tkinter window
root = tk.Tk()
root.title('RGB Control')
root.geometry('400x400')

# Create sliders for RGB control
scale_red = tk.Scale(root, from_=0, to=255, orient='horizontal', resolution=1, label='Red', command=update_rgb)
scale_red.pack(pady=10)

scale_green = tk.Scale(root, from_=0, to=255, orient='horizontal', resolution=1, label='Green', command=update_rgb)
scale_green.pack(pady=10)

scale_blue = tk.Scale(root, from_=0, to=255, orient='horizontal', resolution=1, label='Blue', command=update_rgb)
scale_blue.pack(pady=10)

# Create label to display RGB values
rgb_display = tk.StringVar()
rgb_display.set('RGB:(0,0,0)')
label = tk.Label(root, textvariable=rgb_display)
label.pack(pady=10)

# Start the Tkinter event loop
try:
    # Start flashing effect in a separate thread
    threading.Thread(target=flash_effect, daemon=True).start()

    # Start the Tkinter main loop
    root.mainloop()

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    # Stop PWM and clean up GPIO settings
    r.stop()
    g.stop()
    b.stop()
    GPIO.cleanup()
