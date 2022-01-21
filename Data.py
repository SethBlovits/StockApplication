import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import pandas_market_calendars as mcal
from ta.trend import EMAIndicator, ema_indicator
from pandas_ta import supertrend,stochrsi


#Create a class that will create the stock object. This will be used by the charting program and the stock program.
#This will pull data based on the ticker specified.
class Stock:

    #This is a default class function. Init is short for initialize. Basically this runs the instant you define an object
    #It sets the default values for your object. In this case we want it to be empty 
    def __init__(self):
        self.Ticker=''
        self.Time=[]
        self.Open=[]
        self.Close=[]
        self.High=[]
        self.Low=[]
        self.stochRsi=[]
        self.expMA=[]
        self.expMATime=[]
        #The data structure below is a dictionary. Instead of using index number to get data, you can use names
        #that you assign to it. In this case, the different types of supertrends I want to use
        self.superTrend = {'10-1':[],
                            '11-2':[],
                            '12-3':[],}

    def getData(self,tickername):
        self.Ticker=tickername
        data=yf.download(tickers=tickername,period='1mo',interval='5m') 
        self.Time=data.index
        self.Open=data['Open']
        self.Close=data['Close']
        self.High=data['High']
        self.Low=data['Low']
        #start=data.index[0]
        #end=data.index[len(data.index)-1]
        self.expMA=ema_indicator(close=data['Close'],window=200)
        self.expMATime=self.expMA.tolist()

        #Define each entry in the supertrend dict. The first value comes back as -1, so we have to drop it
        self.superTrend['10-1']=supertrend(data['High'],data['Low'],data['Close'],10,1)
        self.superTrend['11-2']=supertrend(data['High'],data['Low'],data['Close'],11,2)
        self.superTrend['12-3']=supertrend(data['High'],data['Low'],data['Close'],12,3)
        self.superTrend['10-1'].drop(index=self.superTrend['10-1'].index[0],axis=0, inplace=True)
        self.superTrend['11-2'].drop(index=self.superTrend['11-2'].index[0],axis=0, inplace=True)
        self.superTrend['12-3'].drop(index=self.superTrend['12-3'].index[0],axis=0, inplace=True)

        self.stochRsi=stochrsi(data['Close'],length=14,rsi_length=14,k=3,d=3)

        

