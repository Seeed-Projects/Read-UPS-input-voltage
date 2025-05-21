#!/usr/bin/env python3
import smbus2
import time
import errno

# config
I2C_BUS      = 6          # I2C
I2C_ADDR     = 0x09       # LTC3350 I2C address
MAX_RETRIES  = 5
RETRY_DELAY  = 0.05       

# votage/current ADC address
REG_MEAS_VIN = 0x25       

# LSB
VIN_LSB_V    = 0.00221    # 2.21mV / LSB


def read_register_word(bus, reg):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw = bus.read_word_data(I2C_ADDR, reg)
            return raw
        except OSError as e:
            if e.errno == errno.EIO:
                print(f"⚠️ read register 0x{reg:02X}  {attempt} error, try after {RETRY_DELAY}s ")
                time.sleep(RETRY_DELAY)
            else:
                raise
    print(f"❌ read 0x{reg:02X} over {MAX_RETRIES} times, give up.")
    return None

def main():
    print("🚀 Begin LTC3350 UPS monitoring input voltage,  input Ctrl+C will exit\n")
    try:
        with smbus2.SMBus(I2C_BUS) as bus:
            while True:
                vin_code = read_register_word(bus, REG_MEAS_VIN)

                if vin_code is not None:
                    vin = vin_code * VIN_LSB_V
                    print(f"🔌 VIN = {vin:.3f} V  (ADC Code = {vin_code})")
                else:
                    print("🔌 read VIN error")

                print("-" * 40)
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 exit。")

if __name__ == "__main__":
    main()
