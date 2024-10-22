import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

name=input('Enter name of experiment, please: ')

exp_data=pd.read_csv(name+'_data.csv')
exp_settings=pd.read_csv(name+'_settings.csv')

time_st=exp_data['N']
volts=exp_data['ADC']

for i in exp_settings.Experiment:
    time_st[exp_data.Experiment==i]*=exp_settings.dt[i]
    volts[exp_data.Experiment==i]*=exp_settings.dV[i]
data=pd.DataFrame({'E':exp_data.Experiment,'V':volts, 'T':time_st})

X,Y=[],[]
for i in exp_settings['Experiment']:
    datap=data[data.E==i]
    X.append(exp_settings.Frequency[i])
    Y.append(np.max(datap['T']))
X,Y=np.array(X),np.array(Y)

labels=[r'Эксперимент {0} $\nu_{2}={1}Hz$'.format(i+1, exp_settings.Frequency[i],"{disc}") for i in exp_settings.Experiment]
#print(labels)

fig, ax= plt.subplots(figsize=(9,6))

ax.set_title("Зависимость напряжения на конденсаторе от времени зарядки")
ax.set_ylim(np.min(volts), np.max(volts)*1.05)
ax.set_xlim(0, np.max(time_st)*1.05)

ax.minorticks_on()
ax.grid(which='major')
ax.grid(which='minor', linestyle=':')

ax.set_ylabel('Напряжение на конденсаторе $U$, В')
ax.set_xlabel(r'Время эксперимента $\tau$, с')

for i in exp_settings['Experiment']:
    datap=data[data.E==i]
    ax.plot(datap['T'],datap.V,'--o', label=labels[i], linewidth=0.5, markersize=2.)

ax.text(4, 0.75, 'Время зарядки {0}c'.format(np.round(np.average(Y))), fontsize=12)
ax.legend()
fig.tight_layout()


fig1, ax1= plt.subplots(figsize=(9,6))
ax1.set_title("Зависимость времени зарядки от частоты дискретизации")
ax1.minorticks_on()
ax1.grid(which='major')
ax1.grid(which='minor', linestyle=':')
ax1.scatter(X,Y, 4.,'r', marker='o')
ax1.set_ylabel(r'Время зарядки $\tau$, с')
ax1.set_xlabel(r'Частота дискраетизации $\nu$, Гц')

def err(x,y,k,b):
    return np.sum((k*x+b-y)**2)/x.shape[0]
def get_ap(x,y,steps=10000, eps=2e-3, debug=False):
    k,b=0,0
    st=0
    while err(x,y,k,b)>eps and st!=steps:
        k=np.sum(y*x-x*b)/np.sum(x*x)
        b=np.sum(y-k*x)/x.shape[0]
        st+=1
        if debug:
            print(st,':',err(x,y,k,b))
    return k, b
k,b=get_ap(X,Y)
label='Аппроксимация пряиой k={0} b={1}'.format(np.round(k,2),np.round(b,2))
ax1.plot(X,k*X+b,'-.r',label=label,linewidth=0.5, markersize=0.5)
ax1.legend()
fig1.tight_layout()

fig.savefig(name+'_grafic.svg')
fig1.savefig(name+'_frequency_dependence.svg')

plt.show()
