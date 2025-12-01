# Windows-Like Transformation Plan for AgentOS

## Vision
Transform the barebones Linux system into a polished, "Windows-like" experience with a proper login screen, desktop environment, and a "Beige Flowy" aesthetic. The system should be modular and easy to modify.

## Phase 1: Foundation & User Management (The "Underground")
- [ ] **Create Standard User**: Create a non-root user (e.g., `admin` or `user`) to simulate a real OS environment.
- [ ] **Permissions**: Ensure the user has `sudo` access (passwordless for now) and ownership of their home directory.
- [ ] **Home Directory Skeleton**: Set up standard folders (`Documents`, `Downloads`, `Desktop`) in `/etc/skel`.

## Phase 2: The Graphical Login Screen (The "Gatekeeper")
*Goal: A custom, easy-to-modify login screen written in Python.*
- [ ] **GUI Library**: Ensure `python3-tkinter` or a similar lightweight GUI lib is installed.
- [ ] **Login App (`/opt/ai-agent/login.py`)**:
    - [ ] Beige, flowy background.
    - [ ] User profile picture (circle).
    - [ ] Password input field.
    - [ ] "Sign In" button.
- [ ] **Boot Integration**:
    - [ ] Modify `inittab` to start X11 automatically on tty1.
    - [ ] Modify `.xinitrc` to launch `login.py` INSTEAD of the desktop initially.
    - [ ] Make `login.py` launch `openbox-session` upon successful auth.

## Phase 3: The Desktop Environment (The "Workspace")
*Goal: A familiar, beige-themed desktop.*
- [ ] **Panel/Taskbar (`tint2`)**:
    - [ ] Configure to look like Windows 11 (centered icons or left-aligned).
    - [ ] Beige semi-transparent theme.
- [ ] **Wallpaper**:
    - [ ] Generate/Add a "Beige Flowy" abstract wallpaper.
    - [ ] Use `feh` or `pcmanfm` to set it.
- [ ] **Desktop Icons**:
    - [ ] "My Computer", "Recycle Bin", "AI Agent".
- [ ] **Start Menu**:
    - [ ] Configure `rofi` or `dmenu` with a custom theme to act as the Start Menu.

## Phase 4: The "Beige Flowy" Theme (The "Vibe")
- [ ] **GTK Theme**: Create/Install a `BeigeOS` GTK theme.
- [ ] **Openbox Theme**: Create a window border theme with rounded corners and beige tones.
- [ ] **Cursor**: Ensure the mouse cursor is visible and styled (maybe a soft dark arrow).
- [ ] **Fonts**: Install a clean sans-serif font (e.g., Roboto, Inter).

## Phase 5: System Services (The "Plumbing")
- [ ] **Network Manager**: Ensure Wi-Fi/Ethernet connects automatically and has a UI tray icon.
- [ ] **Sound**: Volume control in the tray.
- [ ] **Power Management**: Sleep/Shutdown options in the Start Menu.

## Phase 6: The AI Integration (The "Brain")
- [ ] **Desktop Widget**: A floating AI chat bubble on the desktop.
- [ ] **"Camera" Integration**: Ensure the AI can take screenshots of the desktop to "see" what's happening.

---

## Immediate Next Steps (Execution)
1.  **Verify Python GUI support**: Check if `tkinter` is enabled. If not, enable it.
2.  **Create the Login App**: Write the Python code for the visual login screen.
3.  **Wire it up**: Change the boot sequence to load this app.
