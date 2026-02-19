import subprocess
import os
import re
import time
import tempfile
from typing import List, Dict

class WiFiDriver:
    def __init__(self, debug=False):
        self.debug = debug
        self.current_connection = None
        
    def _run_command(self, cmd):
        if self.debug:
            print(f"[DEBUG] {cmd}")
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if self.debug and result.stderr:
                print(f"[DEBUG] {result.stderr[:200]}")
            
            return result.stdout if result.returncode == 0 else f"Ошибка: {result.stderr}"
            
        except subprocess.TimeoutExpired:
            return "Ошибка: таймаут"
        except Exception as e:
            return f"Ошибка: {e}"

    def _is_root(self):
        return os.geteuid() == 0
    
    def view(self):
        print("Сканирование WiFi сетей...")
        
        networks = []
        
        if os.name == 'nt':
            result = self._run_command("netsh wlan show networks mode=Bssid")
            if "Ошибка" not in result:
                current_ssid = None
                lines = result.split('\n')
                for line in lines:
                    line = line.strip()
                    if 'SSID' in line and ':' in line and 'BSSID' not in line:
                        name = line.split(':', 1)[1].strip()
                        if name and name not in ['0', '1']:
                            current_ssid = name
                            networks.append({
                                'name': name, 
                                'signal': 'N/A', 
                                'security': 'N/A'
                            })
        
        elif os.name == 'posix':
            for interface in ['wlan0', 'wlan1', 'wlp2s0', 'wlp3s0']:
                commands = [
                    f"nmcli -t -f SSID,SIGNAL,SECURITY dev wifi",
                    f"sudo iwlist {interface} scan 2>/dev/null",
                    f"iwlist {interface} scan 2>/dev/null"
                ]
                
                scan_result = None
                for cmd in commands:
                    result = self._run_command(cmd)
                    if result and "Ошибка" not in result and len(result) > 10:
                        scan_result = result
                        break
                
                if not scan_result:
                    continue
                
                if ':' in scan_result and '\n' in scan_result and 'SSID:' not in scan_result:
                    for line in scan_result.strip().split('\n'):
                        if ':' in line:
                            parts = line.split(':')
                            if len(parts) >= 3:
                                name = parts[0] if parts[0] != '--' else 'Скрытая'
                                if name and name != 'off/any':
                                    signal = parts[1] if len(parts) > 1 else 'N/A'
                                    security = parts[2] if len(parts) > 2 else 'N/A'
                                    networks.append({
                                        'name': name,
                                        'signal': signal,
                                        'security': security
                                    })
                else:
                    essid_matches = re.finditer(r'ESSID:"([^"]*)"', scan_result)
                    signal_matches = re.findall(r'Signal level[:=](-?\d+)', scan_result)
                    quality_matches = re.findall(r'Quality[:=](\d+/\d+)', scan_result)
                    encryption_matches = re.findall(r'Encryption key[:=](on|off)', scan_result)
                    
                    essids = []
                    signals = []
                    
                    for match in essid_matches:
                        essid = match.group(1)
                        if essid and essid != 'off/any':
                            essids.append(essid)
                    
                    if signal_matches:
                        signals = signal_matches
                    elif quality_matches:
                        for quality in quality_matches:
                            if '/' in quality:
                                num, denom = quality.split('/')
                                try:
                                    signal_strength = (int(num) / int(denom)) * 100 - 100
                                    signals.append(str(int(signal_strength)))
                                except:
                                    signals.append('N/A')
                    
                    for i, essid in enumerate(essids):
                        signal = signals[i] if i < len(signals) else 'N/A'
                        security = 'WPA2' if (i < len(encryption_matches) and encryption_matches[i] == 'on') else 'Open'
                        
                        if essid:
                            networks.append({
                                'name': essid,
                                'signal': signal,
                                'security': security
                            })
                
                if networks:
                    break
        
        if not networks:
            try:
                ip_output = self._run_command("ip addr show 2>/dev/null | grep -E 'wlan|wl[0-9]+'")
                if ip_output and "Ошибка" not in ip_output:
                    print("Сети не найдены, но WiFi адаптер обнаружен")
                else:
                    print("WiFi адаптер не обнаружен")
            except:
                pass
        
        unique_networks = []
        seen_names = set()
        for net in networks:
            if net['name'] not in seen_names and net['name']:
                seen_names.add(net['name'])
                unique_networks.append(net)
        
        networks = unique_networks
        
        print(f"Найдено сетей: {len(networks)}")
        if networks:
            print("-" * 50)
            for i, net in enumerate(networks, 1):
                print(f"{i:2}. {net['name'][:30]:30} Сигнал: {net['signal']:6} Защита: {net['security']}")
        
        return networks

    def join(self, name, password=None):
        print(f"Подключение к сети: {name}")
        
        if not name or name.strip() == "":
            print("Ошибка: имя сети не может быть пустым")
            return False
        
        success = False
        
        if os.name == 'nt':
            if password:
                xml_profile = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{name}</name>
    <SSIDConfig>
        <SSID>
            <name>{name}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
                
                xml_file = f"{name}.xml"
                with open(xml_file, 'w') as f:
                    f.write(xml_profile)
                
                result = self._run_command(f'netsh wlan add profile filename="{xml_file}"')
                
                if os.path.exists(xml_file):
                    os.remove(xml_file)
                
                if "добавлен" in result or "added" in result:
                    print(f"Профиль для {name} создан")
                else:
                    print(f"Не удалось создать профиль: {result}")
            
            result = self._run_command(f'netsh wlan connect name="{name}"')
            success = "подключено" in result.lower() or "connected" in result.lower()
        
        elif os.name == 'posix':
            if password:
                cmd = f'nmcli device wifi connect "{name}" password "{password}"'
                if not self._is_root():
                    cmd = f'sudo {cmd}'
            else:
                cmd = f'nmcli device wifi connect "{name}"'
                if not self._is_root():
                    cmd = f'sudo {cmd}'
            
            result = self._run_command(cmd)
            success = "успешно" in result.lower() or "successfully" in result.lower()
            
            if not success:
                print("Пробую альтернативный метод...")
                
                wpa_config = f"""
network={{
    ssid="{name}"
    {"psk=\"" + password + "\"" if password else "key_mgmt=NONE"}
}}
                """
                
                config_file = os.path.join(tempfile.gettempdir(), 'wpa_supplicant.conf')
                try:
                    with open(config_file, 'w') as f:
                        f.write(wpa_config)
                except PermissionError:
                    print(f"Нет прав для записи в {config_file}")
                    return False
                
                commands = [
                    "sudo wpa_cli -i wlan0 reconfigure",
                    "sudo dhclient wlan0"
                ]
                
                for cmd in commands:
                    self._run_command(cmd)
                    time.sleep(2)
                
                result = self._run_command("iwconfig wlan0 | grep ESSID")
                success = name in result
        
        if success:
            print(f"Успешно подключено к {name}")
            self.current_connection = name
        else:
            print(f"Не удалось подключиться к {name}")
            print(f"Результат: {result[:200]}")
        
        return success

    def edit(self, old_name, old_password, new_name, new_password):
        print(f"Изменение сети: {old_name} -> {new_name}")
        
        if not old_name or not new_name:
            print("Ошибка: имена сетей не могут быть пустыми")
            return False
        
        if self.current_connection == old_name:
            print(f"Отключаюсь от {old_name}...")
            self._run_command("nmcli connection down id wifi" if os.name == 'posix' else "netsh wlan disconnect")
        
        if os.name == 'nt':
            result = self._run_command(f'netsh wlan delete profile name="{old_name}"')
            print(f"Удаление профиля {old_name}: {result}")
            
            xml_profile = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{new_name}</name>
    <SSIDConfig>
        <SSID>
            <name>{new_name}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{new_password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
            
            xml_file = f"{new_name}.xml"
            with open(xml_file, 'w') as f:
                f.write(xml_profile)
            
            result = self._run_command(f'netsh wlan add profile filename="{xml_file}"')
            
            if os.path.exists(xml_file):
                os.remove(xml_file)
            
            success = "добавлен" in result or "added" in result
        
        elif os.name == 'posix':
            commands = []
            commands.append(f'nmcli connection delete "{old_name}"')
            
            if new_password:
                commands.append(f'nmcli device wifi connect "{new_name}" password "{new_password}"')
            else:
                commands.append(f'nmcli device wifi connect "{new_name}"')
            
            success = True
            for cmd in commands:
                result = self._run_command(cmd if self._is_root() else f"sudo {cmd}")
                if "Ошибка" in result or "error" in result.lower():
                    success = False
                    print(f"Ошибка: {result}")
                    break
        
        if success:
            print(f"Сеть успешно изменена: {old_name} -> {new_name}")
        else:
            print(f"Не удалось изменить сеть")
        
        return success

    def dist(self, ssid, password):
        print(f"Создание точки доступа: {ssid}")
        
        if not self._is_root():
            print("Требуются права root/sudo")
        
        success = False
        
        if os.name == 'nt':
            result = self._run_command(
                f'netsh wlan set hostednetwork mode=allow ssid="{ssid}" key="{password}"'
            )
            
            if "размещенную сеть в результате" or "hosted network" in result:
                result = self._run_command("netsh wlan start hostednetwork")
                success = "запущена" in result or "started" in result
        
        elif os.name == 'posix':
            result = self._run_command("iw list | grep -A 10 'Supported interface modes'")
            
            if "AP" in result:
                hostapd_conf = f"""
interface=wlan0
driver=nl80211
ssid={ssid}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
                """
                
                temp_config = os.path.join(tempfile.gettempdir(), 'hostapd.conf')
                try:
                    with open(temp_config, 'w') as f:
                        f.write(hostapd_conf)
                except PermissionError:
                    print(f"Нет прав для записи в {temp_config}")
                    return False
                
                commands = [
                    "sudo ifconfig wlan0 down",
                    "sudo ifconfig wlan0 192.168.1.1 netmask 255.255.255.0",
                    "sudo ifconfig wlan0 up",
                    "sudo sysctl -w net.ipv4.ip_forward=1",
                    "sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
                    f"sudo hostapd {temp_config} -B"
                ]
                
                success = True
                for cmd in commands:
                    result = self._run_command(cmd)
                    if "Ошибка" in result or "error" in result.lower():
                        print(f"Ошибка: {result}")
                        success = False
                        break
                    time.sleep(1)
            else:
                print("Адаптер не поддерживает режим точки доступа")
                return False
        
        if success:
            print(f"Точка доступа '{ssid}' создана")
            print(f"Пароль: {password}")
            print(f"IP: 192.168.1.1")
        else:
            print(f"Не удалось создать точку доступа")
        
        return success

    def status(self):
        print("Проверка статуса WiFi...")
        
        status = {
            'connected': False,
            'ssid': 'Нет подключения',
            'ip': 'N/A',
            'signal': 'N/A'
        }
        
        if os.name == 'nt':
            result = self._run_command("netsh wlan show interfaces")
            
            if "Состояние" in result:
                lines = result.split('\n')
                for line in lines:
                    line = line.strip()
                    if 'SSID' in line and ':' in line:
                        ssid = line.split(':', 1)[1].strip()
                        if ssid and ssid not in ['0', '1']:
                            status['connected'] = True
                            status['ssid'] = ssid
                    elif 'Signal' in line and ':' in line:
                        signal = line.split(':', 1)[1].strip()
                        status['signal'] = signal
            
            result = self._run_command("ipconfig | findstr /i \"IPv4\"")
            if ':' in result:
                ip = result.split(':', 1)[1].strip()
                status['ip'] = ip
        
        elif os.name == 'posix':
            commands = [
                "iwconfig wlan0 2>/dev/null | grep -E 'ESSID|Signal'",
                "nmcli -t -f ACTIVE,SSID,SIGNAL dev wifi | grep '^да:'",
                "ip addr show wlan0 | grep inet"
            ]
            
            for cmd in commands:
                result = self._run_command(cmd)
                if result and "Ошибка" not in result:
                    if 'ESSID:' in result:
                        essid_match = re.search(r'ESSID:"([^"]*)"', result)
                        signal_match = re.search(r'Signal level=(-?\d+)', result)
                        
                        if essid_match and essid_match.group(1):
                            status['connected'] = essid_match.group(1) != 'off/any'
                            status['ssid'] = essid_match.group(1) if status['connected'] else 'Нет подключения'
                        
                        if signal_match:
                            status['signal'] = signal_match.group(1)
                    
                    elif ':' in result and '\n' not in result:
                        parts = result.split(':')
                        if len(parts) >= 3:
                            status['connected'] = True
                            status['ssid'] = parts[1]
                            status['signal'] = parts[2]
                    
                    elif 'inet ' in result:
                        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result)
                        if ip_match:
                            status['ip'] = ip_match.group(1)
        
        print("\nТекущий статус WiFi:")
        print("-" * 30)
        print(f"Подключен: {'Да' if status['connected'] else 'Нет'}")
        if status['connected']:
            print(f"Сеть: {status['ssid']}")
            print(f"IP: {status['ip']}")
            print(f"Сигнал: {status['signal']}")
        
        return status

WiFi = WiFiDriver(debug=False)