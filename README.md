# Runtime Measuring Module Production

## Overview
This automation project aims to measure the runtime of a machine and update the timing data to a GitHub Pages website in real-time. The module utilizes various components, including a Raspberry Pi, LDR sensors, and an OLED display, to monitor machine operations effectively.

## Features
- Real-time monitoring of machine runtime
- Automatic data upload to GitHub Pages
- User-friendly OLED display for runtime information
- Designed for easy integration and setup

## Components Used
- **Raspberry Pi Zero 2**: The main controller for data processing and communication.
- **LDR (Light Dependent Resistor)**: Used to detect the machine's running phase based on the indicator bulb's light intensity.
- **ADS1115 ADC**: Provides high-precision analog-to-digital conversion for reading LDR values.
- **DS3231 RTC**: Ensures accurate timekeeping for runtime measurements.
- **128x64 OLED Display**: Displays the current runtime information.
- **Potentiometer**: Used to adjust sensitivity for the LDR readings.

## Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Tape-head-3d/runtime-measuring-module-production.git
Install the necessary libraries and dependencies on your Raspberry Pi:
bash
Copy code
pip install -r requirements.txt
Configure your GitHub token and other settings as required.
Usage
Connect the components as per the circuit diagram provided in the repository.
Run the main script to start measuring and uploading the runtime:
bash
Copy code
python main.py
Visit the GitHub Pages site to see real-time updates on the machine's runtime.
Contributing
Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.
