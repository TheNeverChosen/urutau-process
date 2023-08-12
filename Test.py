import pandas as pd
import numpy as np

class Test:
  def __init__(self, totalTime: float, meanMemory: float, totalEnergy: float):
    self.totalTime = totalTime
    self.meanMemory = meanMemory
    self.totalEnergy = totalEnergy
    self.ratioJoulesPerMs = totalEnergy / totalTime

class TestSet:
  def __init__(self, device: str, language: str, algorithm: str):
    self.device = device
    self.language = language
    self.algorithm = algorithm
    self.tests = []
  
  def addTest(self, test):
    self.tests.append(test)
  
  def getMeanFrom(self, attr):
    return np.mean([getattr(test, attr) for test in self.tests])
  
  def getStdFrom(self, attr):
    return np.std([getattr(test, attr) for test in self.tests])
  
  # CV >= 1 indicates a relatively high variation, while a CV < 1 can be considered low.
  def getCVFrom(self, attr):
    return self.getStdFrom(attr) / self.getMeanFrom(attr)