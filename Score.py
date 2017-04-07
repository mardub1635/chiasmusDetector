 # -*- coding: utf-8 -*-

from sklearn import linear_model
from sklearn.metrics import confusion_matrix
import numpy as np
import sys
import dill

import scipy.io.arff as scarff

from sklearn import cross_validation
from sklearn import metrics

from ArffData import ArffData
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedShuffleSplit
from scipy import stats



class Score:
	"""
	Load model
	"""
	print dill.load( open( "model.pkl", "rb" ) )
	clf=dill.load( open( "model.pkl", "rb" ) )['model']
	#y_scores=runModel(X,X,y,y,clf,None)
	print "Model Weights:"
	weightfile=open("weights","r")
	
	
	weightList=[float(weight[0:weight.index(":")]) for weight in weightfile.read().splitlines()[1:]]
	weightfile=open("weights","r")
	weightLines=weightfile.read().splitlines()
	#print weightList
	#print weightLines
	featureList=[feat[feat.index(":")+1:feat.index("/")] for feat in weightLines[1:]]
	#print featureList
	weightfile.close()
	def indexBadFeat(self,weightList,featureList):
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

		#data=scarff.loadarff(self.arffFile)
		indexList=[]#The features are present in a certain order. 
		#Some are useless. Their index is listed for elimination later
		usefulFeat=[]
		i=0
		#print "the weightList:",weightList
		#print "the featureList:",featureList
		for featureName in featureList:

		
			if weightList[i]==0:
				indexList.append(i)
			else:
				usefulFeat.append(featureName)

			i+=1
		indexList.reverse()
		#print usefulFeat
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
	def scoreFeat(self,featList):
		indexList=self.indexBadFeat(self.weightList,self.featureList)[0]
		score=0
		row=self.selFeat(indexList,featList)
		score=self.clf.predict_proba([row])[:,1][0]
		#print score
		#i=0
		# while i<len(featList):
			
		# 	score=score+featList[i]*self.weightList[i]

		# 	i=i+1
		return score#+10		
