## Oracle VirtualBox Setup (Phase 1)

These steps mirror **Phase 1: Oracle VirtualBox Setup (Testing from day 1)** from `design.plan.md`.  
Follow them on your **host machine**; this repo just documents and scripts parts of the process.

### 1. Install Oracle VirtualBox

On most Linux distros:

```bash
sudo apt install virtualbox        # Debian/Ubuntu
# or use your distro's package manager
```

On Windows/macOS: download from the official VirtualBox website and install.

### 2. Create a New VM

Recommended initial settings:

- Name: `AI-OS-Dev`
- Type: Linux
- Version: (your base distro, e.g., Debian (64-bit))
- Memory: **8–16GB RAM**
- CPUs: **4+ vCPUs** (enable nested virtualization if available)
- Disk: **40–80GB** dynamically allocated

Under **System → Acceleration**:

- Ensure VT-x/AMD-V is enabled in your BIOS/UEFI.
- Enable hardware virtualization in VirtualBox if available.

### 3. Install Base Distro in the VM

You can choose **Debian minimal** or **Arch**; this doc assumes **Debian minimal** for simplicity:

1. Download the Debian netinst ISO.
2. Attach ISO to the VM and boot it.
3. During installation, choose:
   - Minimal package selection (no desktop environment yet if you want it really lean).
   - A normal user account (e.g., `dev`).
4. After install, remove ISO and boot into your new system.

### 4. Inside the VM: Dev & Test Environment

Log in and run:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv build-essential \
  xorg xterm openbox    # basic X11 + tiny WM for early tests
```

Clone this repo **inside the VM** and set up Python:

```bash
git clone <your-repo-url> ai-os
cd ai-os
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

If tests all pass, your Phase 1 dev environment is ready.


