# Dual Testing Workflow: Code + Visual

## Two Types of Testing

### 1. Code Testing (Fast - No VM)
**For:** Logic, file operations, agent behavior, tool system
**Command:** `make test` (2 seconds)
**When:** 90% of development time

### 2. Visual/Interactive Testing (VM Required)
**For:** Seeing the OS, UI, AI interface, screen interactions
**Command:** Boot VM, interact with it
**When:** Testing UI, visual features, full system behavior

## The Workflow

### Daily Development Cycle

```bash
# 1. Write code
vim src/agent/file_tools.py

# 2. Test code logic (fast, no VM)
make test
# ✓ All tests pass in 2 seconds

# 3. When ready to see it visually:
make reset-vm    # Reset VM to clean state (5 seconds)

# 4. Start VM in VirtualBox (GUI mode)
# - See the OS
# - Interact with UI
# - Test AI interface
# - See screen capture working
# - Test visual features

# 5. Make changes, repeat
```

## VM Setup for Visual Testing

Your VM needs:
- **Desktop environment** (so you can see/interact)
- **X11/Wayland** (for screen capture to work)
- **Development tools** (to run your code)

### Quick VM Setup with Desktop

1. **Install Debian with desktop:**
   - During Debian install, choose "Desktop Environment" (GNOME, KDE, or XFCE)
   - Or install minimal, then: `sudo apt install xfce4` (lightweight)

2. **Inside VM, set up your project:**
   ```bash
   # Copy your code into VM (via shared folder or git)
   cd ~/dev/AgentOS
   
   # Set up Python
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   .venv/bin/pip install -e .
   
   # Run your agent
   .venv/bin/python -m agent.agent_core
   ```

3. **Create snapshot:**
   ```bash
   # From host
   ./scripts/vm-snapshot-helper.sh create
   ```

## Visual Testing Scenarios

### Test Screen Capture
```bash
# In VM, run your screen capture code
python -m agent.screen_capture
# See it actually capture the screen
```

### Test AI Interface
```bash
# In VM, run your AI agent
python -m agent.agent_core
# See the AI interface overlay
# Interact with it
```

### Test File Operations Visually
```bash
# In VM, use file manager
# Ask AI to organize files
# See it happen in real-time
```

### Test Input Automation
```bash
# In VM, open an app
# Ask AI to click buttons
# Watch it happen
```

## Best of Both Worlds

### Fast Code Development
- Write code
- `make test` (2 seconds)
- Fix issues
- Repeat quickly

### Visual Verification
- When ready: `make reset-vm` (5 seconds)
- Boot VM
- See your OS in action
- Interact with it
- Verify everything works visually

## Time Breakdown

| Task | Time | When |
|------|------|------|
| Code test (`make test`) | 2 seconds | Every code change |
| VM reset (`make reset-vm`) | 5 seconds | When ready for visual test |
| Boot VM | 10-20 seconds | When testing visually |
| Visual testing | As long as needed | See/interact with OS |

**Total development cycle:**
- Code changes: 2 seconds per test
- Visual verification: ~30 seconds to boot + testing time

## Tips for Visual Testing

1. **Keep VM running** when actively testing UI (faster than rebooting)
2. **Use snapshots** to reset when you break something
3. **Test code first** - catch 90% of issues before visual testing
4. **Screenshot/record** visual tests for documentation

## The Key Point

**You need both:**
- Fast code testing (no VM) - for development speed
- Visual testing (VM) - to see your OS actually work

The snapshot system makes visual testing fast too - reset in 5 seconds instead of reinstalling.


