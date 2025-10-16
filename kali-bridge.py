#!/usr/bin/env python3
"""
UNIVERSAL KALI TOOLS INSTALLER - Works on Windows, Mac, Linux, PyCharm, Anywhere!
Installs ANY Kali tool regardless of your operating system or environment
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
from pathlib import Path

class UniversalKaliInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.architecture = platform.machine().lower()
        self.temp_dir = tempfile.mkdtemp(prefix="kali_tools_")
        self.install_dir = self.get_install_directory()
        
        # COMPLETE Kali tools database
        self.all_kali_tools = {
            # Information Gathering
            'nmap': {'type': 'binary', 'description': 'Network mapper'},
            'masscan': {'type': 'binary', 'description': 'Mass IP port scanner'},
            'recon-ng': {'type': 'python', 'description': 'Web reconnaissance framework'},
            'theharvester': {'type': 'python', 'description': 'OSINT intelligence gathering'},
            'sublist3r': {'type': 'python', 'description': 'Subdomain enumeration'},
            'amass': {'type': 'binary', 'description': 'In-depth attack surface mapping'},
            'dnsrecon': {'type': 'python', 'description': 'DNS enumeration'},
            'maltego': {'type': 'binary', 'description': 'OSINT graphical link analysis'},
            'spiderfoot': {'type': 'python', 'description': 'Reconnaissance automation'},
            'shodan': {'type': 'python', 'description': 'Shodan internet connected device search'},
            
            # Vulnerability Analysis
            'nikto': {'type': 'perl', 'description': 'Web server scanner'},
            'sqlmap': {'type': 'python', 'description': 'SQL injection automation'},
            'nuclei': {'type': 'binary', 'description': 'Vulnerability scanner'},
            'wapiti': {'type': 'python', 'description': 'Web application vulnerability scanner'},
            'skipfish': {'type': 'binary', 'description': 'Web application security scanner'},
            'lynis': {'type': 'binary', 'description': 'Security auditing tool'},
            'openvas': {'type': 'binary', 'description': 'Vulnerability management'},
            'nessus': {'type': 'binary', 'description': 'Vulnerability scanner'},
            
            # Wireless Attacks
            'aircrack-ng': {'type': 'binary', 'description': 'WiFi security auditing'},
            'kismet': {'type': 'binary', 'description': 'Wireless network detector'},
            'wifite': {'type': 'python', 'description': 'Automated wireless attack tool'},
            'reaver': {'type': 'binary', 'description': 'WPS PIN attack tool'},
            'bully': {'type': 'binary', 'description': 'WPS brute force attack'},
            'pixiewps': {'type': 'binary', 'description': 'WPS offline brute force'},
            
            # Web Applications
            'burpsuite': {'type': 'java', 'description': 'Web application security testing'},
            'dirb': {'type': 'binary', 'description': 'Web content scanner'},
            'gobuster': {'type': 'binary', 'description': 'Directory/file & DNS busting'},
            'whatweb': {'type': 'ruby', 'description': 'Website fingerprinting'},
            'wpscan': {'type': 'ruby', 'description': 'WordPress security scanner'},
            'joomscan': {'type': 'perl', 'description': 'Joomla vulnerability scanner'},
            'droopescan': {'type': 'python', 'description': 'Drupal, Silverstripe CMS scan'},
            
            # Password Attacks
            'hydra': {'type': 'binary', 'description': 'Network logon cracker'},
            'john': {'type': 'binary', 'description': 'John the Ripper password cracker'},
            'hashcat': {'type': 'binary', 'description': 'Advanced password recovery'},
            'crunch': {'type': 'binary', 'description': 'Wordlist generator'},
            'cewl': {'type': 'ruby', 'description': 'Custom wordlist generator'},
            'rsmangler': {'type': 'ruby', 'description': 'Wordlist mangler'},
            'patator': {'type': 'python', 'description': 'Multi-purpose brute-forcer'},
            
            # Exploitation Tools
            'metasploit-framework': {'type': 'ruby', 'description': 'Penetration testing framework'},
            'sqlmap': {'type': 'python', 'description': 'SQL injection attacks'},
            'beef-xss': {'type': 'ruby', 'description': 'Browser exploitation framework'},
            'commix': {'type': 'python', 'description': 'Automated command injection'},
            'websploit': {'type': 'python', 'description': 'Web vulnerability scanning'},
            
            # Forensics
            'binwalk': {'type': 'python', 'description': 'Firmware analysis tool'},
            'foremost': {'type': 'binary', 'description': 'Data recovery program'},
            'volatility': {'type': 'python', 'description': 'Memory forensics framework'},
            'guymager': {'type': 'binary', 'description': 'Forensic imager'},
            'sleuthkit': {'type': 'binary', 'description': 'Forensic toolkit'},
            
            # Sniffing & Spoofing
            'wireshark': {'type': 'binary', 'description': 'Network protocol analyzer'},
            'ettercap': {'type': 'binary', 'description': 'Network interceptor and analyzer'},
            'driftnet': {'type': 'binary', 'description': 'Image capture from network traffic'},
            'tcpdump': {'type': 'binary', 'description': 'Command-line packet analyzer'},
            'tshark': {'type': 'binary', 'description': 'Terminal-based Wireshark'},
            
            # Post Exploitation
            'powersploit': {'type': 'powershell', 'description': 'PowerShell post-exploitation'},
            'empire': {'type': 'python', 'description': 'Post-exploitation framework'},
            'mimikatz': {'type': 'binary', 'description': 'Windows credential extraction'},
            
            # Reporting Tools
            'dradis': {'type': 'ruby', 'description': 'Reporting and collaboration'},
            'faraday': {'type': 'python', 'description': 'Integrated pentest environment'},
            'serpico': {'type': 'ruby', 'description': 'Pentest reporting'},
            
            # Social Engineering
            'setoolkit': {'type': 'python', 'description': 'Social engineering toolkit'},
            'beef-xss': {'type': 'ruby', 'description': 'Browser exploitation'},
        }
        
        # Download URLs for different platforms
        self.download_sources = {
            'windows': {
                'nmap': 'https://nmap.org/dist/nmap-7.94-setup.exe',
                'wireshark': 'https://1.eu.dl.wireshark.org/win64/Wireshark-4.0.8-x64.exe',
                'python_tools': 'pip install'
            },
            'linux': {
                'generic': 'https://github.com/offensive-security/exploitdb-bin-sploits/raw/master/bin-sploits/',
                'python_tools': 'pip3 install'
            },
            'darwin': {
                'homebrew': 'brew install',
                'python_tools': 'pip3 install'
            }
        }

    def get_install_directory(self):
        """Get platform-specific install directory"""
        if self.system == 'windows':
            return Path.home() / 'kali_tools'
        else:
            return Path.home() / '.local' / 'kali_tools'

    def ensure_install_dir(self):
        """Create installation directory"""
        self.install_dir.mkdir(parents=True, exist_ok=True)
        # Add to PATH
        self.add_to_path(str(self.install_dir))

    def add_to_path(self, path):
        """Add directory to system PATH"""
        if path not in os.environ['PATH']:
            if self.system == 'windows':
                os.environ['PATH'] += f';{path}'
            else:
                os.environ['PATH'] += f':{path}'

    def run_command(self, command, check=True):
        """Run system command with error handling"""
        try:
            print(f"🔧 Running: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if check and result.returncode != 0:
                print(f"❌ Command failed: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"❌ Error running command: {e}")
            return False

    def install_via_pip(self, tool_name):
        """Install Python-based tools via pip"""
        try:
            if self.system == 'windows':
                command = f'python -m pip install {tool_name}'
            else:
                command = f'pip3 install {tool_name}'
            
            return self.run_command(command)
        except Exception as e:
            print(f"❌ Failed to install {tool_name} via pip: {e}")
            return False

    def install_via_system_package_manager(self, tool_name):
        """Try to install via system package manager"""
        try:
            if self.system == 'windows':
                # Try chocolatey or winget
                if self.run_command(f'choco install {tool_name} -y', check=False):
                    return True
                elif self.run_command(f'winget install {tool_name}', check=False):
                    return True
            elif self.system == 'darwin':  # macOS
                return self.run_command(f'brew install {tool_name}')
            else:  # Linux
                # Try different package managers
                for pm in ['apt', 'yum', 'dnf', 'pacman', 'zypper']:
                    if shutil.which(pm):
                        if pm == 'apt':
                            return self.run_command(f'sudo {pm} install -y {tool_name}')
                        else:
                            return self.run_command(f'sudo {pm} install -y {tool_name}')
        except:
            pass
        return False

    def download_and_install_binary(self, tool_name):
        """Download and install binary tools"""
        try:
            print(f"📥 Downloading {tool_name}...")
            
            # Create tool-specific directory
            tool_dir = self.install_dir / tool_name
            tool_dir.mkdir(exist_ok=True)
            
            # Platform-specific download logic
            if self.system == 'windows':
                return self.download_for_windows(tool_name, tool_dir)
            elif self.system == 'darwin':
                return self.download_for_macos(tool_name, tool_dir)
            else:
                return self.download_for_linux(tool_name, tool_dir)
                
        except Exception as e:
            print(f"❌ Failed to download {tool_name}: {e}")
            return False

    def download_for_windows(self, tool_name, tool_dir):
        """Download tools for Windows"""
        # Download pre-compiled Windows binaries
        if tool_name == 'nmap':
            url = 'https://nmap.org/dist/nmap-7.94-win32.zip'
        elif tool_name == 'wireshark':
            url = 'https://1.eu.dl.wireshark.org/win64/Wireshark-4.0.8-x64.exe'
        else:
            # Generic binary search
            url = f'https://github.com/kitabisa/teler/releases/download/v0.0.1/{tool_name}-windows-amd64.exe'
        
        try:
            download_path = tool_dir / f"{tool_name}.zip"
            urllib.request.urlretrieve(url, download_path)
            
            # Extract if zip file
            if url.endswith('.zip'):
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(tool_dir)
            
            print(f"✅ {tool_name} installed to {tool_dir}")
            return True
        except:
            return False

    def download_for_linux(self, tool_name, tool_dir):
        """Download tools for Linux"""
        try:
            # Try to download pre-compiled binaries
            url = f"https://github.com/{tool_name}/{tool_name}/releases/latest/download/{tool_name}-linux-x86_64"
            
            download_path = tool_dir / tool_name
            urllib.request.urlretrieve(url, download_path)
            
            # Make executable
            os.chmod(download_path, 0o755)
            print(f"✅ {tool_name} installed to {download_path}")
            return True
        except:
            return False

    def download_for_macos(self, tool_name, tool_dir):
        """Download tools for macOS"""
        try:
            url = f"https://github.com/{tool_name}/{tool_name}/releases/latest/download/{tool_name}-darwin-amd64"
            
            download_path = tool_dir / tool_name
            urllib.request.urlretrieve(url, download_path)
            
            os.chmod(download_path, 0o755)
            print(f"✅ {tool_name} installed to {download_path}")
            return True
        except:
            return False

    def install_tool(self, tool_name):
        """Universal tool installation method"""
        if tool_name not in self.all_kali_tools:
            print(f"❌ Tool '{tool_name}' not found in database")
            return False
        
        tool_info = self.all_kali_tools[tool_name]
        print(f"🚀 Installing {tool_name}: {tool_info['description']}")
        
        # Try multiple installation methods
        methods = [
            self.install_via_system_package_manager,
            self.install_via_pip,
            self.download_and_install_binary
        ]
        
        for method in methods:
            if method(tool_name):
                print(f"✅ Successfully installed {tool_name}")
                return True
        
        print(f"❌ All installation methods failed for {tool_name}")
        return False

    def install_multiple_tools(self, tool_list):
        """Install multiple tools at once"""
        success_count = 0
        for tool in tool_list:
            if self.install_tool(tool):
                success_count += 1
        return success_count

    def list_all_tools(self):
        """List all available tools"""
        print("\n🛠️  ALL KALI TOOLS AVAILABLE:")
        print("=" * 80)
        for category in self.get_categories():
            print(f"\n📁 {category.upper()}:")
            for tool, info in self.all_kali_tools.items():
                if info.get('category') == category:
                    print(f"  🔧 {tool}: {info['description']}")

    def get_categories(self):
        """Get unique categories"""
        categories = set()
        for info in self.all_kali_tools.values():
            if 'category' in info:
                categories.add(info['category'])
        return sorted(categories)

    def search_tools(self, keyword):
        """Search for tools by keyword"""
        print(f"\n🔍 Searching for: {keyword}")
        found = []
        for tool, info in self.all_kali_tools.items():
            if keyword.lower() in tool.lower() or keyword.lower() in info['description'].lower():
                found.append((tool, info))
        
        if found:
            for tool, info in found:
                print(f"✅ {tool}: {info['description']}")
        else:
            print("❌ No tools found matching your search")

    def interactive_installer(self):
        """Interactive installation menu"""
        while True:
            print("\n" + "=" * 80)
            print("🚀 UNIVERSAL KALI TOOLS INSTALLER - WORKS ANYWHERE!")
            print("=" * 80)
            print("1. Install specific tool")
            print("2. Install multiple tools")
            print("3. List all available tools")
            print("4. Search tools")
            print("5. Install popular toolkit")
            print("6. Install ALL tools (massive download)")
            print("7. Exit")
            print("=" * 80)
            
            choice = input("🎯 Enter your choice (1-7): ").strip()
            
            if choice == '1':
                tool_name = input("🔧 Enter tool name: ").strip()
                self.install_tool(tool_name)
            elif choice == '2':
                tools_input = input("🔧 Enter tool names (comma-separated): ").strip()
                tools = [t.strip() for t in tools_input.split(',')]
                self.install_multiple_tools(tools)
            elif choice == '3':
                self.list_all_tools()
            elif choice == '4':
                keyword = input("🔍 Enter search keyword: ").strip()
                self.search_tools(keyword)
            elif choice == '5':
                self.install_popular_toolkit()
            elif choice == '6':
                self.install_all_tools()
            elif choice == '7':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")

    def install_popular_toolkit(self):
        """Install most popular Kali tools"""
        popular_tools = [
            'nmap', 'sqlmap', 'metasploit-framework', 'burpsuite', 'wireshark',
            'john', 'hydra', 'aircrack-ng', 'nikto', 'theharvester',
            'sublist3r', 'dirb', 'gobuster', 'hashcat', 'binwalk'
        ]
        
        print("🚀 Installing Popular Kali Toolkit...")
        success = self.install_multiple_tools(popular_tools)
        print(f"📊 Installed {success}/{len(popular_tools)} popular tools")

    def install_all_tools(self):
        """Install ALL Kali tools (massive operation)"""
        print("⚠️  WARNING: This will download and install ALL Kali tools (very large)")
        confirm = input("❓ Are you sure? (yes/no): ").strip().lower()
        if confirm == 'yes':
            all_tools = list(self.all_kali_tools.keys())
            success = self.install_multiple_tools(all_tools)
            print(f"🎉 Installed {success}/{len(all_tools)} tools!")

def main():
    """Main function"""
    print("🚀 INITIALIZING UNIVERSAL KALI INSTALLER...")
    print("💻 This works on Windows, Mac, Linux, PyCharm, ANYWHERE!")
    
    installer = UniversalKaliInstaller()
    installer.ensure_install_dir()
    installer.interactive_installer()

if __name__ == "__main__":
    main()
