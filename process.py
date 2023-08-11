import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os.path

devices=['motog200', 'pixel6']
languages=['C', 'CPP', 'JAVA', 'KOTLIN', 'PYTHON']
algorithms=['BINARY_TREES', 'FANNKUCH', 'FASTA', 'NBODY', 'PI_DIGITS']
extension='.csv'
dir='post'
qtTests=11 #ignore first

memCols = ['memoryOthers', 'memoryHeapJava', 'memoryNative', 'memoryCode', 'memoryStack']

class Test:
  def __init__(self, totalTime, memory, energy):
    self.totalTime = totalTime
    self.memory = memory
    self.energy = energy

class TestSet:
  def __init__(self, device, language, algorithm):
    self.device = device
    self.language = language
    self.algorithm = algorithm
    self.tests = []
  
  def addTest(self, test):
    self.tests.append(test)
  
  def getMeanTime(self):
    return np.mean([test.totalTime for test in self.tests])
  
  def getMeanMemory(self):
    return np.mean([test.memory['mean'] for test in self.tests])

  def getMeanEnergy(self):
    return np.mean([test.energy for test in self.tests])

  def __str__(self) -> str:
    return (
      f'{self.device} {self.language} {self.algorithm}:\n'
      f'\tMean time: {self.getMeanTime()}\n'
      f'\tMean memory: {self.getMeanMemory()}\n'
      f'\tMean energy: {self.getMeanEnergy()}'
    )

tests = {}

def processAllFiles():
  for dev in devices:
    for lang in languages:
      for alg in algorithms:
        curSet = TestSet(dev, lang, alg)

        for i in range(1,qtTests+1):
          fileName = f'./{dir}/{dev}/{lang}-{alg}-{i}{extension}'
          if not os.path.isfile(fileName): continue

          df = pd.read_csv(fileName)
          df['tempo'] /= 1000 # ms to s
          df['totalMemory'] = df[memCols].sum(axis=1) / (10 ** 6) # Bytes to MB
          df['power'] = df['current'] * df['voltage'] / (10 ** 9) # Watts

          totalTime = df['tempo'].iloc[-1] - df['tempo'].iloc[0] # last - first
          memory = df['totalMemory'].describe() # mean, std, min, 25%, 50%, 75%, max
          energy = np.trapz(df['power'], df['tempo']) # trapezoidal area
          
          curSet.addTest(Test(totalTime, memory, energy))
        
        tests[f'{dev}-{lang}-{alg}'] = curSet

processAllFiles()

#create a dataframe for each device-algorithm with rows: languagens, columns: tempo, memoria media, energia media
def createDataFrame(device, algorithm):
  data =[]
  for lang in languages:
    curSet = tests[f'{device}-{lang}-{algorithm}']
    data.append([curSet.getMeanTime(), curSet.getMeanMemory(), curSet.getMeanEnergy()])
  
  row_names = languages
  col_names = ['time', 'memory', 'energy']

  return pd.DataFrame(data, index=row_names, columns=col_names)

for dev in devices:
  for alg in algorithms:
    df = createDataFrame(dev, alg)
    print(f'{dev}-{alg}\n{df}\n\n')
    # df.plot.bar(x='time', y='memory', rot=0)
    # plt.show()

# #
# # Correlation between different variables
# #clear

# corr = df.corr()

# plt.figure(figsize=(16, 6))
# heatmap = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap='BrBG')
# heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12);
# # save heatmap as .png file
# # dpi - sets the resolution of the saved image in dots/inches
# # bbox_inches - when set to 'tight' - does not allow the labels to be cropped
# plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')

# plt.show()