# Custom OS Build with Buildroot

## Overview

This document explains the custom barebones OS built with Buildroot for the AgentOS project.

## What is Buildroot?

Buildroot is a simple, efficient, and easy-to-use tool to generate embedded Linux systems through cross-compilation. It creates a completely custom Linux distribution with only the components you need.

## Why Buildroot for AI-OS?

- **Minimal size**: 10-50 MB ISO (vs 800 MB+ for Debian)
- **No installation wizard**: Boots directly, no setup prompts
- **Complete control**: Only includes what you specify
- **Fast boot**: 1-3 seconds from power-on to shell
- **Auto-configured**: Everything set up automatically
- **Custom init**: Can auto-start your AI agent on boot

## What's Included

Our custom AI-OS includes:
- Linux kernel (x86_64, latest stable)
- BusyBox (minimal Unix utilities)
- Python 3 + pip
- Your AI agent code (`/opt/ai-agent`)
- Syslinux bootloader
- Auto-login configuration
- DHCP for automatic networking

## Build Process

### First Time Build

```bash
# Build the OS (takes 30-60 minutes)
make build-custom-os
```

This will:
1. Download all required packages (~200-500 MB)
2. Compile the Linux kernel
3. Build Python and dependencies
4. Create the root filesystem
5. Generate a bootable ISO

### Rebuild (after changes)

```bash
# Quick rebuild (only changed components, 5-10 minutes)
make rebuild-custom-os
```

## Testing the OS

```bash
# Boot in VirtualBox
make test-custom-os
```

This will:
1. Create a VM (if not exists)
2. Attach the custom ISO
3. Boot the OS
4. You'll see: Auto-login → AI agent demo running

## File Locations

- **Buildroot source**: `buildroot/`
- **Configuration**: `buildroot-config/`
- **Custom files (overlay)**: `buildroot-config/overlay/`
- **Built ISO**: `buildroot/output/images/rootfs.iso9660`
- **Build log**: `buildroot-build.log`

## Custom Overlay Structure

The overlay directory contains files that are copied into the final OS:

```
buildroot-config/overlay/
├── etc/
│   ├── inittab                    # Auto-login configuration
│   └── init.d/
│       └── S99ai-agent            # AI agent startup script
├── opt/
│   └── ai-agent/                  # Your AI agent code
│       ├── agent/                 # Python modules
│       └── start.sh               # Agent launcher
└── root/
    └── .profile                   # Welcome message + auto-start
```

## Boot Process

1. **BIOS/UEFI** → Loads Syslinux bootloader (1 second)
2. **Bootloader** → Loads Linux kernel (1 second)
3. **Kernel** → Initializes hardware, mounts root filesystem (0.5 seconds)
4. **Init** → BusyBox init starts (0.5 seconds)
5. **Auto-login** → Direct to shell, no password (instant)
6. **.profile** → Shows welcome banner, starts AI agent
7. **Ready!** Total: ~3 seconds

## Configuration Options

To modify the OS configuration:

```bash
cd buildroot
make menuconfig
```

This opens a menu where you can:
- Add/remove packages
- Change kernel version/config
- Modify filesystem options
- Enable/disable features

After making changes:
```bash
make  # Rebuild
```

## Adding Python Packages

To add Python packages to the OS:

1. **Option A**: Add to Buildroot config
   ```bash
   cd buildroot
   make menuconfig
   # Navigate to: Target packages → Interpreter languages and scripting → python3
   ```

2. **Option B**: Include in your overlay
   - Pre-download Python packages
   - Add to `buildroot-config/overlay/opt/ai-agent/`
   - Install during first boot or in your start script

## Troubleshooting

### Build Fails
- Check `buildroot-build.log` for errors
- Common issues:
  - Missing build dependencies (install gcc, make, etc.)
  - No internet connection (can't download packages)
  - Disk space (need 5-10 GB free)

### ISO Not Generated
- Check if ISO support is enabled:
  ```bash
  grep BR2_TARGET_ROOTFS_ISO9660 buildroot/.config
  ```
- Should see: `BR2_TARGET_ROOTFS_ISO9660=y`

### Python Not Working
- Verify Python is enabled in config
- Check build log for Python compilation errors

### AI Agent Not Starting
- Check `/opt/ai-agent/start.sh` has execute permissions
- Verify your agent code is in the overlay
- Look at boot messages for errors

## Customization Examples

### Change Boot Message
Edit: `buildroot-config/overlay/root/.profile`

### Add More Tools
```bash
cd buildroot
make menuconfig
# Navigate to Target packages → find your tool
```

### Change Kernel Version
```bash
cd buildroot
make menuconfig
# Navigate to Kernel → Kernel version
```

## Performance

- **ISO size**: ~15-40 MB (depends on packages)
- **RAM usage**: 64-128 MB (minimal)
- **Boot time**: 1-3 seconds
- **Build time**: 
  - First build: 30-60 minutes
  - Incremental rebuilds: 5-10 minutes

## Next Steps

Once the OS is built and running:

1. Test that Python works
2. Test that your AI agent runs
3. Add more features:
   - X11 support (for screen capture)
   - Additional Python packages
   - Network tools
   - Development tools (for on-device coding)

## Resources

- [Buildroot Manual](https://buildroot.org/downloads/manual/manual.html)
- [Buildroot Package List](https://buildroot.org/downloads/list.html)
- Project docs: See `PROJECT_STATUS.md`
