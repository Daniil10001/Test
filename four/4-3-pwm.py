import RPi.GPIO as GPIO
import time, threading

GPIO.setmode(GPIO.BCM)

alw_pins=[21,20,26,16,19,25,23,24]
pin=0
while True:
   try:
     pin=int(input())
     if not (pin in alw_pins):
        print('Not allowed pin')
     print('Ok')
     break
   except:
     print('wrong format')

GPIO.setup(pin,GPIO.OUT,initial=0)

duty_cycle=1
N_up=1000
T=1/N_up

def Generator():
    global T, duty_cycle,pin, wk
    while wk:
      GPIO.output(pin,1)
      time.sleep(duty_cycle*T)
      GPIO.output(pin,0)
      time.sleep((1-duty_cycle)*T)

th=threading.Thread(target=Generator, args=())
wk=True
th.start()


def _main_():
   global duty_cycle, wk
   tme=1
   try:
     while True:
       inp=input()
       if inp=='q':
          break
       if not inp.replace('.','',1).isdigit():
          raise Exception('String is not allowed')
       dc=float(inp)
       if not (0<=dc<=1):
          raise Exception('Duty cycle allowed from 0.0 to 1.0')
       duty_cycle=dc
   except Exception as e:
       print(e)
       return
   finally:
       wk=False
       GPIO.output(pin,0)
       GPIO.cleanup()
   print("Quiting program")
   quit()

while True:
 _main_()
