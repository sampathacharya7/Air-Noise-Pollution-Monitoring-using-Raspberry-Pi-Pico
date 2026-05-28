# Air & Noise Pollution Monitoring System using Raspberry Pi Pico

A comprehensive IoT-based environmental monitoring system that detects noise pollution and air quality in real-time using the Raspberry Pi Pico microcontroller with cloud integration.

## 🎯 Project Overview

This project implements a multi-sensor monitoring system that:
- **Measures Sound Levels** in decibels (dB) using an analog microphone sensor
- **Monitors Air Quality** by detecting smoke and harmful gases using the MQ135 sensor
- **Sends Real-time Data** to ThingSpeak cloud platform for visualization and logging
- **Sends Instant Alerts** via Telegram when pollution thresholds are exceeded
- **Prevents Alert Spam** with intelligent cooldown mechanisms

## 📋 Features

✅ Real-time sound level monitoring (in dB)  
✅ Air quality detection (PPM - Parts Per Million)  
✅ Dual-sensor integration  
✅ Cloud data logging via ThingSpeak  
✅ Instant Telegram notifications  
✅ Alert cooldown system (prevents notification spam)  
✅ WiFi connectivity for remote monitoring  
✅ 5-second update interval for continuous monitoring  

## 🛠️ Hardware Components

| Component | Specification | GPIO Pin |
|-----------|---------------|----------|
| **Raspberry Pi Pico** | RP2040 microcontroller | - |
| **Sound Sensor (Microphone)** | Analog microphone module | GPIO 27 (ADC1) |
| **MQ135 Gas Sensor** | Air quality sensor | GPIO 26 (ADC0) |
| **WiFi Module** | Built-in on Pico W (or external) | - |
| **Power Supply** | 5V USB or external | - |

## 📊 Sensor Specifications

### Sound Sensor
- **Input**: Analog microphone signal
- **Output**: ADC value converted to decibels (dB)
- **Calibration**: Peak-to-peak amplitude analysis
- **Reference**: 0.00631V for dB calculation
- **Offset**: +10 dB for realistic readings

### MQ135 Air Quality Sensor
- **Input**: Analog gas sensor output
- **Output**: PPM (Parts Per Million)
- **Detection Range**: 0-500 PPM
- **Conversion**: ADC value / 65535 × 500
- **Alert Threshold**: ≥ 69 PPM

## ⚙️ Software Configuration

### WiFi Settings
```python
SSID = "Your_WiFi_Network"
PASSWORD = "Your_WiFi_Password"
```

### ThingSpeak Configuration
```python
TS_API_KEY = "Your_ThingSpeak_API_Key"
TS_URL = "http://api.thingspeak.com/update"
```

### Telegram Configuration
```python
TG_BOT_TOKEN = "Your_Telegram_Bot_Token"
TG_CHAT_ID = "Your_Chat_ID"
```

### Sensor Parameters
- **Sampling Rate**: 10,000 samples per second
- **Sample Size**: 512 samples per measurement
- **Reference Voltage**: 3.3V
- **ADC Resolution**: 12-bit (0-4095)
- **Update Interval**: 5 seconds
- **Alert Cooldown**: 60 seconds

## 🚀 Getting Started

### Prerequisites
- Raspberry Pi Pico or Pico W
- MicroPython firmware installed
- Sound sensor and MQ135 sensor connected
- WiFi network access
- Telegram bot token and chat ID

### Installation Steps

1. **Flash MicroPython Firmware**
   - Download MicroPython from: https://micropython.org/download/rp2-pico/
   - Flash using Thonny IDE or command line tools

2. **Connect Sensors**
   - Sound Sensor → GPIO 27 (ADC1)
   - MQ135 Sensor → GPIO 26 (ADC0)
   - Ground and 3.3V connections to both sensors

3. **Configure Credentials**
   - Update WiFi SSID and PASSWORD in `MAIN_CODE.py`
   - Add ThingSpeak API key from your channel
   - Create Telegram bot via BotFather and add token and chat ID

4. **Upload and Run**
   - Upload `MAIN_CODE.py` to Raspberry Pi Pico using Thonny IDE
   - Run the script to start monitoring

## 📈 Alert Thresholds

### Sound Level Alerts
- **Threshold**: ≥ 50 dB
- **Status**: "SOUND IS MORE"
- **Alert**: Sent via Telegram with current dB reading

### Air Quality Alerts
- **Threshold**: ≥ 69 PPM
- **Status**: "SMOKE DETECTED"
- **Alert**: Sent via Telegram with current PPM reading

## 📡 Cloud Integration

### ThingSpeak
- **Field 1**: Sound Level (dB)
- **Field 2**: Air Quality (PPM)
- **Update Frequency**: Every 5 seconds
- **Visualization**: Charts and graphs available on ThingSpeak dashboard

### Telegram
- **Alert Format**: 
  - 🔊 Sound alerts with current dB reading
  - 💨 Smoke/air quality alerts with PPM reading
