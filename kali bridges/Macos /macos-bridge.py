#!/usr/bin/env python3
"""
KALI TOOLS macOS INSTALLER - Installs and Configures Real Kali Tools on macOS
Makes tools immediately usable after installation in Terminal
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
import tempfile
import shutil
import plistlib
from pathlib import Path
import getpass

class KaliMacInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.architecture = platform.machine().lower()  # 'x86_64' or 'arm64'
        self.kali_dir = Path.home() / "KaliTools"
        self.bin_dir = self.kali_dir / "bin"
        self.temp_dir = tempfile.mkdtemp(prefix="kali_install_")
        self.user = getpass.getuser()
        
        # Comprehensive Kali tools with macOS-specific downloads
        self.kali_tools = {
            'information_gathering': {
                'nmap': {
                    'brew': 'nmap',
                    'executable': 'nmap',
                    'test_command': 'nmap --version'
                },
                'masscan': {
                    'brew': 'masscan',
                    'executable': 'masscan',
                    'test_command': 'masscan --version'
                },
                'sublist3r': {
                    'pip': 'sublist3r',
                    'executable': 'sublist3r',
                    'test_command': 'sublist3r --help'
                },
                'theharvester': {
                    'pip': 'theharvester',
                    'executable': 'theHarvester',
                    'test_command': 'theHarvester --help'
                },
                'amass': {
                    'brew': 'amass',
                    'executable': 'amass',
                    'test_command': 'amass --version'
                },
                'dnsrecon': {
                    'pip': 'dnsrecon',
                    'executable': 'dnsrecon',
                    'test_command': 'dnsrecon --help'
                },
                'maltego': {
                    'url': 'https://download.maltego.com/maltego-v4.3.0/macos/Maltego.v4.3.0.dmg',
                    'dmg': True,
                    'executable': 'Maltego'
                }
            },
            'vulnerability_analysis': {
                'sqlmap': {
                    'pip': 'sqlmap',
                    'executable': 'sqlmap',
                    'test_command': 'sqlmap --version'
                },
                'nikto': {
                    'brew': 'nikto',
                    'executable': 'nikto',
                    'test_command': 'nikto -Version'
                },
                'nuclei': {
                    'brew': 'nuclei',
                    'executable': 'nuclei',
                    'test_command': 'nuclei -version'
                },
                'wapiti': {
                    'pip': 'wapiti3',
                    'executable': 'wapiti',
                    'test_command': 'wapiti --help'
                }
            },
            'web_applications': {
                'dirb': {
                    'brew': 'dirb',
                    'executable': 'dirb',
                    'test_command': 'dirb --help'
                },
                'gobuster': {
                    'brew': 'gobuster',
                    'executable': 'gobuster',
                    'test_command': 'gobuster --help'
                },
                'whatweb': {
                    'brew': 'whatweb',
                    'executable': 'whatweb',
                    'test_command': 'whatweb --version'
                },
                'wpscan': {
                    'brew': 'wpscan',
                    'executable': 'wpscan',
                    'test_command': 'wpscan --version'
                },
                'burpsuite': {
                    'url': 'https://portswigger.net/burp/releases/download?product=community&version=2023.10.3&type=macosx',
                    'executable': 'Burp Suite Community Edition'
                }
            },
            'password_attacks': {
                'john': {
                    'brew': 'john',
                    'executable': 'john',
                    'test_command': 'john --help'
                },
                'hashcat': {
                    'brew': 'hashcat',
                    'executable': 'hashcat',
                    'test_command': 'hashcat --version'
                },
                'hydra': {
                    'brew': 'hydra',
                    'executable': 'hydra',
                    'test_command': 'hydra --version'
                },
                'crunch': {
                    'brew': 'crunch',
                    'executable': 'crunch',
                    'test_command': 'crunch --help'
                }
            },
            'wireless_attacks': {
                'aircrack-ng': {
                    'brew': 'aircrack-ng',
                    'executable': 'aircrack-ng',
                    'test_command': 'aircrack-ng --version'
                },
                'kismet': {
                    'brew': 'kismet',
                    'executable': 'kismet',
                    'test_command': 'kismet --version'
                },
                'wifite': {
                    'pip': 'wifite2',
                    'executable': 'wifite',
                    'test_command': 'wifite --help'
                }
            },
            'sniffing_spoofing': {
                'wireshark': {
                    'brew': 'wireshark',
                    'executable': 'wireshark',
                    'test_command': 'wireshark --version'
                },
                'ettercap': {
                    'brew': 'ettercap',
                    'executable': 'ettercap',
                    'test_command': 'ettercap --version'
                },
                'tcpdump': {
                    'brew': 'tcpdump',
                    'executable': 'tcpdump',
                    'test_command': 'tcpdump --version'
                },
                'tshark': {
                    'brew': 'wireshark',
                    'executable': 'tshark',
                    'test_command': 'tshark --version'
                }
            },
            'exploitation_tools': {
                'metasploit': {
                    'brew': 'metasploit',
                    'executable': 'msfconsole',
                    'test_command': 'msfconsole --version'
                },
                'commix': {
                    'pip': 'commix',
                    'executable': 'commix',
                    'test_command': 'commix --version'
                },
                'sqlmap': {
                    'pip': 'sqlmap',
                    'executable': 'sqlmap',
                    'test_command': 'sqlmap --version'
                }
            },
            'forensics': {
                'binwalk': {
                    'brew': 'binwalk',
                    'executable': 'binwalk',
                    'test_command': 'binwalk --help'
                },
                'foremost': {
                    'brew': 'foremost',
                    'executable': 'foremost',
                    'test_command': 'foremost -h'
                },
                'volatility': {
                    'pip': 'volatility3',
                    'executable': 'vol',
                    'test_command': 'vol --help'
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

    def run_command(self, command, shell=False):
        """Run system command with error handling"""
        try:
            if shell:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            else:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def install_homebrew(self):
        """Install Homebrew package manager for macOS"""
        if not shutil.which("brew"):
            print("🍺 Installing Homebrew package manager...")
            command = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            success, output = self.run_command(command, shell=True)
            if success:
                # Add Homebrew to PATH
                brew_path = "/opt/homebrew/bin" if self.architecture == 'arm64' else "/usr/local/bin"
                self.add_to_shell_path(brew_path)
                print("✅ Homebrew installed successfully")
                return True
            else:
                print("❌ Failed to install Homebrew")
                return False
        return True

    def add_to_shell_path(self, directory):
        """Add directory to shell PATH"""
        shell_rc_files = [
            Path.home() / ".zshrc",
            Path.home() / ".bash_profile",
            Path.home() / ".bashrc"
        ]
        
        path_line = f'\nexport PATH="{directory}:$PATH"\n'
        
        for rc_file in shell_rc_files:
            if rc_file.exists():
                with open(rc_file, 'r') as f:
                    content = f.read()
                
                if directory not in content:
                    with open(rc_file, 'a') as f:
                        f.write(path_line)
                    print(f"✅ Added {directory} to {rc_file}")

        # Add to current session
        os.environ["PATH"] = f"{directory}:{os.environ['PATH']}"

    def install_via_brew(self, package_name):
        """Install package via Homebrew"""
        try:
            print(f"🍺 Installing {package_name} via Homebrew...")
            subprocess.run(["brew", "install", package_name], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name} via Homebrew")
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

    def download_file(self, url, destination):
        """Download file from URL"""
        try:
            print(f"📥 Downloading {url}...")
            urllib.request.urlretrieve(url, destination)
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

    def mount_dmg(self, dmg_path):
        """Mount DMG file"""
        try:
            print(f"📀 Mounting {dmg_path}...")
            result = subprocess.run(["hdiutil", "attach", dmg_path], capture_output=True, text=True, check=True)
            
            # Extract mount point from output
            for line in result.stdout.split('\n'):
                if '/Volumes/' in line:
                    mount_point = line.split('\t')[-1].strip()
                    return mount_point
            return None
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to mount DMG: {e}")
            return None

    def unmount_dmg(self, mount_point):
        """Unmount DMG file"""
        try:
            subprocess.run(["hdiutil", "detach", mount_point], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def install_dmg_package(self, dmg_path):
        """Install application from DMG"""
        mount_point = self.mount_dmg(dmg_path)
        if not mount_point:
            return False
        
        try:
            # Look for .app in mount point
            for item in Path(mount_point).iterdir():
                if item.suffix == '.app':
                    # Copy to Applications
                    app_name = item.name
                    dest_path = Path("/Applications") / app_name
                    
                    if dest_path.exists():
                        print(f"⚠️ {app_name} already exists in Applications")
                    else:
                        print(f"📦 Installing {app_name} to Applications...")
                        shutil.copytree(item, dest_path)
                    
                    self.unmount_dmg(mount_point)
                    print(f"✅ {app_name} installed successfully")
                    return True
            
            print("❌ No .app file found in DMG")
            self.unmount_dmg(mount_point)
            return False
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            self.unmount_dmg(mount_point)
            return False

    def install_nmap(self):
        """Specialized NMAP installation"""
        print("🔧 Installing NMAP...")
        return self.install_via_brew("nmap")

    def install_sqlmap(self):
        """Specialized SQLMap installation"""
        print("💉 Installing SQLMap...")
        return self.install_via_pip("sqlmap")

    def install_metasploit(self):
        """Specialized Metasploit installation"""
        print("💣 Installing Metasploit Framework...")
        return self.install_via_brew("metasploit")

    def install_wireshark(self):
        """Specialized Wireshark installation"""
        print("📡 Installing Wireshark...")
        if self.install_via_brew("wireshark"):
            # Add wireshark to user groups for packet capture
            subprocess.run(["sudo", "dseditgroup", "-o", "edit", "-a", self.user, "-t", "user", "access_bpf"], 
                         capture_output=True)
            return True
        return False

    def install_aircrack(self):
        """Specialized Aircrack-ng installation"""
        print("📶 Installing Aircrack-ng...")
        return self.install_via_brew("aircrack-ng")

    def install_tool(self, tool_name):
        """Install a specific tool"""
        print(f"\n🚀 Installing {tool_name}...")
        
        # Special handling for common tools
        special_installers = {
            'nmap': self.install_nmap,
            'sqlmap': self.install_sqlmap,
            'metasploit': self.install_metasploit,
            'wireshark': self.install_wireshark,
            'aircrack-ng': self.install_aircrack
        }
        
        if tool_name in special_installers:
            return special_installers[tool_name]()
        
        # Find tool in database
        tool_info = self.find_tool_info(tool_name)
        if not tool_info:
            print(f"❌ Tool {tool_name} not found in database")
            return False
        
        # Try different installation methods
        if 'brew' in tool_info:
            return self.install_via_brew(tool_info['brew'])
        elif 'pip' in tool_info:
            return self.install_via_pip(tool_info['pip'])
        elif 'url' in tool_info:
            return self.download_and_install_tool(tool_name, tool_info)
        else:
            print(f"❌ No installation method for {tool_name}")
            return False

    def find_tool_info(self, tool_name):
        """Find tool information in database"""
        for category, tools in self.kali_tools.items():
            if tool_name in tools:
                return tools[tool_name]
        return None

    def download_and_install_tool(self, tool_name, tool_info):
        """Download and install tool from URL"""
        if 'url' not in tool_info:
            return False
        
        download_path = self.temp_dir / f"{tool_name}_download"
        if not self.download_file(tool_info['url'], download_path):
            return False
        
        # Handle different file types
        if download_path.suffix == '.dmg':
            return self.install_dmg_package(download_path)
        elif download_path.suffix in ['.pkg', '.mpkg']:
            return self.install_pkg_package(download_path)
        else:
            print(f"❌ Unsupported file type: {download_path.suffix}")
            return False

    def install_pkg_package(self, pkg_path):
        """Install PKG package"""
        try:
            print(f"📦 Installing {pkg_path}...")
            subprocess.run(["sudo", "installer", "-pkg", str(pkg_path), "-target", "/"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PKG: {e}")
            return False

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
        popular_tools = ['nmap', 'sqlmap', 'wireshark', 'metasploit', 'aircrack-ng', 'theharvester', 'sublist3r']
        print("\n🎯 Installing popular Kali tools...")
        
        success_count = 0
        for tool in popular_tools:
            if self.install_tool(tool):
                success_count += 1
        
        print(f"✅ Installed {success_count}/{len(popular_tools)} popular tools")
        return success_count

    def verify_installation(self, tool_name):
        """Verify if tool is installed and working"""
        tool_info = self.find_tool_info(tool_name)
        if not tool_info:
            print(f"❌ Tool {tool_name} not found")
            return False
        
        test_command = tool_info.get('test_command', f"{tool_name} --version")
        
        try:
            subprocess.run(test_command.split(), capture_output=True, check=True)
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
            'wireshark': 'wireshark (launches GUI) or tshark -i en0',
            'theharvester': 'theHarvester -d example.com -b google',
            'sublist3r': 'sublist3r -d example.com',
            'masscan': 'masscan -p80 192.168.1.0/24',
            'aircrack-ng': 'aircrack-ng -w wordlist.txt capture.cap',
            'metasploit': 'msfconsole',
            'hydra': 'hydra -l admin -P passwords.txt ssh://192.168.1.1',
            'john': 'john --wordlist=wordlist.txt hashes.txt',
            'gobuster': 'gobuster dir -u http://test.com -w wordlist.txt'
        }
        
        print("\n📚 macOS USAGE EXAMPLES:")
        print("=" * 50)
        for tool, example in examples.items():
            print(f"🔧 {tool}:")
            print(f"   {example}")
        print("=" * 50)

    def setup_environment(self):
        """Setup the complete environment"""
        print("🛠️ Setting up Kali tools environment on macOS...")
        
        # Install Homebrew first
        if not self.install_homebrew():
            print("❌ Homebrew installation failed - some tools may not install")
            return False
        
        # Update Homebrew
        print("🔄 Updating Homebrew...")
        subprocess.run(["brew", "update"], capture_output=True)
        
        # Add Kali tools bin to PATH
        self.add_to_shell_path(str(self.bin_dir))
        
        print("✅ macOS environment setup completed!")
        return True

    def check_system_compatibility(self):
        """Check macOS version and compatibility"""
        mac_version = platform.mac_ver()[0]
        architecture = platform.machine()
        
        print(f"🍎 macOS {mac_version} ({architecture}) detected")
        
        if architecture == 'arm64':
            print("✅ Apple Silicon (M1/M2) - Native support available")
        else:
            print("✅ Intel Mac - Full support available")
        
        return True

    def interactive_menu(self):
        """Interactive installation menu"""
        while True:
            print("\n" + "=" * 60)
            print("🛡️  KALI TOOLS macOS INSTALLER")
            print("=" * 60)
            print("1. Check system compatibility")
            print("2. Setup environment (run this first)")
            print("3. Install popular tools")
            print("4. Install specific tool")
            print("5. Install tools by category") 
            print("6. Verify tool installation")
            print("7. Show usage examples")
            print("8. Open Kali tools directory")
            print("9. Exit")
            print("=" * 60)
            
            choice = input("🎯 Enter your choice (1-9): ").strip()
            
            if choice == '1':
                self.check_system_compatibility()
            elif choice == '2':
                self.setup_environment()
            elif choice == '3':
                self.install_popular_tools()
            elif choice == '4':
                tool_name = input("🔧 Enter tool name: ").strip()
                self.install_tool(tool_name)
            elif choice == '5':
                print("\n📁 Available categories:")
                for category in self.kali_tools.keys():
                    print(f"  - {category}")
                category = input("📁 Enter category name: ").strip()
                self.install_category(category)
            elif choice == '6':
                tool_name = input("🔍 Enter tool name to verify: ").strip()
                self.verify_installation(tool_name)
            elif choice == '7':
                self.show_usage_examples()
            elif choice == '8':
                subprocess.run(["open", str(self.kali_dir)])
            elif choice == '9':
                print("👋 Goodbye! Open a NEW Terminal to use your tools!")
                break
            else:
                print("❌ Invalid choice")

def main():
    """Main function"""
    print("🚀 KALI TOOLS macOS INSTALLER")
    print("💻 Installing real Kali tools on macOS...")
    
    # Check if running on macOS
    if platform.system().lower() != 'darwin':
        print("❌ This installer is designed for macOS only!")
        return
    
    installer = KaliMacInstaller()
    installer.interactive_menu()

if __name__ == "__main__":
    main()
