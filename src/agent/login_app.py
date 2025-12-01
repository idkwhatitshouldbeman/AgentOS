#!/usr/bin/env python3
import sys
import os
import subprocess

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("WARNING: Tkinter not found. Falling back to console login.")
    # Fallback: Just start the session directly for now, or show a text prompt
    # In a real scenario, we might use a text-based dialog (whiptail)
    print("Starting Openbox session (fallback)...")
    subprocess.Popen(["openbox-session"])
    sys.exit(0)

# Configuration
BACKGROUND_COLOR = "#F5F5DC"  # Beige
ACCENT_COLOR = "#8B4513"      # SaddleBrown (Woody/Earthy)
TEXT_COLOR = "#3E2723"        # Dark Brown
FONT_FAMILY = "Sans"

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AgentOS Login")
        
        # Fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Bind escape to exit (for debugging)
        self.root.bind("<Escape>", lambda e: sys.exit(1))

        # Main Container
        self.frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Profile Picture (Placeholder)
        self.canvas = tk.Canvas(self.frame, width=120, height=120, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack(pady=20)
        self.draw_profile_pic()

        # Username
        self.lbl_user = tk.Label(self.frame, text="admin", font=(FONT_FAMILY, 24, "bold"), 
                                 bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.lbl_user.pack(pady=10)

        # Password Entry
        self.ent_pass = tk.Entry(self.frame, show="*", font=(FONT_FAMILY, 16), width=20,
                                 bg="white", fg="black", relief="flat", highlightthickness=1, highlightbackground=ACCENT_COLOR)
        self.ent_pass.pack(pady=10, ipady=5)
        self.ent_pass.bind("<Return>", self.login)
        self.ent_pass.focus_set()

        # Login Button
        self.btn_login = tk.Button(self.frame, text="Sign In", font=(FONT_FAMILY, 14), 
                                   bg=ACCENT_COLOR, fg="white", activebackground=TEXT_COLOR, activeforeground="white",
                                   relief="flat", command=self.login, width=15)
        self.btn_login.pack(pady=20)

        # Power Controls (Bottom Right)
        self.pwr_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.pwr_frame.place(relx=0.95, rely=0.95, anchor="se")
        
        tk.Button(self.pwr_frame, text="Shutdown", command=self.shutdown, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, relief="flat").pack(side="right", padx=10)
        tk.Button(self.pwr_frame, text="Restart", command=self.restart, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, relief="flat").pack(side="right", padx=10)

    def draw_profile_pic(self):
        # Draw a circle
        self.canvas.create_oval(10, 10, 110, 110, fill="#D2B48C", outline=ACCENT_COLOR, width=3)
        # Draw a simple user icon silhouette
        self.canvas.create_oval(35, 25, 85, 75, fill=ACCENT_COLOR, outline="") # Head
        self.canvas.create_arc(20, 80, 100, 160, start=0, extent=180, fill=ACCENT_COLOR, outline="") # Shoulders

    def login(self, event=None):
        password = self.ent_pass.get()
        if password == "admin":
            self.start_session()
        else:
            messagebox.showerror("Login Failed", "Incorrect password")
            self.ent_pass.delete(0, tk.END)

    def start_session(self):
        # Destroy the login window
        self.root.destroy()
        
        # Start Openbox
        # We use os.execvp to replace the current process with openbox
        # This ensures openbox takes over the X session
        print("Starting Openbox session...")
        try:
            # We need to run openbox-session
            # Note: In a real display manager, we would setuid to the user here.
            # But since we are running as root (from inittab -> startx -> .xinitrc), 
            # we are already root.
            # TODO: Switch to 'admin' user before executing if we want to run as user.
            # For now, let's keep it simple and run as the current user (which is root in the current setup).
            
            # Switch to 'admin' user and start Openbox
            # We use 'su' to switch user. 
            # We need to preserve environment variables like DISPLAY.
            # We also need to ensure the user can access the X server (handled in .xinitrc via xhost +)
            
            cmd = ["su", "admin", "-c", "export DISPLAY=:0 && openbox-session"]
            
            # We use Popen so this script can exit
            subprocess.Popen(cmd)
            sys.exit(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start session: {e}")

    def shutdown(self):
        os.system("poweroff")

    def restart(self):
        os.system("reboot")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
