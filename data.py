import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns


cwd = os.getcwd()

df = pd.read_csv(cwd +'\\' +'table.csv')
df.dropna(axis=1)

#%%

data = df[0:5000]

sns.pairplot(data, hue = 'time', vars = ['t2m', 'latitude', 'longitude'])
plt.show()

data.plot(x = 'time', y=['t2m', 'latitude', 'longitude'], figsize = (18,10)) # le variabili possono essere n
plt.ylabel('t2m')
plt.title('time on river')
plt.legend('best')
plt.show()

#%%

x = df['time'] # variabile 1
y = df['t2m'] # variabile 2
plt.figure(figsize=(15, 10))
plt.scatter(x, y)
plt.show()