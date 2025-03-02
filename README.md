# RFID-Based Door Lock System

## Introduction  
This project implements an RFID-based door lock system using Arduino, integrating servo motors, an LCD display, and a security mechanism. It enhances security while reducing energy consumption, aligning with green technology principles. Additionally, the system includes a fail-safe security feature: after three incorrect RFID scans, an alert email is sent to the owner, notifying them of a potential unauthorized access attempt.

## Components Used  
- Arduino Uno  
- RFID Module (MFRC522)  
- Servo Motor  
- LCD Display (I2C)  
- LED Indicator  
- Computer for Serial Communication  

## Connection Tables  
### RFID Module Connections  
| RFID Pin | Arduino Pin |
|----------|------------|
| VCC      | 3.3V       |
| GND      | GND        |
| SS       | 10         |
| RST      | 9          |
| MOSI     | 11         |
| MISO     | 12         |
| SCK      | 13         |

### LCD Display (I2C) Connections  
| LCD Pin | Arduino Pin |
|---------|------------|
| VCC     | 5V         |
| GND     | GND        |
| SDA     | A4         |
| SCL     | A5         |

### Servo Motor Connection  
| Servo Pin | Arduino Pin |
|-----------|------------|
| VCC       | 5V         |
| GND       | GND        |
| Signal    | 3          |

### LED Indicator Connection  
| LED Pin | Arduino Pin |
|---------|------------|
| VCC     | 5V         |
| GND     | GND        |
| Signal  | 4          |

## Functionality  
- RFID authentication is used to control door access.  
- A servo motor locks/unlocks the door based on valid card scans.  
- An LCD displays access status.  
- Unauthorized access attempts trigger warning Mail Alerts via a Python script.  
- The system resets after three wrong attempts.  
- After three failed authentication attempts, the Python script sends an alert email to the owner, notifying them of possible unauthorized access.

## Code Implementation  
- **Arduino Code**: Handles RFID authentication, door control, and LED indications.  
- **Python Script**: Reads serial input from Arduino and plays corresponding alert videos. Additionally, it monitors incorrect attempts and triggers an email alert if three consecutive failures occur.

## Green Technology Aspects  
- **Energy Efficiency**: The system only activates when needed, reducing power consumption.  
- **Automation**: Reduces manual intervention and improves security.  
- **Sustainability**: Uses minimal hardware components, reducing electronic waste.  

## Conclusion  
This RFID-based door security system improves access control while promoting energy efficiency. The integration of IoT and automation enhances security while minimizing environmental impact. The inclusion of an email alert system further strengthens security by providing real-time notifications of unauthorized access attempts.

