import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import digitalio
import csv
import threading

# I2C Setup
i2c = busio.I2C(board.SCL, board.SDA)

# ADC Setup
ads = ADS.ADS1115(i2c)
ldr_channel = AnalogIn(ads, ADS.P0)  # Using AIN0 for LDR input

# LED Setup (GPIO 18 for LED)
led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT

# OLED Display Setup
WIDTH = 128
HEIGHT = 64
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# CSV File Path
log_file_path = "/home/isuru/Desktop/RM/runtime_log.csv"

# Clear display
oled.fill(0)
oled.show()

# Initialize CSV File
def initialize_csv_file():
    try:
        with open(log_file_path, mode='x', newline='') as log_file:
            writer = csv.writer(log_file)
            writer.writerow(["Date", "Shift", "Runtime"])  # Write headers
    except FileExistsError:
        pass  # File already exists

initialize_csv_file()

# Custom function to display text on OLED using Pillow
def display_on_oled(date_time, runtime_text, shift, ldr_voltage):
    # Create an image buffer
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # Load default font
    font = ImageFont.load_default()

    # Clear the display
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Draw the date and time on the same line with some space between
    draw.text((0, 0), date_time, font=font, fill=1)

    # Draw runtime information and shift below the date and time
    draw.text((0, 16), runtime_text, font=font, fill=1)
    draw.text((0, 32), shift, font=font, fill=1)

    # Draw LDR voltage information below the shift
    draw.text((0, 48), f"LDR Voltage: {ldr_voltage:.2f}V", font=font, fill=1)

    # Display the image on OLED
    oled.image(image)
    oled.show()
    
# Function to get LDR value and corresponding voltage
def read_ldr():
    return ldr_channel.value, ldr_channel.voltage

# Function to format time in HH:MM:SS format
def format_runtime(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Function to get the current shift based on the time of day
def get_shift():
    current_hour = datetime.now().hour
    return "Day" if 6 <= current_hour < 18 else "Night"

# Function to log data to CSV in a separate thread to avoid delays
def log_data_to_csv(date, shift, runtime):
    with open(log_file_path, mode='a', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow([date, shift, runtime])
    print(f"Logged: Date={date}, Shift={shift}, Runtime={runtime}")

def log_to_csv_in_thread(date, shift, runtime):
    log_thread = threading.Thread(target=log_data_to_csv, args=(date, shift, runtime))
    log_thread.start()
    
# Function to monitor LDR and determine when the machine is on
def monitor_ldr_runtime():
    machine_on = False
    runtime_start = 0
    total_runtime = 0  # Track total runtime for pause/resume functionality
    last_logged_time = None
    last_runtime = ""  # Track last OLED display runtime to avoid unnecessary updates
    last_update_time = time.monotonic()  # Track when OLED was last updated

    while True:
        # Get current date and time from Raspberry Pi
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        date_time = f"{current_date}    {current_time}"  # Date and time in the same line
        shift = get_shift()  # Determine if it's day or night shift

        ldr_value, ldr_voltage = read_ldr()

        # Control the LED based on the LDR voltage
        if ldr_voltage < 2.9:
            led.value = True  # Turn LED on when LDR voltage is below 2.9V
            if not machine_on:
                machine_on = True
                runtime_start = time.monotonic() - total_runtime  # Resume from where it was paused
                print("Machine started.")
        else:
            led.value = False  # Turn LED off when LDR voltage is above 2.9V
            if machine_on:
                machine_on = False
                total_runtime = time.monotonic() - runtime_start  # Pause runtime
                print(f"Runtime paused at: {format_runtime(total_runtime)}")

        # Display date, time, runtime, shift, and LDR voltage information on OLED
        if machine_on:
            runtime_duration = time.monotonic() - runtime_start
            runtime_display_text = f"Runtime: {format_runtime(runtime_duration)}"
        else:
            runtime_display_text = f"Runtime: {format_runtime(total_runtime)}"

        # Update OLED only if the runtime changes or at least 2 seconds have passed since the last update
        if last_runtime != runtime_display_text or (time.monotonic() - last_update_time) >= 2:
            display_on_oled(date_time, runtime_display_text, shift, ldr_voltage)
            last_runtime = runtime_display_text
            last_update_time = time.monotonic()

        # Get the current hour and check for logging time (06:00:00 or 18:00:00)
        now = datetime.now()
        if (now.hour == 6 or now.hour == 18) and now.minute == 0 and now.second == 0:
            if last_logged_time is None or (now - last_logged_time) >= timedelta(hours=12):
                # Log to CSV just before resetting runtime
                runtime_to_log = total_runtime if not machine_on else (time.monotonic() - runtime_start)
                log_to_csv_in_thread(current_date, shift, format_runtime(runtime_to_log))

                # Reset the runtime after logging
                total_runtime = 0  # Reset runtime
                runtime_start = time.monotonic()  # Reset start time

                # Update OLED to reflect reset runtime (showing 00:00:00)
                display_on_oled(date_time, "Runtime: 00:00:00", shift, ldr_voltage)
                
                last_logged_time = now  # Record last logging time

        # Faster loop with reduced sleep time for higher accuracy
        time.sleep(0.01)  # 10 ms sleep for quick response

# Main loop
try:
    monitor_ldr_runtime()
except KeyboardInterrupt:
    print("Program terminated.")
