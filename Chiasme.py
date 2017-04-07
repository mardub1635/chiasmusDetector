 # -*- coding: utf-8 -*-

from nltk.util import ngrams
from Score import Score

#stats=open("#stats",u'w')

class Chiasme:
	nodeA=""
	nodeB=""
	iA=0
	iD=0#iD ou position de A' dans la figure A B B' A' à l'intérieur du texte
	text=""
	iB=0
	iC=0
	stopfile=open("StopWords","r")#file with the stopwords list
	stoplist=stopfile.read().splitlines()[1:]
	stopfile.close()

	weightfile=open("weights","r")
	
	weightDico={}
	for line in  weightfile.read().splitlines()[1:]:
		limit=line.index(":")
		
		weight=float(line[0:limit])
		name=line[limit+1:line.index("/")]
		weightDico[name]=weight
	weightfile.close()
	parseFeats={}
	for w in weightDico:
		if 'Dep' in w or 'Gov' in w:
			parseFeats[w]=weightDico[w]
	


	parseList=[]
	hardPuncts=[":",".",";","*","?","!",")","(","-lrb-","-rrb-","\""]
	def __init__(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9,arg10,arg11):
		self.nodeA=arg1
		self.nodeB=arg2
		self.nodeC=arg3
		self.nodeD=arg4
		self.iA=arg5
		self.iB=arg6
		self.iC=arg7
		self.iD=arg8
		self.tokens=arg9
		self.lemmLwLst=arg10
		self.sourcefile=arg11
	def extract(self):
		"""(Chiasme)->String
		
		given the words position and the all text returns the part of the text containing the chiasmus
		
		>>>node555, node558, node564,node580,555,558,564,580,['Blabla', 'and', 'Portos', 'said', ':' all' ,'for', 'one', ',' 'one',  'for', 'all', '!', 'Then', 'Aramis', 'opens', 'a', 'good', 'bottle', 'of', 'wine', 'blablabla'
		"all for one , one  for all"
		"""

		sentlst=self.tokens[self.iA:self.iD+1]
		sent=" ".join(sentlst)#this is the chiasmus as a string
		return sent
		
		
	def extractContext(self):
		"""
		(Chiasme)->String
		
		given the words position and the all text returns the part of the text containing the chiasmus+ a little bit of context (5 words extra)
		
		>>>one,all,125,128,"Blabla and Portos said : all for one , one  for all ! Then Aramis opens a good bottle of wine blablabla ", 130,132,[the, all, i, a, an]
		"and Portos said : all for one , one  for all ! Then Aramis opens a good bottle"
		"""
		#textEspace = self.text
		#liste=textEspace#.split()
		sentlst=[token for token in self.tokens[self.iA-5:self.iD+5]]

		
		sent=" ".join(sentlst)#this is the chiasmus as a string
		return sent
#		for threeList in self.text[self.iA-5:self.iD+5]:
#			sentContextlst.append(threeList[0])
#		sentContext=" ".join(sentContextlst)
#		return sentContext
	def extractSentence(self):
		"""
		(Chiasme)->list
		given the words position returns the part of the sentences containing the chiasmus
		"""
		sentenceA=self.nodeA.getparent().getparent().getparent().attrib['id']
		sentenceD=self.nodeD.getparent().getparent().getparent().attrib['id']
		sentenceB=self.nodeB.getparent().getparent().getparent().attrib['id']
		sentenceC=self.nodeC.getparent().getparent().getparent().attrib['id']
		self.sourcefile
		
		#beg=self.nodeA.xpath("../../token[1]/CharacterOffsetBegin")[0].text
		sbeg=self.nodeA.getparent().getparent().getchildren()[0].getchildren()[2].text
		#end=self.nodeD.xpath("../../token[last()]/CharacterOffsetEnd")[0].text
		send=self.nodeD.getparent().getparent().getchildren()[-1].getchildren()[3].text
		
		beg=int(sbeg)
		end=int(send)
		sents=self.sourcefile[beg:end]
		return [sents,[sentenceA,sentenceB,sentenceC,sentenceD],sbeg,send]
				
			
		
	def getFeat(self,sentID):
		"""
		(Chiasme)->list
		
		Given a chiamus returns a list of features values
		>>>one,all,125,128,"Blabla and Portos said : all for one , one  for all ! Then Aramis opens a good bottle of wine blablabla ", 130,132,[the, all, i, a, an]
		[5,0,2,3,5,5,47.6,59]
		"""
