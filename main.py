import parse_brat
import features
import ast
import sys
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from vectoriser import Vectoriser
from scipy import sparse

def load_configs(filename):
  f = open(filename)
  j = json.load(f)
  f.close()
  return j

def run_component(data_folder, categories, annotation_extention):
  print "Parsing data files..."
  docs = parse_brat.read_data(data_folder, categories, annotation_extention)
  print "Extracting features..."
  classes, features = extract_features(docs, categories)
  print "Training model..."
  model = train_model(classes, features)
  print "Scoring model..."
  score_model(model, classes, features, categories)
  
# Docs is a list of documents, in which each document is a list of sentences
def extract_features(docs, categories):
  # a) extract features
  with open('tmp_features.tmp', 'w') as tmp_file:
    for doc in docs:
      for sentence in doc:
        feature_dict_list = features.convert_to_feature_vectors(sentence)
        for feature_dict in feature_dict_list:
          tmp_file.write(str(feature_dict)+'\n')

  # b) Build Vectoriser
  vectoriser = Vectoriser()
  with open('tmp_features.tmp', 'r') as tmp_file:
    for line in tmp_file:
      feature_dict = ast.literal_eval(line)
      vectoriser.add_features(feature_dict)
  vectoriser.compile()

  # c) Convert to data point matrix
  with open('tmp_features.tmp', 'r') as tmp_file:
    data_point_vectors = []
    for line in tmp_file:
      feature_dict = ast.literal_eval(line)
      data_point_vectors.append(vectoriser.transform(feature_dict))
  data_point_matrix = sparse.vstack(data_point_vectors, format="csr")

  # b) find the answers 
  classes = []
  for doc in docs:
    for sentence in doc:
      for annotation_class in sentence.annotations:
        if annotation_class in categories:
          classes.append(categories.index(annotation_class)+1)        
        else:
          classes.append(0)

  return classes, data_point_matrix

def train_model(classes, features):
  classifier = svm.LinearSVC()
  return classifier.fit(features, classes)

def score_model(model, classes, features, categories):
  confusion_matrix = [[0 for i in xrange(len(categories)+1)] for j in xrange(len(categories)+1)]
  for i in xrange(len(classes)):
    p = model.predict(features[i])
    c = classes[i]
    confusion_matrix[p][c] += 1

  for aa in confusion_matrix:
    print ["%05d" % element for element in aa]

  scores = []
  for klass in xrange(len(categories)):
    class_name = categories[klass]
    class_index = klass+1
    false_positives = 0
    false_negatives = 0
    true_positives = confusion_matrix[class_index][class_index]
    for i in xrange(len(confusion_matrix)):
      if i != class_index:
        false_positives += confusion_matrix[class_index][i]
        false_negatives += confusion_matrix[i][class_index]
    precision = float(true_positives) / (true_positives + false_positives)
    recall = float(true_positives) / (true_positives + false_negatives)
    scores.append((class_name, precision, recall))

  for a, b, c in scores:
    print a, b, c
 

if __name__=="__main__":
    settings_file = sys.argv[-1]
    cfg = load_configs(settings_file)
    run_component(cfg['data']['folder'],
             cfg['component']['categories'],
             cfg['data']['annotation_file_format'])
    exit()
