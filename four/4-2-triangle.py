import RPi.GPIO as GPIO
import time, threading

GPIO.setmode(GPIO.BCM)

def dec2bin(n):
    if n>=256:
       raise Exception("Too big value")
    if n<0:
       raise Exception("Below zero not alowed")
    bits=[0]*8
    for i in range(8):
        bits[i]=(n%2)
        n//=2
    return bits

DAC=[8,11,7,1,0,5,12,6][::-1]
GPIO.setup(DAC,GPIO.OUT,initial=0)

tme=1

def Generator():
    global tme, wk
    i=-1
    while True:
      while i<255:
         i+=1
         GPIO.output(DAC,dec2bin(i))
         time.sleep(tme/255)
         if not wk:
            return
      while i>0:
         i-=1
         GPIO.output(DAC,dec2bin(i))
         time.sleep(tme/255)
         if not wk:
            return

th=threading.Thread(target=Generator, args=())
wk=True
th.start()


def _main_():
   global tme, wk
   tme=1
   try:
     while True:
       inp=input()
       if inp=='q':
          break
       if not inp.replace('.','',1).isdigit():
          raise Exception('String is not allowed')
       tme=float(inp)
   except Exception as e:
       print(e)
       return
   finally:
       wk=False
       GPIO.output(DAC,[0]*8)
       GPIO.cleanup()
   print("Quiting program")
   quit()

while True:
 _main_()