#		sentlst=[]

#		for trio in self.text[self.iA:self.iD+1]:
#			sentlst.append(trio[0]) 

		
		softPuncts=","
		conjCoords=["and","as","because","for","yet","nor","so","or","but"]
		
		#======================True/False Feature tests=====================
		punctScore=0
		softPunctScore=0
		isInStopListA=0
		isInStopListB=0
		diffSize=0
		sameStringBetween=0
		distance=0
		hasConjBC=0
		centralPunctScore=0
		simScore=0.0
		relativSimScore=0.0
#		hasNo=0
#		hasNot=0
#		hasNever=0
#		hasNothing=0
		hasIntoTo=0
		bigramScore=0
		trigramScore=0
		simContCent=0
		hasMainsRep=-2
		sameSentAB_CD=0
		sameSentBC=0
		sameDepAC_Main=0
		sameDepAC_All=0
		sameDepBD_Main=0
		sameDepBD_All=0
		govAllIfDepMainAC=0#Activated only if Dep is >0
		govAllIfDepMainBD=0
		govMainIfDepMainAC=0
		govMainIfDepMainBD=0
		sameDepAB_Main=0
		sameDepCD_Main=0
		sameGovAC_All=0
		sameGovAC_Main=0
		sameGovBD_All=0
		sameGovBD_Main=0
		hasNeg=0
		sameTagAD=0
		sameTagBC=0
		sameTagAC=0
		sameTagBD=0
		sameTagABCD_ext=0
		sameTagABCD=0
		sameDepAD_Main=0
		sameDepBC_Main=0

		noPunctAllowed=self.lemmLwLst[self.iA+1:self.iB]+self.lemmLwLst[self.iC+1:self.iD]
		for punct in self.hardPuncts:#loop for checking the position of the ponctuations
			punctScore+=noPunctAllowed.count(punct)
		
		softPunctScore=noPunctAllowed.count(softPuncts)
		motaLower=self.lemmLwLst[self.iA]
		motbLower=self.lemmLwLst[self.iB]
		if motaLower in self.stoplist: #Filters -> THE cat live with a cat but THE dog
			isInStopListA=1
		if motbLower in self.stoplist:#Filters inner stopwords -> Max likes THE cat and THE dog but my cat does not like Max.
			isInStopListB=1	
#			
		diffSize=len(self.tokens[self.iA:self.iB])-len(self.tokens[self.iC:self.iD])
		diffSize=abs(diffSize)
		
		if self.tokens[self.iA+1:self.iB]==self.tokens[self.iC+1:self.iD]:
			sameStringBetween=1
		
		distance=self.iC-self.iB
		
		centerPart=self.lemmLwLst[self.iB+1:self.iC]
		for punct in self.hardPuncts:#loop for checking the position of the ponctuations
			centralPunctScore+=centerPart.count(punct)


		for conj in conjCoords:
			if conj in centerPart:
				hasConjBC=1
		

		lemmsAtoB=self.lemmLwLst[self.iA+1:self.iB]
		lemmsCtoD=self.lemmLwLst[self.iC+1:self.iD]
		simScore=float(len(set(lemmsAtoB).intersection(lemmsCtoD)))
		
		lengthAtoBCtoD=float(self.iB-self.iA+self.iD-self.iC)
		relativSimScore=simScore/lengthAtoBCtoD
		
		#***Negations dectection in chiasm AND context***
		lemmWthContlst=self.lemmLwLst[self.iA-5:self.iD+5]


		if "no" in lemmWthContlst or "not" in lemmWthContlst or "never" in lemmWthContlst or  "nothing" in lemmWthContlst:
			hasNeg=1
		
		if "to" in lemmsAtoB and "to" in lemmsCtoD or "into" in lemmsAtoB and "into" in lemmsCtoD or "from" in lemmWthContlst and "to" in lemmWthContlst and lemmWthContlst.index('from')<lemmWthContlst.index('to'):
			hasIntoTo=1
