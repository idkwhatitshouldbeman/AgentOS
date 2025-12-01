# Fast OS Testing Setup

## The Problem
OS testing is slow because you have to:
- Boot VM
- Install OS
- Set up environment
- Test
- Repeat

## The Solution: Snapshots + Automation

**One-time setup (15 minutes), then testing is instant (5 seconds).**

## Quick Setup (One Time)

### 1. Create and Configure VM
```bash
./scripts/setup-vm-fast.sh
```

This creates the VM with optimal settings and attaches the ISO.

### 2. Install Debian
- Start the VM in VirtualBox
- Install Debian (minimal install is fine)
- Don't install desktop environment (saves time)

### 3. Post-Install Setup (Inside VM)
Copy `scripts/vm-post-install.sh` into the VM (via shared folder or copy-paste), then:

```bash
chmod +x vm-post-install.sh
./vm-post-install.sh
```

This installs all dev tools, clones repo, sets up Python, runs tests.

### 4. Create Snapshot (From Host)
```bash
./scripts/vm-snapshot-helper.sh create
```

**Done!** Now testing is fast.

## Fast Testing Workflow

### Option 1: Just Reset VM
```bash
make reset-vm
# or
./scripts/test-os-fast.sh
```

This resets the VM to clean state in ~5 seconds. Then start it and test.

### Option 2: Complete Cycle
```bash
make test-cycle
# or
./scripts/quick-test-cycle.sh
```

This:
1. Runs local tests (2 seconds)
2. Resets VM to clean state (5 seconds)
3. VM ready for OS testing

**Total: ~7 seconds instead of 30+ minutes!**

## Daily Workflow

1. **Write code**
2. **Run `make test`** (local, 2 seconds)
3. **Fix issues**
4. **When ready for OS test: `make reset-vm`** (5 seconds)
5. **Start VM, test OS features**
6. **Repeat from step 1**

## Tips

- **Keep VM powered off** when not testing (saves resources)
- **Use headless mode** for automated testing:
  ```bash
  VBoxManage startvm AgenticOS --type headless
  ```
- **Create multiple snapshots** for different test scenarios
- **Local tests catch 90% of issues** - only use VM for OS-specific testing

## Time Comparison

| Task | Without Snapshots | With Snapshots |
|------|------------------|---------------|
| Reset VM | 30+ min (reinstall) | 5 seconds |
| Test cycle | 30+ min | 7 seconds |
| Daily dev | Slow | Fast |

**That's why snapshots are essential for fast OS testing!**