- **Delivery**: Real-time notifications
- **Cooldown**: 60-second delay between duplicate alerts

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────┐
│         Raspberry Pi Pico                           │
│                                                      │
│  ┌──────────────┐         ┌─────────────────┐      │
│  │ Sound Sensor │─────┐   │ MQ135 Sensor    │      │
│  │  (GPIO 27)   │     │   │  (GPIO 26)      │      │
│  └──────────────┘     │   └─────────────────┘      │
│                       │                              │
│                   ┌───▼────────────┐                │
│                   │   ADC Module   │                │
│                   └───┬────────────┘                │
│                       │                              │
│              ┌────────┴────────────┐                │
│              │  Processing Logic   │                │
│              │  - Convert to dB    │                │
│              │  - Convert to PPM   │                │
│              │  - Check Thresholds │                │
│              └────────┬────────────┘                │
│                       │                              │
│          ┌────────────┼────────────┐                │
│          │            │            │                │
│      ┌───▼──┐    ┌───▼──┐    ┌───▼──┐             │
│      │ WiFi │    │ WiFi │    │ WiFi │             │
│      └───┬──┘    └───┬──┘    └───┬──┘             │
└─────────┼────────────┼────────────┼─────────────────┘
          │            │            │
     ┌────▼──┐    ┌───▼──┐    ┌───▼──┐
     │  WiFi │    │      │    │      │
     │ Router│   │ThingSpeak│ │Telegram│
     └───────┘    └────────┘    └──────┘
```

## 💻 Code Structure

### Main Functions

**`setup()`**
- Initializes sensors and WiFi connection
- Displays startup message

**`connect_wifi()`**
- Establishes WiFi connection
- Displays connection status and IP address

**`read_sound()`**
- Collects 512 audio samples at 10 kHz
- Calculates peak-to-peak amplitude
- Converts to dB using logarithmic formula

**`read_smoke()`**
- Reads MQ135 analog value
- Converts ADC reading to PPM scale (0-500)

**`send_thingspeak(sound_db, smoke_ppm)`**
- Sends sensor data to ThingSpeak API
- Updates Field 1 (sound) and Field 2 (air quality)

**`send_telegram_alert(message)`**
- Sends alert messages via Telegram bot
- Includes fallback from HTTPS to HTTP

**`loop()`**
- Main monitoring loop (runs every 5 seconds)
- Reads both sensors
- Displays status in console
- Triggers alerts based on thresholds
- Sends data to cloud

## 🔍 Sensor Calibration

### Sound Level Calibration
The sound level uses peak-to-peak amplitude analysis:
```
dB = 20 * log10(voltage / 0.00631) + 10
```
- Reference voltage: 0.00631V
- Offset: +10 dB for realistic readings
- Minimum value: 0 dB (clamped)

### Air Quality Calibration
The MQ135 sensor converts ADC readings to PPM:
```
PPM = (ADC_Value / 65535) × 500
```
- Full scale ADC range: 0-65535
- PPM scale: 0-500
- Rounded to 2 decimal places

## 🐛 Troubleshooting

### WiFi Connection Issues
- Verify SSID and password are correct
- Check WiFi signal strength
- Ensure credentials have no special characters that need escaping

### No Sensor Readings
- Verify pin connections (GPIO 26 and 27)
- Check sensor power supply (3.3V)
- Test ADC values in isolation

### ThingSpeak Not Updating
- Verify API key is correct
- Check internet connection
- Ensure ThingSpeak channel is active

### Telegram Alerts Not Arriving
- Verify bot token is correct
- Check chat ID matches your user ID
- Ensure WiFi connection is stable
- Try HTTP fallback (already in code)

## 📝 Example Output

```
=== Raspberry Pi Pico Multi-Sensor Monitor ===
Reading sound levels (dB) and air quality (PPM)...

Connecting to WiFi...
.........
Connected!
IP: 192.168.1.100

Sound Level: 45.2 dB | Air Quality: 35.50 PPM
  Sound Status: NORMAL | Smoke Status: NORMAL
ThingSpeak Response: {"code":200,"message":"OK"}

Sound Level: 55.8 dB | Air Quality: 75.20 PPM
  Sound Status: SOUND IS MORE | Smoke Status: SMOKE DETECTED
🔊 ALERT: SOUND IS MORE! Sound Level: 55.8 dB
Telegram sent | Status: 200
💨 ALERT: SMOKE DETECTED! Air Quality: 75.20 PPM
Telegram sent | Status: 200
ThingSpeak Response: {"code":200,"message":"OK"}
```

## 🔒 Security Notes

⚠️ **Important**: The credentials in this example code should **NOT** be used in production:
- WiFi SSID and password are exposed
- ThingSpeak API key is public
- Telegram bot token is visible

**Best Practices**:
1. Store credentials in a separate `config.py` file (add to .gitignore)
2. Use environment variables if supported
3. Rotate API keys and tokens regularly
4. Never commit credentials to version control

## 📚 References

- [Raspberry Pi Pico Documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
- [MicroPython Docs](https://docs.micropython.org/en/latest/)
- [ThingSpeak API](https://www.mathworks.com/help/thingspeak/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [MQ135 Gas Sensor](https://www.olimex.com/Products/Components/Sensors/SNS-MQ135/resources/SNS-MQ135.pdf)

## 📄 Project Documentation

Additional documentation and reports included:
- `DIAGRAM.jpeg` - Circuit diagram and connections
- `FLOW.jpeg` - System flow diagram
- `Final_IoT_report__2_ (1).pdf` - Detailed technical report
- `air and noise pollution detection system (1).pptx` - Project presentation
- Result screenshots showing real-time data and Telegram alerts

## 👤 Author

**Sampath Acharya**  
GitHub: [@sampathacharya7](https://github.com/sampathacharya7)

## 📄 License

This project is open source and available for educational and development purposes.

## 🤝 Contributing

Contributions, improvements, and bug reports are welcome! Feel free to fork this repository and submit pull requests.

## ⭐ Support

If you find this project helpful, please consider giving it a star ⭐

---

**Last Updated**: 2026  
**Status**: Active & Maintained
