import json,os,sys,re
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier
import numpy as np
from collections import Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
diseaseclassifier = Trainer(tokenizer)

disease_symptom_dict = dict()
with open(dir_path+"/priors.csv", 'r') as p:
	for prior in p:
		className, count = prior.split(',')
		count = int(count)
		diseaseclassifier.setPriors(className, count)
with open(dir_path+"/Dataset.csv", "r") as file:
    for i in file:
       lines = i.split(",")  
       diseaseclassifier.train(lines[1].strip('\n'),  lines[0])
       if lines[0] in disease_symptom_dict:
           disease_symptom_dict[lines[0]].append(lines[1].strip('\n'))
       else:
           disease_symptom_dict[lines[0]] = [lines[1].strip('\n')]
diseaseclassifier = Classifier(diseaseclassifier.data, tokenizer)
initial_submitted_symptoms = sys.argv[1].split(',')


def formatted_print(symptoms, disease_predictions):
    print('\n'+'*'*20)
    print('Symptoms:')
    print(','.join(symptoms))
    print('\n'+'*'*20)
    print('Top 5 disease predictions with probability:\n')
    for res in disease_predictions:
        print(res)

def get_unique_symptoms(other_possible_symtoms):
    unique_list_of_symptoms = []
    sets = [set(i) for i in other_possible_symptoms]
    for i in range(len(sets)):
        temp = set()
        for j in sets[:i]:
            temp = temp.union(j)
        for j in sets[i+1:]:
            temp = temp.union(j)        
        unique_list_of_symptoms += list(sets[i].difference(temp))[:2]
    return unique_list_of_symptoms
    
def ask_user_for_more_details(unique_symptoms):
    if unique_symptoms:
        print("If you have any of these symptoms, enter as comma separated values")
        for i in unique_symptoms:
            print(i)
        user_input = input()
        return user_input
    return None


while(True):
    classification = diseaseclassifier.classify(','.join(initial_submitted_symptoms)) 
    formatted_print(initial_submitted_symptoms, classification[:5])    
    other_possible_symptoms = []
    for disease in classification[:5]:
        d = disease[0]
        other_possible_symptoms.append([symptom for symptom in disease_symptom_dict[d] if symptom not in initial_submitted_symptoms]) 
    unique_symptoms = get_unique_symptoms(other_possible_symptoms)
    next_input = ask_user_for_more_details(unique_symptoms)
    if not next_input or not unique_symptoms:
        break
    for symptom in next_input.split(','):
        initial_submitted_symptoms.append(symptom)




