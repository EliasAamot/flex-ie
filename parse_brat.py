"""
    Extracts the annotation data from Brat annotations. Currently entites only.

    Assumes folder consists of documents with .txt and .ann suffices, where
    .txt files contain the raw text, and .ann contain the annotations.

    .txt files are assumed to hold one sentence per line.
    
    Creates list of documents, in which each document is a list of Sentence objects.
"""
import os 
import xml.etree.ElementTree as ET
from sentence import Sentence, Dependency

def read_data(folder, cats, annotation_extention):
    filenames = set([filename[:filename.rfind('.')] for filename in os.listdir(folder)])
    docs = [] 
    for filename in filenames:
        # Read parsed document
        xml_content = ET.parse(folder+filename+".xml")
        xml_sentences = [sentence for sentence in 
            xml_content.getroot().find("document").find("sentences")] 
        sentences = []
        for xml_sentence in xml_sentences:
            sentence = Sentence()
            for token in xml_sentence.find("tokens"):
              sentence.words.append(token.find("word").text)
              sentence.lemmas.append(token.find("lemma").text)
              sentence.pos.append(token.find("POS").text)
              sentence.offsets.append((int(token.find("CharacterOffsetBegin").text),
                int(token.find("CharacterOffsetEnd").text)))
            for dep in xml_sentence.find("dependencies[@type='collapsed-ccprocessed-dependencies']"):
              governor = int(dep.find("governor").attrib["idx"])-1
              dependent = int(dep.find("dependent").attrib["idx"])-1
              dep_type = dep.attrib["type"]
              sentence.dependencies.append(Dependency(dep_type, governor, dependent))
            sentences.append(sentence)
        # Read annotations
        annotated_spans = dict()
        ann_file = open(folder+filename+"."+annotation_extention, 'r')
        for line in ann_file:
            line = line.strip()
            line = line.split()
            # Ignore non entity-categories for now
            if line[0][0] != 'T':
                continue
            # TODO: Generalize categories
            if not line[1] in cats:
                continue
            # Store annotated spans
            indices = (int(line[2]), int(line[3]))
            category = line[1]
            annotated_spans[indices] = category
        ann_file.close()
        # Build sentences with annotation tags
        tagged_sentences = []
        word_start = 0
        for sentence in sentences:
          for word_start, word_end in sentence.offsets:
            for indices, category in annotated_spans.iteritems():
              # Break for optimization
              if word_start >= indices[0] and word_end <= indices[1]:
                sentence.annotations.append(category)
                break
            else:
              sentence.annotations.append(None)
        docs.append(sentences)
    return docs
             
