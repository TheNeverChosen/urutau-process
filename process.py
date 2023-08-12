import os.path
import pandas as pd
import numpy as np
import constants as consts
import Test as t
# import matplotlib.pyplot as plt
# import seaborn as sns

def getDfFromFile(fileName):
  if not os.path.isfile(fileName): return None
  df = pd.read_csv(fileName)
  df['totalMemory'] = df[consts.memCols].sum(axis=1) / (10 ** 6) # Bytes to MB
  df['power'] = df['current'] * df['voltage'] / (10 ** 9) # Watts
  return df

def processAllFiles():
  tests = {}
  for dev in consts.devices:
    for lang in consts.languages:
      for alg in consts.algorithms:
        curSet = t.TestSet(dev, lang, alg)

        for i in range(1,consts.qtTests+1):
          fileName = f'./{consts.processedDir}/{dev}/{lang}-{alg}-{i}{consts.extension}'
          df = getDfFromFile(fileName)
          if df is None: continue # skip if file doesn't exist

          totalTime = df['tempo'].iloc[-1] - df['tempo'].iloc[0] # last - first
          meanMemory = df['totalMemory'].mean()
          totalEnergy = np.trapz(df['power'], df['tempo']/1000) # trapezoidal area
          
          curSet.addTest(t.Test(totalTime/1000, meanMemory, totalEnergy))
        tests[f'{dev}-{lang}-{alg}'] = curSet
  return tests

#create a dataframe for each device-algorithm with rows: languagens, columns: tempo, memoria media, energia media
def createDataFrame(tests, device, algorithm, simple=True):
  attrs = ['totalTime', 'meanMemory', 'totalEnergy']
  if not simple: attrs.append('ratioJoulesPerMs')

  data = []
  for lang in consts.languages:
    curSet = tests[f'{device}-{lang}-{algorithm}']
    
    if simple: data.append([curSet.getMeanFrom(attr) for attr in attrs])
    else: data.append([x for attr in attrs for x in [curSet.getMeanFrom(attr), curSet.getStdFrom(attr)]])

  row_names = consts.languages
  col_names = ['time', 'memory', 'energy'] if simple else ['time', 'time-cv', 'memory', 'memory-cv', 'energy', 'energy-cv', 'ratio', 'ratio-cv']

  return pd.DataFrame(data, index=row_names, columns=col_names)


tests = processAllFiles()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 100)
for dev in consts.devices:
  for alg in consts.algorithms:
    df = createDataFrame(tests, dev, alg)
    print(f'{dev}-{alg}\n{df}\n\n')