# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:39:27 2021

@author: sevde
"""

import numpy as np
import matplotlib.pyplot as plt

def fun(x):
    return sum(np.power(x,2))

def dogalSecilim(populasyon, obj, populasyon_boyutu):
    #Bu bir minimum minimilizasyon problemi olduğu için en düşük değeri almak için 1/obj dedik
    obj = 1/obj
    sumObj = sum(obj) #toplamını bulduk
    probs = obj / sumObj #toplama böldük #uygunluk fonksiyonu 
    cprobs = probs #kümülatif olasılıkları bulduk 
    
    for i in range(1,populasyon_boyutu):
        cprobs[i] = cprobs[i-1] + probs[i]
        #kümülatifi bulurken bi öncekinin toplamı ile o anki satırdaki değerleri topladık
        #sonuç olarak kümülatif olasılıkları bulduk
        #Kağıttaki örnekte 0.28, 0.39, 0.83, 1 değerini bulduk --> o kısmın okdu
        
        
    rs = np.random.ranf(populasyon_boyutu) #popülasyona random değer attık. Bu random değerler şu aralıkta(0.28, 0.39, 0.83, 1) hangisiyse onu seçtik 
    araPopulasyon = populasyon.copy()
    
    for i in range(populasyon_boyutu):
        idx = np.argwhere(rs[i] < cprobs) [0][0] #cprobs hangisinden küçükse ilk değerini seçtik
        araPopulasyon[i,:] = populasyon[idx, :].copy()
        #index ini ve değerini seçtik 
        
        #seçerken araPopulasyon 'da hep kopya değerini aldık. Önceki değerini almadık, yani değiştirirsek normal değeri değişmesin diye
        
        return araPopulasyon

def caprazla(araPopulasyon, populasyonBoyutu, caprazlamaOlasiligi, problem_boyutu):
    ciftler = np.random.permutation(populasyonBoyutu) #random permütasyon seçtik, yani hangi noktadan hangi çiftleri çaprazlayalım
    #populasyonBoyutu çift olacak
    
    for i in range (populasyonBoyutu // 2):
        parent1idx = ciftler[2*i]
        parent2idx = ciftler[2*i+1]
        #parent1idx ve parent2idx --> 1 ve 2 yi çaprazladık
        
        parent1 = araPopulasyon[parent1idx,:]
        parent2 = araPopulasyon[parent2idx,:]
        
        rs = np.random.ranf() #random değer attık
        
        #çaprazlayıp çaprazlamadığını kontrol ettik
        if rs < caprazlamaOlasiligi:
            caprazlamaNoktasi = np.random.randint(0, problem_boyutu)
            temp = parent1[caprazlamaNoktasi:].copy()
            parent1[caprazlamaNoktasi:] = parent2[caprazlamaNoktasi:].copy()
            parent2[caprazlamaNoktasi:] = temp
            araPopulasyon[parent1idx, : ] = parent1
            araPopulasyon[parent2idx, : ] = parent2
            #parent1 ve parent2 --> çaprazlama sonucunda oluşan çocuklar
    
    return araPopulasyon #ve gönderdik
    

def mutasyon(araPopulasyon, mutasyonOlasiligi, populasyon_boyutu, problem_boyutu, delta, ust_sinir, alt_sinir):
    rs = np.random.ranf([populasyon_boyutu, problem_boyutu]) #random değer oluşturuyoruz
    # 4-4 matristeki tüm değerler için rasgele bi değer. 
    
    #popülasyondaki bütün elemanların tek tek tüm genlereine bakıp 
    for i in range(populasyon_boyutu):
        for j in range(problem_boyutu):
            if rs[i,j] < mutasyonOlasiligi: #Oluşturulan rasgele sayı mutasyon olasılığından küçükse mutasyon işlemi yapıyor. Yani o geni değiştiriyoruz
                rs2 = 2*np.random.ranf()-1
                araPopulasyon[i,j] = araPopulasyon[i,j] + rs2*delta*(ust_sinir-alt_sinir)
    return araPopulasyon

alt_sinir = -10
ust_sinir = 10
problem_boyutu = 4
populasyon_boyutu = 4 

#Popülasyonda random sayı ürettik, Kaç tane popülasyon sayımız varsa bunun populasyon_boyutu ve problem_boyutu kadar matris oluşturduk
populasyon = np.random.ranf([populasyon_boyutu, problem_boyutu]) * (ust_sinir-alt_sinir) + alt_sinir()
 
#her iterasyondaki en iyi değeri tuttuk
objit = list()

eniyideger=100000000

for i in range(500): #500 iterasyon 
    obj = np.zeros(populasyon_boyutu) #populasyon_boyutu 'nda zeros fonksiyonunu belirledik, zeros fonksiyonuyla 0 0 0 0 değerini verdik 
    
    for i in range(populasyon_boyutu):
        obj[i] = fun(populasyon[i,:])
        #karelerin değeri toplamını obj ye atadık
       
    #en iyi minimum obj değerini bulma
    if min(obj) < eniyideger: #en iyi değerden küçükse
        eniyideger = min(obj) #en küçüğü bulduk
        idx = np.where(obj == eniyideger)[0][0] #en küçüğünün olduğu index değerini bulduk
        eniyicozum = populasyon[idx:] #popülasyonun en iyi çözümünü bulduk
    
    objit.append(eniyideger) #en iyi değeri ekledik
    
    #araPopulasyon 'da dogalSecilim yaptık
    araPopulasyon = dogalSecilim(populasyon, obj, populasyon_boyutu)
    #araPopulasyon 'da caprazlama yaptık
    araPopulasyon =  caprazla(araPopulasyon, populasyon_boyutu, 0.95, problem_boyutu)
    # 0.95 --> çaprazlama yapalım mı yapmayalım mı?
    
    populasyon = mutasyon(araPopulasyon, 0.05, populasyon_boyutu, problem_boyutu, 0.05, ust_sinir, alt_sinir)
    #mutasyona alt ve üst sınır değeri verilmesinin sebebi --> alt veya üst sınırda değerden başka bir yere gitmişse diye kontrolü
    
    #en son mutasyondan sonra yeni popülasyon ortaya çıkıyo
    
    
plt.plot(objit)
plt.xlabel("iterasyon")
plt.show()
    
#Önce çaprazladık, sonra mutasyona uğrattık sonra en iyi değeri bulup iterasyonu çizdirdik     
    
#Olasılıklar aynı zamanda yerel optimuma takılı kalmasını engelliyo