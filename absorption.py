# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:24:21 2022

@author: leael
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:25:43 2022

@author: leael
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import copy
cwd=os.getcwd()

#Henter spotpriser
#fil=os.path.join(cwd, 'nordpoolmarket_2018.csv') #DKK/MWh 2018
fil=os.path.join(cwd, 'nordpoolmarket_2019.csv') #DKK/MWh 2019
#fil=os.path.join(cwd, 'nordpoolmarket_2020.csv') #DKK/MWh 2020 (skudår)

df=pd.read_csv(fil)

df.drop(1)
df.drop(df.index[0:46],0,inplace=True)
#Fjerner DK2
priser_DK1 = df[df.index % 2 == 0]
    
#Hiver spotprisen for DK1 ud
spotpris=list(priser_DK1.SpotPriceDKK) #DKK/MWh

##Hente forbrugsdata
consumption = pd.read_excel('Heat demand per hour DINF 2019.xlsx') #MWh

#Hiver total ud
con_total=list(consumption.Total) #MWh
con_total[:] = [number - 90 for number in con_total] #Trækker 90MW 
con_total = [0 if i < 0 else i for i in con_total] #Fjerner negative værdier og sætter forbrug=0

#Biomassepris 2020
#fra "Klimastatus og –fremskrivning 2022 (KF22):Brændselspriser"
flis_pris_opvarm=51*3600*0.001 #DKK/MWh



##########################################################
#Priser absorptionsvarmepumper
"""
#Absorption eta=0.5, 250grader, luft DENNE HAR ÆNDRET SIG
flis_pris= [184.55 for i in range(2190)]
flis_pris.extend(173.71 for i in range(2*2190))
flis_pris.extend(184.55 for i in range(2190))
"""

"""
#Absorption eta=0.6, 250grader, luft
flis_pris= [159.12 for i in range(2190)]
flis_pris.extend(149.48 for i in range(2*2190))
flis_pris.extend(159.12 for i in range(2190))
"""

"""
#Absorption eta=0.7, 250grader, luft DENNE HAR ÆNDRET SIG
flis_pris= [139.85 for i in range(2190)]
flis_pris.extend(131.18 for i in range(2*2190))
flis_pris.extend(139.85 for i in range(2190))
"""

"""
#Absorption eta=0.5, 250grader, hav DENNE HAR ÆNDRET SIG
flis_pris= [182.75 for i in range(2190)]
flis_pris.extend(173.22 for i in range(2*2190))
flis_pris.extend(182.75 for i in range(2190))
"""

"""
#Absorption eta=0.6, 250grader, hav
flis_pris= [157.52 for i in range(2190)]
flis_pris.extend(149.04 for i in range(2*2190))
flis_pris.extend(157.52 for i in range(2190))
"""

"""
#Absorption eta=0.7, 250grader, hav DENNE HAR ÆNDRET SIG
flis_pris= [138.41 for i in range(2190)]
flis_pris.extend(130.78 for i in range(2*2190))
flis_pris.extend(138.41 for i in range(2190))
"""

"""
#Absorption eta=0.5, 450grader, luft DENNE HAR ÆNDRET SIG
flis_pris= [148.83 for i in range(2190)]
flis_pris.extend(137.72 for i in range(2*2190))
flis_pris.extend(148.83 for i in range(2190))
"""

""" 
#Absorption eta=0.6, 440grader, luft 
flis_pris= [127.47 for i in range(2190)]
flis_pris.extend(117.71 for i in range(2*2190))
flis_pris.extend(127.47 for i in range(2190))
"""

"""
#Absorption eta=0.7, 440grader, luft
flis_pris= [111.47 for i in range(2190)]
flis_pris.extend(102.77 for i in range(2*2190))
flis_pris.extend(111.47 for i in range(2190))
"""

"""
#Absorption eta=0.5, 450grader, hav DENNE HAR ÆNDRET SIG
flis_pris= [146.95 for i in range(2190)]
flis_pris.extend(137.22 for i in range(2*2190))
flis_pris.extend(146.95 for i in range(2190))
"""

#"""
#Absorption eta=0.6, 440grader, hav DETTE ER DEN BEDSTE
flis_pris= [125.82 for i in range(2190)]
flis_pris.extend(117.27 for i in range(2*2190))
flis_pris.extend(125.82 for i in range(2190))
#"""

