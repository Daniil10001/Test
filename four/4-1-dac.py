import RPi.GPIO as GPIO

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

def _main_():
   try:
     while True:
       inp=input()
       if inp=='q':
          break
       if not inp.isdigit():
          if inp.replace('.','',1).isdigit():
             raise Exception('Float values not allowed')
          else:
             raise Exception('String is not allowed')
       GPIO.output(DAC,dec2bin(int(inp)))
   except Exception as e:
       print(e)
       return
   print("Quiting program")
   GPIO.output(DAC,[0]*8)
   GPIO.cleanup()
   quit()

while True:
 _main_()
