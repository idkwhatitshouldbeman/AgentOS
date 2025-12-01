#!/usr/bin/env python3
import socket
import sys
import time
import os

SOCKET_PATH = "qemu-monitor-socket"
SCREENSHOT_FILE = "screenshot.ppm"

def connect_and_capture():
    if not os.path.exists(SOCKET_PATH):
        print(f"Error: Socket {SOCKET_PATH} not found. Is QEMU running?")
        return False

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        client.recv(1024) # Greeting
        cmd = f"screendump {SCREENSHOT_FILE}\n"
        client.sendall(cmd.encode())
        time.sleep(1)
        client.close()
        return True
    except Exception as e:
        print(f"Error communicating with QEMU: {e}")
        return False

def analyze_image():
    if not os.path.exists(SCREENSHOT_FILE):
        print("Error: Screenshot file not created.")
        return False

    try:
        with open(SCREENSHOT_FILE, 'rb') as f:
            header = b""
            while True:
                byte = f.read(1)
                header += byte
                if header.count(b'\n') >= 3:
                    break
            
            lines = header.decode().split('\n')
            dims = lines[1].split()
            width, height = int(dims[0]), int(dims[1])
            data = f.read()
            
            beige_count = 0
            black_count = 0
            other_count = 0
            
            # Sample every 100th pixel to be fast
            for i in range(0, len(data), 300): 
                if i+2 >= len(data): break
                r = data[i]
                g = data[i+1]
                b = data[i+2]
                
            # Check for Beige (#F5F5DC -> 245, 245, 220)
            # Check for SaddleBrown (#8B4513 -> 139, 69, 19) - Login Button
            
            saddle_brown_count = 0
            
            # Sample every 100th pixel to be fast
            for i in range(0, len(data), 300): 
                if i+2 >= len(data): break
                r = data[i]
                g = data[i+1]
                b = data[i+2]
                
                # Beige tolerance
                if 235 <= r <= 255 and 235 <= g <= 255 and 210 <= b <= 230:
                    beige_count += 1
                # SaddleBrown tolerance (Login Button)
                elif 120 <= r <= 160 and 50 <= g <= 90 and 0 <= b <= 40:
                    saddle_brown_count += 1
                elif r < 10 and g < 10 and b < 10:
                    black_count += 1
                else:
                    other_count += 1
            
            total_samples = beige_count + black_count + other_count + saddle_brown_count
            print(f"Analysis (Samples: {total_samples}):")
            print(f"  Beige Pixels: {beige_count} ({(beige_count/total_samples)*100:.1f}%)")
            print(f"  Brown Pixels: {saddle_brown_count} ({(saddle_brown_count/total_samples)*100:.1f}%)")
            print(f"  Black Pixels: {black_count} ({(black_count/total_samples)*100:.1f}%)")
            print(f"  Other Pixels: {other_count} ({(other_count/total_samples)*100:.1f}%)")
            
            if saddle_brown_count > 0:
                print("STATUS: LOGIN SCREEN DETECTED (Found 'Sign In' button color)")
                return True
            elif beige_count > 0:
                print("STATUS: BEIGE BACKGROUND DETECTED (Success!)")
                return True
            elif other_count > 0:
                 print("STATUS: SOMETHING VISIBLE (Not beige, but not black)")
                 return True
            else:
                print("STATUS: BLACK SCREEN (Failed)")
                return False

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return False

if __name__ == "__main__":
    print("Capturing screen...")
    if connect_and_capture():
        analyze_image()
