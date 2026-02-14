from asyncio.windows_events import NULL
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from PIL.TiffTags import UNDEFINED
from indicatorfunctions import *

import pandas as pd
import copy

def movingavg(data, ma):
    copydata = copy.deepcopy(data)
    copydata['SMA'] = copydata.rolling(window=ma).mean()
    return copydata

names = ["AAPL", "NVDA", "GOOG", "MSFT", "AMZN", "META", "AVGO", "TSLA", "WMT", "GDXU", "LLY", "JPM", "V", "XOM", "JNJ", "MA", "COST", "MU", "ORCL", "BAC", "ABBV", "HD", "PG", "CVX", "NFLX", "KO", "CAT", "GDXD"]
returndic = {}
x = 0
while x < 25:
      for name in names:
            data = yf.download(name, start="2020-01-01", end="2025-01-01")
            data = pd.DataFrame(data)
            closeprice = data["Close"]
      ## ADD MOVING
            moving  = movingavg(closeprice, x)
            lengths = len(closeprice)
            moving.columns = [name, 'SMA']
            print(moving)
            i = 0
            priceabove = 0
            pricebelow = 0
            priceabovearray = []
            ownedpreviousday = False
            for price in closeprice[name]:
                  if i >= lengths:
                      continue
                 #i += i + 1
                 #print(moving["SMA"][i])
                  if moving[name][i] > moving["SMA"][i] or ownedpreviousday == True:
                        pricechange = moving[name][i] - moving[name][i-1]
                        priceabove += pricechange
                        print(priceabove)
                        priceabovearray.append(priceabove)
                        ownedpreviousday = True
                        if moving[name][i] < moving["SMA"][i]:
                            ownedpreviousday = False
                  else:
                        priceabovearray.append(priceabove)
                        ownedpreviousday = False
                #for move in moving["SMA"]:
                    #print("Moving Avg: " + str(move))
                    #print("Todays Price: " + str(price))
                    #if move > price:
                        #continue

                  i += 1

            last_elementpriceabove = priceabovearray[-1]
            last_elementcloseprice = moving[name].iloc[-1]
            #print(last_elementpriceabove)
            #print(last_elementcloseprice)
            percentreturn = round(last_elementpriceabove/last_elementcloseprice * 100, 1)

            returndic[name + " DayMA: " +str(x)] = percentreturn
            #print(returndic)

            moving["priceabove" + str(x)] = priceabovearray
      x += 1
#plt.plot(moving["GDXD DayMA: 2"])
#plt.show()
sorted_dict = dict(sorted(returndic.items(), key=lambda item: item[1], reverse =True))
print(sorted_dict)