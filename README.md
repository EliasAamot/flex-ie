# FLEXIE: Flexible Pipeline Information Extraction

Machine learning-based information extraction meant based on a flexible pipeline. Intended to be used withcorpora annotated using the Brat rapit annotation tool. Uses scipy-learn.

Can only perform NER at the moment. Will hopefully expand to cover full event extraction by the end of the month.

If you are interested in using this software, feel free to contact me at elias.aamot(在)gmail(点)com.

## Version history:

0.0.1: Somewhat functioning NER extraction system

0.0.2: System now able to deal with large data sets, by writing temporary data to disk.

0.0.3: Implemented basic config-file interface. This will be improved further.

0.0.4: System now supports multiple extraction steps, and features can be specified on a per-step basis.

## Plan

Version 0.1: Minimal Viable Version:
* Full event extraction pipeline, with component customisable through cfg script.
* Reads and writes data from/to Brat format

Possible post MVV plans:
* Intelligent recommendation of ideal pipeline for task
* Intelligent feature selection
* Word embedding based features
* Structural rules

## Short term TODOs:

* Add support for relation extraction.
* Evaluation procedures
* Write output to brat format
* Feature extraction and vectorising seems to have a negative effect on precision and recall. Figure out why, and fix it.
* Add support for aspect extraction (negation etc.)

## Post MVV TODOS:

* Choose between multiclass classification (current approach) or two-part classification: First binary (no tag vs. tag), then multiclass to set actual class.
