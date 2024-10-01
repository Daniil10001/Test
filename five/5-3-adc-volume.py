import RPi.GPIO as GPIO
import time

dac=[ 8,11, 7, 1, 0, 5,12, 6]
led=[ 2, 3, 4,17,27,22,10, 9]
led
comp=14
troyka=13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT,initial=0)
GPIO.setup(led,GPIO.OUT,initial=0)
GPIO.setup(troyka,GPIO.OUT, initial=1)
GPIO.setup(comp,GPIO.IN)

Vref=3.27

def dtb(n):
   l=[0]*8
   for i in range(8):
     l[7-i]=n%2
     n//=2
   return l

def adc():
   global Vref, comp
   l,r=-1,255
   while r-l>1:
     c=0
     #print(l,r)
     m=(l+r)//2
     GPIO.output(dac,dtb(m))
     time.sleep(1e-3)
     for _ in range(10):
        c+=GPIO.input(comp)
        time.sleep(1e-4)
     #print(i,c)
     if c>5:
       r=m
     else:
       l=m
   return round(Vref*r/255,2)

def setled(v):
   global Vref
   n=round(8*v/Vref,0)
   out=[int(i<n) for i in range(7,-1,-1)]
   GPIO.output(led,out)

try:
  while True:
    setled(adc())
except:
  GPIO.cleanup()
print('end')