# Speeding Up Testing

## Problem
VM setup and testing cycles are slow because you have to:
- Boot the VM
- Install/configure the system
- Run tests
- Repeat

## Solutions

### 1. Use VirtualBox Snapshots (BEST for VM testing)

**One-time setup:**
1. Create your VM and install Debian
2. Install development tools (git, python3, etc.)
3. Clone this repo into the VM
4. Set up the environment (venv, dependencies)
5. **Create a snapshot** in VirtualBox:
   - Right-click VM → Snapshots → Take Snapshot
   - Name it "Clean Base" or "Ready for Testing"

**For each test run:**
1. Right-click VM → Snapshots → Restore Snapshot → "Clean Base"
2. Boot VM (takes ~10 seconds instead of full install)
3. Run your tests
4. If you need to test changes, make them, then restore snapshot again

**This reduces test cycle from 30+ minutes to ~30 seconds!**

### 2. Use Docker for Unit/Integration Tests (Fastest)

For tests that don't need full OS (most of our tests), use Docker:

```bash
# Create Dockerfile for testing
docker build -t ai-os-test .
docker run --rm ai-os-test pytest tests/
```

This runs tests in seconds instead of minutes.

### 3. Test Locally First, VM Second

- Run all unit tests locally (fast feedback)
- Only use VM for E2E tests that need full OS
- This catches 90% of issues before slow VM testing

### 4. Parallel Test Execution

```bash
# Run tests in parallel (faster)
pytest tests/ -n auto  # Requires pytest-xdist
```

### 5. Incremental ISO Builds

For ISO building, live-build caches packages. Subsequent builds are faster if you don't clean the cache.

## Recommended Workflow

1. **Development**: Test locally with `pytest tests/` (fast)
2. **Integration**: Use Docker for integration tests (medium speed)
3. **E2E**: Use VM snapshots for full OS testing (fast restore)
4. **ISO Build**: Only when you need a new ISO (one-time, can run in background)

## Quick Setup Script

I'll create a script to automate snapshot management.



