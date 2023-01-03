import schedule
import nums_from_string
import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

import config as conf

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
    
class app_memory():
    def __init__(self):
        self.onoff = 0
        self.dtime = 0

    def reset(self):
        self.onoff = 0
        self.dtime = 0

status = app_memory()

kahve_gpio = 21 # GPIO number
def_off_time = 60 # Default close minute
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(kahve_gpio, GPIO.OUT)
GPIO.output(kahve_gpio, 0) # Off initially
status.reset()


def job(chat_id):
    GPIO.output(kahve_gpio, 0)
    status.reset()
    bot.sendMessage(chat_id, 'Makina zamanlanmış komut ile kapandı') # The machine closed with a timed command
    return schedule.CancelJob

def status_check():
    on_off = "Açık" if status.onoff else "Kapalı" # On or Off

    if not status.dtime == 0:
        diff = status.dtime - datetime.datetime.now()
        diff = diff.total_seconds()/(60)
        diff = f'{diff:.1f} dakika sonra kapanacak.' # x minute(s) later 
    else:
        diff = "Yok" # None

    return f"Kahve Makinası: {on_off} \
            Zamanlama: {diff}" # Coffee machine: on|off Times: {diff}


def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].lower()

    print ('Received: %s' % command)
    message = "Kahve makinası " # Coffee machine...
    if 'aç' in command: # open
        if 'kahve' in command: # coffee
            GPIO.output(kahve_gpio, 1)
            status.onoff = 1
            message += " açılıyor " # opening...
            schedule.every(def_off_time).minutes.do(job, chat_id)
            status.dtime = datetime.datetime.now() + datetime.timedelta(minutes = def_off_time)
    elif 'kapat' in command: # close
        if 'kahve' in command: # coffee
            GPIO.output(kahve_gpio, 0)
            status.reset()
            message += " kapandı " # closed
        if 'dakika' in command: # minute
            temp = nums_from_string.get_nums(command)
            if not temp:
                message = "lütfen dakikayı sayı olarak yazınız." # please write as number.
            else:
                schedule.every(temp[0]).minutes.do(job, chat_id)
                status.dtime = datetime.datetime.now() + datetime.timedelta(minutes = temp[0])
                message += str(temp[0]) + " dakika sonra kapanacak." # close after x minutes later.
    elif 'durum' in command: # status
        message = status_check()
    elif command == '/saat':
        now = datetime.datetime.now()
        message = str(now.hour)+str(":")+str(now.minute)
    elif command == '/ip':
        message = get_ip()

    else:
        message = "Nasıl yardım edebilirim?" # How can I help you?

    bot.sendMessage(chat_id, message, parse_mode= 'Markdown')

bot = telepot.Bot(conf.API_TOKEN)
# print (bot.getMe())
MessageLoop(bot, action).run_as_thread()
print ('Up and Running....')
while 1:
    schedule.run_pending()
    time.sleep(10)

