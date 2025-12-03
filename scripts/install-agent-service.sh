#!/bin/bash
set -e

# AgentOS Service Installer
# Sets up the AI Agent as a startup service for the current user.

AGENT_DIR="/home/ai/AgentOS"
VENV_DIR="$AGENT_DIR/venv"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/agent-overlay.desktop"

echo "=== Installing AgentOS Service ==="

# 1. Ensure dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-pyqt6 python3-pip python3-venv

# 2. Create Virtual Environment (if not exists)
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Install Python libs
echo "Installing Python libraries..."
"$VENV_DIR/bin/pip" install pynput

# 4. Create Autostart Entry
echo "Configuring autostart..."
mkdir -p "$AUTOSTART_DIR"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=AgentOS Overlay
Comment=AI Agent Sidebar
Exec=$VENV_DIR/bin/python3 $AGENT_DIR/src/agent/interface/overlay.py
Icon=utilities-terminal
Terminal=false
Categories=Utility;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

chmod +x "$DESKTOP_FILE"

echo "=== Installation Complete ==="
echo "The Agent Sidebar will now start automatically on login."
echo "You can start it manually now with:"
echo "$VENV_DIR/bin/python3 $AGENT_DIR/src/agent/interface/overlay.py"
