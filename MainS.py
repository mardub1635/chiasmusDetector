#!/usr/bin/env python
# -*- coding: utf-8 -*-



#import xml.etree.ElementTree as ET
import sys
import re
from Chiasme import Chiasme
from lxml import etree
#from lxml.builder import E
#""""
#(xml) -> lemmas
#	
#""""
listInput=sys.argv
corpus=listInput[1]#Corpus file e.g. 'Bible.txt.xml'
source=corpus[:-4]
sortie=listInput[2]
g=open(sortie,u'w')
stopfile=open("StopWords","r")#file with the stopwords list
stoplist=stopfile.read().splitlines()[1:]
stopfile.close()

sourcefile=open(source,"r").read().decode('utf8')

#allXml=ET.parse(corpus)
#root=allXml.getroot()
#print root
#lemmas=root.iter('lemma')
##print "ceci est mon element",lemmas[55].text#findall('..')
#	
#	

#lemmas=root.findall("./document/sentences/sentence/tokens/token/lemma")
#print lemmas[55].find("..")
parser = etree.XMLParser(encoding='utf-8')
allXml=etree.parse(corpus, parser)
lemms=allXml.findall('.//lemma')
tokens=allXml.findall('.//word')
regex=re.compile("^[A-Za-z\'-]+$")#For other languages: "^[A-Za-zàùéèçâîûêôëïöäœ\'-]+$"
regexNO=re.compile("^[\'-]+$")
#================Absurd func================

def absurd(word):#Caution:we transform -100 into an hard constraint
	if regex.match(word)==None:
		return True
	if regexNO.match(word)!=None:
		return True
	if word=="-" or word=="'" or word=="''" or word=="-rrb-" or word=="-lrb-" or word=="-rsb-" or word=="-lsb-":
		return True
	return False
lemmLwLst = [etree.tostring(lemm,method="text",encoding="utf8").lower()[:-13] for lemm in lemms]

tokenList = [token.text for token in tokens]

def absurd2(word1,word2):
	if word1==word2:
		return True
	return False

#================Main loop================
iRevers=0#a count of the total reversion in the text
iA=0#"i" means the position number of the word in the text e.g. in the text "The cat is blue" if motA is the word 'cat' iA==1
chiasmaList={}#dictionary will contain every chiasm extracted indexed by there ranking score, e.g.{99,999:trust in money, money in trust, 5,5:One for all all for one}
print "Main loop starting"	
for motA in lemms:
	motALower=lemmLwLst[iA]
	if absurd(motALower):
		iA=iA+1
		continue
	iD=iA+1
	
	
	for motD in lemms[iA+1:iA+30]:#this loop check 30 words after word A in order to catch an aidentical pair A A' (or motA motD pair)
			
			if motALower==lemmLwLst[iD]:#motD[2].lower():				
				
				iB=iA+1#iB is the position of motB
				
				for motB in lemms[iA+1:iD-1]:#only up to D-2
					motBLower=lemmLwLst[iB]
					if absurd(motBLower):
						iB=iB+1
						continue
					
					
					if absurd2(motALower,motBLower):
						iB=iB+1
						continue
					iC=iB+1

					for motC in lemms[iB+1:iD]:#Do not forget that the end limit is NOT inclusive so NO iD-1
						
						if motBLower!=lemmLwLst[iC]:#motC[2].lower():
							
							iC=iC+1
						else:								
							iRevers+=1

							
							chiasmus = Chiasme(motA,motB,motC,motD,iA,iB,iC,iD,tokenList,lemmLwLst,sourcefile)
							
							chiasmusSent=chiasmus.extractSentence()
							chiasmusRankFeat=chiasmus.rank(chiasmusSent[1])
							chiasmusScore=chiasmusRankFeat[0]
							
							
							if chiasmusScore>=-100: 
								chiasmusRawFeat=chiasmusRankFeat[1]
								chiasmusTxt = chiasmus.extract()
								
								chiasmusContxt=chiasmus.extractContext()
								begA=motA.getnext()
								endA=motA.getnext().getnext()
								begB=motB.getnext()
								endB=motB.getnext().getnext()
								begC=motC.getnext()
								endC=motC.getnext().getnext()
								begD=motD.getnext()
								endD=motD.getnext().getnext()
								
								if chiasmusScore in chiasmaList:
									
									chiasmaList[chiasmusScore].append([chiasmusTxt,chiasmusSent[0],chiasmusSent[1],begA,endA,begB,endB,begC,endC,begD,endD,chiasmusContxt,chiasmusRawFeat,chiasmusSent[2],chiasmusSent[3]])	
								else:
									
									
									
									chiasmaList[chiasmusScore] = [[chiasmusTxt]+[chiasmusSent[0]]+[chiasmusSent[1]]+[begA]+[endA]+[begB]+[endB]+[begC]+[endC]+[begD]+[endD]+[chiasmusContxt]+[chiasmusRawFeat]+[chiasmusSent[2]]+[chiasmusSent[3]]]
									
							
							iC=iC+1			
					iB=iB+1
			iD=iD+1
			
	iA=iA+1	


