"""
  Custom vectoriser, similar to sklearn.feature_extraction.DictVectorizer, but
  adapted to our purposes; needed to stream large data sets.

  Usage: Call add_features() with the feature_dict of each data point, followed
  by compile() when all data points have been added. Then call transform() for
  each feature.
"""
import collections
from scipy.sparse import dok_matrix
import numpy as np

class Vectoriser:

  def __init__(self):
    self.features = collections.defaultdict(list)
    self.compiled = False
    self.vector_length = -1

  def add_features(self, feature_dict):
    if self.compiled:
       raise Exception("Cannot add features to a compiled Vectoriser!")
    for feature, value in feature_dict.iteritems():
      self.features[feature].extend(value)     

  def compile(self):
    self.compiled = True
    indexed_features = {}
    next_index = 0
    for feature, values in self.features.iteritems():
      value_dict = {}
      for value in values:  
        value_dict[value] = next_index
        next_index += 1
      indexed_features[feature] = value_dict
    self.features = indexed_features
    self.vector_length = next_index

  def transform(self, feature_dict):
    vector = dok_matrix((1, self.vector_length), dtype=np.float64)
    if not self.compiled:
      raise Exception("Compile Vectoriser first, then run transfrom!")
    for feature, values in feature_dict.iteritems():
      values_list = []
      values_list.extend(values) 
      for value in values_list:
        index = self.features[feature][value]
        vector[0, index] = 1
    return vector