#		
		bigrams1=ngrams(self.lemmLwLst[self.iA:self.iB+1],2)
		bigrams2=ngrams(self.lemmLwLst[self.iC:self.iD+1],2)
		bigramScore=len(set(bigrams1).intersection(bigrams2))
#		
		trigrams1=ngrams(self.lemmLwLst[self.iA:self.iB+1],3)
		trigrams2=ngrams(self.lemmLwLst[self.iC:self.iD+1],3)
		trigramScore=len(set(trigrams1).intersection(trigrams2))
#		
		contextLeft=self.lemmLwLst[self.iA-5:self.iA]
		simContCent=len(set(contextLeft).intersection(centerPart))
		
		hasMainsRep+=self.lemmLwLst[self.iA+1:self.iD].count(motaLower)+self.lemmLwLst[self.iA+1:self.iD].count(motbLower)
		

		##***Starting loop to detect similar syntactic roles***
		#**A and C as governors**
		def scoreRole(nodeX,nodeY):
			"""
			(node,node)->int 
			returns the score of role similarity"""
			#idX=nodeX.xpath("../@id")[0]
			idX=nodeX.getparent().attrib['id']
			#idY=nodeY.xpath("../@id")[0]
			idY=nodeY.getparent().attrib['id']
			#Dictionary of the number of deptype
			sameRole={'dependent':{"main":0,"det":0,"case":0,"mark":0,"aux":0},'governor':{"main":0,"det":0,"case":0,"mark":0,"aux":0}}
			depsX=nodeX.getparent().getparent().getparent().getchildren()[4].getchildren()#depsX=nodeX.xpath("../../../dependencies[3]/dep")==collapsed cc processed dependencies
			depsY=nodeY.getparent().getparent().getparent().getchildren()[4].getchildren()
			i=-1
			for role in ["governor","dependent"]:
				i+=1
				
				for node1 in depsX:
					
					if node1.getchildren()[i].attrib['idx']==idX:
						
					#if node1.xpath("./"+role+"/@idx")==idX:
						
						for node2 in depsY:
							if node2.getchildren()[i].attrib['idx']==idY:
								
							#if node2.xpath("./"+role+"/@idx")==idY:
								depTypeX=node1.attrib['type']
								
								if depTypeX!='dep' and depTypeX!='case' and depTypeX!='det' and depTypeX!='aux' and depTypeX!='mark':
									depTypeY=node2.attrib['type']
									
									if depTypeX==depTypeY:
										sameRole[role]["main"]+=1
										#stats.write(role+' #'+depTypeX+" ")
								elif depTypeX=='det':
									depTypeY=node2.attrib['type']
									if depTypeX==depTypeY:
										sameRole[role]["det"]+=1
										#stats.write(role+' #'+depTypeX+" ")
								elif depTypeX=='case':
									depTypeY=node2.attrib['type']
									if depTypeX==depTypeY:
										sameRole[role]["case"]+=1
										#stats.write(role+' #'+depTypeX+" ")
								elif depTypeX=='aux':
									depTypeY=node2.attrib['type']
									if depTypeX==depTypeY:
										sameRole[role]["aux"]+=1	
										#stats.write(role+' #'+depTypeX+" ")
								elif depTypeX=='mark':
									depTypeY=node2.attrib['type']
									if depTypeX==depTypeY:
										sameRole[role]["mark"]+=1
										#stats.write(role+' #'+depTypeX+" ")
								#elif depTypeX=='Dep':
										#stats.write(role+' #'+depTypeX+" ")

