# Coffee-Bot
Bu sistem kahve makinasını telegram üzerinden kontrol etmek için kullanılmaktadır. Sistem ile makinaya aşağıdaki yetenekler kazandırılmıştır:

- Kahve makinasına aç veya kapat
- Kahve makinası varsayılan bir kapatma süresi ile açılır.
- X dakika sonra kapat
- Anlık durum özeti
- Bunların haricinde  ip adresi, zaman ve durum bilgileri de sorgulanabilir.

![telegram_bot](telegram_bot.jpeg)

## Malzeme Listesi

- Raspberry Pi 
- Relay Module

Aygıtın Hazırlanması
--------------------

### Gerekli Altyapı Uygulamaları
$ sudo apt-get install gcc-arm* 
$ sudo apt-get install build-essential 
$ sudo apt install python3
$ sudo apt-get install python3-dev

### RaspberryPi GPIO için gerekli uygulamalar
$ sudo dietpi-software list | grep gpio
$ sudo dietpi-software install 69
$ apt install python3-pip3
$ sudo apt-get install rpi.gpio

### GPIO uygulamasını non-root kullanıcı ile çalıştırmak için:
$ sudo adduser "${USER}" dialout
$ sudo adduser "${USER}" gpio
$ sudo adduser "${USER}" kmem
$ sudo vim /etc/udev/rules.d/99-com.rules

```bash
SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c 'chown -R root:gpio /sys/class/gpio && chmod -R 770 /sys/class/gpio; chown -R root:gpio /sys/devices/virtual/gpio && chmod -R 770 /sys/devices/virtual/gpio'"
```

$ sudo chmod +x /etc/udev/rules.d/99-com.rules

### Gerekli Python Kütüphaneleri ve Telegram İstemci Kurulumu
$ pip install telepot
$  pip install nums_from_string 
$  pip install schedule

### Creating telegram bot:
open BotFather
/newbot

Enter name: Coffee-Bot
.....

### Aygıt Wifi (eduroam) Bağlantısı
Dietpi'nin eduroam ağlarına bağlanması için 
/etc/wpa_supplicant/wpa_supplicant.conf dosyası:

```bash
country=TR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
	ssid="eduroam"
	scan_ssid=1
	key_mgmt=WPA-EAP
	eap=PEAP
	identity="eposta@university.edu"
	password="XXXXXXXXX"
	phase1="peaplabel=0"
	phase2="auth=MSCHAPV2"
}
```

Kaynak:
https://github.com/MichaIng/DietPi/issues/3101#issuecomment-529730446

### coffee-bot Servisinin Başlatılması:
Servis dosyası içeriği: 
$ vim /etc/systemd/services/coffee-bot.service

```bash
[Unit]
Description=coffee-bot Coffee Machine Internet Control
After=syslog.target network.target

[Service]
User=dietpi
Group=dietpi

Type=simple
ExecStart=python3 /home/dietpi/coffee-bot/main.py
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Sistem komutları:
$ systemctl daemon-reload
$ systemctl enable coffee-bot.service
$ systemctl start coffee-bot.service

Kaynak:
https://wiki.debian.org/systemd/Services

Notlar ve Kaynaklar:
-------
https://dietpi.com/forum/t/need-help-installing-rpi-gpio-on-a-zero-w/5793

Kullanılan Kütüphane:
https://telepot.readthedocs.io/en/latest/

https://circuitdigest.com/microcontroller-projects/control-raspberry-pi-gpio-with-telegram

https://stackoverflow.com/questions/45558984/how-to-make-telegram-bot-dynamic-keyboardbutton-in-python-every-button-on-one-ro

https://stackoverflow.com/questions/30938991/access-gpio-sys-class-gpio-as-non-root
https://support.embeddedts.com/support/solutions/articles/22000272026-how-to-access-gpio-as-a-non-root-user-

Control electronics using a relay switch 
https://raspberrypi-guide.github.io/electronics/control-electronics-with-a-relay

GPIO Pinout – Rasp Pi 1 Model B+/Rasp Pi 2 Model B:
https://www.raspberry-pi-geek.com/howto/GPIO-Pinout-Rasp-Pi-1-Model-B-Rasp-Pi-2-Model-B

