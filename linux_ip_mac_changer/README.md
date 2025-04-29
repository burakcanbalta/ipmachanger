# Linux IP ve MAC Değiştirici

Bu araç, Linux sistemlerde IP adresi ve MAC adresini hızlıca değiştirmenizi sağlar.  
İzinli test ortamlarında, eğitim amaçlı ve kişisel güvenlik projelerinde kullanım için tasarlanmıştır.

---

## 🚀 Özellikler
- Rastgele MAC adresi atama
- Rastgele IP adresi üretme
- Manuel IP ve MAC adresi belirleme desteği
- Ağ adaptörü (interface) hızlı güncelleme
- Minimal bağımlılık (sadece `ifconfig` ve `sudo` gerektirir)

---

## ⚙️ Gereksinimler
- Python 3.x
- Linux tabanlı işletim sistemi (Ubuntu, Kali, Debian, Arch, vs.)
- `ifconfig` komutunun yüklü olması (`net-tools` paketi)

---

## 📦 Kurulum

```bash
git clone https://github.com/kullaniciadi/linux_ip_mac_changer.git
cd linux_ip_mac_changer
sudo python3 ip_mac_changer.py -i eth0 -r
```

> Not: Kullanım için root yetkisi (`sudo`) gereklidir.

---

## 🛠️ Kullanım

```bash
sudo python3 ip_mac_changer.py -i [arayüz_adı] [seçenekler]
```

### Parametreler:
- `-i`, `--interface` : Değiştirilecek ağ arayüzü (zorunlu)
- `-m`, `--mac` : Manuel MAC adresi belirleme
- `-ip`, `--ipaddress` : Manuel IP adresi belirleme
- `-r`, `--random` : Rastgele MAC ve IP adresi ata

---

### 📚 Kullanım Örnekleri:

```bash
sudo python3 ip_mac_changer.py -i eth0 -r
sudo python3 ip_mac_changer.py -i wlan0 -m 00:11:22:33:44:55 -ip 192.168.1.66
```

---

## 💡 İpuçları
- MAC adresini değiştirmeden önce ağ adaptörünüzü doğru girdiğinizden emin olun (`eth0`, `wlan0` gibi).
- Sanal makine ortamlarında MAC değişimi her zaman desteklenmeyebilir.
- MAC değişimi sonrası bazı ağlar yeniden DHCP IP dağıtımı isteyebilir.
- Komut çalışmıyorsa `net-tools` paketinin yüklü olduğundan emin olun (`sudo apt install net-tools`).

---

## 🛡️ Lisans

Bu proje MIT lisansı ile sunulmuştur.  
Özgürce kullanabilir, dağıtabilir ve geliştirebilirsiniz.  
Ancak izinsiz sistemlerde kullanımı yasaktır ve sorumluluk kullanıcıya aittir.

---

## ⚠️ Yasal Uyarı
Bu araç sadece eğitim, araştırma ve izinli test ortamlarında kullanılmalıdır.  
Yetkisiz kullanım yasal sonuçlar doğurabilir.  
Geliştirici bu aracın kötüye kullanımından sorumlu değildir.

---
