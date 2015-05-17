import parse_brat
import features
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm

CATS = ['Protein']
ANNOTATION_EXTENTION = ".a1"

# 1 parse brat
print "Parse data files..."
docs = parse_brat.read_data('/home/eliasaa/GENIA/subcorpus/', CATS, ANNOTATION_EXTENTION)

# 2 convert to datapoints: a) extract features
print "Extracting features..."
datapoints = []
for doc in docs:
  for sentence in doc:
    datapoints.extend(features.convert_to_feature_vectors(sentence))
vectorizer = DictVectorizer()
feature_points = vectorizer.fit_transform(datapoints).toarray()

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
classifier.fit(feature_points[1000:], classes[1000:])

# 4 classify
print "Classifying test data..."
confusion_matrix = [[0 for i in xrange(len(CATS)+1)] for j in xrange(len(CATS)+1)]
for i in xrange(1000):
  p = classifier.predict(feature_points[i])
  c = classes[i]
  confusion_matrix[p][c] += 1

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

for aa in confusion_matrix:
  print ["%05d" % element for element in aa]
for a, b, c in scores:
  print a, b, c
