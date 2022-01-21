from Data import Stock
import time
import schedule
from datetime import datetime

#This file is going to be used to check the stock data for the pattern. If the pattern lines up we want to send a message
#This file could run indefinitely and refresh the check every five minutes, or we could schedule a cronjob to run the file every five minutes
#I think the most robust solution is to just run this program in constantly.
#Instead of running it on a personal computer, we could run it on a dedicated raspberry pi, that way it would act like a makeshift server

MSFT=Stock()
LCID=Stock()
AMD=Stock()

#We are going to want to change this, so that we pass the object into the function for now it isn't important since we have the object we are looking for as a global variable
#In the future it will need to be changed if we are ever going to scale it into a full fledged app
def superTrendLong(stock):
    low=stock.Low.iloc[-1]
    #print('Low is equal to:',low)
    count=0
    ###FIXME NEED TO COME UP WITH A WAY TO PARSE THROUGH DATAFRAME REGARDLESS OF THE TYPE OF SUPERTREND
    #JUST KIDDING I DID IT ALREADY HAHAHAHHAHAHAH FUCK YOU MAXWELL
    for key,value in stock.superTrend.items():
        pointer=stock.superTrend[key].columns[0]
        trendValue=stock.superTrend[key][pointer].iloc[-1]
        #print("Trend is equal to:",trendValue)
        if(low>trendValue):
            count+=1
    if(count>=2):
        return True
    return False

def superTrendShort(stock):
    high=stock.High.iloc[-1]
    #print('High is equal to:',high)
    count=0
    for key,value in stock.superTrend.items():
        pointer=stock.superTrend[key].columns[0]
        trendValue=stock.superTrend[key][pointer].iloc[-1]
        #print("Trend is equal to:",trendValue)
        if(high<trendValue):
            count+=1
    if(count>=2):
        return True
    return False
#We take longs when the data is above the EMA
def checkEmaLong(stock):
    ema=stock.expMATime[-1]
    low=stock.Low.iloc[-1]
    #print('This is the EMA:',ema)
    #print("This is the Low Price",low)
    if(low>ema):
        return True
    return False
#We take shorts when the data is below the EMA
def checkEmaShort(stock):
    ema=stock.expMATime[-1]
    high=stock.High.iloc[-1]
    #print("This is the EMA:",ema)
    #print("This is the high price",high)
    if(high<ema):
        return True
    return False
#We also need to perform checks on the RSI
#RSI cross up on the oversold, <20
def checkRsiLong(stock):
    rsi=stock.stochRsi
    rsik=rsi.columns[0]
    rsid=rsi.columns[1]
    if(rsi[rsik].iloc[-2]<rsi[rsid].iloc[-2] and rsi[rsik].iloc[-1]>rsi[rsid].iloc[-1] and rsi[rsik].iloc[-2]<20):
        return True
    return False
#RSI cross down on the overbought, >80
def checkRsiShort(stock):
    rsi=stock.stochRsi
    rsik=rsi.columns[0]
    rsid=rsi.columns[1]
    if(rsi[rsik].iloc[-2]>rsi[rsid].iloc[-2] and rsi[rsik].iloc[-1]<rsi[rsid].iloc[-1] and rsi[rsik].iloc[-2]>80):
        return True
    return False
def checkLong(stock):
    #Check for at least two supertrends below the candle
    #Check that the candles are above the ema
    #All the data frames are going to be compared using the last entry in the dataframe
    #We need to check that the RSI is crossing on the oversold
    if(superTrendLong(stock) and checkEmaLong(stock) and checkRsiLong(stock)):
        print(stock,"Long triggered at:",stock.Time[-1])

def checkShort(stock):
    if(superTrendShort(stock) and checkEmaShort(stock) and checkRsiShort(stock)):
        print(stock,"Short triggered at:",stock.Time[-1])
    
def checkTrade():
    MSFT.getData('MSFT')
    LCID.getData('LCID')
    AMD.getData('AMD')
    checkShort(MSFT)
    checkLong(MSFT)
    checkShort(LCID)
    checkLong(LCID)
    print(datetime.now())
    if(checkRsiLong(LCID)):
        print("LCID Long RSI:")
        print(LCID.stochRsi)
    elif(checkRsiShort(LCID)):
        print("LCID Short RSI:")
        print(LCID.stochRsi)
    if(checkRsiLong(MSFT)):
        print("MSFT Long RSI:")
        print(MSFT.stochRsi)
    elif(checkRsiShort(MSFT)):
        print("MSFT Short RSI:")
        print(MSFT.stochRsi)
    if(checkRsiLong(AMD)):
        print("AMD Long RSI:")
        print(AMD.stochRsi)
    elif(checkRsiShort(AMD)):
        print("AMD Short RSI:")
        print(AMD.stochRsi)
    print("Testing Cycle Complete")
    print('-------------------------')

checkTrade()
schedule.every(1).minutes.do(checkTrade)
while True:
    schedule.run_pending()
    time.sleep(1)
