# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:09:38 2021

@author: sevde
"""

import numpy as np
import matplotlib.pyplot as plt

def fun(x):
    return sum(np.power(x,2))

alt_sinir =-5
ust_sinir = 5
problem_boyutu = 5
populasyon_boyutu = 10
w  = 0.8
c1 = 2
c2 = 2

#rastgele popülasyonumuzu oluşturduk
populasyon = np.random.ranf([populasyon_boyutu,problem_boyutu]) * (ust_sinir-alt_sinir) + alt_sinir

obj = np.zeros(populasyon_boyutu) #popülasyon boyutunu sıfırlıyoruz

#Popülasyondaki her birey için amaç fonksiyonu değerlerini tutacak bir dizi oluşturup, her bireyin amaç fonksiyonunu hesaplattık
for i in range(populasyon_boyutu):
    obj[i] = fun(populasyon[i,:])
        
#hız(velocity) değerlerini tutan dizi tanımlıyoruz
velocity = np.zeros([populasyon_boyutu,problem_boyutu])

#Bireylerin pBest pozisyon ve değerlerini tutacak değişkenler oluşturduk
#Parçacığın en iyi pozisyonuna pbest adı verilir
pBestPos = populasyon #p best position
pBestVal = obj #p best value

#Tüm parçacıkların en iyi pozisyonu gbest olarak adlandırılır
#Popülasyondaki gBest değerini tespit ettik
gBestVal = min(obj)
idx = np.where(obj == gBestVal)
gBestPos = populasyon[idx,:]

# Grafik çizdirmek için her bir iterasyonda gBestVal değerinin ekleneceği boş bir liste oluşturup, ilk bulduğumuz gBestVal değerini listeye ekledik
objit = list()
objit.append(gBestVal)

for k in range(100): #algoritma 100 kere çalışıyor
    for i in range(populasyon_boyutu): 
        velocity[i,:] = w*velocity[i,:] + \
                        c1*np.random.ranf()*(pBestPos[i,:] - populasyon[i,:]) + \
                        c2*np.random.ranf()*(gBestPos - populasyon[i,:])
                        #o konumdaki hız vektörünü(değişimi) oluşturuyoruz
                        #velocity[i,:]  --> ilk satırın bütün elemanlarını al
                        #pBestPos[i,:] - populasyon[i,:] --> kendi best pozisyon değerinden o anki değerini çıkardık
                        #gBestPos-populasyon[i,:] --> grubun en iyisinden o anki değerini çıkarıp o fark kadar iyileştirmeye çalışacağız
                        # 1. satırdaki hız vektörünü oluşturmaya çalıştık,  2. satırdaki hız vektörünü oluşturmaya çalıştık, sonra 1. parçacığın konumunu değiştireceğiz, 2. parçacığın konumunu değiştireceğiz 

    vmax = (ust_sinir - alt_sinir) / 2  #hız çok fazla artmasın ki arama alanının dışına çıkmasın
    
    
    """10 birimlik bi arama alanım var ama 10 birim vermek çok matıklı değil o zaman 5 birimlik bi artış olsun maksimum,
    minimum da -5 olsun yani hızda çok değişimler olmasın 
    Burda büyük değerler için ayar yapıyoruz ekleyeceğimiz hız değeri 5 ten büyük çıkarsa 5 yap, -5 ten küçük çıkarsa da -5 yap. Yani
    çok büyütme
    Hızvektörü --> aralığı bizim arama aralığı 10 birimdi ondan büyük veya küçük olmasın"""
    for i in range(populasyon_boyutu):   
        for j in range(problem_boyutu):
            if velocity[i,j] > vmax:
                velocity[i,j] = vmax
            elif velocity[i,j] < -vmax:
                velocity[i,j] = -vmax


    """Amaç fonksiyonu için yani x i -5 ve 5 değerleri arasında arıyoruz ama görüyoruz ki olur da popülasyon
    değeri 5 i geçerse geçmesin, -5 ten de küçük olmasın.
    Çünkü rastgele değerler katıyosunuz ve burda daha büyük değerler çıkarsa bu ayarı yapıyoruz
    Yani popülasyondaki değerler -5 ve 5 aralığında olsun
    """
    populasyon = populasyon + velocity

    for i in range(populasyon_boyutu):
        for j in range(problem_boyutu):
            if populasyon[i,j]>ust_sinir:
                populasyon[i,j]=ust_sinir
            elif populasyon[i,j]<alt_sinir:
                populasyon[i,j]=alt_sinir


#amaç fonksiyonu oluşturduk
    for i in range(populasyon_boyutu):
        obj[i]=fun(populasyon[i,:])

#bu amaç fonksiyonunu daha önceki popülasyon değerleriyle karşılaştır, 
    for i in range(populasyon_boyutu):
        if obj[i]<pBestVal[i]:
            pBestVal[i,:] = populasyon[i,:] #parçacığın pbest ini küçült
            pBestVal[i] = obj[i]  #pbestVal e obj nin değerini ata

    if min(obj)<gBestVal: #grubun en iyisiyle karşılaştır
        gBestVal=min(obj) #yeni en iyi değer obj olacak
        idx = np.where(obj==gBestVal)
        gBestPos = populasyon[idx,:] #pozisyon değerini güncelle
    
    objit.append(gBestVal) # en iyi değerini bi tane iterasyon dizisine ekle. Onun da grafiğini çizeceğiz ki nasıl değiştiğini göreyim en iyi değerin nasıl değiştiğini görelim diye
    
    print("iterasyon :{}, obj :{}".format(k,gBestVal))

    
plt.plot(objit)
plt.xlabel("iterasyon")
plt.ylabel("obj") #amaç fonksiyon değeri
plt.show()
#Grafikte her iterasyondaki amaç fonksiyon değeri gitgide düşüyor. Zaten amacımız amaç fonksiyonunu minimize etmekti

gBestPos = gBestPos[0][0]

print("{:.2f}^2 + {:.2f}^2 + {:.2f}^2 + {:.2f}^2 + {:.2f}^2 = {:.2f}".
      format(gBestPos[0],gBestPos[1],
             gBestPos[2],gBestPos[3],
             gBestPos[4],gBestVal))