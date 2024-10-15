import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt
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

pw=np.array([128,64,32,16,8,4,2,1])
zr=[0]*8

def adc(z=False):
   global Vref, comp
   ch=[0]*8
   c=0
   for i in np.arange(0,8):
     c=0
     ch[i]=1
     GPIO.output(dac,ch)
     time.sleep(1e-3)
     for _ in np.arange(0,6):
        c+=GPIO.input(comp)
        time.sleep(1e-3)
     #print(i,c)
     ch[i]=c<3
   if z:
      GPIO.output(dac,zr)
   return np.sum(ch*pw)

def setled(v):
   global Vref
   n=v/256*8
   out=[int(i<=n) for i in range(7,-1,-1)]
   GPIO.output(led,out)


getd=np.zeros(1000000, dtype=np.int32)
results=[]
print(adc())
try:
  for i in range(6):
   vp,a=-1.0, adc(True)
   GPIO.output(troyka, 0)
   print('wait until start')
   while abs(a-vp)>2 or a>12:
      vp=a
      time.sleep(2)
      a=adc(True)
      print(abs(vp-a), a)
   n,st=0,0
   a,vp=10,3
   GPIO.output(troyka, 1)
   print("Start voltage ",adc(), ". Staring measures")
   stime, etime=time.time(),0
   while n<70 and abs(vp-a)>1:
      vp=(3*vp+a)/4
      t=time.time()
      a=adc(True)
      getd[n]=a
      setled(a)
      time.sleep(0.08+0.02*(i//2))
      t2=time.time()
      st+=t2-t
      n+=1
   else:
      etime=time.time()
   print("End of", i, "experiment. Average delay is",st/n,"vp", vp)
   print("It consumes", etime-stime, "seconds")
   plt.plot(getd[:n])
   results.append((st/n,getd[:n]))
except Exception as e:
  print(e)
  GPIO.cleanup()


s=input('set names of files: ')
import pandas as pd
N,ex,ADC=np.array([], dtype=np.int32),np.array([], dtype=np.int32), np.array([], dtype=np.int32)
l=len(results)
ex2, dt, dV, nu=np.zeros(l, dtype=np.int32), np.zeros(l), np.zeros(l), np.zeros(l) 

for i in range(len(results)):
   d1=results[i][0]
   d2=results[i][1]
   sh=d2.shape[0]
   N=np.append(N,np.arange(0,sh, dtype=np.int32))
   ex=np.append(ex,np.zeros(sh, dtype=np.int32)+i)
   ADC=np.append(ADC, d2)
   ex2[i]=i
   dt[i]=d1
   dV[i]=Vref/256
   nu[i]=np.round(1/d1,2)

data1=pd.DataFrame({"Experiment":ex, "N":N , "ADC":ADC})

data2=pd.DataFrame({"Experiment":ex2, "dt":dt , "dV":dV, "Frequency":nu})

data1.to_csv(s+'_data.csv')
data2.to_csv(s+'_settings.csv')
plt.show()
print('end')
