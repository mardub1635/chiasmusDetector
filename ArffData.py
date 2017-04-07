# -*- coding: utf-8 -*-
import scipy.io.arff as scarff
import numpy as np
class ArffData:
	arffFile=""
	uselessFeat=[]
	def __init__(self, arg1, arg2):
		self.arffFile=arg1#myData.arff
		self.uselessFeat=arg2#[sentFeat, tagAB]
	"""
	Feature selection
	"""


	def indexBadFeat(self,uselessFeat):
		"""
		(self,list)->tuple(list, list)

		calls the arffLoader/converter for the arfFile of the current object.
		Returns the list of features names as a list and the list of useless feqture position
		in the arff file. That keeps track of the useless feature position for later elimination.
		Elimination via pop() the list must be in decrease order
		"@Arff file
		Feat0
		Feat1
		Feat_TagAB
		Feat_TagABCD
		>>>indexBadFeat(self,[Feat2,Feat_TagAB])
		([2,1],[Feat0,Feat_TagABCD])
		"""

		data=scarff.loadarff(self.arffFile)
		indexList=[]#The features are present in a certain order. 
		#Some are useless. Their index is listed for elimination later
		usefulFeat=[]
		i=0
		for featureName in data[1]:

		
			if featureName in uselessFeat:
				indexList.append(i)
			else:
				usefulFeat.append(featureName)

			i+=1
		indexList.reverse()
		return (indexList,usefulFeat)

	def selFeat(self,indexFeat,row):
		"""
		returns the predictor instance cleaned from its useless data/features
		>>>selFeat([0,1,0,0.3333,])
		[0,0.3333]

		"""
		for i in indexFeat:
			row.pop(i)
		return row
	"""
	Open and convert the arff Data file
	"""
	def getX_y(self):#X the predictor variables; y the target variable
		"""
		(self)->list[array, array, int]

		calls the arffLoader/converter for the arfFile of the current object.
		Returns the data in python readable format (array) 
		and the number of true instances (iTrue)
		>>>getX_y()
		[[0,0.333],[1,0.2]],[[1],[0]],1
		"""
		iTrue=0

		indexList=self.indexBadFeat(self.uselessFeat)[0]

		X=[]
		y=[]
		for row in scarff.loadarff(self.arffFile)[0]:
			rowX=self.selFeat(indexList,list(row)[0:-1])

			X.append(rowX)
			
			if row[-1]=='True':
				y.append(1.0)
				iTrue+=1
			else:
				y.append(0.0)
			

		X = np.array(X)

		y = np.array(y)
		return [X,y,iTrue]


	def getX_y_bord(self):#X the predictor variables; y the target variable
		
		"""
		(self)->list[array, array, int]
		More sofisticated version of getX_y
		calls the arffLoader/converter for the arfFile of the current object.
		Returns the data in python readable format (array) 
		and the number of true instances (iTrue)
		>>>getX_y()
		[[0,0.333],[1,0.2]],[[1],[0]],1
		"""
		iTrue=0

		indexList=self.indexBadFeat(self.uselessFeat)[0]

		X=[]
		y=[]
		for row in scarff.loadarff(self.arffFile)[0]:
			#rowX=self.selFeat(indexList,list(row)[0:-1])

			#X.append(rowX)
			
			if row[-1]=='True':
				y.append(1.0)
				iTrue+=1
			elif row[-1]=='Duplicate':
				y.append(2.0)
			elif row[-1]=='Borderline':
				y.append(3.0)
			elif row[-1]=='DuplicateOfBorderline':
				y.append(4.0)
			elif row[-1]=='Unknown':
				y.append(5.0)
			else:
				y.append(0.0)
			

		X = np.array(X)

		y = np.array(y)
		return [X,y,iTrue]

	def getX_y_bord1(self):#X the predictor variables; y the target variable
		
		"""
		(self)->list[array, array, int]
		More sofisticated version of getX_y
		calls the arffLoader/converter for the arfFile of the current object.
		Returns the data in python readable format (array) 
		and the number of true instances (iTrue)
		>>>getX_y()
		[[0,0.333],[1,0.2]],[[1],[0]],1
		"""
		iTrue=0

		indexList=self.indexBadFeat(self.uselessFeat)[0]

		X=[]
		y=[]
		for row in scarff.loadarff(self.arffFile)[0]:
			#rowX=self.selFeat(indexList,list(row)[0:-1])

			#X.append(rowX)
			
			if row[-1]=='True':
				y.append(1.0)
				iTrue+=1
			elif row[-1]=='Borderline':
				y.append(1.0)
				iTrue+=1
			else:
				y.append(0.0)
			

		X = np.array(X)

		y = np.array(y)
		return [X,y,iTrue]