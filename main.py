import parse_brat
import features
import ast
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from vectoriser import Vectoriser
from scipy import sparse

CATS = ['Protein']
ANNOTATION_EXTENTION = ".a1"

# 1 parse brat
print "Parse data files..."
docs = parse_brat.read_data('/home/eliasaa/GENIA/full/', CATS, ANNOTATION_EXTENTION)

# 2 convert to datapoints: a) extract features
print "Extracting features..."
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
print "Setting up classes..."
classes = []
for doc in docs:
  for sentence in doc:
    for word in sentence.annotations:
      if word in CATS:
        classes.append(CATS.index(word)+1)        
      else:
        classes.append(0)

# 3 train
print "Training classifier..."
classifier = svm.LinearSVC()
classifier.fit(data_point_matrix, classes)

# 4 classify
print "Classifying test data..."
confusion_matrix = [[0 for i in xrange(len(CATS)+1)] for j in xrange(len(CATS)+1)]
for i in xrange(1000):
  p = classifier.predict(data_point_matrix[i])
  c = classes[i]
  confusion_matrix[p][c] += 1

for aa in confusion_matrix:
  print ["%05d" % element for element in aa]

scores = []
for klass in xrange(len(CATS)):
  class_name = CATS[klass]
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
