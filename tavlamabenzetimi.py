# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 12:56:38 2021

@author: sevde
"""

import numpy as np
import matplotlib.pyplot as plt

def fun(x):
    return sum(np.power(x,2))

alt = -5
ust = 5
problem_boyutu = 4
#başlangıç çözümünü bulduk (rasgele --> bir ilk çözümü bul)
cozum = np.random.ranf([problem_boyutu]) * (ust-alt) + alt
obj = fun(cozum)

objit = list()
iterasyon=0

#bulduğumuz tek çözüm en iyi çözüm olmuş oluyo
cozumeniyi = cozum;
objeniyi = obj;

T = 10000 #başlangıçta sıcaklık
Tend = 0.1 # en son sıcaklık 
delta = 0.10 #komşu çözümü bulma
soguma_katsayisi = 0.99

alt_degisim = (alt-ust) * delta/2
ust_degisim = (ust-alt) * delta/2

while T > Tend:
        degisim_miktari = np.random.ranf(problem_boyutu) * (ust_degisim - alt_degisim) + alt_degisim
        komsu = cozum + degisim_miktari 
        obj_komsu = fun(komsu); #komşu çözümün amaç fonksiyonunu bulmuşuz
        
        #en düşük mü
        if obj_komsu <= obj: #amaç fonksiyonu daha önceki çözümden küçükse kabul et
            cozum = komsu
            obj = obj_komsu
        else: #amaç fonksiyonu daha önceki çözümden küçük değilse bu olasılığı kullan
            de = obj_komsu - obj
            pa = np.exp(-de/T) #kabul edilme olasılığı
            rs = np.random.ranf() #random sayı üret
            if rs < pa: #random sayı kabul edilme olasılığından düşükse kabul et, değilse o çözümü kabul etme
                cozum = komsu
                obj = obj_komsu
        
        T = T * soguma_katsayisi #sıcaklığı burada düşürüyoruz
        #soğutarak T yi küçültmüş oluyoruz
        
        objit.append(obj) #iterasyona çözümü ekle
        
        if objit[iterasyon] < objeniyi: #en iyi çözümden büyükse
            objeniyi = obj
            cozumeniyi = cozum  #en iyi çözümü güncelle
        
        iterasyon = iterasyon + 1 #her iterasyondaki değişimi görmek için iterasyon sayısını 1 arttır

print("Optimum karar değişkenleri : " , cozumeniyi)
print("Optimum Çözüm : " , objeniyi)

plt.plot(objit)
plt.xlabel("iterasyon")
plt.show()
            
        