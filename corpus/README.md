
# Corpus

## Description:

The following files:

- annotated0t16M_i_0t16J.xml
- annotated16t24M_i_16t24J.xml

are the list of chiasmus annotated by both Marie Dubremetz and Joakim Nivre. Taking into account the intersection of what both of them agreed, this means if both of them said True the chiasmus was True, if one said True and the other said False (or borderline etc.), then it was False (or borderline etc.). The first one is used for training the second one for test.

I add the following files:

 - EuroSv0to160000.txt 
 - EuroSv160001to240000.txt

which are the corresponding parts of the europarl english version (swedish to english part) that I used for the experiments. The first one is the training part the second is the test part.

The xml files above use the characters offsets data given by the stanford parser. For the xml files to make more sense, you must parse the *.txt files. On my computer I used the following command, please adapt the variables and path to yours:

    java8 -cp stanford-corenlp-3.5.2.jar:stanford-corenlp-3.5.2-models.jar:xom.jar:joda-time.jar:jollyday.jar:ejml-3.5.2.jar -Xmx60g edu.stanford.nlp.pipeline.StanfordCoreNLP -parse.lenmax 200 -annotators tokenize,ssplit,pos,lemma,parse -outputDirectory 60gMaxLen/ -file myFile

