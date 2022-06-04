# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:23:11 2022

@author: leael
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import copy
#import statistics
cwd=os.getcwd()

#Henter pris data fra 2018
#fil=os.path.join(cwd, 'nordpoolmarket_2018.csv') #DKK/MWh 2018
fil=os.path.join(cwd, 'nordpoolmarket_2019.csv') #DKK/MWh 2019
#fil=os.path.join(cwd, 'nordpoolmarket_2020.csv') #DKK/MWh 2020 (skudår)
df=pd.read_csv(fil)

df.drop(1)
df.drop(df.index[0:46],0,inplace=True)
#Fjerner DK2
priser_DK1 = df[df.index % 2 == 0]
    
#Hiver spotprisen ud
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
#flis_pris=144.58 #DKK/MWh
flis_pris= [123.2218286 for i in range(2190)]
flis_pris.extend(132.1722699 for i in range(2*2190))
flis_pris.extend(123.2218286 for i in range(2190))


#Laver liste med COP (3 om vinter og 3.5 om sommeren)
cop= [3 for i in range(2190)]
cop.extend(3.5 for i in range(2*2190))
cop.extend(3 for i in range(2190))
cop=np.asarray(cop)

tid=list(range(0, 8760))


#Lister for hvor meget de forskellige værker producerer
spids_belast=[]
prod_flis=[]
prod_kombi=[]
prod_hp_flis=[]
prod_hp_spot=[]

############Specifikationer for elektrisk
max_vaerk= [61.72839506 for i in range(2190)]
max_vaerk.extend(52.91005291  for i in range(2*2190))
max_vaerk.extend(61.72839506 for i in range(2190))
max_vaerk=np.asarray(max_vaerk) #MW


el_fra_flis=0.27*cop
varm_fra_flis=0.73

el_fra_flis_max=max_vaerk*0.27*cop
el_fra_flis_min=el_fra_flis_max*0.7

varm_fra_flis_max=max_vaerk*0.73
varm_fra_flis_min=varm_fra_flis_max*0.7

max_flis=varm_fra_flis_max +el_fra_flis_max #MW
min_flis=0.7*max_flis


min_hp=0.5*25
max_hp=50 #MW

max_total=max_hp+varm_fra_flis_max


def borderline_hp_spot():
    prod_hp_spot.append(min_hp)


for i in range(len(spotpris)):
    if con_total[i]==0: #Ingen produktion
        prod_hp_spot.append(0)
        prod_hp_flis.append(0)
        prod_flis.append(0) 
        spids_belast.append(0)
    if con_total[i]>=max_total[i]: #HP og boiler kører full load + spidsbelastning
        spids_belast.append(con_total[i]-max_total[i])
        prod_flis.append(varm_fra_flis_max[i])
        prod_hp_flis.append(el_fra_flis_max[i])
        prod_hp_spot.append(0)       
    if con_total[i]>0 and con_total[i]<=max_hp:
        if spotpris[i]*(1/cop[i])<flis_pris[i]:
            prod_flis.append(0)
            prod_hp_flis.append(0)
            if con_total[i]<min_hp:
                borderline_hp_spot()
            else:  
                prod_hp_spot.append(con_total[i])
        elif spotpris[i]*(1/cop[i])>flis_pris[i]:     
            if spotpris[i]*(1/cop[i])*con_total[i]<flis_pris[i]*min_flis[i]:
                prod_flis.append(0)
                prod_hp_flis.append(0)
                if con_total[i]<min_hp:
                    borderline_hp_spot()
                else:  
                    prod_hp_spot.append(con_total[i])
            else:    
                prod_hp_spot.append(0)
                prod_flis.append(varm_fra_flis_min[i])
                prod_hp_flis.append(el_fra_flis_min[i])
    if con_total[i]>max_hp and con_total[i]<=min_flis[i]:
        prod_hp_spot.append(0)
        prod_flis.append(varm_fra_flis_min[i])
        prod_hp_flis.append(el_fra_flis_min[i])
    if con_total[i]>min_flis[i] and con_total[i]<min_flis[i]+min_hp:
        prod_hp_spot.append(0)
        flis=(73*con_total[i])/((27*cop[i])+73)
        prod_flis.append(flis)
        hp_flis=(27*con_total[i]*cop[i])/((27*cop[i])+73)
        prod_hp_flis.append(hp_flis)
    if con_total[i]>=min_flis[i]+min_hp and con_total[i]<=min_flis[i]+15:
        if spotpris[i]*(1/cop[i])<flis_pris[i]: #Spotpris billigst
            prod_flis.append(varm_fra_flis_min[i])
            prod_hp_flis.append(el_fra_flis_min[i])  
            prod_hp_spot.append(con_total[i]-prod_flis[-1]-prod_hp_flis[-1])
        elif spotpris[i]*(1/cop[i])>flis_pris[i]:
            prod_hp_spot.append(0)
            flis=(73*con_total[i])/((27*cop[i])+73)
            prod_flis.append(flis)
            hp_flis=(27*con_total[i]*cop[i])/((27*cop[i])+73)
            prod_hp_flis.append(hp_flis)        
    if con_total[i]>min_flis[i]+15 and con_total[i]<max_flis[i]:
        prod_hp_spot.append(0)
        flis=(73*con_total[i])/((27*cop[i])+73)
        prod_flis.append(flis)
        hp_flis=(27*con_total[i]*cop[i])/((27*cop[i])+73)
        prod_hp_flis.append(hp_flis)


