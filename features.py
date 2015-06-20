"""
    Feature extraction module for NER.

    Current features:
        - POS of word
        - Lemma of word
        - Annotation of word (sanity check feature)
        - Dependency type to governor
        - Dependency type + lemma for governor
        - Class of governor
        - Dependenct type for dependent
        - Dependency type + lemma for dependent
        - Class + dependency type of dependent

    Planned features:
    # TODO :  Word embeddings
    # TODO : Find more
"""
from sklearn.feature_extraction import DictVectorizer

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
   feature_dict["pos"] = [sentence.pos[index]]

def extract_ann_feature(index, sentence, feature_dict):
  a = sentence.annotations[index]
  if a == None:
    a = "None"
  feature_dict["class"] = [a]

def extract_lemma_feature(index, sentence, feature_dict):
  feature_dict["lemma"] = [sentence.lemmas[index]]

def extract_has_dependent_features(index, sentence, feature_dict):
  feature_dict["has_dependency"] = [dep.dep_type for dep in sentence.get_dependencies_of(index)]

def extract_dependent_lemma_features(index, sentence, feature_dict):
  feature_dict["dependency_lemma"] = [dep.dep_type + "-" + sentence.lemma_at(dep.dependent) in sentence.get_dependencies_of(index)]

def extract_has_governor_features(index, sentence, feature_dict):
  deps = [dep.dep_type for dep in sentence.get_governor_of(index)]
  for dep in deps:
    feature_dict["has_governor_" + dep] = [True] 

def extract_governor_lemma_features(index, sentence, feature_dict):
  deps = [dep for dep in sentence.get_governor_of(index)]
  for dep in deps:
    feature_dict["governor_" + dep.dep_type + "_" + sentence.lemma_at(dep.governor)] = [True]

def extract_governor_class_features(index, sentence, feature_dict):
  deps = [dep for dep in sentence.get_governor_of(index)]
  for dep in deps:
    feature_dict["governor_class"] = [sentence.class_at(dep.governor)] 

def extract_dependent_class_features(index, sentence, feature_dict):
  deps = [dep for dep in sentence.get_dependencies_of(index)]
  for dep in deps:
    feature_dict["dependency_" + dep.dep_type] = [sentence.class_at(dep.dependent)] 

"""
    Main method
"""
 
def convert_to_feature_vectors(sentence, features_to_use):
  feature_vectors = [{} for i in xrange(len(sentence))]
  for i in xrange(len(sentence)):
    for feature_to_use in features_to_use:
      if feature_to_use == "pos":
        extract_pos_feature(i, sentence, feature_vectors[i])
      elif feature_to_use == "ann":
        extract_ann_feature(i, sentence, feature_vectors[i])
      elif feature_to_use == "lemma":
        extract_lemma_feature(i, sentence, feature_vectors[i])
      elif feature_to_use == "dependent":
        extract_has_dependent_features(i, sentence, feature_vectors[i])
      elif feature_to_use == "dependent_lemma":
        extract_dependent_lemma_features(i, sentence, feature_vectors[i])
      elif feature_to_use == "dependent_class":
        extract_dependent_class_features(i, sentence, feature_vectors[i])
      elif feature_to_use == "governor":
        extract_has_governor_features(i, sentence, feature_vectors[i])
      elif feature_to_use == "governor_lemma":
        extract_governor_lemma_features(i, sentence, feature_vectors[i])
      elif feature_to_use == "governor_class":
        extract_governor_class_features(i, sentence, feature_vectors[i])
      else:
        raise Exception("Feature " + feature_to_use + " is not a valid feature type. Check your config file!")
  return feature_vectors   
