"""
System control tools for the AI agent.
Provides privileged access to system operations.
"""

from __future__ import annotations

import os
import platform
import psutil
import subprocess
import time
from typing import Any, Dict, List, Optional


class SystemTools:
    """
    System control tools with safety checks.
    
    Provides system information, process management, and system control.
    """

    def __init__(self, allow_privileged: bool = True):
        """
        Initialize system tools.
        
        Args:
            allow_privileged: Whether to allow privileged operations (default: True for AI-first OS)
        """
        self.allow_privileged = allow_privileged

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information.
        
        Returns:
            Dict with system information
        """
        try:
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "success": True,
                "system": {
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "platform_version": platform.version(),
                    "architecture": platform.machine(),
                    "hostname": platform.node(),
                    "processor": platform.processor(),
                },
                "cpu": {
                    "count": cpu_count,
                    "percent": cpu_percent,
                    "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "percent": memory.percent,
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100,
                },
            }
        except Exception as e:
            return {"error": f"Error getting system info: {e}"}

    def list_processes(self, limit: int = 20) -> Dict[str, Any]:
        """
        List running processes.
        
        Args:
            limit: Maximum number of processes to return
            
        Returns:
            Dict with process list
        """
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
            
            return {
                "success": True,
                "processes": processes[:limit],
                "total": len(processes),
            }
        except Exception as e:
            return {"error": f"Error listing processes: {e}"}

    def get_process_info(self, pid: int) -> Dict[str, Any]:
        """
        Get detailed information about a process.
        
        Args:
            pid: Process ID
            
        Returns:
            Dict with process information
        """
        try:
            proc = psutil.Process(pid)
            return {
                "success": True,
                "pid": pid,
                "name": proc.name(),
                "status": proc.status(),
                "cpu_percent": proc.cpu_percent(interval=0.1),
                "memory_percent": proc.memory_percent(),
                "memory_info": proc.memory_info()._asdict(),
                "create_time": proc.create_time(),
                "cmdline": proc.cmdline(),
                "cwd": proc.cwd(),
            }
        except psutil.NoSuchProcess:
            return {"error": f"Process {pid} not found"}
        except Exception as e:
            return {"error": f"Error getting process info: {e}"}

    def run_command(self, command: str, timeout: int = 30, shell: bool = True) -> Dict[str, Any]:
        """
        Run a system command.
        
        Args:
            command: Command to run
            timeout: Timeout in seconds
            shell: Whether to run in shell
            
        Returns:
            Dict with command output
        """
        if not self.allow_privileged:
            # Safety check: prevent dangerous commands
            dangerous = ['rm -rf', 'format', 'dd if=', 'mkfs', 'fdisk']
            if any(cmd in command.lower() for cmd in dangerous):
                return {"error": "Dangerous command blocked"}
        
        try:
            result = subprocess.run(
                command if shell else command.split(),
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=os.environ.copy(),
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command,
            }
        except subprocess.TimeoutExpired:
            return {"error": f"Command timed out after {timeout} seconds"}
        except Exception as e:
            return {"error": f"Error running command: {e}"}

    def get_network_info(self) -> Dict[str, Any]:
        """
        Get network interface information.
        
        Returns:
            Dict with network information
        """
        try:
            interfaces = []
            net_io = psutil.net_io_counters()
            
            for interface, addrs in psutil.net_if_addrs().items():
                interfaces.append({
                    "name": interface,
                    "addresses": [
                        {
                            "family": str(addr.family),
                            "address": addr.address,
                            "netmask": addr.netmask,
                        }
                        for addr in addrs
                    ],
                })
            
            return {
                "success": True,
                "interfaces": interfaces,
                "io": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                },
            }
        except Exception as e:
            return {"error": f"Error getting network info: {e}"}

    def get_environment_vars(self) -> Dict[str, Any]:
        """
        Get environment variables.
        
        Returns:
            Dict with environment variables
        """
        try:
            # Filter out sensitive variables
            sensitive = ['PASSWORD', 'SECRET', 'KEY', 'TOKEN', 'API']
            env_vars = {
                k: v if not any(s in k.upper() for s in sensitive) else "***REDACTED***"
                for k, v in os.environ.items()
            }
            
            return {
                "success": True,
                "environment": env_vars,
            }
        except Exception as e:
            return {"error": f"Error getting environment: {e}"}