prod_hp=np.add(prod_hp_flis,prod_hp_spot)
samlet_prod1=np.add(prod_hp,prod_flis)


#########################################OPVARMNING###########################


######### sammenhængende timer 0 ##########
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
sluk_timer=48
opvarm_timer=6 #Antal timer hvor al produktion går til spilde
startup_timer=6 #Antal timer hvor man kan udnyte 20%
startup_prod=0.2*max_vaerk #Produktion som bruges under opvarmning
varmup_prod=0.2*max_vaerk
colors=['red']
labels=['48 timer']
opvarmning=[]
ak_pris1=[] #Liste til at gemme nye varmepumpe produktioner
#########################Funktioner for at ændre på produktionen
def opvarm_flis():
    prod_nyflis[index[b]]=varm_fra_flis_min[index[b]]
    prod_nyhp_flis[index[b]]=el_fra_flis_min[index[b]]
    if con_total[index[b]]-(varm_fra_flis_min[index[b]]+el_fra_flis_min[index[b]])>0:
        prod_nyhp_spot[index[b]]=con_total[index[b]]-varm_fra_flis_min[index[b]]-el_fra_flis_min[index[b]]
    else:
        prod_nyhp_spot[index[b]]=0



def startup_flis():
    if d<6: #Timerne hvor der er 20% som kan gå til produktionen    
        prod_nyflis[index[b-(d+1)]]=startup_prod[index[b-(d+1)]]
        if con_total[index[b-(d+1)]]-startup_prod[index[b-(d+1)]]<=0:
            prod_nyhp_flis[index[b-(d+1)]]=0
            prod_nyhp_spot[index[b-(d+1)]]=0
        elif con_total[index[b-(d+1)]]-startup_prod[index[b-(d+1)]]<min_hp:
            prod_nyhp_spot[index[b-(d+1)]]=min_hp
            prod_nyhp_flis[index[b-(d+1)]]=0
        else:
            prod_nyhp_spot[index[b-(d+1)]]=con_total[index[b-(d+1)]]-startup_prod[index[b-(d+1)]]
    elif d>=6:
        prod_nyflis[index[b-(d+1)]]=0
        opvarm_pris[index[b-(d+1)]]=flis_pris_opvarm*varmup_prod[index[b-(d+1)]] #Pris hvor al produktion går til splilde
        opvarm_spild_flis[index[b-(d+1)]]=varmup_prod[index[b-(d+1)]]


prod_nyflis=copy.copy(prod_flis) #Kopierer produktionen uden at ændrer originalen
prod_nyhp_spot=copy.copy(prod_hp_spot)
prod_nyhp_flis=copy.copy(prod_hp_flis)
opvarm_pris=[0]*8760 #List hvor opvarmningspriserne gemmes
opvarm_spild_flis=[0]*8760
a=0    
b=0
d=0
for i in range(len(hours)):
    if hours[i]<sluk_timer: #Kedlen slukkes ikke men holdes på minimumgrænsen
        for a in range(hours[i]): #Produktionen og pris for hp og flis ændres
            opvarm_flis()
            b=b+1
    elif hours[i]>=sluk_timer: #Opvarmningstimer og pris tilføjes
        b=b+hours[i]
        for d in range(startup_timer+opvarm_timer):
            startup_flis()

