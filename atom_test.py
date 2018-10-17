import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import sklearn

df = pd.DataFrame([[1,2,3],[1,2,3],[3,2,1]],columns=['a','b','c'])

print(df)

df.a.hist()
