# Testing Strategy - Keep It Simple

## The Reality: You Don't Need VMs for Most Testing

**90% of your tests can run locally in seconds.** VMs are only needed for:
- Testing the actual OS installation process
- E2E tests that need full system integration
- Testing hardware-specific features (overclocking, etc.)

## Simple Testing Workflow

### Daily Development (No VM)

```bash
# Just run tests - that's it!
make test

# Or even simpler:
./scripts/test.sh
```

**This runs all your unit tests, integration tests, file operation tests, etc. - all locally in seconds.**

### When You Actually Need a VM

Only use VMs for:
1. **Testing ISO builds** - Does the ISO boot correctly?
2. **Full OS integration** - Does everything work together in a real install?
3. **Hardware features** - Overclocking, system-level APIs

For these rare cases, use snapshots (fast restore).

## Test Categories

### ✅ Local Tests (No VM - Fast)
- Unit tests (agent logic, file tools, etc.)
- Integration tests (agent + tools together)
- File operation tests
- Tool system tests
- LLM interface tests (with mocks)

**These run in seconds locally.**

### 🐳 Docker Tests (Optional - Isolated)
- Same as local tests but in isolated container
- Use if you want guaranteed clean environment
- Still fast (seconds)

### 💻 VM Tests (Rare - Full OS)
- E2E tests that need real OS
- ISO boot testing
- Full system integration
- Use snapshots to make this fast

## Recommended Workflow

1. **Write code**
2. **Run `make test`** (local, fast feedback)
3. **Fix issues** (repeat)
4. **Commit when tests pass**
5. **Use VM only when you need to test full OS** (rare)

## The Bottom Line

**For development: Just run `make test`. That's it.**

VMs are for the final "does it work in a real OS?" check, not for daily development.


