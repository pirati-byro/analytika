#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''dane.py

Taxes of the Czech Republic
'''

import numpy as np
import math
import matplotlib.pyplot as plt
import operator

def dan(schema, m):
    '''Vrací daň při definovaném daňovém schématu a mzdových nákladech m'''
    delka = len(schema["hranice"])
    schema["hranice"].append(100000000000000.0)
    tax=0
    H=schema["hranice"]
    s=schema["sazby"]

    for i in range(0,delka):
        if H[i] <= m and m <= H[i+1]:
            tax += (m-H[i])*s[i]
        elif H[i+1] < m:
            tax += (H[i+1]-H[i])*s[i]
        elif m < H[i]:
            break

    return tax

def mezni_sazba(schema, m):
    '''Vrací mezdní sazbu daně při definovaném daňovém schématu a mzdových nákladech m'''
    delka = len(schema["hranice"])
    schema["hranice"].append(100000000000000.0)

    H=schema["hranice"]
    s=schema["sazby"]

    for i in range(0,delka):
        if H[i] <= m and m <= H[i+1]:
            return s[i]

# Platný stav

h_bar = 28232.0
sleva = 2070
k = 1.34

H0=0.0
s0=0.45/k

H1=sleva/0.15
s1=(0.15 + 0.45/k)

H2=4*h_bar*k
s2=(0.15 + 0.135/k + 0.07/k)

schema_old = { "hranice": [H0, H1, H2],
               "sazby"  : [s0, s1, s2] }

# ČSSD

H0=0
s0=0.45/k

H1=17250
s1=0.12+0.45/k

H2=40200
s2=0.15+0.45/k

H3=53600
s3=0.25+0.45/k

H4=67000
s4=0.32+0.45/k

schema_cssd = { "hranice": [H0, H1, H2, H3, H4],
                "sazby"  : [s0, s1, s2, s3, s4] }

# ODS
# http://www.ods.cz/volby2017/kalkulacka


k=1.32

H0=0.0
s0=0.43/k

H1=sleva/0.15
s1=(0.15/k + 0.43/k) # mezní sazba 0.439

H2=4*h_bar*k
s2=0.15  # mezní sazba 0.15

schema_ods = { "hranice": [H0, H1, H2],
               "sazby"  : [s0, s1, s2] }

# Piráti

H0=0.0
s0=0.0

H1=sleva/0.47
s1=0.47

schema_pir = { "hranice": [H0, H1],
               "sazby"  : [s0, s1] }

print('  mzda   nyní   ods    čssd   piráti')

for h in range(14000,80000,2000):
    print('{0:6.0f} {1:6.0f} {2:6.0f} {3:6.0f} {4:6.0f}'.format(h,dan(schema_old,1.34*h),
    dan(schema_ods,1.32*h),dan(schema_cssd,1.34*h),dan(schema_pir,1.34*h)))

import matplotlib
matplotlib.rc('font', family='Liberation Sans')

def plot_dane(hspace,label):
    f, axarr = plt.subplots(2, sharex=True)

    oldspace = [ dan(schema_old,h*1.34) for h in hspace ]
    odsspace = [ dan(schema_ods,h*1.32) for h in hspace ]
    cssdspace = [ dan(schema_cssd,h*1.34) for h in hspace ]
    pirspace = [ dan(schema_pir,h*1.34) for h in hspace ]

    axarr[0].set_title('Zdanění práce – '+label)
    axarr[0].plot(hspace,oldspace, color='darkgray')
    axarr[0].plot(hspace,odsspace, color='blue')
    axarr[0].plot(hspace,cssdspace, color='orange')
    axarr[0].plot(hspace,pirspace, color='black')
    axarr[0].set_ylabel('zdanění práce [Kč]')

    oldspace2 = [ mezni_sazba(schema_old,h*1.34) for h in hspace ]
    odsspace2 = [ mezni_sazba(schema_ods,h*1.32) for h in hspace ]
    cssdspace2 = [ mezni_sazba(schema_cssd,h*1.34) for h in hspace ]
    pirspace2 = [ mezni_sazba(schema_pir,h*1.34) for h in hspace ]


    axarr[1].set_title('Mezní sazba daně  – '+label)
    axarr[1].plot(hspace,oldspace2, color='darkgray')
    axarr[1].plot(hspace,odsspace2, color='blue')
    axarr[1].plot(hspace,cssdspace2, color='orange')
    axarr[1].plot(hspace,pirspace2, color='black')
    axarr[1].set_ylabel('mezní sazba daně [%]')

    plt.xlabel('dnešní hrubá mzda [Kč]')

    plt.savefig(label+'.png', dpi=600)
    #plt.show() # show the plot

hspace = np.linspace(12000, 20000, 1000)
#plot_dane(hspace,'nízkopříjmové skupiny')

hspace = np.linspace(20000, 50000, 1000)
#plot_dane(hspace,'střední třída')

hspace = np.linspace(12000, 300000, 1000)
#plot_dane(hspace,'vysokopříjmové skupiny')

def my_color(couple):
    if couple[1]>=0:
        return 'g'
    else:
        return 'r'

def plot_vydelek(hspace,dopad,label):

    colors = [ my_color(couple) for couple in zip(hspace,dopad) ]
    plt.bar(hspace,dopad)

    #plt.set_title('Mezní sazba daně  – '+label)
    plt.xlabel('dnešní hrubá mzda [Kč]')
    plt.ylabel('kolik ušetří na daních [Kč]')
    plt.savefig('dopad '+label+'.png', dpi=600)

hspace = np.linspace(12000, 130000, 10)
dopad=np.fromiter((dan(schema_old,h*1.34)-dan(schema_pir,h*1.34) for h in hspace), np.float64)

plot_vydelek(hspace,dopad,'Piráti')
print(hspace)
print(dopad)
