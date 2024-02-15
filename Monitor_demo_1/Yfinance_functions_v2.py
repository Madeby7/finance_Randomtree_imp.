import yfinance as yf
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#------------- sklearn libraries -----------------
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
#----------------------stock lists------------------------
from stocks import *


#-> bu sayfa altında genel olarak yapıyı .py uzantısına taşıyıp, aynı zamanda genel bir fonskyon yapısına taşımayı hedefliyorum.
name = "ODAS.IS"
state_time = int(input("Please enter the state time:: "))
period_ema = int(input("Please enter the EMA period value:: "))
array_properties = []
transfer_arr = []
# periot değeri EMA functionu içinde yazılmıştı.
# main fonksiyonu en son çağrılacak...

#!!! -> V2 olarak eklediğimiz update state_time da bir gelişmedir. Eklenti budur.



#======================== main =======================

def main_yfinance(name,state_time,period):
    # burada tüm kodları toplaryacağız,
    SMI, prices = get_price(name)
    #========================
    #period değerini globel olarak tanımlayacağım.
    #-------------------------------
    weighting_factor = 0.007 #!!!!
    weighting_factor_ask = 0.007
    #--------------------------------
    ema, cte= exponential_moving_average(prices, period, weighting_factor)
    EMA = ema[-state_time:] # last state_time ema's
    PRICES = prices[-state_time:] #last state_time prices's
    df_with_EMA_main = concat_data(PRICES,EMA)
    
    percent_arr,time_update = pr_percentage(state_time,df_with_EMA_main)
    state_time = time_update
    classes_statues = class_est(percent_arr,state_time)
    ask,percent_ask = pr_ask(SMI,EMA,weighting_factor_ask)
    properties(SMI,name,ask,percent_ask,state_time,percent_arr,classes_statues) # -> en sondaki fonksiyondur.
    
    
    

    





#========================functions =======================




def get_price(fn_name):
    fn_name = str(fn_name)
    
    SMI = yf.Ticker(fn_name)
    #SMI = Stock Market Info
    SMI_history = SMI.history(period="6y")
    data_SMI = SMI_history.iloc[:,3:4].values
    return SMI,data_SMI # prices olan değer
    





def exponential_moving_average(prices, period, weighting_factor):
    ema = np.zeros(len(prices))
    # belirli bir aralık belirtmeden elimizdeki tüm fiyatları aldık, sonrasında periodu ayrı şekilde EMA da kaç tane gelmesini istiyorsak ona göre çektik.
    try:
        sma = np.mean(prices[:period]) 
        ema[period - 1] = sma 
        print("we in the try section")
    except Exception as e:
        sma = np.mean(prices[:len(prices)])
        period = 1
        ema[period - 1] = sma
        print("we in the except section")

    counter = 1
    for i in range(period, len(prices)):
        ema[i] = (prices[i] * weighting_factor) + (ema[i - 1] * (1 - weighting_factor))
        counter +=1
    return ema,counter

def concat_data(price_st,ema_st):
    df_p = pd.DataFrame(data=price_st)
    df_ema= pd.DataFrame(data=ema_st)
    df_with_EMA = pd.concat([df_p,df_ema],keys=["Prices","EMA-200"],axis=1)
    return df_with_EMA

def pr_percentage(state_time,df_with_EMA):
    percent_arr=[]
    if len((df_with_EMA.iloc[:,:1].values))<state_time:
        # yeni state time bu az olan değerin kendisi kadar eşitlenebilir zaten öbür türlü problem çıkmaz.
        state_time = len((df_with_EMA.iloc[:,:1].values))
        print("we dont find the any interaction before the state time :::: \n\n!!! So, we limited max lower iteraction time")

    for i in range(state_time):
        percent = (((df_with_EMA.iloc[:,:1].values)[i]-(df_with_EMA.iloc[:,1:].values)[i])/(df_with_EMA.iloc[:,:1].values)[i])*100
        percent_arr.append(percent)
    percent_arr = np.array(percent_arr)
    #?print(percent_arr)
    return percent_arr,state_time # main alanda bu değer bir değişkene atanacak

def plots():
    # burası athplot ile yapılan çizimler cart vurtun yapıldığı yer,
        #jupyterde var ama eklemedim daha dursun burada 
    pass