cop=cop.tolist()

ak_pris=[0]
ak_pris_flis=[0]
ak_pris_hp=[0]
for i in range(len(prod_nyflis)):
    ak_pris.append(ak_pris[-1]+prod_nyhp_spot[i]*spotpris[i]*(1/cop[i])+(prod_nyflis[i]+prod_nyhp_flis[i])*flis_pris[i]+opvarm_pris[i])
    ak_pris_flis.append(ak_pris_flis[-1]+prod_nyflis[i]*flis_pris[i]+opvarm_pris[i])
    ak_pris_hp.append(ak_pris_hp[-1]+prod_nyhp_spot[i]*spotpris[i]*(1/cop[i])+prod_nyhp_flis[i]*flis_pris[i])
del ak_pris[0]
del ak_pris_flis[0]
del ak_pris_hp[0]
ak_pris=np.array(ak_pris)
ak_pris_flis=np.array(ak_pris_flis)
ak_pris_hp=np.array(ak_pris_hp)
ak_pris=(ak_pris)/1000000
ak_pris_flis=(ak_pris_flis)/1000000
ak_pris_hp=(ak_pris_hp)/1000000


prod_hp=np.add(prod_nyhp_flis,prod_nyhp_spot)
samlet_prod=np.add(prod_nyflis,prod_hp)

inputflis=[]
for i in range(len(prod_nyflis)):
    inputflis.append(prod_nyflis[i]+prod_nyhp_flis[i]/cop[i]+opvarm_spild_flis[i])



capex=446400000


opex=max(ak_pris)*1000000
LCOE=(capex+opex*25)/(sum(samlet_prod)*25)

print('AEP total=', sum(samlet_prod)/1000, 'GWh' )
print('Annual boiler heat production including startup but not electricity:', sum(prod_nyflis+opvarm_spild_flis)/1000, 'GWh')
print('Annual production from SWHP:', sum(prod_hp)/1000, 'GWh')
print('Weekly overproduction:', sum(samlet_prod[2800:2968])-sum(con_total[2800:2968]))
print('Input yearly wood chip:', sum(inputflis)/1000, 'GWh')
print('Opex=', opex/sum(samlet_prod), 'DKK/MWh')
print('Capex=', capex/1000000, 'MDKK')
print('LCOE=', LCOE, 'DKK/MWh')

flis_fra_hp=[]
for i in range(len(prod_nyhp_flis)):
    flis_fra_hp.append(prod_nyhp_flis[i]/cop[i])


#print('Wood chip percentage:', (sum(prod_nyflis+flis_fra_hp+opvarm_spild_flis)/1000)/(sum(samlet_prod)/1000))



plt.figure()
plt.scatter(tid, samlet_prod,marker='o', s=8, alpha=0.5, label='Total production',color='lightcoral')
plt.scatter(tid, prod_hp, marker='o', s=8, alpha=0.5, label='MESHP',color='darkorange')
plt.scatter(tid, prod_nyflis, marker='o', s=8, alpha=0.5,label='CHPP',color='dodgerblue')
plt.xlabel('Hour of the year [h]')
plt.ylabel('Production [MWh]')
plt.xlim(0,8760)
plt.ylim(0,152)
#plt.ylim(0,100)
plt.title('Scenario C, Annual heat production.')
plt.grid()
plt.legend()
plt.show()            
   

       
##Produktion og consumption
plt.figure()
plt.plot(con_total, label='Demand',color='forestgreen')
plt.plot(samlet_prod,label='Total production', color='lightcoral')
plt.xlabel('Hour of the year [h]')
plt.ylabel('Heat [MWh]')
plt.title('Scenario C. Total demand and production for a week')
plt.ylim(0,95)
plt.xlim(2800,2968)
plt.grid()
plt.legend()
plt.show()     


plt.figure()
plt.plot(ak_pris,label='Total cost', color='lightcoral')
plt.plot(ak_pris_flis,label='Cost of CHPP production', color='dodgerblue')
plt.plot(ak_pris_hp,label='Cost of MESHP production', color='darkorange')
plt.grid()
plt.xlim(0,8760)
plt.ylim(0,65)
plt.title('Scenario C, Accumulated cost of AEP')
plt.xlabel('Hour of the year [h]')
plt.ylabel('Cost [MDKK]')
plt.legend()
plt.show()