"""
#Absorption eta=0.7, 440grader, hav
flis_pris= [109.99 for i in range(2190)]
flis_pris.extend(102.38 for i in range(2*2190))
flis_pris.extend(109.99 for i in range(2190))
"""



#Laver liste med COP (3 om vinter og 3.5 om sommeren)
cop= [3 for i in range(2190)]
cop.extend(3.5 for i in range(2*2190))
cop.extend(3 for i in range(2190))


##############################################
#COP for absorptionsvarmepumper

"""
#Absorption eta=0.5, 250grader, luft
copmek= [0.99 for i in range(2190)]
copmek.extend(1.07 for i in range(2*2190))
copmek.extend(0.99 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.6, 250grader, luft
copmek= [1.19 for i in range(2190)]
copmek.extend(1.29 for i in range(2*2190))
copmek.extend(1.19 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.7, 250grader, luft
copmek= [1.39 for i in range(2190)]
copmek.extend(1.5 for i in range(2*2190))
copmek.extend(1.39 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.5, 250grader, hav
copmek= [1 for i in range(2190)]
copmek.extend(1.07 for i in range(2*2190))  #DENNE ER ÆNDRET
copmek.extend(1 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.6, 250grader, hav
copmek= [1.21 for i in range(2190)]
copmek.extend(1.29 for i in range(2*2190))
copmek.extend(1.21 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.7, 250grader, hav
copmek= [1.41 for i in range(2190)] #DENNE ER ÆNDRET
copmek.extend(1.5 for i in range(2*2190))
copmek.extend(1.41 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.5, 450grader, luft
copmek= [1.29 for i in range(2190)]
copmek.extend(1.42 for i in range(2*2190))
copmek.extend(1.29 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.6, 440grader, luft
copmek= [1.55 for i in range(2190)]
copmek.extend(1.70 for i in range(2*2190)) #DENNE ER ÆNDRET
copmek.extend(1.55 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.7, 440grader, luft
copmek= [1.81 for i in range(2190)]
copmek.extend(1.98 for i in range(2*2190))
copmek.extend(1.81 for i in range(2190))
copmek=np.asarray(copmek)
"""

"""
#Absorption eta=0.5, 450grader, hav
copmek= [1.31 for i in range(2190)]
copmek.extend(1.42 for i in range(2*2190))
copmek.extend(1.31 for i in range(2190))
copmek=np.asarray(copmek)
"""

#"""
#Absorption eta=0.6, 440grader, hav   DETTE ER DEN BEDSTE
copmek= [1.57 for i in range(2190)]
copmek.extend(1.71 for i in range(2*2190))
copmek.extend(1.57 for i in range(2190))
copmek=np.asarray(copmek)
#"""

"""
#Absorption eta=0.7, 440grader, hav
copmek= [1.84 for i in range(2190)]
copmek.extend(1.99 for i in range(2*2190))
copmek.extend(1.84 for i in range(2190))
copmek=np.asarray(copmek)
"""

tid=list(range(0, 8760))


#Lister for hvor meget de forskellige enheder producerer
spids_belast=[]
prod_flis=[]
prod_kombi=[]
prod_hp=[]


############Specifikationer HOP og MESHP

max_vaerk=63.8 #MW

min_hp=0.5*25
max_hp=50 #MW


####################################################

#"""
##Med absorption varmepumpe
mek_fra_flis=max_vaerk*0.8*copmek
varm_fra_flis=max_vaerk*0.2

max_flis=varm_fra_flis+mek_fra_flis #MW
min_flis=0.7*max_flis


max_total=max_hp+max_flis
#"""



##Metoder
def borderline_flis(): #Kaldes i flow chart borderline BIP no. 2
#    prod_flis.append(min_flis[i])
    if con_total[i]-min_flis[i]<=0:
        prod_flis.append(min_flis[i])
        prod_hp.append(0)
    elif con_total[i]-min_flis[i]<min_hp and min_flis[i]*flis_pris[i]+spotpris[i]*(1/cop[i])*min_hp<con_total[i]*flis_pris[i]:
        prod_flis.append(min_flis[i])
        borderline_hp1()
    elif con_total[i]-min_flis[i]<min_hp and min_flis[i]*flis_pris[i]+spotpris[i]*(1/cop[i])*min_hp>con_total[i]*flis_pris[i]:
        prod_hp.append(0)
        prod_flis.append(con_total[i])
    else:
        prod_flis.append(min_flis[i])
        prod_hp.append(con_total[i]-min_flis[i])
        
        
