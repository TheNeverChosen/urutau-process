import sys
import os.path
from enum import IntEnum
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Error(IntEnum):
  NOT_FILENAME = 1
  NOT_FILE = 2

def fileOpen():
  n = len(sys.argv)
  if n<=1:
    print('Filename not provided')
    sys.exit(Error.NOT_FILENAME)
  if not os.path.isfile(sys.argv[1]):
    print('File provided does not exist')
    sys.exit(Error.NOT_FILE)
  return pd.read_csv(sys.argv[1])


df = fileOpen()

memCols = ['memoryOthers', 'memoryHeapJava', 'memoryNative', 'memoryCode', 'memoryStack']
df['totalMemory'] = df[memCols].sum(axis=1)
df['power'] = df['current'] * df['voltage'] / (10 ** 9)

print(df.to_string())
print(df.describe())

#
# Correlation between different variables
#clear

corr = df.corr()

plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12);
# save heatmap as .png file
# dpi - sets the resolution of the saved image in dots/inches
# bbox_inches - when set to 'tight' - does not allow the labels to be cropped
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')

plt.show()