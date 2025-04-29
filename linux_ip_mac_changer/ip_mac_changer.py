#!/usr/bin/env python3
import os
import random
import subprocess
import argparse
from time import sleep

def get_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def change_mac(interface, new_mac):
    print(f"[*] {interface} arayüzünün MAC adresi {new_mac} olarak değiştiriliyor...")
    try:
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["sudo", "ifconfig", interface, "up"])
        print("[+] MAC adresi başarıyla değiştirildi!")
    except Exception as e:
        print(f"[-] Hata: {e}")

def change_ip(interface, new_ip):
    print(f"[*] {interface} arayüzünün IP adresi {new_ip} olarak değiştiriliyor...")
    try:
        subprocess.call(["sudo", "ifconfig", interface, new_ip])
        print("[+] IP adresi başarıyla değiştirildi!")
    except Exception as e:
        print(f"[-] Hata: {e}")

def get_random_ip():
    return f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"

def main():
    parser = argparse.ArgumentParser(description='Linux IP ve MAC Değiştirici')
    parser.add_argument('-i', '--interface', required=True, help='Ağ arayüzü (eth0, wlan0)')
    parser.add_argument('-m', '--mac', help='Yeni MAC adresi')
    parser.add_argument('-ip', '--ipaddress', help='Yeni IP adresi')
    parser.add_argument('-r', '--random', action='store_true', help='Rastgele MAC ve IP ata')
    args = parser.parse_args()

    new_mac = args.mac if args.mac else get_random_mac()
    new_ip = args.ipaddress if args.ipaddress else get_random_ip()

    if args.random:
        new_mac = get_random_mac()
        new_ip = get_random_ip()

    print(f"\n[+] Mevcut Ağ Bilgileri:")
    os.system(f"ifconfig {args.interface} | grep -E 'ether|inet'")
    
    change_mac(args.interface, new_mac)
    sleep(2)
    change_ip(args.interface, new_ip)
    
    print(f"\n[+] Yeni Ağ Bilgileri:")
    os.system(f"ifconfig {args.interface} | grep -E 'ether|inet'")

if __name__ == "__main__":
    main()