def borderline_hp(): #Kaldes i flowcharts borderline SHP no. 2
    prod_hp.append(min_hp)
    prod_flis.append(con_total[i]-min_hp)
        

def borderline_flis1(): #Kaldes i flowcharts borderline boiler
    if con_total[i]>=min_hp and spotpris[i]*(1/cop[i])*con_total[i]<min_flis[i]*flis_pris[i]:
        prod_hp.append(con_total[i])
        prod_flis.append(0)
    elif spotpris[i]*(1/cop[i])*min_hp<min_flis[i]*flis_pris[i]:
        prod_hp.append(min_hp)
        prod_flis.append(0)
    else:
        prod_hp.append(0)
        prod_flis.append(min_flis[i])


def borderline_hp1(): #Kaldes i flowcharts borderline SHP
    prod_hp.append(min_hp)

    
for i in range(len(spotpris)): 
    if con_total[i]==0: #Ingen produktion
        prod_hp.append(0)
        prod_flis.append(0) 
        spids_belast.append(0)
    if con_total[i]>max_total[i]: #HP og boiler kører full load + spidsbelastning
        spids_belast.append(con_total[i]-max_total[i])
        prod_flis.append(max_flis[i])
        prod_hp.append(max_hp)
    if con_total[i]>max_hp and con_total[i]<=max_flis[i]: #Enten kun kedel eller kombi
        if spotpris[i]*(1/cop[i])<flis_pris[i]: #Kombi billigere end kedel
            spids_belast.append(0)
            borderline_flis() ##OBS
        if spotpris[i]*(1/cop[i])+flis_pris[i]>flis_pris[i]*2: #Flis er billigst, HP slukket
            spids_belast.append(0)
            if con_total[i]<min_flis[i]:   #Obs denne er ikke relevant for basecase men måske for de andre
                spids_belast.append(0)
                borderline_flis()   
            else:
                prod_flis.append(con_total[i])
                prod_hp.append(0)
    if con_total[i]<=max_hp and con_total[i]>0 and flis_pris[i]*min_flis[i]<spotpris[i]*(1/cop[i])*con_total[i]: #flis er billigst
        spids_belast.append(0)
        if con_total[i]<min_flis[i]: #Nedre grænse for flis er nået
            borderline_flis1()
        else:
            prod_flis.append(con_total[i])
            prod_hp.append(0)
    if con_total[i]<=max_hp and con_total[i]>0 and flis_pris[i]*min_flis[i]>spotpris[i]*(1/cop[i])*con_total[i]: #HP er billigst
        spids_belast.append(0)
        if con_total[i]<min_hp: #Nedre grænse for HP er nået
            prod_flis.append(0)  
            borderline_hp1()            
        else:
            prod_hp.append(con_total[i])
            prod_flis.append(0)     
    if con_total[i]>max_flis[i] and con_total[i]<=max_total[i]: #Altid en kombination
       if spotpris[i]*(1/cop[i])<flis_pris[i]: #HP billigst kører 100%
           spids_belast.append(0)
           if con_total[i]-max_hp<min_flis[i]:
               borderline_flis()
           else:    
               prod_flis.append(con_total[i]-max_hp)
               prod_hp.append(max_hp)
       if spotpris[i]*(1/cop[i])>flis_pris[i]: #flis billigst kører 100%
           spids_belast.append(0)
           if con_total[i]-max_flis[i]<min_hp: #Nedre grænse for HP nået
               borderline_hp()
           else:
               prod_flis.append(max_flis[i])
               prod_hp.append(con_total[i]-max_flis[i])
    
##Løber igennem hvor mange sammehængende timer kedlen er slukket
hours=[]
count=0
index=[] #gemmer indeks

for i in range(8759):
    if count>0 and prod_flis[i+1]>0:
        hours.append(count+1)
        index.append(i)
        count=0   
    elif prod_flis[i]==0 and prod_flis[i+1]>0 and count==0:
        hours.append(1)
        index.append(i)
    elif prod_flis[i]+prod_flis[i+1]==0:
        index.append(i)
        count+=1


