# chiasmusDetector
Description:

Software that detects chiasmus (i.e., First shouId be last, last should be first). 

python MainS.py myStanfordParsedFile.xml myOutput.xml

Example:

python MainS.py exampleTrue.xml output.xml

xsltproc annotationDoc.xsl output.xml > userFriendlyOutput.txt

Licence:

If you are running all or part of this code please cite: 

"Marie Dubremetz and Joakim Nivre (2017); Machine Learning for Rhetorical Figure Detection: More Chiasmus with Less Annotation In: Proceedings of the 21st Nordic Conference of Computational Linguistics (NODALIDA 2017)."

Note that the license is like the Stanford CoreNLP: it is the full GPL , which allows many free uses, but not its use in proprietary software which is distributed to others. For distributors of proprietary software, for commercial licensing contact Marie Dubremetz. firstname.lastname@lingfil.uu.se

You may cite the papers related to the version of the parser you use (Stanford CoreNLP) and NLTK or other packages used in the code.