def class_est(percent_arr,state_time):
    min_arr = percent_arr.min()
    max_arr = percent_arr.max()
    inc = float((max_arr-min_arr)/5)

    length_arr = state_time+1
    counter = 1
    classes = np.zeros(state_time)
    i = 0
    for value in percent_arr:
    
        value_f = float(value)
    
        if(value_f>(min_arr) and value_f<(min_arr+inc)):
            classes[i] = 1
    
        elif(value_f>=(min_arr+inc) and value_f<(min_arr+2*inc)):
            classes[i] = 2
    
        elif(value_f>=(min_arr+2*inc) and value_f<(min_arr+3*inc)):
            classes[i] = 3
    
        elif(value_f>=(min_arr+3*inc) and value_f<(min_arr+4*inc)):
            classes[i] = 4
    
        elif(value_f>=(min_arr+4*inc) and value_f<(max_arr)):
            classes[i] = 5
    
        elif(value_f>=(max_arr)):
            classes[i] = 5 # -> ML öğrenmesinde sadece bir örnek olma ihtimali var o yüzden class 7 - en yüksek oran içine çekildi.
        # /-/ en yüksek oranda ama rekoru kırabilcek değer gelirse bu öğrenimde sınır değerlere ilişkin bir parametre eklenebilir.
        
        # overrated /-/ son 200 günün EMA-Price değeri arasındaki enn yüksek fark görülme durumu, satım tavsiyesi max durumdadır.
        
        
        elif(value_f<=(min_arr)):
            classes[i] = 1  #-> ML öğrenmesinde sadece bir örnek olma ihtimali var o yüzden class 6 - en düşük oran içine çekildi.
        #downrated /-/ son 200 günün EMA-price değeri arasındaki min değerdir. -> alım yapılması en yüksek tavsiye grubundadır
        
        else:
            pass
        counter +=1
        i +=1
    classes = classes.astype(int)
    return classes # -> bu ve percent_arr ML lin X ve Y değerleri olacaktır.


def random_forest(percent_arr,classes,daily_cs):
    X = percent_arr
    Y = classes
    #?print(X)
    #?print(Y)
    
# train - test :: bağımlı(y) - bağımsız(x) değişknelerin ayarlanması \\\\\\\\\\\\\\\\\

    x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size = 0.33, random_state = 0)



#  standartscaler ile veirelrin aynı ölçeğe çekilmesi  \\\\\\\\\\\\\\\\\

    sc = StandardScaler()   



    X_train = sc.fit_transform(x_train)
    X_test = sc.transform(x_test)


#  random forest classifier \\\\\\\\\\\\\\\\\

    rfc = RandomForestClassifier(n_estimators=5 , criterion="gini")
    rfc.fit(x_train, y_train)

    y_pred = rfc.predict(x_test)

    # -> önceki örneklerde yeterince kullandığımız bir syntax yeter gari yorum vermeyeceğim artık.

    
#  confusion matrixes \\\\\\\\\
    
    con_matrix = confusion_matrix(y_test, y_pred)

    #?print("*********Random Forest Classifier***********")
    #?print(con_matrix)
    #===================================================

    return rfc.predict(daily_cs)
    # direkt olarak status değerini burada predict edip main içerisinde değişkene alacağız.


def pr_ask(SMI,EMA,weighting_factor_ask):
    #! -> ask değerini yapıya hazır hale getireceğiz.
    yesterday_ema = float(EMA[-1:])
    #?print(yesterday_ema, type(yesterday_ema),"\n\n\n")
    ask = float(SMI.info['ask'])
    weighting_factor_ask = 0.007

    ema_ask = ((ask)*weighting_factor_ask) + (yesterday_ema*(1-weighting_factor_ask))
    ema_ask = round(ema_ask,2)

    #ema[i] = (prices[i] * weighting_factor) + (ema[i - 1] * (1 - weighting_factor))

    percent_ask = ((ask - ema_ask)/ask)*100
    percent_ask = round(percent_ask,2)
    return ask,percent_ask

def properties(SMI,fn_name,ask,percent_ask,state_time,percent_arr,classes):
    daily_cs = np.array(float(percent_ask)) # bu percent arr değil percent ask değeri dikkat.
    daily_cs = np.reshape(daily_cs, (1,-1))
    status_class = random_forest(percent_arr,classes,daily_cs)
    #?print(daily_cs)
    #?print("\n\n\nName :: ",fn_name,"\n\nask :: ",ask,"\n\nterm (last [x] day based) :: ",state_time,"\n\nstatus :: ",status_class)
    #----------------------------------
    # direkt yazdırdığımız değişkenleri aynı zamanda global bir arrayde muhafaza edelim.
    status_check = int(status_class)
    new_item = {"Name":fn_name,"Ask":ask,"State time":state_time,"Status":status_check}
    array_properties.append(new_item)
    
    
    
    
    
    
"""
-> fonskyonların input ve output değerleri direkt olarak main adındaki fonksiyonun içindeki değişkenler ile ilerleyecektir.
    ve bu büyük listeler ile bir araya getirdiğimizde direkt bir liste içinde properties olarak dictionary formatı oluşturabiliriz
    Bunuda kendi page sayfamız içine yollayacağız.
        
"""
    
for stock in hisse_senetleri:
    main_yfinance(stock,state_time,period_ema)


transfer_arr = array_properties


#!!! -> EMa değeri özellikle verilen günden az iterasyon yapmış firmalarda ayrıca kontrol edilecektir.
#!! Çalışıyor olsada EMA değerleri buna göre yeniden organize edilecektir. hata ayıklaması yapılacakıtr.
