#!/bin/bash
set -e

# AgentOS Service Installer
# Sets up the AI Agent as a startup service for the current user.

# Detect where we are running from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

TARGET_DIR="$HOME/AgentOS"
VENV_DIR="$TARGET_DIR/venv"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/agent-overlay.desktop"

echo "=== Installing AgentOS Service ==="
echo "Source: $REPO_ROOT"
echo "Target: $TARGET_DIR"

# 1. Ensure dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-pyqt6 python3-pip python3-venv

# 2. Copy files to local home (to avoid permission issues with shared folders)
echo "Copying files to $TARGET_DIR..."
mkdir -p "$TARGET_DIR"
# Copy everything except venv, .git, and large build artifacts
rsync -av --exclude 'venv' --exclude '.git' --exclude 'iso-build' --exclude '*.iso' --exclude '*.vdi' "$REPO_ROOT/" "$TARGET_DIR/"

# 3. Create Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# 4. Install Python libs
echo "Installing Python libraries..."
"$VENV_DIR/bin/pip" install pynput

# 5. Create Autostart Entry
echo "Configuring autostart..."
mkdir -p "$AUTOSTART_DIR"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=AgentOS Overlay
Comment=AI Agent Sidebar
Exec=$VENV_DIR/bin/python3 $TARGET_DIR/src/agent/interface/overlay.py
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
echo "$VENV_DIR/bin/python3 $TARGET_DIR/src/agent/interface/overlay.py"
