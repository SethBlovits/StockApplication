##FIXME IN THE ADD TRACES I NEED TO SET ALL THE PARAMETERS RIGHT AT THE BEGINNING, THEN I DON'T HAVE TO  HAVE THE LENGTHY NAMES
##NO NEED FOR FUNCTIONS IN THIS PROGRAM SINCE THE ONLY CODE HERE IS USED TO MAKE THE GRAPH

from Data import Stock

import plotly.graph_objs as go
import pandas_market_calendars as mcal
from plotly.subplots import make_subplots

MSFT=Stock()
MSFT.getData('MSFT')

fig = make_subplots(
    rows=5, cols=2,
    specs=[[{"colspan":2,"rowspan": 4}, None],
           [None, None],
           [None, None],
           [None, None],
           [{'colspan':2}, None]],
    print_grid=False)
fig.add_trace(go.Candlestick(x=MSFT.Time,
                open=MSFT.Open,
                high=MSFT.High,
                low=MSFT.Low,
                close=MSFT.Close, name= MSFT.Ticker),
                row=1,col=1)
fig.add_trace(go.Scatter(x=MSFT.expMA.index,y=MSFT.expMATime,line={'color':'mediumpurple'}),
                row=1,col=1)
#make the line where the supertrend is on the uptrend, or the line is green
#Since all the supertrends are in a dictionary, they have to be picked out using hteir designations
fig.add_trace(go.Scatter(x=MSFT.superTrend['10-1'].index,y=MSFT.superTrend["10-1"]['SUPERT_10_1.0'].where(MSFT.superTrend["10-1"]['SUPERTd_10_1.0']==1),line={'color':'limegreen'}),
                row=1,col=1)
#make line where the supertrend is on the downtrend, or the line is red
fig.add_trace(go.Scatter(x=MSFT.superTrend['10-1'].index,y=MSFT.superTrend["10-1"]['SUPERT_10_1.0'].where(MSFT.superTrend["10-1"]['SUPERTd_10_1.0']==-1),line={'color':'crimson'}),
                row=1,col=1)
#Repeat for the rest of the supertrends
#SuperTrend 11-2
fig.add_trace(go.Scatter(x=MSFT.superTrend['11-2'].index,y=MSFT.superTrend["11-2"]['SUPERT_11_2.0'].where(MSFT.superTrend["11-2"]['SUPERTd_11_2.0']==1),line={'color':'limegreen'}),
                row=1,col=1)
fig.add_trace(go.Scatter(x=MSFT.superTrend['11-2'].index,y=MSFT.superTrend["11-2"]['SUPERT_11_2.0'].where(MSFT.superTrend["11-2"]['SUPERTd_11_2.0']==-1),line={'color':'crimson'}),
                row=1,col=1)
#SuperTrend 12-3
fig.add_trace(go.Scatter(x=MSFT.superTrend['12-3'].index,y=MSFT.superTrend["12-3"]['SUPERT_12_3.0'].where(MSFT.superTrend["12-3"]['SUPERTd_12_3.0']==1),line={'color':'limegreen'}),
                row=1,col=1)
fig.add_trace(go.Scatter(x=MSFT.superTrend['12-3'].index,y=MSFT.superTrend["12-3"]['SUPERT_12_3.0'].where(MSFT.superTrend["12-3"]['SUPERTd_12_3.0']==-1),line={'color':'crimson'}),
                row=1,col=1)

fig.add_trace(go.Scatter(x=MSFT.stochRsi.index,y=MSFT.stochRsi['STOCHRSIk_14_14_3_3'],line={'color':'orange'}),
                row=5,col=1)
fig.add_trace(go.Scatter(x=MSFT.stochRsi.index,y=MSFT.stochRsi['STOCHRSId_14_14_3_3'],line={'color':'powderblue'}),
                row=5,col=1)
fig.add_hrect(y0=30,y1=70,line_width=0,fillcolor='grey',opacity=0.2,
                row=5,col=1)

fig.update_layout(
    title=MSFT.Ticker,
    yaxis_title='Stock Price'
)

fig.update_xaxes(
    rangeslider_visible=False,
    matches='x',
    rangebreaks=[dict(bounds=["sat","mon"]),
        dict(bounds=[16,9.5],pattern="hour"),
        #dict(holidays)
    ],
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="minute", stepmode="backward"),
            dict(count=5, label="5m", step="minute",stepmode="backward"),
            dict(count=15, label="15m", step="minute",stepmode="backward"),
            dict(count=45,label="45m",step="minute",stepmode="backward"),
            dict(count=1, label="HTD",step="hour", stepmode="todate"),
            dict(count=3, label="3h",step="hour",stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.update_yaxes(
    
)
fig.show()