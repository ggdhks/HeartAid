#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Essentials
import numpy as np
import pandas as pd
import random

# Plots 642345	
import seaborn as sns
import matplotlib.pyplot as plt

# Models sklearn
from sklearn.ensemble import RandomForestClassifier 

# Misc
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.externals import joblib

'''
# Read in the dataset as a dataframe
dt = pd.read_csv("heart.csv")

# change the column name
dt.columns = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate',
       'exercise_induced_angina', 'st_depression', 'st_slope', 'num_major_vessels', 'thalassemia', 'target']

# categorical variable
dt['sex'][dt['sex'] == 0] = 'female'
dt['sex'][dt['sex'] == 1] = 'male'
dt['sex'] = dt['sex'].astype('object')

dt['chest_pain_type'][dt['chest_pain_type'] == 1] = 'typical angina'
dt['chest_pain_type'][dt['chest_pain_type'] == 2] = 'atypical angina'
dt['chest_pain_type'][dt['chest_pain_type'] == 3] = 'non-anginal pain'
dt['chest_pain_type'][dt['chest_pain_type'] == 4] = 'asymptomatic'
dt['chest_pain_type'] = dt['chest_pain_type'].astype('object')

dt['fasting_blood_sugar'][dt['fasting_blood_sugar'] == 0] = 'lower than 120mg/ml'
dt['fasting_blood_sugar'][dt['fasting_blood_sugar'] == 1] = 'greater than 120mg/ml'
dt['fasting_blood_sugar'] = dt['fasting_blood_sugar'].astype('object')

dt['rest_ecg'][dt['rest_ecg'] == 0] = 'normal'
dt['rest_ecg'][dt['rest_ecg'] == 1] = 'ST-T wave abnormality'
dt['rest_ecg'][dt['rest_ecg'] == 2] = 'left ventricular hypertrophy'
dt['rest_ecg'] = dt['rest_ecg'].astype('object')

dt['exercise_induced_angina'][dt['exercise_induced_angina'] == 0] = 'no'
dt['exercise_induced_angina'][dt['exercise_induced_angina'] == 1] = 'yes'
dt['exercise_induced_angina'] = dt['exercise_induced_angina'].astype('object')

dt['st_slope'][dt['st_slope'] == 1] = 'upsloping'
dt['st_slope'][dt['st_slope'] == 2] = 'flat'
dt['st_slope'][dt['st_slope'] == 3] = 'downsloping'
dt['st_slope'] = dt['st_slope'].astype('object')

dt['thalassemia'][dt['thalassemia'] == 1] = 'normal'
dt['thalassemia'][dt['thalassemia'] == 2] = 'fixed defect'
dt['thalassemia'][dt['thalassemia'] == 3] = 'reversable defect'
dt['thalassemia'] = dt['thalassemia'].astype('object')

#print(dt.dtypes) # check types

# creating dummy variable, one-hot code
dt = pd.get_dummies(dt, drop_first=True)


# split the data
x = dt.drop('target', 1)
y = dt['target']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20, random_state=1) 

# random forest
rfc = RandomForestClassifier(max_depth=5)
rfc.fit(x_train, y_train)

rfc_score = rfc.score(x_test, y_test)
print('Random Forest Accuracy: ', round(rfc_score, 5)*100, '%')
'''
# save model
#joblib.dump(rfc, 'rfc.pkl')

def is_target(age, sex, chest, rest, serum, fast, resting, maxi, exercise, old, slope, ca, thal):
	flag = -1
	clf = joblib.load('rfc.pkl')

	# categorical variable
	age = int(age)
	rest = int(rest)
	serum = int(serum)
	maxi = int(maxi)
	old = float(old)
	ca = int(ca)
	
	if sex == "Female":
		sex_male = 0
	else:
		sex_male = 1


	if chest == "Atypical Angina":
		chp = [1,0,0]
	elif chest == "Non-anginal Pain":
		chp = [0,1,0]
	elif chest == "Typical Angina":
		chp = [0,0,1]
	else:
		chp = [0,0,0]


	if fast == "0":
		fast = 1
	else:
		fast = 0

	if resting == "0": # normal
		restingl = [0,1]
	elif resting == "1": # 'ST-T wave abnormality'
		restingl = [0,0]
	else: # 'left ventricular hypertrophy'
		restingl = [1,0]

	if exercise == "1": # yes
		exercise = 1
	else:
		exercise = 0 # no

	if slope == "0": # upsloping
		slopel = [0,1]
	elif slope == "1": # flat
		slopel = [1,0]
	else: # downsloping
		slopel = [0,0]

	if thal == "1": # normal
		thal = [0,1,0]
	elif thal == "2": # fixed defect
		thal = [1,0,0]
	elif thal == "3": # reversable defect
		thal = [0,0,1]
	else:
		thal = [0,0,0]


	k = [[age, rest, serum, maxi, old, ca, sex_male, chp[0], chp[1], chp[2], fast,restingl[0],restingl[1],exercise,slopel[0],slopel[1],thal[0], thal[1],thal[2]]]
	flag = clf.predict(k)

	return flag






