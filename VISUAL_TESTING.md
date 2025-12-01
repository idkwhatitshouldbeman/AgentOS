# Visual Testing Guide

## You Need Both Types of Testing

### 1. Code Testing (Fast)
```bash
make test    # 2 seconds - test logic
```
**For:** File operations, agent logic, tool system

### 2. Visual Testing (VM)
```bash
make test-visual    # Code tests + start VM
# or
make start-vm       # Just start VM
```
**For:** Seeing the OS, UI, AI interface, screen interactions

## Quick Visual Testing

### Option 1: Full Workflow
```bash
make test-visual
```
This:
1. Runs code tests (2 seconds)
2. Optionally resets VM (5 seconds)
3. Starts VM with GUI (10-20 seconds)
4. You can now see and interact with the OS

### Option 2: Just Start VM
```bash
make start-vm
```
If VM is already set up, just start it.

## What You Can Test Visually

### In the VM Desktop:
- **See the OS** - Desktop environment, windows, UI
- **Run your AI agent** - See it in action
- **Test screen capture** - Watch it capture the screen
- **Test input automation** - See AI click/type
- **Test file operations** - See files being managed
- **Interact with AI interface** - Use the overlay/panel

## Setup for Visual Testing

### 1. VM with Desktop
Your VM needs a desktop environment:
- XFCE (lightweight, recommended)
- GNOME (full-featured)
- KDE (full-featured)

The `vm-post-install.sh` script installs XFCE automatically.

### 2. Inside VM
After booting:
```bash
# Your code should be in ~/dev/AgentOS
cd ~/dev/AgentOS

# Run your agent
.venv/bin/python -m agent.agent_core

# Or test screen capture
.venv/bin/python -c "from agent.screen_capture import capture; capture()"
```

## Workflow

### Development (Most of the time):
```bash
# Write code
vim src/agent/file_tools.py

# Test logic (fast)
make test

# Fix issues
# Repeat
```

### Visual Verification (When needed):
```bash
# Test code first
make test

# Then see it visually
make test-visual

# Interact with OS in VM
# See everything working
```

## Time Breakdown

- **Code test:** 2 seconds (do this often)
- **VM reset:** 5 seconds (when needed)
- **VM boot:** 10-20 seconds (when testing visually)
- **Visual testing:** As long as you need

**Most development:** Just `make test` (2 seconds)
**Visual verification:** `make test-visual` (~30 seconds total)

## Tips

1. **Keep VM running** when actively testing UI (don't reboot each time)
2. **Use snapshots** to reset when you break something
3. **Test code first** - catch issues before visual testing
4. **Screenshot** visual tests for documentation

## The Bottom Line

- **Code development:** `make test` (fast, no VM)
- **Visual testing:** `make test-visual` (VM with GUI)
- **Both are fast** thanks to snapshots and local testing

You get the best of both worlds!


