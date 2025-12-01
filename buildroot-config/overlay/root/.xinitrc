#!/bin/sh
# Debugging .xinitrc - redirecting to serial console

# Redirect ALL output to serial console so we can see it on host
exec > /dev/ttyS0 2>&1
echo "=== XINITRC STARTING ==="

echo "User: $(whoami)"
echo "Display: $DISPLAY"

# Allow local users (like 'admin') to connect to X server
if which xhost >/dev/null; then
    xhost +local:
else
    echo "WARNING: xhost not found, user session might fail"
fi

# Check for required binaries
if which openbox-session >/dev/null; then
    echo "Found openbox-session: $(which openbox-session)"
else
    echo "ERROR: openbox-session NOT FOUND"
fi

if which xsetroot >/dev/null; then
    echo "Found xsetroot: $(which xsetroot)"
    # Set the background color
    xsetroot -solid '#F5F5DC'
    # Force a visible mouse cursor (left pointer)
    xsetroot -cursor_name left_ptr
else
    echo "WARNING: xsetroot NOT FOUND"
fi

# Start the Custom Login App
echo "Starting AgentOS Login..."
python3 /opt/ai-agent/login_app.py

# If login app exits (e.g. crash), we fall back to shell
echo "Login app exited."