#######################Opvarmning og slukning
sluk_timer=[48]
opvarm_timer=6 #Antal timer hvor al produktion går til spilde
startup_timer=6 #Antal timer hvor man kan udnyte 20%
startup_prod=0.2*max_flis #Produktion som bruges under opvarmning
varmup_prod=0.2*max_vaerk
colors=['red']
labels=['48 timer']
prod_flis1=[] #Liste til at gemme nye kedel produktioner
prod_hp1=[] #Liste til at gemme nye varmepumpe produktioner
opvarmning=[]
ak_pris1=[] #Liste til at gemme nye varmepumpe produktioner
#########################Funktioner for at ændre på produktionen

def opvarm_flis():
    prod_nyflis[index[b]]=min_flis[index[b]]
    if con_total[index[b]]-min_flis[index[b]]<=0:
        prod_nyhp[index[b]]=0
    elif con_total[index[b]]-min_flis[index[b]]<min_hp:
        opvarm_hp()
    else:
        prod_nyhp[index[b]]=con_total[index[b]]-min_flis[index[b]]

def opvarm_hp():
    prod_nyhp[index[b]]=min_hp

def startup_flis():
    if d<6: #Timerne hvor der er 20% som kan gå til produktionen    
        prod_nyflis[index[b-(d+1)]]=startup_prod[index[b-(d+1)]]
        if con_total[index[b-(d+1)]]-startup_prod[index[b-(d+1)]]<=0:
            prod_nyhp[index[b-(d+1)]]=0
        elif con_total[index[b-(d+1)]]-startup_prod[index[b-(d+1)]]<min_hp:
            prod_nyhp[index[b-(d+1)]]=min_hp
        else:
            prod_nyhp[index[b-(d+1)]]=con_total[index[b-(d+1)]]-startup_prod[index[b-(d+1)]]
    elif d>=6:
        prod_nyflis[index[b-(d+1)]]=0
        opvarm_pris[index[b-(d+1)]]=flis_pris_opvarm*varmup_prod #Pris hvor al produktion går til splilde
        opvarm_spild_flis[index[b-(d+1)]]=varmup_prod

for c in range(len(sluk_timer)):
    prod_nyflis=copy.copy(prod_flis) #Kopierer produktionen uden at ændrer originalen
    prod_nyhp=copy.copy(prod_hp)
    opvarm_pris=[0]*8760 #List hvor opvarmningspriserne gemmes
    opvarm_spild_flis=[0]*8760
    a=0    
    b=0
    d=0
    for i in range(len(hours)):
        if hours[i]<sluk_timer[c]: #Kedlen slukkes ikke men holdes på minimumgrænsen
            for a in range(hours[i]): #Produktionen og pris for hp og flis ændres
                opvarm_flis()
                b=b+1
        elif hours[i]>=sluk_timer[c]: #Opvarmningstimer og pris tilføjes
            b=b+hours[i]
            for d in range(startup_timer+opvarm_timer):
                startup_flis()

    ##Den samlede produktion udregnes
    samlet_prod=np.add(prod_nyhp, prod_nyflis) #Production from boiler and hp        

    ##Den akumulerede pris udregnes
    #Liste til den akkumulerede pris
    ak_pris=[0]
    ak_pris_hp=[0]
    ak_pris_boiler=[0]
    ak_pris_heating=[0]
    for i in range(len(prod_nyflis)):
        ak_pris_hp.append(ak_pris_hp[-1]+prod_nyhp[i]*spotpris[i]*(1/cop[i]))
        ak_pris_boiler.append(ak_pris_boiler[-1]+prod_nyflis[i]*flis_pris[i]+opvarm_pris[i])
        ak_pris_heating.append(ak_pris_heating[-1]+opvarm_pris[i])
        ak_pris.append(ak_pris[-1]+prod_nyhp[i]*spotpris[i]*(1/cop[i])+prod_nyflis[i]*flis_pris[i]+opvarm_pris[i])


    del ak_pris[0]
    del ak_pris_hp[0]
    del ak_pris_boiler[0]
    del ak_pris_heating[0]
    #Laver om til et array og omregner til mio. 
    ak_pris=np.array(ak_pris)
    ak_pris_hp=np.array(ak_pris_hp)
    ak_pris_boiler=np.array(ak_pris_boiler)
    ak_pris_heating=np.array(ak_pris_heating)
    
    
    ak_pris=(ak_pris)/1000000
    ak_pris_hp=(ak_pris_hp)/1000000
    ak_pris_boiler=(ak_pris_boiler)/1000000
    ak_pris_heating=(ak_pris_heating)/1000000
    
    
    
    print('Annual price for production: ', max(ak_pris), 'MDKK')
    
    prod_flis1.append(prod_nyflis)    #Gemmer produktionerne
    prod_hp1.append(prod_nyhp)
    opvarmning.append(opvarm_pris)
    ak_pris1.append(ak_pris)
    
    plt.figure()
    plt.plot(ak_pris,label='Total cost', color='lightcoral')
    plt.plot(ak_pris_boiler,label='Cost of BIP production', color='dodgerblue')
    plt.plot(ak_pris_hp,label='Cost of MESHP production', color='darkorange')
    plt.grid()
    plt.xlim(0,8760)
    plt.ylim(0,65)
    plt.title('Scenario D, Accumulated cost of AEP')
    plt.xlabel('Hour of the year [h]')
    plt.ylabel('Cost [MDKK]')
    plt.legend()
    plt.show()



