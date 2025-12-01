# Complete Setup Guide - Step by Step

## Where Everything Goes

```
/home/aaroh/Downloads/AgentOS/          ← Your project (already here)
├── scripts/                           ← Automation scripts (already here)
├── debian-netinst.iso                 ← ISO file (already here)
└── ... (all your code)

VM will be created at:
/home/aaroh/VirtualBox VMs/AgenticOS/  ← VirtualBox creates this automatically
```

## Step-by-Step Setup

### Step 1: Delete Old VM (If It Exists)

In VirtualBox:
1. Right-click "AgenticOS" → Remove → Delete all files

Or via command:
```bash
VBoxManage unregistervm AgenticOS --delete
```

### Step 2: Create New VM (Automated)

From your project directory:
```bash
cd /home/aaroh/Downloads/AgentOS
./scripts/setup-vm-fast.sh
```

This will:
- Create VM named "AgenticOS"
- Set RAM to 4GB (reasonable)
- Set 2 CPUs
- Create 20GB disk
- Attach the Debian ISO automatically

**Output location:** `/home/aaroh/VirtualBox VMs/AgenticOS/`

### Step 3: Install Debian in VM

1. **Start the VM** in VirtualBox (click "Start")
2. **Install Debian:**
   - Choose "Install" (not graphical install - faster)
   - Language: English
   - Region: Your region
   - Keyboard: Your layout
   - Hostname: `ai-os-dev` (or anything)
   - Domain: leave blank
   - Root password: set one
   - User: create a user (remember password)
   - Partition: Use entire disk (guided, single partition)
   - Software: **Uncheck everything** (we'll install manually - faster)
   - Install GRUB: Yes
   - Finish installation

**This takes ~5-10 minutes**

### Step 4: Set Up Development Environment (Inside VM)

After Debian installs and reboots:

**Option A: Copy script into VM (Easiest)**

1. In VirtualBox, go to VM Settings → Shared Folders
2. Add shared folder:
   - Folder Path: `/home/aaroh/Downloads/AgentOS`
   - Folder Name: `AgentOS`
   - Check "Auto-mount" and "Make Permanent"
3. Inside VM, mount it:
   ```bash
   sudo mkdir -p /mnt/AgentOS
   sudo mount -t vboxsf AgentOS /mnt/AgentOS
   ```
4. Copy and run the setup script:
   ```bash
   cp /mnt/AgentOS/scripts/vm-post-install.sh ~/
   chmod +x ~/vm-post-install.sh
   ./vm-post-install.sh
   ```

**Option B: Manual setup (If shared folders don't work)**

Inside the VM, run these commands:

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install dev tools
sudo apt install -y git python3 python3-pip python3-venv curl wget vim build-essential

# Create workspace
mkdir -p ~/dev
cd ~/dev

# Clone your repo (you'll need to get it into the VM somehow)
# Option 1: Use git if you have a remote repo
# git clone <your-repo-url> AgentOS

# Option 2: Copy files via USB/shared folder
# Option 3: Use scp from host if you enable SSH

cd AgentOS  # or wherever you put the files

# Set up Python
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .

# Test it works
.venv/bin/python -m pytest tests/ -v
```

### Step 5: Create Snapshot (From Host Machine)

Back on your **host machine** (not in VM):

```bash
cd /home/aaroh/Downloads/AgentOS
./scripts/vm-snapshot-helper.sh create
```

This saves the current VM state. Now you can reset to this state in 5 seconds!

## Quick Reference

### File Locations

**Host Machine:**
- Project: `/home/aaroh/Downloads/AgentOS/`
- ISO: `/home/aaroh/Downloads/AgentOS/debian-netinst.iso`
- VM files: `/home/aaroh/VirtualBox VMs/AgenticOS/` (auto-created)

**Inside VM:**
- Your code: `~/dev/AgentOS/` (or wherever you put it)
- Python venv: `~/dev/AgentOS/.venv/`

### Common Commands

**On Host:**
```bash
# Reset VM to clean state (5 seconds)
make reset-vm

# Full test cycle (local + VM reset)
make test-cycle

# Create new snapshot
./scripts/vm-snapshot-helper.sh create

# List snapshots
./scripts/vm-snapshot-helper.sh list
```

**Inside VM:**
```bash
# Run tests
cd ~/dev/AgentOS
.venv/bin/python -m pytest tests/ -v

# Or activate venv first
source .venv/bin/activate
pytest tests/ -v
```

## Troubleshooting

### Shared Folders Not Working?
- Make sure VirtualBox Guest Additions are installed in VM
- Or use manual copy/SCP/USB

### VM Won't Start?
- Check KVM is disabled (see `docs/fix-virtualbox-kvm-conflict.md`)
- Check VM has enough resources

### Snapshot Fails?
- Make sure VM is powered off
- Check snapshot name matches exactly

## Next Steps After Setup

1. **Test locally first:** `make test` (fast)
2. **When ready for OS test:** `make reset-vm` (resets VM)
3. **Start VM and test OS features**
4. **Repeat**

That's it! The setup is one-time, then testing is fast.


