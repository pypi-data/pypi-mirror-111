import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


file  = input('Enter the file name ')
df = pd.read_csv(file, index_col=0)

print('\n')
print('\033[1m' + 'Summary Statistic' + '\033[0m')
print('\n')
print('There are total {0} row and {1} columns.'.format(df.shape[0], df.shape[1]))
print('\n')
print('Columns in data: {}'.format(list(df.columns)))    
print('\n')

Numeric, Categorical, datetime = [], [], []
for i in df.columns:
    if df[i].dtype == 'int64':
        Numeric.append(i)
    elif df[i].dtype == 'float64':
        Numeric.append(i)
    elif df[i].dtype == 'object':
        Categorical.append(i)
    else:
        datetime.append(i)              
print('There are {0} Numeric, {1} Categorical, and {2} Datetime features are in dataset'.format(len(Numeric),len(Categorical),len(datetime)))

print('\n')
print(df.head(5))
print('\n')
print(df.tail(5))
print('\n')
missing_value = pd.DataFrame({
        'Missing Value': df.isnull().sum(),
        'Percentage': (df.isnull().sum() / len(df))*100 })
print(missing_value.sort_values(by='Percentage', ascending=False))
print('\n')
print(df.describe())
print('\n')

try:
    print(df.describe(include=object))
except ValueError as e:
    print(e)
print('\n')

df_num_features=df.select_dtypes(include=np.number)
print('Outlier using Z-score \n')
for i in df_num_features.columns:
    thresold = 3
    mean = df[i].mean()
    std = df[i].std()

    outliers = []
    
    for value in df[i]:
        zscore = (value-mean)/std
        if abs(zscore) > thresold:
            outliers.append(value)       
    
    print('The count of Outliers in the column {0} is {1}'.format(i,len(outliers)))

print('\n Outlier using IQR \n')
Q1 = df_num_features.quantile(0.25)
Q3 = df_num_features.quantile(0.75)
IQR = Q3 - Q1
outlier = pd.DataFrame((df_num_features < (Q1 - 1.5 * IQR)) | (df_num_features > (Q3 + 1.5 * IQR)))
for i in outlier.columns:
    print('Total number of Outliers in column {} are {}'.format(i, (len(outlier[outlier[i] == True][i]))))