#			
			
			return sameRole 
		#stats.write("\nRole AC:::")
		def isInteresting(letters):
			interess=False#turns off the feature extraction if the weight=0
			#interess=True#Turns on all feature extraction whatever value they have (Warning very time consuming!)#TODO:remove:comment/uncomment if arff generation
			for w in self.parseFeats:
				if letters in w and self.parseFeats[w]!=0.0:	
					interess=True
			return interess
		

		if isInteresting('AC'):
			sameRoleAC=scoreRole(self.nodeA,self.nodeC)	
		else:
			
			sameRoleAC={'dependent':{"main":0,"det":0,"case":0,"mark":0,"aux":0},'governor':{"main":0,"det":0,"case":0,"mark":0,"aux":0}}
		
		#stats.write("\nRole BD:::")
		if isInteresting('BD'):
			sameRoleBD=scoreRole(self.nodeB,self.nodeD)
		else:
			sameRoleBD={'dependent':{"main":0,"det":0,"case":0,"mark":0,"aux":0},'governor':{"main":0,"det":0,"case":0,"mark":0,"aux":0}}
		#stats.write("\nRole !AB!:::")

		if isInteresting('AB'):
			sameRoleAB=scoreRole(self.nodeA,self.nodeB)
		else:
			sameRoleAB={'dependent':{"main":0,"det":0,"case":0,"mark":0,"aux":0},'governor':{"main":0,"det":0,"case":0,"mark":0,"aux":0}}

		if isInteresting('CD'):

		#stats.write("\nRole !CD!:::")
			sameRoleCD=scoreRole(self.nodeC,self.nodeD)
		else:
			sameRoleCD={'dependent':{"main":0,"det":0,"case":0,"mark":0,"aux":0},'governor':{"main":0,"det":0,"case":0,"mark":0,"aux":0}}

		
		#sentID=self.extractSentence()[1]
		if sentID[0]==sentID[1]:#A is in the same sentence as B
			sameSentAB_CD+=1
		if sentID[2]==sentID[3]:#C is in the same sentence as D
			sameSentAB_CD+=1
		if sentID[1]==sentID[2]:#B is in the same sentence as C
			sameSentBC=1
		#sameRoleAC=scoreRole(self.nodeA,self.nodeC)
		#sameRoleBD=scoreRole(self.nodeB,self.nodeD)
		
		sameDepAC_Main=sameRoleAC["dependent"]["main"]
		# sameDepAC_MainDetCase=sameRoleAC["dependent"]["main"]+sameRoleAC["dependent"]["det"]+sameRoleAC["dependent"]["case"]
		#sameDepAC_MainMarkAux=sameRoleAC["dependent"]["main"]+sameRoleAC["dependent"]["aux"]+sameRoleAC["dependent"]["mark"]
		sameDepAC_All=sameRoleAC["dependent"]["main"]+sameRoleAC["dependent"]["det"]+sameRoleAC["dependent"]["case"]+sameRoleAC["dependent"]["aux"]+sameRoleAC["dependent"]["mark"]
		
		sameDepBD_Main=sameRoleBD["dependent"]["main"]
		# sameDepBD_MainDetCase=sameRoleBD["dependent"]["main"]+sameRoleBD["dependent"]["det"]+sameRoleBD["dependent"]["case"]
		# sameDepBD_MainMarkAux=sameRoleBD["dependent"]["main"]+sameRoleBD["dependent"]["aux"]+sameRoleBD["dependent"]["mark"]
		sameDepBD_All=sameRoleBD["dependent"]["main"]+sameRoleBD["dependent"]["det"]+sameRoleBD["dependent"]["case"]+sameRoleBD["dependent"]["aux"]+sameRoleBD["dependent"]["mark"]
		
		sameGovAC_Main=sameRoleAC["governor"]["main"]
		sameGovAC_All=sameRoleAC["governor"]["main"]+sameRoleAC["governor"]["det"]+sameRoleAC["governor"]["case"]+sameRoleAC["governor"]["aux"]+sameRoleAC["governor"]["mark"]
		sameGovBD_Main=sameRoleBD["governor"]["main"]
		sameGovBD_All=sameRoleBD["governor"]["main"]+sameRoleBD["governor"]["det"]+sameRoleBD["governor"]["case"]+sameRoleBD["governor"]["aux"]+sameRoleBD["governor"]["mark"]


		sameDepAB_Main=sameRoleAB["dependent"]["main"]
		sameDepCD_Main=sameRoleCD["dependent"]["main"]
		


		if sameDepAC_Main>0:
			govAllIfDepMainAC=sameRoleAC["governor"]["main"]+sameRoleAC["governor"]["det"]+sameRoleAC["governor"]["case"]+sameRoleAC["governor"]["aux"]+sameRoleAC["governor"]["mark"]
			govMainIfDepMainAC=sameRoleAC["governor"]["main"]
		if sameDepBD_Main>0:
			govAllIfDepMainBD=sameRoleBD["governor"]["main"]+sameRoleBD["governor"]["det"]+sameRoleBD["governor"]["case"]+sameRoleBD["governor"]["aux"]+sameRoleBD["governor"]["mark"]
			govMainIfDepMainBD=sameRoleBD["governor"]["main"]

		tagA=self.nodeA.getnext().getnext().getnext().text
		tagB=self.nodeB.getnext().getnext().getnext().text
		tagC=self.nodeC.getnext().getnext().getnext().text
		tagD=self.nodeD.getnext().getnext().getnext().text
		

		if tagA==tagD:
			sameTagAD=1
		if tagB==tagC:
			sameTagBC=1
		
		if tagA==tagC:
			sameTagAC=1
		if tagB==tagD:
			sameTagBD=1

		if tagA==tagB==tagC==tagD:
			sameTagABCD=1
			

		if tagA[:1]==tagB[:1]==tagC[:1]==tagD[:1]:
			sameTagABCD_ext=1
			
		if isInteresting('AD'):
			sameRoleAD=scoreRole(self.nodeA,self.nodeD)
		else:
			sameRoleAD={'dependent':{"main":0,"det":0,"case":0,"mark":0,"aux":0},'governor':{"main":0,"det":0,"case":0,"mark":0,"aux":0}}
			
		if isInteresting('BC'):
			sameRoleBC=scoreRole(self.nodeB,self.nodeC)	
		else:
			sameRoleBC={'dependent':{"main":0,"det":0,"case":0,"mark":0,"aux":0},'governor':{"main":0,"det":0,"case":0,"mark":0,"aux":0}}
		sameDepAD_Main=sameRoleAD["dependent"]["main"]
		sameDepBC_Main=sameRoleBC["dependent"]["main"]

		return [punctScore,softPunctScore,isInStopListA,isInStopListB,
		diffSize,
		sameStringBetween,distance,centralPunctScore,hasConjBC,
		simScore,relativSimScore,hasIntoTo,bigramScore,trigramScore,simContCent,
		hasMainsRep,sameSentAB_CD,sameSentBC,sameDepAC_Main,sameDepAC_All,
		sameDepBD_Main,sameDepBD_All,govAllIfDepMainAC, govAllIfDepMainBD,govMainIfDepMainAC,govMainIfDepMainBD,sameDepAB_Main,sameDepCD_Main,
		sameGovAC_All,sameGovAC_Main,sameGovBD_All,sameGovBD_Main,hasNeg,sameTagAD,sameTagBC,sameTagAC,sameTagBD,sameTagABCD,sameTagABCD_ext,sameDepAD_Main,sameDepBC_Main]
	def rank(self,sentID):
		"""(Chiasme)->Float
#		
#		given a chiasmus and its words returns a score of probability
#		
#		>>>one,all,125,128,"Blabla and Portos said : all for one , one  for all ! Then Aramis opens a good bottle of wine blablabla ", 130,132,[the, all, i, a, an]
#		42.0
#		"""


		score=0
		featList=self.getFeat(sentID)
		score=Score().scoreFeat(featList)
		return (score,featList)#+10		
