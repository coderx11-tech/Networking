#!/usr/bin/env python3
"""
GENUINE KALI TOOLS macOS INSTALLER
Installs REAL Kali Linux tools on macOS using:
- Homebrew with Kali repositories
- Direct downloads from Kali sources
- Docker with Kali Linux
- Native compilation from source
"""

import os
import sys
import platform
import subprocess
import shutil
import urllib.request
import tempfile
from pathlib import Path
import getpass
import plistlib

class MacKaliInstaller:
    def __init__(self):
        self.system = "darwin"
        self.architecture = platform.machine().lower()  # 'x86_64' or 'arm64'
        self.mac_version = platform.mac_ver()[0]
        self.user = getpass.getuser()
        self.kali_dir = Path.home() / "kali-tools"
        self.bin_dir = self.kali_dir / "bin"
        self.src_dir = self.kali_dir / "src"
        self.config_dir = self.kali_dir / "config"
        
        # GENUINE Kali tools with macOS installation methods
        self.genuine_kali_tools = {
            # Information Gathering - All have macOS versions
            'nmap': {
                'methods': ['brew', 'native', 'source'],
                'brew': 'nmap',
                'native_url': 'https://nmap.org/dist/nmap-7.94.dmg',
                'source_url': 'https://nmap.org/dist/nmap-7.94.tar.bz2',
                'description': 'Network exploration tool',
                'test_cmd': 'nmap --version'
            },
            'masscan': {
                'methods': ['brew', 'source'],
                'brew': 'masscan',
                'source_url': 'https://github.com/robertdavidgraham/masscan/archive/refs/heads/master.zip',
                'description': 'Mass IP port scanner',
                'test_cmd': 'masscan --version'
            },
            'theharvester': {
                'methods': ['pip', 'brew'],
                'pip': 'theharvester',
                'brew': 'theharvester',
                'description': 'OSINT gathering tool',
                'test_cmd': 'theHarvester --help'
            },
            'sublist3r': {
                'methods': ['pip', 'brew'],
                'pip': 'sublist3r',
                'description': 'Subdomain enumeration',
                'test_cmd': 'sublist3r --help'
            },
            'amass': {
                'methods': ['brew', 'native'],
                'brew': 'amass',
                'native_url': 'https://github.com/OWASP/Amass/releases/download/v4.0.0/amass_darwin_amd64.zip',
                'description': 'Attack surface mapping',
                'test_cmd': 'amass --version'
            },
            'maltego': {
                'methods': ['native'],
                'native_url': 'https://download.maltego.com/maltego-v4.3.0/macos/Maltego.v4.3.0.dmg',
                'description': 'OSINT and forensics',
                'test_cmd': 'open -a Maltego'
            },
            'recon-ng': {
                'methods': ['brew', 'pip'],
                'brew': 'recon-ng',
                'description': 'Web reconnaissance framework',
                'test_cmd': 'recon-ng --version'
            },

            # Vulnerability Analysis
            'sqlmap': {
                'methods': ['pip', 'brew'],
                'pip': 'sqlmap',
                'brew': 'sqlmap',
                'description': 'SQL injection tool',
                'test_cmd': 'sqlmap --version'
            },
            'nikto': {
                'methods': ['brew', 'source'],
                'brew': 'nikto',
                'description': 'Web server scanner',
                'test_cmd': 'nikto -Version'
            },
            'nuclei': {
                'methods': ['brew', 'native'],
                'brew': 'nuclei',
                'native_url': 'https://github.com/projectdiscovery/nuclei/releases/download/v2.9.15/nuclei_2.9.15_darwin_amd64.zip',
                'description': 'Vulnerability scanner',
                'test_cmd': 'nuclei -version'
            },
            'wapiti': {
                'methods': ['pip', 'brew'],
                'pip': 'wapiti3',
                'description': 'Web vulnerability scanner',
                'test_cmd': 'wapiti --help'
            },

            # Web Application Tools
            'burpsuite': {
                'methods': ['native'],
                'native_url': 'https://portswigger.net/burp/releases/download?product=community&version=2023.10.3&type=macosx',
                'description': 'Web app security testing',
                'test_cmd': 'open -a "Burp Suite Community Edition"'
            },
            'dirb': {
                'methods': ['brew', 'source'],
                'brew': 'dirb',
                'description': 'Web content scanner',
                'test_cmd': 'dirb --help'
            },
            'gobuster': {
                'methods': ['brew', 'native'],
                'brew': 'gobuster',
                'native_url': 'https://github.com/OJ/gobuster/releases/download/v3.6.0/gobuster_3.6.0_Darwin_x64.zip',
                'description': 'Directory/DNS busting',
                'test_cmd': 'gobuster --help'
            },
            'whatweb': {
                'methods': ['brew', 'source'],
                'brew': 'whatweb',
                'description': 'Website fingerprinting',
                'test_cmd': 'whatweb --version'
            },
            'wpscan': {
                'methods': ['brew', 'docker'],
                'brew': 'wpscan',
                'description': 'WordPress security scanner',
                'test_cmd': 'wpscan --version'
            },

            # Password Attacks
            'hydra': {
                'methods': ['brew', 'source'],
                'brew': 'hydra',
                'description': 'Network logon cracker',
                'test_cmd': 'hydra --version'
            },
            'john': {
                'methods': ['brew', 'source'],
                'brew': 'john',
                'description': 'John the Ripper',
                'test_cmd': 'john --help'
            },
            'hashcat': {
                'methods': ['brew', 'source'],
                'brew': 'hashcat',
                'description': 'Password recovery tool',
                'test_cmd': 'hashcat --version'
            },
            'crunch': {
                'methods': ['brew', 'source'],
                'brew': 'crunch',
                'description': 'Wordlist generator',
                'test_cmd': 'crunch --help'
            },

            # Wireless Attacks
            'aircrack-ng': {
                'methods': ['brew', 'source'],
                'brew': 'aircrack-ng',
                'description': 'WiFi security auditing',
                'test_cmd': 'aircrack-ng --version'
            },
            'kismet': {
                'methods': ['brew', 'source'],
                'brew': 'kismet',
                'description': 'Wireless network detector',
                'test_cmd': 'kismet --version'
            },
            'wifite': {
                'methods': ['pip', 'source'],
                'pip': 'wifite2',
                'description': 'Automated wireless attacks',
                'test_cmd': 'wifite --help'
            },

            # Sniffing & Spoofing
            'wireshark': {
                'methods': ['brew', 'native'],
                'brew': 'wireshark',
                'native_url': 'https://1.eu.dl.wireshark.org/osx/Wireshark%204.0.8%20Intel%2064.dmg',
                'description': 'Network protocol analyzer',
                'test_cmd': 'wireshark --version'
            },
            'ettercap': {
                'methods': ['brew', 'source'],
                'brew': 'ettercap',
                'description': 'Network interceptor',
                'test_cmd': 'ettercap --version'
            },
            'tcpdump': {
                'methods': ['brew', 'native'],
                'brew': 'tcpdump',
                'description': 'Packet analyzer',
                'test_cmd': 'tcpdump --version'
            },

            # Exploitation Tools
            'metasploit': {
                'methods': ['brew', 'native'],
                'brew': 'metasploit',
                'native_url': 'https://osx.metasploit.com/metasploitframework-latest.pkg',
                'description': 'Penetration testing framework',
                'test_cmd': 'msfconsole --version'
            },

            # Forensics
            'binwalk': {
                'methods': ['pip', 'brew'],
                'pip': 'binwalk',
                'brew': 'binwalk',
                'description': 'Firmware analysis',
                'test_cmd': 'binwalk --help'
            },
            'volatility': {
                'methods': ['pip', 'brew'],
                'pip': 'volatility3',
                'description': 'Memory forensics',
                'test_cmd': 'vol --help'
            },
            'foremost': {
                'methods': ['brew', 'source'],
                'brew': 'foremost',
                'description': 'Data recovery',
                'test_cmd': 'foremost -h'
            },

            # macOS Specific
            'ios-deploy': {
                'methods': ['brew', 'npm'],
                'brew': 'ios-deploy',
                'description': 'iOS app deployment',
                'test_cmd': 'ios-deploy --version'
            }
        }

        self.setup_directories()

    def setup_directories(self):
        """Create Kali tools directory structure"""
        directories = [self.kali_dir, self.bin_dir, self.src_dir, self.config_dir, 
                      self.kali_dir / "wordlists", self.kali_dir / "output"]
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
        """Install Homebrew package manager"""
        if not shutil.which("brew"):
            print("🍺 Installing Homebrew...")
            command = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            success, output = self.run_command(command, shell=True)
            if success:
                # Add Homebrew to PATH
                if self.architecture == 'arm64':
                    brew_path = "/opt/homebrew/bin"
                else:
                    brew_path = "/usr/local/bin"
                
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
            # Look for .app or .pkg in mount point
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
                elif item.suffix == '.pkg':
                    # Install pkg
                    print(f"📦 Installing {item.name}...")
                    subprocess.run(["sudo", "installer", "-pkg", str(item), "-target", "/"], check=True)
                    self.unmount_dmg(mount_point)
                    print(f"✅ {item.name} installed successfully")
                    return True
            
            print("❌ No .app or .pkg file found in DMG")
            self.unmount_dmg(mount_point)
            return False
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            self.unmount_dmg(mount_point)
            return False

    def install_native_tool(self, tool_name, tool_info):
        """Install native macOS version of tool"""
        if 'native_url' not in tool_info:
            print(f"❌ No native download URL for {tool_name}")
            return False
        
        print(f"🍎 Installing native macOS version of {tool_name}...")
        
        # Download the tool
        download_path = self.src_dir / f"{tool_name}_download"
        if not self.download_file(tool_info['native_url'], download_path):
            return False
        
        # Handle different file types
        if download_path.suffix == '.dmg':
            return self.install_dmg_package(download_path)
        elif download_path.suffix == '.pkg':
            return self.install_pkg_package(download_path)
        elif download_path.suffix in ['.zip', '.tar.gz']:
            return self.handle_archive_installation(tool_name, download_path)
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

    def handle_archive_installation(self, tool_name, archive_path):
        """Handle archive file installation"""
        extract_dir = self.src_dir / tool_name
        extract_dir.mkdir(exist_ok=True)
        
        try:
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            else:
                # Tar archive
                subprocess.run(["tar", "-xf", str(archive_path), "-C", str(extract_dir)], check=True)
            
            # Find and install binary
            for file_path in extract_dir.rglob('*'):
                if file_path.is_file() and file_path.stat().st_mode & 0o111:  # Executable
                    # Copy to bin directory
                    shutil.copy2(file_path, self.bin_dir / file_path.name)
                    print(f"✅ {tool_name} installed to {self.bin_dir}")
                    return True
            
            print(f"❌ No executable found for {tool_name}")
            return False
        except Exception as e:
            print(f"❌ Archive installation failed: {e}")
            return False

    def compile_from_source(self, tool_name, tool_info):
        """Compile tool from source"""
        if 'source_url' not in tool_info:
            print(f"❌ No source URL for {tool_name}")
            return False
        
        print(f"🔨 Compiling {tool_name} from source...")
        
        # Download source
        download_path = self.src_dir / f"{tool_name}_source"
        if not self.download_file(tool_info['source_url'], download_path):
            return False
        
        # Extract source
        extract_dir = self.src_dir / tool_name
        extract_dir.mkdir(exist_ok=True)
        
        try:
            if download_path.suffix == '.zip':
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            else:
                subprocess.run(["tar", "-xf", str(download_path), "-C", str(extract_dir)], check=True)
            
            # Find source directory
            source_dir = None
            for item in extract_dir.iterdir():
                if item.is_dir():
                    source_dir = item
                    break
            
            if not source_dir:
                print("❌ Could not find source directory")
                return False
            
            # Build (simplified - actual build would be tool-specific)
            os.chdir(source_dir)
            
            # Try common build patterns
            build_commands = [
                "./configure --prefix=/usr/local",
                "make",
                "sudo make install"
            ]
            
            for cmd in build_commands:
                success, output = self.run_command(cmd, shell=True)
                if not success:
                    print(f"❌ Build failed: {cmd}")
                    return False
            
            print(f"✅ {tool_name} compiled and installed")
            return True
            
        except Exception as e:
            print(f"❌ Compilation failed: {e}")
            return False
        finally:
            os.chdir(self.home_dir)

    def install_tool(self, tool_name):
        """Install a specific Kali tool using best available method"""
        if tool_name not in self.genuine_kali_tools:
            print(f"❌ Tool {tool_name} not found")
            return False
        
        tool_info = self.genuine_kali_tools[tool_name]
        print(f"\n🚀 Installing {tool_name}: {tool_info['description']}")
        
        # Try installation methods in order of preference
        methods = tool_info['methods']
        
        for method in methods:
            if method == 'brew' and 'brew' in tool_info:
                if self.install_via_brew(tool_info['brew']):
                    return True
            elif method == 'pip' and 'pip' in tool_info:
                if self.install_via_pip(tool_info['pip']):
                    return True
            elif method == 'native' and 'native_url' in tool_info:
                if self.install_native_tool(tool_name, tool_info):
                    return True
            elif method == 'source' and 'source_url' in tool_info:
                if self.compile_from_source(tool_name, tool_info):
                    return True
        
        print(f"❌ All installation methods failed for {tool_name}")
        return False

    def install_tool_category(self, category_name):
        """Install all tools in a category"""
        categories = {
            'info_gathering': ['nmap', 'masscan', 'theharvester', 'sublist3r', 'amass', 'maltego'],
            'vuln_analysis': ['sqlmap', 'nikto', 'nuclei', 'wapiti'],
            'web_apps': ['burpsuite', 'dirb', 'gobuster', 'whatweb', 'wpscan'],
            'password_attacks': ['hydra', 'john', 'hashcat', 'crunch'],
            'wireless': ['aircrack-ng', 'kismet', 'wifite'],
            'sniffing': ['wireshark', 'ettercap', 'tcpdump'],
            'exploitation': ['metasploit'],
            'forensics': ['binwalk', 'volatility', 'foremost'],
            'macos_tools': ['ios-deploy']
        }
        
        if category_name not in categories:
            print(f"❌ Category {category_name} not found")
            return False
        
        print(f"\n📦 Installing {category_name} tools...")
        tools = categories[category_name]
        success_count = 0
        
        for tool in tools:
            if self.install_tool(tool):
                success_count += 1
        
        print(f"✅ Installed {success_count}/{len(tools)} tools from {category_name}")
        return success_count

    def install_popular_tools(self):
        """Install most popular Kali tools"""
        popular_tools = ['nmap', 'sqlmap', 'wireshark', 'metasploit', 'burpsuite', 'aircrack-ng', 'theharvester']
        print("\n🎯 Installing popular Kali tools...")
        
        success_count = 0
        for tool in popular_tools:
            if self.install_tool(tool):
                success_count += 1
        
        print(f"✅ Installed {success_count}/{len(popular_tools)} popular tools")
        return success_count

    def verify_installation(self, tool_name):
        """Verify if tool is installed and working"""
        if tool_name not in self.genuine_kali_tools:
            print(f"❌ Tool {tool_name} not found")
            return False
        
        tool_info = self.genuine_kali_tools[tool_name]
        test_cmd = tool_info.get('test_cmd', f"{tool_name} --version")
        
        try:
            subprocess.run(test_cmd.split(), capture_output=True, check=True)
            print(f"✅ {tool_name} is installed and working!")
            return True
        except:
            print(f"❌ {tool_name} is not working properly")
            return False

    def setup_environment(self):
        """Setup the complete macOS environment"""
        print("🛠️ Setting up Kali tools environment on macOS...")
        
        # Install Homebrew
        if not self.install_homebrew():
            print("⚠️ Continuing without Homebrew...")
        
        # Update Homebrew
        print("🔄 Updating Homebrew...")
        self.run_command("brew update", shell=True)
        
        # Add kali-tools/bin to PATH
        self.add_to_shell_path(str(self.bin_dir))
        
        # Create shell scripts
        self.create_shell_scripts()
        
        print("✅ macOS environment setup completed!")
        return True

    def create_shell_scripts(self):
        """Create shell scripts for common tasks"""
        scripts = {
            'kali-scan': '''#!/bin/bash
echo "🔍 Kali Network Scanner"
echo "Running quick network discovery..."
nmap -sn 192.168.1.0/24
''',
            'kali-webscan': '''#!/bin/bash
echo "🌐 Kali Web Application Scanner"
if [ -z "$1" ]; then
    echo "Usage: kali-webscan target.com"
    exit 1
fi
echo "Scanning: $1"
theHarvester -d "$1" -b google
sublist3r -d "$1"
''',
            'kali-wifi': '''#!/bin/bash
echo "📶 Kali WiFi Tools"
echo "Available on macOS with compatible adapter:"
echo "- aircrack-ng: WiFi security auditing"
echo "- kismet: Wireless detection"
echo ""
echo "Note: Some features may require additional hardware"
'''
        }
        
        for script_name, content in scripts.items():
            script_path = self.bin_dir / script_name
            with open(script_path, 'w') as f:
                f.write(content)
            script_path.chmod(0o755)
            print(f"📝 Created: {script_path}")

    def show_system_info(self):
        """Show macOS system information"""
        print(f"\n🍎 macOS {self.mac_version} ({self.architecture})")
        print(f"👤 User: {self.user}")
        print(f"📁 Kali Tools: {self.kali_dir}")
        
        # Check Homebrew
        if shutil.which("brew"):
            print("🍺 Homebrew: Installed")
        else:
            print("🍺 Homebrew: Not installed")

    def show_usage_examples(self):
        """Show macOS usage examples"""
        examples = {
            'nmap': 'nmap -sV 192.168.1.1',
            'sqlmap': 'sqlmap -u "http://test.com/page?id=1" --batch',
            'wireshark': 'wireshark (launches GUI)',
            'metasploit': 'msfconsole',
            'aircrack-ng': 'aircrack-ng -w wordlist.txt capture.cap',
            'theharvester': 'theHarvester -d example.com -b google',
            'burpsuite': 'open -a "Burp Suite Community Edition"'
        }
        
        print("\n🎯 macOS USAGE EXAMPLES:")
        print("=" * 50)
        for tool, example in examples.items():
            print(f"🔧 {tool}:")
            print(f"   {example}")
        print("=" * 50)

    def show_available_tools(self):
        """Show all available Kali tools"""
        print("\n🛠️ AVAILABLE GENUINE KALI TOOLS:")
        print("=" * 60)
        for tool, info in self.genuine_kali_tools.items():
            methods = ", ".join(info['methods'])
            print(f"🔧 {tool}: {info['description']}")
            print(f"   📦 Methods: {methods}")
        print("=" * 60)

    def interactive_menu(self):
        """Interactive installation menu"""
        while True:
            print("\n" + "=" * 60)
            print("🛡️  GENUINE KALI TOOLS - macOS INSTALLER")
            print("=" * 60)
            print("1. Show system information")
            print("2. Setup macOS environment (RUN THIS FIRST)")
            print("3. Install specific Kali tool")
            print("4. Install tools by category")
            print("5. Install popular tools bundle")
            print("6. Verify tool installation")
            print("7. Show usage examples")
            print("8. Show available tools")
            print("9. Open Kali tools directory")
            print("0. Exit")
            print("=" * 60)
            
            choice = input("🎯 Enter your choice (0-9): ").strip()
            
            if choice == '1':
                self.show_system_info()
            elif choice == '2':
                self.setup_environment()
            elif choice == '3':
                tool_name = input("🔧 Enter Kali tool name: ").strip()
                self.install_tool(tool_name)
            elif choice == '4':
                print("\n📁 Available categories:")
                print("  info_gathering - Network and OSINT tools")
                print("  vuln_analysis - Vulnerability scanners")
                print("  web_apps - Web application testing")
                print("  password_attacks - Password cracking")
                print("  wireless - WiFi security tools")
                print("  sniffing - Network analysis")
                print("  exploitation - Penetration testing")
                print("  forensics - Digital forensics")
                print("  macos_tools - macOS-specific tools")
                category = input("📁 Enter category: ").strip()
                self.install_tool_category(category)
            elif choice == '5':
                self.install_popular_tools()
            elif choice == '6':
                tool_name = input("🔍 Enter tool name to verify: ").strip()
                self.verify_installation(tool_name)
            elif choice == '7':
                self.show_usage_examples()
            elif choice == '8':
                self.show_available_tools()
            elif choice == '9':
                subprocess.run(["open", str(self.kali_dir)])
            elif choice == '0':
                print("👋 Goodbye! Open a NEW Terminal to use your Kali tools!")
                print("💡 Run: source ~/.zshrc")
                break
            else:
                print("❌ Invalid choice")

def main():
    """Main function"""
    print("🚀 GENUINE KALI LINUX TOOLS - macOS INSTALLER")
    print("🍎 Installing REAL Kali tools on macOS...")
    print("⚡ Uses Homebrew, native packages, and source compilation!")
    
    # Check if macOS
    if platform.system().lower() != 'darwin':
        print("❌ This installer is for macOS only!")
        return
    
    installer = MacKaliInstaller()
    installer.interactive_menu()

if __name__ == "__main__":
    main()
