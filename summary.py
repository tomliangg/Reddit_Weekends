import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

data1 = pd.read_csv('data-1.csv')
data1_x_mean = data1['x'].mean()
data1_y_mean = data1['y'].mean()

data1_x_std = data1['x'].std()
data1_y_std = data1['y'].std()

data1_x_min = data1['x'].min()
data1_y_min = data1['y'].min()

data1_x_max = data1['x'].max()
data1_y_max = data1['y'].max()

# correlation - r
data1_r = stats.linregress(data1['x'], data1['y']).rvalue
print (data1_r)

# use scatter plot to visually verify if they are correlated
plt.scatter(data1['x'], data1['y'])
plt.title('data-1 correlation scatter plot')
plt.show()