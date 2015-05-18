"""
    Feature extraction module for NER.

    Planned features:
        - Lemmas
        - POS
        - Dependency chain
    # TODO :  Word embeddings
    # TODO : Find more
"""
from sklearn.feature_extraction import DictVectorizer

# TODO : make this more modular
USE_POS_FEATURES = True
USE_ANN_FEATURES = False
USE_WRD_FEATURES = True
USE_HAS_DEP_FEATURES = True
USE_DEP_LEMMA_FEATURES = False
USE_HAS_GOV_FEATURES = False
USE_GOV_LEMMA_FEATURES = False

"""
    Each feature generator function takes three inputs: 
       - index : the index of the word in the sentence that we are extracting 
           features for.
       - sentence : the Sentence object
       - feature_dict : the dict of features extracted thus far for the word

    Each feature generator should add extra features to the feature_dict, 
    without modifying or reading existing features.
"""
def extract_pos_feature(index, sentence, feature_dict):  
   feature_dict["pos"] = sentence.pos[index] 

def extract_ann_feature(index, sentence, feature_dict):
  a = sentence.annotations[index]
  if a == None:
    a = "None"
  feature_dict["class"] = a

def extract_lemma_feature(index, sentence, feature_dict):
  feature_dict["lemma"] = sentence.lemmas[index] 

def extract_has_dependent_features(index, sentence, feature_dict):
  feature_dict["has_dependency"] = [dep.dep_type for dep in sentence.get_dependencies_of(index)]

def extract_dependent_lemma_features(index, sentence, feature_dict):
  feature_dict["dependency_lemma"] = [dep.dep_type + "-" + sentence.lemma_at(dep.dependent) in sentence.get_dependencies_of(index)]

def extract_has_governor_features(index, sentence, feature_dict):
  deps = [dep.dep_type for dep in sentence.get_governor_of(index)]
  for dep in deps:
    feature_dict["has_governor_" + dep] = True 

def extract_governor_lemma_features(index, sentence, feature_dict):
  deps = [dep for dep in sentence.get_governor_of(index)]
  for dep in deps:
    feature_dict["governor_" + dep.dep_type + "_" + sentence.lemma_at(dep.dependent)] = True

"""
    Main method
"""
 
def convert_to_feature_vectors(sentence):
  feature_vectors = [{} for i in xrange(len(sentence))]
  for i in xrange(len(sentence)):
    if USE_POS_FEATURES:
      extract_pos_feature(i, sentence, feature_vectors[i])
    if USE_ANN_FEATURES:
      extract_ann_feature(i, sentence, feature_vectors[i])
    if USE_WRD_FEATURES:
      extract_lemma_feature(i, sentence, feature_vectors[i])
    if USE_HAS_DEP_FEATURES:
      extract_has_dependent_features(i, sentence, feature_vectors[i])
    if USE_DEP_LEMMA_FEATURES:
      extract_dependent_lemma_features(i, sentence, feature_vectors[i])
    if USE_HAS_GOV_FEATURES:
      extract_has_governor_features(i, sentence, feature_vectors[i])
    if USE_GOV_LEMMA_FEATURES:
      extract_governor_lemma_features(i, sentence, feature_vectors[i])
  return feature_vectors   
