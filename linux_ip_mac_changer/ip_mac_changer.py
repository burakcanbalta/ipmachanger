#!/usr/bin/env python3
import os
import random
import subprocess
import argparse
import re
from time import sleep

def get_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def validate_mac(mac_address):
    if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac_address):
        return True
    return False

def validate_ip(ip_address):
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip_address):
        parts = ip_address.split('.')
        if all(0 <= int(part) <= 255 for part in parts):
            return True
    return False

def get_interface_info(interface):
    try:
        result = subprocess.run(['ip', 'addr', 'show', interface], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def change_mac(interface, new_mac):
    if not validate_mac(new_mac):
        print(f"[-] Geçersiz MAC adresi: {new_mac}")
        return False
    
    print(f"[*] {interface} arayüzünün MAC adresi {new_mac} olarak değiştiriliyor...")
    try:
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'down'], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'address', new_mac], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'up'], check=True)
        
        sleep(2)
        current_mac = get_current_mac(interface)
        if current_mac and current_mac.lower() == new_mac.lower():
            print("[+] MAC adresi başarıyla değiştirildi!")
            return True
        else:
            print("[-] MAC adresi değiştirilemedi!")
            return False
    except subprocess.CalledProcessError as e:
        print(f"[-] MAC değiştirme hatası: {e}")
        return False
    except Exception as e:
        print(f"[-] Beklenmeyen hata: {e}")
        return False

def change_ip(interface, new_ip, subnet_mask="24"):
    if not validate_ip(new_ip):
        print(f"[-] Geçersiz IP adresi: {new_ip}")
        return False
    
    print(f"[*] {interface} arayüzünün IP adresi {new_ip}/{subnet_mask} olarak değiştiriliyor...")
    try:
        subprocess.run(['sudo', 'ip', 'addr', 'flush', 'dev', interface], check=True)
        subprocess.run(['sudo', 'ip', 'addr', 'add', f'{new_ip}/{subnet_mask}', 'dev', interface], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'up'], check=True)
        
        sleep(2)
        current_ip = get_current_ip(interface)
        if current_ip and current_ip == new_ip:
            print("[+] IP adresi başarıyla değiştirildi!")
            return True
        else:
            print("[-] IP adresi değiştirilemedi!")
            return False
    except subprocess.CalledProcessError as e:
        print(f"[-] IP değiştirme hatası: {e}")
        return False
    except Exception as e:
        print(f"[-] Beklenmeyen hata: {e}")
        return False

def get_current_mac(interface):
    try:
        result = subprocess.run(['cat', f'/sys/class/net/{interface}/address'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        try:
            result = subprocess.run(['ip', 'link', 'show', interface], 
                                  capture_output=True, text=True, check=True)
            mac_match = re.search(r'link/ether (([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))', result.stdout)
            return mac_match.group(1) if mac_match else None
        except:
            return None

def get_current_ip(interface):
    try:
        result = subprocess.run(['ip', '-4', 'addr', 'show', interface], 
                              capture_output=True, text=True, check=True)
        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
        return ip_match.group(1) if ip_match else None
    except:
        return None

def get_random_ip():
    return f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"

def restore_network(interface):
    print(f"[*] {interface} arayüzü orijinal ayarlarına döndürülüyor...")
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)
        print("[+] Ağ yöneticisi yeniden başlatıldı!")
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['sudo', 'dhclient', '-r', interface], check=False)
            subprocess.run(['sudo', 'dhclient', interface], check=False)
            print("[+] DHCP istemci yeniden başlatıldı!")
            return True
        except:
            print("[-] Ağ sıfırlama başarısız!")
            return False

def display_network_info(interface):
    print(f"\n[+] {interface} Ağ Bilgileri:")
    print("-" * 40)
    
    mac = get_current_mac(interface)
    ip = get_current_ip(interface)
    
    if mac:
        print(f"MAC Adresi: {mac}")
    else:
        print("MAC Adresi: Bulunamadı")
    
    if ip:
        print(f"IP Adresi: {ip}")
    else:
        print("IP Adresi: Bulunamadı")
    
    try:
        result = subprocess.run(['ip', 'route', 'show', 'dev', interface], 
                              capture_output=True, text=True, check=True)
        routes = [line for line in result.stdout.split('\n') if line.strip()]
        if routes:
            print("Yönlendirme:")
            for route in routes:
                print(f"  {route}")
    except:
        pass
    
    print("-" * 40)

def check_interface_exists(interface):
    try:
        subprocess.run(['ip', 'link', 'show', interface], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description='Linux IP ve MAC Değiştirici')
    parser.add_argument('-i', '--interface', required=True, help='Ağ arayüzü (eth0, wlan0)')
    parser.add_argument('-m', '--mac', help='Yeni MAC adresi')
    parser.add_argument('-ip', '--ipaddress', help='Yeni IP adresi')
    parser.add_argument('-s', '--subnet', default='24', help='Subnet mask (varsayılan: 24)')
    parser.add_argument('-r', '--random', action='store_true', help='Rastgele MAC ve IP ata')
    parser.add_argument('-d', '--dhcp', action='store_true', help='DHCP ile otomatik IP al')
    parser.add_argument('-R', '--restore', action='store_true', help='Orijinal ağ ayarlarına dön')
    
    args = parser.parse_args()

    if not check_interface_exists(args.interface):
        print(f"[-] {args.interface} arayüzü bulunamadı!")
        print("[*] Mevcut arayüzler:")
        subprocess.run(['ip', 'link', 'show'], check=False)
        return

    if args.restore:
        restore_network(args.interface)
        sleep(3)
        display_network_info(args.interface)
        return

    print(f"[*] İşlemler başlatılıyor: {args.interface}")
    
    print(f"\n[+] Mevcut Ağ Bilgileri:")
    display_network_info(args.interface)

    if args.dhcp:
        print(f"\n[*] {args.interface} için DHCP ile IP alınıyor...")
        try:
            subprocess.run(['sudo', 'dhclient', '-r', args.interface], check=False)
            subprocess.run(['sudo', 'dhclient', args.interface], check=True)
            sleep(3)
            display_network_info(args.interface)
            return
        except Exception as e:
            print(f"[-] DHCP hatası: {e}")

    mac_success = True
    ip_success = True

    if args.mac or args.random:
        new_mac = args.mac if args.mac else get_random_mac()
        mac_success = change_mac(args.interface, new_mac)

    if args.ipaddress or args.random:
        new_ip = args.ipaddress if args.ipaddress else get_random_ip()
        ip_success = change_ip(args.interface, new_ip, args.subnet)

    if mac_success or ip_success:
        print(f"\n[+] Yeni Ağ Bilgileri:")
        display_network_info(args.interface)
        
        if mac_success and ip_success:
            print("\n[✓] Tüm işlemler başarıyla tamamlandı!")
        else:
            print("\n[!] Bazı işlemler tamamlanamadı!")
    else:
        print("\n[-] Hiçbir işlem tamamlanamadı!")

if __name__ == "__main__":
    main()