################      PLOTS       ##################################



inputflis=[]
for i in range(len(prod_nyflis)):
    inputflis.append(prod_nyflis[i]/(0.2+0.8*copmek[i]))

##Årlig produktion
print('Annual energy production: ', sum(samlet_prod)/1000, 'GWh')
print('Annual boiler production including startup:', sum(prod_nyflis+opvarm_spild_flis)/1000, 'GWh')
print('Annual production from HP:', sum(prod_nyhp)/1000, 'GWh')
print('Weekly overproduction:', sum(samlet_prod[2800:2968])-sum(con_total[2800:2968]))



##Udregner LCOE
capex=409380000

#Absorption
#"""
#capex_hp=158628393.2   #eta=0.5, 250grader, luft
#capex_hp=190354071.9   #eta=0.6, 250grader, luft
#capex_hp=222079750.8   #eta=0.7, 250grader, luft
#capex_hp=159190525.1   #eta=0.5, 250grader, hav
#capex_hp=191028630.1   #eta=0.6, 250grader, hav
#capex_hp=222866735.1   #eta=0.7, 250grader, hav
#capex_hp=209773514.1   #eta=0.5, 450grader, luft
#capex_hp=251728216.9   #eta=0.6, 440grader, luft
#capex_hp=293682919.6   #eta=0.7, 440grader, luft
#capex_hp=210675566.0   #eta=0.5, 450grader, hav
capex_hp=252810679.1    #eta=0.6, 440grader, hav
#capex_hp=294945792.3    #eta=0.7, 440grader, hav



capex=capex+capex_hp
#"""


opex=max(ak_pris)*1000000
LCOE=(capex+opex*25)/(sum(samlet_prod)*25)

print('Opex=', opex/sum(samlet_prod), 'DKK/MWh')
print('Capex=', capex/1000000, 'MDKK')
print('LCOE=', LCOE, 'DKK/MWh')
#print('Wood chip percentage:', (sum(inputflis+opvarm_spild_flis)/1000)/(sum(samlet_prod)/1000))
print('Wood chip input:', (sum(inputflis+opvarm_spild_flis)/1000))



#Scatter plot for production fra flis og HP

for i in range(1):
    plt.figure()
    plt.scatter(tid, samlet_prod,  marker='o', s=5, alpha=0.5, label='Total production', color='lightcoral')
    plt.scatter(tid, prod_hp1[i], marker='o', s=5, alpha=0.5,label='MESHP',color='darkorange') 
    plt.scatter(tid, prod_flis1[i], marker='o', s=5, alpha=0.5, label='BIP', color='dodgerblue')
    plt.xlabel('Hour of the year [h]')
    plt.ylabel('Production [MWh]')
    plt.title('Scenario D, Annual heat production')
    plt.xlim(0,8760)
    plt.ylim(0,152)
    plt.grid()
    plt.legend()
    plt.show()
    
    
##Produktion og consumption
plt.figure()
plt.plot(con_total, label='Demand', color='forestgreen')
plt.plot(samlet_prod,label='Total production', color='lightcoral')
plt.xlabel('Hour of the year [h]')
plt.ylabel('Heat [MWh]')
plt.title('Scenario D. Total demand and production for a week')
plt.ylim(0,95)
plt.xlim(2800,2968)
plt.grid()
plt.legend()
plt.show()







