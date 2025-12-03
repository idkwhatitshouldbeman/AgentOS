import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor

def main():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    geometry = screen.availableGeometry()
    
    print("=== AgentOS Overlay Debugger ===")
    print(f"Screen Geometry: {geometry}")
    print(f"Screen Width (Right Edge): {geometry.width() + geometry.x()}")
    print(f"Screen Height: {geometry.height()}")
    print(f"Screen Top: {geometry.y()}")
    print("--------------------------------")
    print("Move your mouse to the right edge to test trigger...")
    print("Press Ctrl+C to exit.")
    print("--------------------------------")
    
    try:
        while True:
            pos = QCursor.pos()
            x = pos.x()
            y = pos.y()
            
            right_edge = geometry.width() + geometry.x()
            trigger_zone = right_edge - 10
            
            status = " [IDLE]"
            if x >= trigger_zone:
                status = " [TRIGGERED!]"
            
            # Overwrite line
            sys.stdout.write(f"\rMouse: ({x}, {y}) | Trigger Zone: > {trigger_zone}{status}   ")
            sys.stdout.flush()
            
            app.processEvents() # Keep Qt alive
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
