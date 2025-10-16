#!/usr/bin/env python3
"""
KALI TOOLS WINDOWS INSTALLER - Installs and Configures Real Kali Tools on Windows
Makes tools immediately usable after installation
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tempfile
import shutil
import winreg
import ctypes
import json
from pathlib import Path
import psutil

class KaliWindowsInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.architecture = platform.architecture()[0]
        self.kali_dir = Path.home() / "KaliTools"
        self.bin_dir = self.kali_dir / "bin"
        self.temp_dir = tempfile.mkdtemp(prefix="kali_install_")
        
        # Comprehensive Kali tools with Windows-specific downloads
        self.kali_tools = {
            'information_gathering': {
                'nmap': {
                    'url': 'https://nmap.org/dist/nmap-7.94-setup.exe',
                    'installer': True,
                    'executable': 'nmap.exe',
                    'post_install': ['nmap --version']
                },
                'masscan': {
                    'url': 'https://github.com/robertdavidgraham/masscan/releases/download/1.3.2/masscan-1.3.2.exe',
                    'executable': 'masscan.exe',
                    'rename_to': 'masscan.exe'
                },
                'sublist3r': {
                    'type': 'python',
                    'pip_name': 'sublist3r',
                    'executable': 'sublist3r.py'
                },
                'theharvester': {
                    'type': 'python', 
                    'pip_name': 'theharvester',
                    'executable': 'theHarvester.py'
                },
                'amass': {
                    'url': 'https://github.com/OWASP/Amass/releases/download/v3.23.3/amass_windows_amd64.zip',
                    'executable': 'amass.exe'
                }
            },
            'vulnerability_analysis': {
                'sqlmap': {
                    'type': 'python',
                    'pip_name': 'sqlmap',
                    'executable': 'sqlmap.py'
                },
                'nikto': {
                    'url': 'https://github.com/sullo/nikto/archive/refs/heads/master.zip',
                    'type': 'perl',
                    'executable': 'program\\nikto.pl'
                },
                'nuclei': {
                    'url': 'https://github.com/projectdiscovery/nuclei/releases/download/v2.9.15/nuclei_2.9.15_windows_amd64.zip',
                    'executable': 'nuclei.exe'
                }
            },
            'web_applications': {
                'dirb': {
                    'url': 'https://downloads.sourceforge.net/project/dirb/dirb/2.22/dirb222.tar.gz',
                    'executable': 'dirb.exe'
                },
                'gobuster': {
                    'url': 'https://github.com/OJ/gobuster/releases/download/v3.6.0/gobuster_3.6.0_Windows_x64.zip',
                    'executable': 'gobuster.exe'
                },
                'whatweb': {
                    'type': 'ruby',
                    'url': 'https://github.com/urbanadventurer/WhatWeb/archive/refs/heads/master.zip',
                    'executable': 'whatweb'
                }
            },
            'password_attacks': {
                'john': {
                    'url': 'https://github.com/openwall/john/archive/refs/heads/bleeding-jumbo.zip',
                    'build_required': True,
                    'executable': 'run\\john.exe'
                },
                'hashcat': {
                    'url': 'https://github.com/hashcat/hashcat/releases/download/v6.2.6/hashcat-6.2.6.7z',
                    'executable': 'hashcat.exe'
                },
                'hydra': {
                    'url': 'https://github.com/vanhauser-thc/thc-hydra/archive/refs/heads/master.zip',
                    'build_required': True,
                    'executable': 'hydra.exe'
                }
            },
            'wireless_attacks': {
                'aircrack-ng': {
                    'url': 'https://download.aircrack-ng.org/aircrack-ng-1.7-win.zip',
                    'executable': 'aircrack-ng.exe'
                }
            },
            'sniffing_spoofing': {
                'wireshark': {
                    'url': 'https://1.eu.dl.wireshark.org/win64/Wireshark-4.0.8-x64.exe',
                    'installer': True,
                    'system_install': True
                },
                'nmap': {
                    'url': 'https://nmap.org/dist/nmap-7.94-setup.exe', 
                    'installer': True,
                    'executable': 'nmap.exe'
                }
            },
            'exploitation_tools': {
                'metasploit': {
                    'url': 'https://windows.metasploit.com/metasploitframework-latest.msi',
                    'installer': True,
                    'system_install': True
                },
                'commix': {
                    'type': 'python',
                    'pip_name': 'commix',
                    'executable': 'commix.py'
                }
            }
        }
        
        # Create necessary directories
        self.setup_directories()

    def setup_directories(self):
        """Create Kali tools directory structure"""
        directories = [self.kali_dir, self.bin_dir, self.kali_dir / "logs", self.kali_dir / "config"]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        print(f"📁 Kali tools directory: {self.kali_dir}")

    def is_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_powershell(self, command):
        """Run PowerShell command"""
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def install_chocolatey(self):
        """Install Chocolatey package manager for Windows"""
        if not shutil.which("choco"):
            print("🍫 Installing Chocolatey package manager...")
            command = 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))'
            success, output = self.run_powershell(command)
            if success:
                print("✅ Chocolatey installed successfully")
                return True
            else:
                print("❌ Failed to install Chocolatey")
                return False
        return True

    def download_file(self, url, destination):
        """Download file from URL"""
        try:
            print(f"📥 Downloading {url}...")
            urllib.request.urlretrieve(url, destination)
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

    def extract_zip(self, zip_path, extract_to):
        """Extract ZIP file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False

    def add_to_path(self, directory):
        """Add directory to system PATH"""
        try:
            # Get current PATH
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ) as key:
                try:
                    current_path = winreg.QueryValueEx(key, "PATH")[0]
                except FileNotFoundError:
                    current_path = ""

            # Add new directory to PATH
            if str(directory) not in current_path:
                new_path = f"{current_path};{directory}" if current_path else str(directory)
                
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                
                print(f"✅ Added {directory} to PATH")
                return True
        except Exception as e:
            print(f"❌ Failed to add to PATH: {e}")
        return False

    def install_via_pip(self, package_name):
        """Install Python package via pip"""
        try:
            print(f"🐍 Installing {package_name} via pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name} via pip")
            return False

    def install_via_chocolatey(self, package_name):
        """Install package via Chocolatey"""
        try:
            print(f"🍫 Installing {package_name} via Chocolatey...")
            subprocess.run(["choco", "install", package_name, "-y", "--force"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def run_installer(self, installer_path, silent=True):
        """Run Windows installer"""
        try:
            print(f"⚙️ Running installer: {installer_path}")
            if silent:
                subprocess.run([installer_path, "/S", "/quiet", "/norestart"], check=True)
            else:
                subprocess.run([installer_path], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def install_nmap(self):
        """Specialized NMAP installation"""
        print("🔧 Installing NMAP...")
        
        # Try multiple installation methods
        methods = [
            lambda: self.install_via_chocolatey("nmap"),
            lambda: self.download_and_install_tool('nmap')
        ]
        
        for method in methods:
            if method():
                # Verify installation
                try:
                    subprocess.run(["nmap", "--version"], capture_output=True, check=True)
                    print("✅ NMAP installed and working!")
                    return True
                except:
                    print("⚠️ NMAP installed but not in PATH")
        
        return False

    def install_sqlmap(self):
        """Specialized SQLMap installation"""
        print("💉 Installing SQLMap...")
        
        if self.install_via_pip("sqlmap"):
            # Create batch file for easy execution
            batch_content = f'''@echo off
python -m sqlmap %*
'''
            batch_file = self.bin_dir / "sqlmap.bat"
            with open(batch_file, 'w') as f:
                f.write(batch_content)
            print("✅ SQLMap installed with batch wrapper!")
            return True
        return False

    def install_metasploit(self):
        """Specialized Metasploit installation"""
        print("💣 Installing Metasploit Framework...")
        
        if self.install_via_chocolatey("metasploit"):
            print("✅ Metasploit installed via Chocolatey!")
            return True
        
        # Alternative manual installation
        print("📥 Downloading Metasploit installer...")
        return self.download_and_install_tool('metasploit')

    def install_wireshark(self):
        """Specialized Wireshark installation"""
        print("📡 Installing Wireshark...")
        return self.install_via_chocolatey("wireshark") or self.download_and_install_tool('wireshark')

    def create_tool_wrapper(self, tool_name, command):
        """Create batch wrapper for tools"""
        batch_file = self.bin_dir / f"{tool_name}.bat"
        with open(batch_file, 'w') as f:
            f.write(f'@echo off\n{command} %*\n')
        print(f"📝 Created wrapper: {batch_file}")

    def download_and_install_tool(self, tool_name, category=None):
        """Generic tool installation method"""
        if not category:
            category = self.find_tool_category(tool_name)
        
        if not category:
            print(f"❌ Tool {tool_name} not found in database")
            return False

        tool_info = self.kali_tools[category][tool_name]
        
        if tool_info.get('type') == 'python':
            return self.install_via_pip(tool_info['pip_name'])
        
        if 'url' not in tool_info:
            print(f"❌ No download URL for {tool_name}")
            return False

        # Download the tool
        download_path = self.temp_dir / f"{tool_name}_download"
        if not self.download_file(tool_info['url'], download_path):
            return False

        # Handle installation based on file type
        if download_path.suffix.lower() in ['.exe', '.msi'] and tool_info.get('installer'):
            return self.run_installer(download_path)
        elif download_path.suffix.lower() in ['.zip', '.7z', '.tar.gz']:
            return self.handle_archive_installation(tool_name, download_path, tool_info)
        else:
            print(f"❌ Unsupported file type for {tool_name}")
            return False

    def handle_archive_installation(self, tool_name, archive_path, tool_info):
        """Handle archive file installation"""
        tool_dir = self.kali_dir / tool_name
        tool_dir.mkdir(exist_ok=True)
        
        if not self.extract_zip(archive_path, tool_dir):
            return False
        
        # Find and setup executable
        executable = self.find_executable(tool_dir, tool_info.get('executable'))
        if executable:
            # Create batch wrapper
            wrapper_content = f'@echo off\n"{executable}" %*\n'
            wrapper_file = self.bin_dir / f"{tool_name}.bat"
            with open(wrapper_file, 'w') as f:
                f.write(wrapper_content)
            print(f"✅ {tool_name} installed to {tool_dir}")
            return True
        
        print(f"❌ Could not find executable for {tool_name}")
        return False

    def find_executable(self, directory, expected_name=None):
        """Find executable file in directory"""
        if expected_name:
            potential_path = directory / expected_name
            if potential_path.exists():
                return potential_path
        
        # Search for common executable patterns
        patterns = ['*.exe', '*.bat', '*.py', '*.pl']
        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                if file_path.is_file():
                    return file_path
        return None

    def find_tool_category(self, tool_name):
        """Find which category contains the tool"""
        for category, tools in self.kali_tools.items():
            if tool_name in tools:
                return category
        return None

    def install_tool(self, tool_name):
        """Install a specific tool"""
        print(f"\n🚀 Installing {tool_name}...")
        
        # Special handling for common tools
        special_installers = {
            'nmap': self.install_nmap,
            'sqlmap': self.install_sqlmap,
            'metasploit': self.install_metasploit,
            'wireshark': self.install_wireshark
        }
        
        if tool_name in special_installers:
            return special_installers[tool_name]()
        else:
            return self.download_and_install_tool(tool_name)

    def install_category(self, category_name):
        """Install all tools in a category"""
        if category_name not in self.kali_tools:
            print(f"❌ Category {category_name} not found")
            return False
        
        print(f"\n📦 Installing {category_name} tools...")
        tools = self.kali_tools[category_name]
        success_count = 0
        
        for tool_name in tools:
            if self.install_tool(tool_name):
                success_count += 1
        
        print(f"✅ Installed {success_count}/{len(tools)} tools from {category_name}")
        return success_count

    def install_popular_tools(self):
        """Install most popular Kali tools"""
        popular_tools = ['nmap', 'sqlmap', 'wireshark', 'metasploit', 'john', 'hydra', 'aircrack-ng']
        print("\n🎯 Installing popular Kali tools...")
        
        success_count = 0
        for tool in popular_tools:
            if self.install_tool(tool):
                success_count += 1
        
        print(f"✅ Installed {success_count}/{len(popular_tools)} popular tools")
        return success_count

    def verify_installation(self, tool_name):
        """Verify if tool is installed and working"""
        try:
            # Try to run the tool
            if tool_name == 'nmap':
                subprocess.run(["nmap", "--version"], capture_output=True, check=True)
            elif tool_name == 'sqlmap':
                subprocess.run(["python", "-m", "sqlmap", "--version"], capture_output=True, check=True)
            else:
                # Generic check
                subprocess.run([tool_name, "--help"], capture_output=True, check=True)
            
            print(f"✅ {tool_name} is installed and working!")
            return True
        except:
            print(f"❌ {tool_name} is not working properly")
            return False

    def show_usage_examples(self):
        """Show usage examples for installed tools"""
        examples = {
            'nmap': 'nmap -sV 192.168.1.1',
            'sqlmap': 'sqlmap -u "http://test.com/page?id=1" --batch',
            'wireshark': 'wireshark (launches GUI)',
            'theharvester': 'theHarvester -d example.com -b google',
            'sublist3r': 'sublist3r -d example.com',
            'masscan': 'masscan -p80 192.168.1.0/24',
            'gobuster': 'gobuster dir -u http://test.com -w wordlist.txt'
        }
        
        print("\n📚 USAGE EXAMPLES:")
        print("=" * 50)
        for tool, example in examples.items():
            print(f"🔧 {tool}:")
            print(f"   {example}")
        print("=" * 50)

    def setup_environment(self):
        """Setup the complete environment"""
        print("🛠️ Setting up Kali tools environment...")
        
        # Install Chocolatey first
        if not self.install_chocolatey():
            print("⚠️ Continuing without Chocolatey...")
        
        # Add bin directory to PATH
        self.add_to_path(str(self.bin_dir))
        
        print("✅ Environment setup completed!")

    def interactive_menu(self):
        """Interactive installation menu"""
        while True:
            print("\n" + "=" * 60)
            print("🛡️  KALI TOOLS WINDOWS INSTALLER")
            print("=" * 60)
            print("1. Setup environment (run this first)")
            print("2. Install popular tools")
            print("3. Install specific tool")
            print("4. Install tools by category") 
            print("5. Verify tool installation")
            print("6. Show usage examples")
            print("7. Open Kali tools directory")
            print("8. Exit")
            print("=" * 60)
            
            choice = input("🎯 Enter your choice (1-8): ").strip()
            
            if choice == '1':
                self.setup_environment()
            elif choice == '2':
                self.install_popular_tools()
            elif choice == '3':
                tool_name = input("🔧 Enter tool name: ").strip()
                self.install_tool(tool_name)
            elif choice == '4':
                print("\n📁 Available categories:")
                for category in self.kali_tools.keys():
                    print(f"  - {category}")
                category = input("📁 Enter category name: ").strip()
                self.install_category(category)
            elif choice == '5':
                tool_name = input("🔍 Enter tool name to verify: ").strip()
                self.verify_installation(tool_name)
            elif choice == '6':
                self.show_usage_examples()
            elif choice == '7':
                os.startfile(self.kali_dir)
            elif choice == '8':
                print("👋 Goodbye! Tools are ready to use!")
                break
            else:
                print("❌ Invalid choice")

def main():
    """Main function"""
    print("🚀 KALI TOOLS WINDOWS INSTALLER")
    print("💻 Installing real Kali tools on Windows...")
    
    # Check if running on Windows
    if platform.system().lower() != 'windows':
        print("❌ This installer is designed for Windows only!")
        return
    
    installer = KaliWindowsInstaller()
    installer.interactive_menu()

if __name__ == "__main__":
    main()
