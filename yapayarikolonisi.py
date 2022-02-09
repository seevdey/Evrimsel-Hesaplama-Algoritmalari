# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 12:42:10 2021

@author: sevde
"""

import numpy as np
import matplotlib.pyplot as plt

def fun(x):
    return np.array([sum(np.power(x,2))])
#array oluşturuyoruz xi2 lerin fonksiyonu, yani karelerin toplamını alıyoruz. Bu amaç fonksiyonudur.

#Fitness değerini hesaplayan fonksiyon
#Yiyeceğin ne kadar kaliteli olduğunun bilgisi
def calculateFitness(fObjV):
    fFitness = np.zeros(len(fObjV))
    ind = np.where(fObjV >= 0) #pozitif değerlerin indisini buluyor bu da bi matris
    fFitness[ind] = 1 / (1 + fObjV[ind])
    ind = np.where(fObjV < 0)
    fFitness[ind] = 1 / abs(fObjV[ind])
    return fFitness #fitness fonksiyonunu geri dönüyoruz. Yani burdaki bütün f fonksiyonlarının amaç fonksiyonları için fitness fonksiyonunu yani yeni fitness fonksiyonunu geri dönüyoruz


#Problemin çözüm uzayının istenen aralıklarda olmasını sağlayan fonksiyon
def repair(x, lb, ub):
    for i in range(len(x)):
        if x[i] > ub: #x değeri üst limiti geçerse üst limit değerlerini ver. Yani sınır değerini aşmamaya çalışıyoruz
            x[i] = ub
        if x[i] < lb: #x değeri alt limitten küçükse alt limit değerlerini ver. 
            x[i] = lb
        #Yani sınır değerini aşmamaya çalışıyoruz. Örneğin -50 ve 50 arasındaysa x[i] değerinin 50 den büyük olmasına gerek yok
    return x

#Kolonideki toplam arı sayısı
NP = 20

#20 arı var yarısı gözcü arı, diğer yarısı kaşif arı

#Yiyecek sayısı toplam koloninin yarısı, yiyecek sayısı kadar işçi arı var
FoodNumber = NP // 2

#Hangi kaynağın işçi arısının kaşif arı olacağına karar veren parametre
limit = 100  #çözüm 100 defada iyileşmiyorsa artık onu bırakıyoruz

#Algoritma kaç iterasyon çalışacak
maxCycle = 2500

D = 100 #Problemin boyutu
ub = 100 #Çözüm uzayının max limiti
lb = -100 #Çözüm uzayının min limiti

#Yiyecek kaynağı [-100, 100] aralığında rasgele olarak belirleniyor
Foods = lb + np.random.ranf([FoodNumber, D]) * (ub-lb)
#Foods ile 10 a 100 lük matris oluşuyor

#Yiyeceklerin temsil ettiği çözümün amaç fonksiyonu değeri
ObjVal = np.zeros(FoodNumber)
for i in range(FoodNumber):
    ObjVal[i] = fun(Foods[i,:]) #Her bir satırın karesini al --> fun fonksiyonu
    

#Fitness fonksiyonu yiyecek kaynağının kalitesi hesaplanır
#Amaç fonksiyonun minimum olduğu durumlar daha kaliteli sonuçlar üretir
Fitness = calculateFitness(ObjVal)

#Hangi kaynağın işçi arısının kaşif arı olacağının kontrolü
trial = np.zeros(FoodNumber) #10 deneme matrisi oluşturuyoruz. Her biri için trial numarasını tutmamız gerekiyor
#trial'in limiti 100

#Rasgele oluşturulan çözümlerden en iyi çözüm uzayı ve değeri
#GlobalParams ve GlobalMin olarak tutuluyor
BestInd = np.where(ObjVal == min(ObjVal))[0]  #en düşük indisi veren değeri bulmaya çalışıyorum
#iki değerden aynısı varsa 2. değeri al
BestInd = BestInd[-1]
GlobalMin = ObjVal[BestInd]
GlobalParams = Foods[BestInd,:]

objit = list()
objit.append(GlobalMin)
#GlobalMin'i bi iterasyondaki en iyi değere atıyoruz

iteration = 1
while(iteration <= maxCycle): #iterasyon sayısı 2500'e gelene kadar
    #İŞÇİ ARI FAZI
    for i in range(FoodNumber): #işçi arı besin kaynağı kadar en iyi çözümü bulmaya çalışıyor
        Param2Change = np.random.randint(0, D) #değişecek parametreyi belirliyoruz. Örneğin 3 numaralı komşuyu değiştiriyoruz
        neighbour = np.random.randint(0, FoodNumber) #Hangi komşuyu seçeceğimize karar veriyoruz
        
        """Burda komşuyu seçiyoruz  mesela iterasyon sayısı 1 nolu elemandan başlıyor. 1 ile 0 arasında yine kendisi gelebilir. 
         Kendisini kendisiyle karşılaştırmak mantıklı değil. Dolayısıyla bu kendisinden farklı bir sayı gelene kadar random sayı üretiyo"""
        while neighbour == i:
            neighbour = np.random.randint(0, FoodNumber)
            
            sol = Foods[i,:].copy()
            sol[Param2Change] = Foods[i, Param2Change] \
                +Foods[i, Param2Change] - Foods[neighbour, Param2Change] \
                    * (np.random.rand() - 0.5*2)
            #Örneğin değişecek parametresi --> 1. numaranın 90. parametresini değiştiriyorum, bunu 5. numaralı komşunun 90. parametresi ile karşılaştırıyorum
            #1 numaranın parametresi - 5 numaranın 90.parametresi       
            #x1 in 90 numaralı parametresini değiştirdik
            
            sol=repair(sol, lb, ub)
            #-100 ile 100 arasında olup olmadığını kontrol ediyoruz
            ObjValSol = fun(sol)
            FitnessSol = calculateFitness(ObjValSol)
            #yeni Fitness değeri buluyoruz
            
            if FitnessSol > Fitness[i]: #yeni fitness değeri(FitnessSol) daha önceki Fitness'tan büyükse çözümü bu kabul ediyoruz
                Foods[i,:] = sol
                Fitness[i] = FitnessSol
                ObjVal[i] = ObjValSol
                trial[i] = 0 #trial'i sıfırlıyoruz
            else: #değiştirdiğimiz yeni değer eski değerden küçükse trial'i 1 artırıyoruz
                trial[i] = trial[i] + 1

#GÖZCÜ ARI FAZI
#işçi arıların bulduğu değerlere bakıyor. İçerisindeki en iyi değere kadar
#Sürekli 10 değere bakıyor. 1'den 10'a kadar
prob = Fitness / sum(Fitness)
i=0
t=-1
"""prob değeri Fitness değerlerinin her biri için örneğin 1 numaranın değeri bu random 
değerden büyükse o zaman bu çözüm içinde (1 nolu çözüm değeri içinde) yine tekrar bi komşuluk
değeri seçiyoruz.
Yani çözümü yeni bi komşulukla yine iyileştirmeye çalışıyoruz
Gözcü arı bakıyor en iyi kaynağı buluyor"""
while t < FoodNumber:
    if np.random.rand() < prob[i]:
        t = t+1
        Param2Change = np.random.randint(0,D)
        neighbour = np.random.randint(0, FoodNumber) #en iyi komşulukta iyileştirmeye çalışıyor
        
        while neighbour == i:
            neighbour = np.random.randint(0, FoodNumber)
            
            sol= Foods[i,:].copy()
            sol[Param2Change] = Foods[i, Param2Change] \
                +Foods[i, Param2Change] - Foods[neighbour, Param2Change] \
                    * (np.random.rand() - 0.5*2)
            
            sol=repair(sol, -100, 100)
            ObjValSol = fun(sol)
            FitnessSol = calculateFitness(ObjValSol)
            #Bütün gözcü arılar için bi olasılık değeri hesaplıyor eğer büyükse yeni bi komşulukta yeni bi değere gitmeye çalışıyor
            #Yani gözcü arıları en iyi kaynağa yönlendirmeye çalışıyoruz
            
            if FitnessSol > Fitness[i]:
                Foods[i,:] = sol
                Fitness[i] = FitnessSol
                ObjVal[i] = ObjValSol
                trial[i] = 0
            else:
                trial[i] = trial[i] + 1

    i = i+1  
    if i == FoodNumber:
        i=0
   
    ind = np.where(ObjVal==min(ObjVal))[0] #indis (1 den fazla değer gelirse) aynı min değere sahip 1'den fazla değer varsa onlardan son değeri al   
    ind = ind[-1]
    if ObjVal[ind] < GlobalMin: 
        GlobalMin = ObjVal[ind]    #bu değeri global min ile karşılaştır
        GlobalParams = Foods[ind,:]
        objit.append(GlobalMin)    #global değer en iyi değerse iterasyondaki değere kaydet, çözüm uzayını bul
       
        
    #KAŞİF ARI FAZI
    ind = np.where(trial==max(trial))[0]
    ind = ind[-1]
    
    #1. adımda max trial sayısını kim yapmışsa yani iyi çözüm üretememişse her birinin trial durumuna bakıyoruz

    if trial[ind] > limit: #trial durumu limitten büyükse 
    #Ordaki arıyı kaşif arıya çevir. Diyoruz ki sana yeni bi değer atayacağız. Yani çözüm uzayında yeni bi değer atıyoruz
        trial[ind] = 0
        sol = np.random.ranf([D]) * (ub-lb) + lb
        ObjValSol = fun[sol]   #değer hesaplıyoruz. 
        FitnessSol = calculateFitness(ObjValSol) #Fitness fonksiyonunu hesaplıyoruz
        Foods[ind,:] = sol
        Fitness[ind] = FitnessSol
        ObjVal[ind] = ObjValSol #eski çözümü bırakıp artık yeni çözüme devam ediyoruz 
        
    iteration = iteration + 1
    
    print("iterasyon :{} , obj :{}".format(iteration, GlobalMin))

plt.plot(objit)
plt.xlabel("iterasyon")
plt.show()


