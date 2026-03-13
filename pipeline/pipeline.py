import sys
import pandas as pd
import numpy as np

print('arguments', sys.argv)

month = int(sys.argv[1])
print(f'Hello pipeline, month={month}')

df  = pd.DataFrame({'day': [1, 2], 'Num_students' : [11, 22]})
df['month'] = month

print(df.head())


df.to_parquet(f"output_{month}.parquet")


print (f'Hello pipeline, month{month}')