"""
AI Agent Overlay Interface.
Built with PyQt6 for a modern, animated, always-on-top experience.
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QPalette, QBrush, QCursor

class AgentSidebar(QWidget):
    def __init__(self):
        super().__init__()
        
        # Screen Setup
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry() # Accounts for taskbar
        self.screen_width = geometry.width() + geometry.x() # Absolute right edge
        self.screen_height = geometry.height()
        self.screen_top = geometry.y()
        
        self.sidebar_width = 400
        self.is_visible = False
        
        # Window Setup
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Initial Geometry (Hidden off-screen to the right)
        self.setGeometry(self.screen_width, self.screen_top, self.sidebar_width, self.screen_height)
        
        # Styling
        self.init_ui()
        
        # Animation Setup
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(300) # ms
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Mouse Polling (More reliable than pynput in VMs)
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_mouse_position)
        self.poll_timer.start(100) # Check every 100ms
        
    def init_ui(self):
        # Main Container with Glass-morphism look
        self.container = QFrame(self)
        self.container.setGeometry(0, 0, self.sidebar_width, self.screen_height)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 25, 0.95);
                border-left: 1px solid rgba(255, 255, 255, 0.15);
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(30, 50, 30, 30)
        
        # Header
        title = QLabel("AgentOS")
        title.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 1px;
        """)
        layout.addWidget(title)
        
        # Status
        self.status = QLabel("● Online")
        self.status.setStyleSheet("color: #00ff9d; font-size: 14px; margin-top: 5px;")
        layout.addWidget(self.status)
        
        # Placeholder for Chat
        chat_area = QLabel("Waiting for user input...")
        chat_area.setStyleSheet("color: rgba(255,255,255,0.5); font-style: italic; margin-top: 20px;")
        chat_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(chat_area)
        
        layout.addStretch()
        
    def slide_in(self):
        if self.is_visible: return
        self.is_visible = True
        self.show()
        self.anim.setStartValue(QPoint(self.screen_width, self.screen_top))
        self.anim.setEndValue(QPoint(self.screen_width - self.sidebar_width, self.screen_top))
        self.anim.start()
        
    def slide_out(self):
        if not self.is_visible: return
        self.is_visible = False
        self.anim.setStartValue(QPoint(self.screen_width - self.sidebar_width, self.screen_top))
        self.anim.setEndValue(QPoint(self.screen_width, self.screen_top))
        self.anim.start()

    def check_mouse_position(self):
        cursor_pos = QCursor.pos()
        x = cursor_pos.x()
        
        # Trigger zone: Rightmost 10 pixels
        if x >= self.screen_width - 10:
            self.slide_in()
        
        # Close zone: If mouse moves far left of the sidebar
        elif x < self.screen_width - self.sidebar_width - 50:
             self.slide_out()

def main():
    app = QApplication(sys.argv)
    sidebar = AgentSidebar()
    # Keep running
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
