
import json,os,sys,re
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier


##SETTING UP
diseaseclassifier = Trainer(tokenizer) #STARTS CLASIFIERS

with open("priors.csv", 'r') as p:
	for prior in p:
		className, count = prior.split(',')
		count = int(count)
		diseaseclassifier.setPriors(className, count)
with open("Dataset.csv", "r") as file: #OPENS DATASET
    for i in file: #FOR EACH LINE       
       lines = i.split(",") #PARSE CSV <DISEASE> <SYMPTOM>              
       diseaseclassifier.train(lines[1].strip('\n'),  lines[0]) #TRAINING
diseaseclassifier = Classifier(diseaseclassifier.data, tokenizer)
classification = diseaseclassifier.classify(sys.argv[1]) #CLASIFY INPUT
print(sys.argv[1])
for res in classification[:10]:
	print(res) #PRINT CLASIFICATION

