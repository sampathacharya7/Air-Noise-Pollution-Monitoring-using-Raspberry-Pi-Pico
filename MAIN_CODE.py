"""
Raspberry Pi Pico Sound Level Monitor + MQ135 Smoke Sensor with ThingSpeak & Telegram
Reads analog sound levels and smoke/gas levels
Sends data to ThingSpeak and alerts via Telegram
"""

import machine
import time
import math
import network
import urequests
from machine import ADC, Pin

# WiFi Configuration
SSID         = "OPPO A59 5G"
PASSWORD     = "sampath81"

# ThingSpeak Configuration
TS_API_KEY   = "N2XYTDR1MMS0YHCP"
TS_URL       = "http://api.thingspeak.com/update"

# Telegram Configuration
TG_BOT_TOKEN = "8761473200:AAHOKR-l5m01x4nAb-U2UY8HYEZz1GA3qhE"
TG_CHAT_ID   = "1839206133"

# Sensor Configuration
SOUND_SENSOR_PIN = 27  # GPIO27 (ADC1) - analog input from microphone
SAMPLING_RATE = 10000  # samples per second
SAMPLE_SIZE = 512      # number of samples to collect
MQ135_SENSOR_PIN = 26  # GPIO26 (ADC0) - analog input from MQ135

# Reference values for dB calculation
REFERENCE_VOLTAGE = 3.3
ADC_RESOLUTION = 4095  # 12-bit ADC (0-4095)

# Initialize ADC
sound_adc = ADC(Pin(SOUND_SENSOR_PIN))
mq135_adc = ADC(Pin(MQ135_SENSOR_PIN))

# Alert tracking to prevent spam
last_sound_alert = 0
last_smoke_alert = 0
alert_cooldown = 60  # 60 seconds cooldown between alerts

def setup():
    """Initialize both sensors and WiFi"""
    print("\n=== Raspberry Pi Pico Multi-Sensor Monitor ===")
    print("Reading sound levels (dB) and air quality (PPM)...\n")
    connect_wifi()

def connect_wifi():
    """Connect to WiFi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)

    print("\nConnected!")
    print("IP:", wlan.ifconfig()[0])

def send_telegram_alert(message):
    """Send alert message to Telegram"""
    try:
        # Simplify message to avoid URL encoding issues
        safe_message = message.replace("\n", " ")
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={safe_message}"
        
        response = urequests.get(url, timeout=5)
        print(f"Telegram sent | Status: {response.status_code}")
        response.close()
    except Exception as e:
        print(f"Telegram Error: {e}")
        # Try HTTP as fallback
        try:
            safe_message = message.replace("\n", " ")
            url = f"http://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={safe_message}"
            response = urequests.get(url, timeout=5)
            print(f"Telegram sent via HTTP | Status: {response.status_code}")
            response.close()
        except Exception as e2:
            print(f"Telegram HTTP Error: {e2}")

def send_thingspeak(sound_db, smoke_ppm):
    """Send sensor data to ThingSpeak"""
    try:
        url = TS_URL + "?api_key=" + TS_API_KEY + "&field1=" + str(sound_db) + "&field2=" + str(smoke_ppm)
        response = urequests.get(url)
        print(f"ThingSpeak Response: {response.text}")
        response.close()
    except Exception as e:
        print(f"ThingSpeak Error: {e}")

def read_sound():
    """Read and return sound level in dB"""
    # Collect samples
    max_val = 0
    min_val = 4095
    
    for i in range(SAMPLE_SIZE):
        # Pico ADC returns 16-bit value, shift to 12-bit
        adc_value = sound_adc.read_u16() >> 4
        if adc_value > max_val:
            max_val = adc_value
        if adc_value < min_val:
            min_val = adc_value
        time.sleep_us(100)
    
    # Calculate peak-to-peak amplitude
    peak_to_peak = max_val - min_val
    
    # Convert to voltage
    voltage = (peak_to_peak * REFERENCE_VOLTAGE) / ADC_RESOLUTION
    
    # Calculate dB (20 * log10(V / V_ref))
    db = 0.0
    if voltage > 0:
        db = 20.0 * math.log10(voltage / 0.00631)
    
    # Add offset for realistic readings
    db = db + 10.0
    
    # Ensure dB doesn't go negative
    if db < 0:
        db = 0
    
    return db

def read_smoke():
    """Read and return air quality in PPM"""
    # Read 16-bit ADC value
    air_value = mq135_adc.read_u16()
    
    # Convert to PPM
    air_quality_ppm = round((air_value / 65535) * 500, 2)
    
    return air_quality_ppm

def loop():
    """Read and display both sensor data"""
    global last_sound_alert, last_smoke_alert
    
    # Read sound level
    db = read_sound()
    
    # Read smoke level
    ppm = read_smoke()
    
    # Display results
    print(f"Sound Level: {db:.1f} dB | Air Quality: {ppm} PPM")
    
    # Sound status
    if db >= 50:
        sound_status = "SOUND IS MORE"
        # Send Telegram alert if cooldown passed
        if time.time() - last_sound_alert > alert_cooldown:
            send_telegram_alert(f"🔊 ALERT: SOUND IS MORE!\nSound Level: {db:.1f} dB")
            last_sound_alert = time.time()
    else:
        sound_status = "NORMAL"
    
    # Smoke status
    if ppm >= 69:
        smoke_status = "SMOKE DETECTED"
        # Send Telegram alert if cooldown passed
        if time.time() - last_smoke_alert > alert_cooldown:
            send_telegram_alert(f"💨 ALERT: SMOKE DETECTED!\nAir Quality: {ppm} PPM")
            last_smoke_alert = time.time()
    else:
        smoke_status = "NORMAL"
    
    print(f"  Sound Status: {sound_status} | Smoke Status: {smoke_status}")
    
    # Send data to ThingSpeak
    send_thingspeak(db, ppm)
    
    print()

# Main loop
if __name__ == "__main__":
    setup()
    while True:
        loop()
        time.sleep(5)  # Update every 5 seconds