print "Chiasmi extraction done. Start XML tree"
root = etree.Element("output")
#child2 = etree.SubElement(root, "tie").attrib["t"]="taupe"
featureParent=etree.SubElement(root,"weights")

weightfile=open("weights","r")
weightLines=weightfile.read().splitlines()
weightList=[float(weight[0:weight.index(":")]) for weight in weightLines[1:]]
featureList=[feat[feat.index(":")+1:feat.index("/")] for feat in weightLines[1:]]
weightfile.close()


#featureList=weightLines[1].split(",")

for i in range(len(featureList)):
	weight=etree.SubElement(featureParent,'feat')
	weight.attrib['weight']=str(weightList[i])
	weight.text=str(featureList[i])
iRank=1
iPosition=1
ties=etree.SubElement(root,'ties')

for key in sorted(chiasmaList.keys(), reverse=True):
	if iPosition<=3000:#TODO:removeme: Change size of output (avoit big files)
		tie = etree.SubElement(ties,'tie')
		tie.attrib['rank']=str(iPosition)
		tie.attrib['id']=str(iRank)
		tie.attrib['score']=str(key)
		iRank+=1
	
		for result in chiasmaList[key]:
			if "StOp" in result[0]:
				continue
				
			chi=etree.SubElement(tie,"chi")
			chi.attrib['pos']=str(iPosition)
			wA=etree.SubElement(chi,'wA')
			wB=etree.SubElement(chi,'wB')
			wA.attrib['begA']=result[3].text
			wA.attrib['endA']=result[4].text
			wB.attrib['begB']=result[5].text
			wB.attrib['endB']=result[6].text
			wB.attrib['begC']=result[7].text
			wB.attrib['endC']=result[8].text
			wA.attrib['begD']=result[9].text
			wA.attrib['endD']=result[10].text
			wA.text=result[3].getprevious().text
			wB.text=result[5].getprevious().text
			extract=etree.SubElement(chi,"extract")

			extract.text=result[0]
			cont=etree.SubElement(chi,"cont")
			cont.text=result[11]
			sent=etree.SubElement(chi,"sent")
			#print result[1].decode('utf8')
			sent.text=result[1]#.decode('utf8')
		
			sent.attrib['idA']=result[2][0]
			sent.attrib['idB']=result[2][1]
			sent.attrib['idC']=result[2][2]
			sent.attrib['idD']=result[2][3]
			sent.attrib['ibeg']=str(result[13])
			sent.attrib['iend']=str(result[14])

			featSpec=etree.SubElement(chi,"featSpec")
			featSpec.text=str(result[12])
			iPosition+=1
print "Now will print XML file"
g.write(etree.tostring(root, pretty_print=True,encoding="utf8"))
g.close()
print "Done"
print iRevers," inversions were present in your text"
