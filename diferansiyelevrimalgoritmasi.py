# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 10:31:45 2021

@author: sevde
"""

import numpy as np
import matplotlib.pyplot as plt

def fun(x):
    return sum(np.power(x,2))

alt = -5
ust = 5
#D = 10  #problem boyutu = 10 yani x1 den x10 a kadar gidecek
D = 3
F = 0.5
CR = 0.5
popSize = 100 #100 tane popülasyon olacak
max_iter = 100 #100 iterasyon


populasyon = np.random.ranf([popSize, D]) * (ust-alt) + alt
#popülasyon oluşturuyoruz
#(ust-alt) ile rastgele bir sayı seçeceğiz (0 ile 10 arasında) bunu alt değere ekleyince -5 ile 5 arasında bi sayı elde edeceğiz

cocuk = populasyon.copy()
obj = np.zeros(popSize)

for i in range(popSize):
    obj[i] = fun(populasyon[i,:])
    
#best_ind = int(np.round(1+(popSize-1)*np.random.ranf()))
best_val1 = min(obj)
best_ind1 = np.where(obj == best_val1)[0]

print(obj)
print(obj[best_ind1])

objit = list()
objit.append(obj[best_ind1])


for iterasyon in range(max_iter):
    for k in range(popSize):
        #mutasyon değerini buluyoruz
        #1 ile 10 arasında permütasyon değeri oluştur (rasgele değerler), ilk 3 ünü seçiyoruz
        mut_deg = np.random.permutation(popSize)[:3] #permütasyonla 3 tane değer seçiyoruz
        #permütasyonla rasgele bir dizilim oluşturdum. Bunun ilk 3 elemanı seçeceğim 3 eleman olack
        
        #MUTASYON İŞLEMİ --> seçilen 3 elemanla mutasyon işlemi yapıyoruz
        mutasyon = F*(populasyon[mut_deg[0],:]) - populasyon[mut_deg[1],:] + populasyon[mut_deg[2],:]
        #seçilen 3 değerden 0. ile 1. iy çıkar 2. yi ekle --> mutasyonu oluşturmuş olduk
        # [mut_deg[0],:] --> 1. elemanın bütün kolonlarını seçtik
        print(mutasyon)
        
        #mutasyona uğramış değerin (Zaten 1 tane değer oluşacak). Bunun her bir elemanına bakıcam problem boyutu 10'du. 10 elemanın her birine bakıcam mutasyon üst sınırdan büyükse üst sınıra, mutasyon<altinir ise alt sınıra getireceğim  
        #mutasyon değerlerinin hepsinin üst, alt sınırlarını kontrol ettik 
        for i in range (D):
            if mutasyon[i] > ust:
                mutasyon[i] = ust
            elif mutasyon[i] < alt:
                mutasyon[i] = alt
                
        #REKOMBİNASYON İŞLEMİ
        for i in range(D):
            secim = np.random.ranf() #random bi sayı atıyorum
            if secim > CR: #bu sayı CR den büyükse
                cocuk[k,i] = populasyon[k,i] #cocuk değere populasyon değerini alıyorum 
            else: 
                cocuk[k,i] = mutasyon[i] #değilse mutasyon değerini atıyorum
        
        #eskisi ile yenisi arasında bi değişim yoksa rasgele bi tanesini bu mutasyondan alırsınız
        
        c_obj = fun(cocuk[k,:]) #cocuk değerin obj fonksiyonunu buluyorum
        if c_obj < obj[k]: #cocuk değerini o andaki popülasyon değeri ile karşılaştırıyoruz --> cocuk küçükse(minimizasyon olduğu için) cocuk a ata değilse eski değeri kullan
            populasyon[k,:] = cocuk[k, :] #hangisi daha küçük değer vermişse onu seçiyorum popülasyona çocuk veya kendi değeri olacak
            obj[k] = c_obj
            #cocuk daha küçükse çocuğu atıyorum yoksa eski değeri kalıyo popülasyonda
            
        #bütün popülasyonlar arasındaki en iyisini bulduk
        if min(obj) < obj[best_ind1]: 
            bestVal = min(obj) #obj değerinin minimiumunu buluyorum
            idx = np.where(obj == bestVal)[0][0]
            bestVal = fun(populasyon[idx, :]) #bestVal değerini buluyorum
            
    objit.append(bestVal) #bestVal değerini iterasyona ekliyorum
    print("iterasyon: {}, obj: {}".format(iterasyon, bestVal))
    
print("Optimum karar değişkenleri : " , populasyon[idx,:])
print("Optimum çözüm : " , bestVal)

print(bestVal)
plt.plot(objit)
plt.xlabel("iterasyon")
plt.show()

        