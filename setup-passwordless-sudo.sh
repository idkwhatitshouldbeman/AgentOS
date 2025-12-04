#!/bin/bash
# Script to enable passwordless sudo for the current user
# Run this script with: bash setup-passwordless-sudo.sh

USERNAME=$(whoami)
SUDOERS_FILE="/etc/sudoers.d/${USERNAME}-nopasswd"

echo "Setting up passwordless sudo for user: $USERNAME"
echo "This will allow sudo commands to run without a password."
echo ""
echo "Security warning: This reduces security. Anyone with access to your account can run commands as root."
echo ""

# Create the sudoers configuration
echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" | sudo tee "$SUDOERS_FILE" > /dev/null

# Set proper permissions (sudoers files must be 0440)
sudo chmod 0440 "$SUDOERS_FILE"

# Validate the sudoers file
if sudo visudo -c -f "$SUDOERS_FILE" 2>/dev/null; then
    echo "✓ Passwordless sudo configured successfully!"
    echo "✓ Configuration file: $SUDOERS_FILE"
    echo ""
    echo "You can now run sudo commands without a password."
    echo "Test it with: sudo whoami"
else
    echo "✗ Error: Invalid sudoers configuration. Removing file..."
    sudo rm -f "$SUDOERS_FILE"
    exit 1
fi

