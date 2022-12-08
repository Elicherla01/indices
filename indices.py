#Author: ravindra elicherla
#This is a hobby project and do not expect code to be robust and not suitable for production use

import yfinance as yf
import pandas as pd

import time
import datetime
import streamlit as st 

from numerize.numerize import numerize

from streamlit_autorefresh import st_autorefresh


indices = ["^NSEI" , "^NSEBANK", "^GSPC", "^DJI", "^IXIC", "^HSI", "^N225", "^STI",  "000001.SS",  "GC=F", "CL=F", "INR=X", "^FTSE", "^TNX", "^GDAXI", "NIFTY_FIN_SERVICE.NS"]
Indices_in_words = ["Nifty", "BankNifty", "S&P100", "DowJones", "Nasdaq", "HongKong", "Japan", "Singapore",  "Shanghai",  "Gold", "CrudeOil", "USD-INR", "FTSE", "10 Y Bond", "DAX", "FINNIFTY"]
#indices

current_time = datetime.datetime.now()
print('day_of_week: ',  current_time.weekday())

current_hour = current_time.hour

print("Hour:", current_hour)

indices_list = []
for index in indices:
    print(index)
    df = yf.download(index, period="3d", interval = "1d")
    df.dropna(inplace=True)
    indices_list.append(df['Adj Close'])
    
data = pd.concat (indices_list, axis=1)
data.columns = Indices_in_words

data = data.fillna(method ='pad')
data = data.fillna(method ='bfill')

st.write(data)



st.markdown("""
    <style>
    div[data-testid="metric-container"] {
    background-color: rgba(300, 300, 300, 0.1);
    border: 1px solid rgba(28, 131, 225, 0.1);
    padding: 5% 5% 5% 10%;
    border-radius: 5px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    text-align: center;
    color: rgb(100, 100, 100);
    overflow-wrap: break-word;
    }

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    overflow-wrap: break-word;
    white-space: break-spaces;
    color: green;
    }
    </style>
    """
    , unsafe_allow_html=True)


def metric_value_timebased(df, metric, current_time):
    #Current Value
    
    st.write(current_time)
    
    if (metric == "S&P100" or "DowJones" or "Nasdaq" and current_time > 19):
        cvalue = df[metric].iloc[-2] 
    
    try:
        #Previous value
        pvalue = df[metric].iloc[-3] 
        
    except:

        pvalue = cvalue
    
    if (metric == "Nifty" or "BankNifty" and current_time > 9):
        cvalue = df[metric].iloc[-2] 
    
    try:
        #Previous value
        pvalue = df[metric].iloc[-3] 
        
    except:

        pvalue = cvalue
        

    cvalue = df[metric].iloc[-2] 
    diffvalue = cvalue - pvalue
    #diffvaluepercentage = (diffvalue/pvalue)*100

    return diffvalue

def metric_value(df, metric):
    #Current Value
    
    cvalue = df[metric].iloc[-1] 
    
    try:
        #Previous value
        pvalue = df[metric].iloc[-2] 
        
    except:

        pvalue = cvalue
        

    cvalue = df[metric].iloc[-1] 
    diffvalue = cvalue - pvalue
    #diffvaluepercentage = (diffvalue/pvalue)*100

    return diffvalue

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


metric = "Nifty"

delta = metric_value(data, metric)

kpi1.metric(
label=metric,
value=int(data['Nifty'].iloc[-1]),
delta = numerize(delta)
)

metric = "BankNifty"
delta = metric_value(data, metric)

kpi2.metric(
label=metric,
value=int(data['BankNifty'].iloc[-1]),
delta = numerize(delta)
)


metric = "S&P100"
delta = metric_value(data, metric)
kpi3.metric(
label=metric,
value=int(data['S&P100'].iloc[-1]),
delta = numerize(delta)
)



metric = "DowJones"
delta = metric_value(data, metric)
kpi4.metric(
label=metric,
value=int(data['DowJones'].iloc[-1]),
delta = numerize(delta)
)

metric = "Nasdaq"
delta = metric_value(data, metric)
kpi5.metric(
label=metric,
value=int(data['Nasdaq'].iloc[-1]),
delta = numerize(delta)
)

metric = "Singapore"
delta = metric_value(data, metric)
kpi1.metric(
label=metric,
value=int(data['Singapore'].iloc[-1]),
delta = numerize(delta)
)

metric = "HongKong"
delta = metric_value(data, metric)
kpi3.metric(
label=metric,
value=int(data['HongKong'].iloc[-1]),
delta = numerize(delta)
)

metric = "Japan"
delta = metric_value(data, metric)
kpi2.metric(
label=metric,
value=int(data['Japan'].iloc[-1]),
delta = numerize(delta)
)

metric = "Shanghai"
delta = metric_value(data, metric)
kpi4.metric(
label=metric,
value=int(data['Shanghai'].iloc[-1]),
delta = numerize(delta)
)

metric = "USD-INR"
delta = metric_value(data, metric)
kpi1.metric(
label=metric,
value=int(data['USD-INR'].iloc[-1]),
delta = numerize(delta)
)

metric = "Gold"
delta = metric_value(data, metric)
kpi3.metric(
label=metric,
value=int(data['Gold'].iloc[-1]),
delta = numerize(delta)
)

metric = "CrudeOil"
delta = metric_value(data, metric)
kpi2.metric(
label=metric,
value=int(data['CrudeOil'].iloc[-1]),
delta = numerize(delta)
)

metric = "10 Y Bond"
delta = metric_value(data, metric)
kpi4.metric(
label=metric,
value=numerize(data['10 Y Bond'].iloc[-1]),
delta = (delta)
)



metric = "FTSE"
delta = metric_value(data, metric)
kpi5.metric(
label=metric,
value=int(data['FTSE'].iloc[-1]),
delta = numerize(delta)
)

metric = "DAX"
delta = metric_value(data, metric)
kpi5.metric(
label=metric,
value=int(data['DAX'].iloc[-1]),
delta = numerize(delta)
)



metric = "FINNIFTY"
delta = metric_value(data, metric)
kpi5.metric(
label=metric,
value=int(data['FINNIFTY'].iloc[-1]),
delta = numerize(delta)
)





# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=10000, limit=100, key="fizzbuzzcounter")

# The function returns a counter for number of refreshes. This allows the
# ability to make special requests at different intervals based on the count
if count == 0:
    st.write("")
elif count % 3 == 0 and count % 5 == 0:
    st.write("")
elif count % 3 == 0:
    st.write("")
elif count % 5 == 0:
    st.write("")
else:
    st.write("")


