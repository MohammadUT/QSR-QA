

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 10:26:14 2021

@author: Mohammad Kazemi Beydokhti
"""

import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math



#################### Question generation step: generating three QSR questions types: Qtypes 1,2,3 #################


def qualification (Input_points):
    k = 1
    evidence = []
    
    for  i in Input_points[0:len(Input_points)-1]:
        
        for j in Input_points[k:]:
            
            if ( i[2]<points[j[0]-1][2] and i[3]<points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'northeast'))
            
            if ( i[2]<points[j[0]-1][2] and i[3]==points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'east'))
            
            if ( i[2]<points[j[0]-1][2] and i[3]>points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'southeast'))
            
            if ( i[2]==points[j[0]-1][2] and i[3]>points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'south'))
            
            if ( i[2]>points[j[0]-1][2] and i[3]>points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'southwest'))
            
            if ( i[2]>points[j[0]-1][2] and i[3]==points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'west'))
            
            if ( i[2]>points[j[0]-1][2] and i[3]<points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'northwest'))
                
            if ( i[2]==points[j[0]-1][2] and i[3]<points[j[0]-1][3] ):
                evidence.append((j[0], i[0], 'north'))
        
        k = k+1

    return evidence
                
def find_equivalent_relation(points):
    equivalentSet = []
    for  i in points:
        if (i[2] =='north'):
            equivalentSet.append((i[1],i[0],'south'))
        
        if (i[2] =='northeast'):
            equivalentSet.append((i[1],i[0], 'southwest'))
        
        if (i[2] =='east'):
            equivalentSet.append((i[1],i[0],'west'))
        
        if (i[2] =='southeast'):
            equivalentSet.append((i[1],i[0], 'northwest'))
        
        if (i[2] =='south'):
            equivalentSet.append((i[1],i[0],'north'))
            
        if (i[2] =='southwest'):
            equivalentSet.append((i[1],i[0], 'northeast'))
        
        if (i[2] =='west'):
            equivalentSet.append((i[1],i[0],'east'))
        
        if (i[2] =='northwest'):
            equivalentSet.append((i[1],i[0], 'southeast'))
            
    return equivalentSet
    
def finding_point_direction(RandomPoints):
    
    
    Xmax = max([x[2] for x in points])
    Xmin = min([x[2] for x in points])

    Ymax = max([x[3] for x in points])
    Ymin = min([x[3] for x in points])


    XM = (Xmax + Xmin)/2
    YM = (Ymax + Ymin)/2
    
    
    if (XM <RandomPoints[2] and YM < RandomPoints[3] ):
        
        return ('northeast')
    
    if (XM <RandomPoints[2]  and YM == RandomPoints[3]):
        
        return ('east')
    
    if (XM < RandomPoints[2]  and RandomPoints[3] < YM):
        
        return ('southeast')
    
    if (XM == RandomPoints[2] and RandomPoints[3] < YM):
        
        return ('south')
    
    
    if (RandomPoints[2] < XM and  RandomPoints[3] < YM):
        
        return ('southwest')
    
    if (RandomPoints[2] < XM and  RandomPoints[3] == YM):
        
        return ('west')
    
    if ( RandomPoints[2]< XM and YM < RandomPoints[3]):
        
        return ('northwest')
    
    if (XM == RandomPoints[2] and YM < RandomPoints[3]):
        
        return ('north')
    

def check_relation(queried_points, placeP, relation):
    
    direction = qualification(PlaceP + queried_points) 
    
    if ( direction[0][2] == relation ):
        return ('YES')
    
    else:
        return ('NO')
    
    
    
    
pd = pd.read_csv('C:/Users/S3763411/Dropbox/Mohammad/RMIT - PhD Works/Papers/QSR journal paper/Implementation/Input dataset/PlaceNames-500.csv')
points = pd.values.tolist()
# points = points[1:]
PlaceP = [[501, 'Place P', round(144.9448852500,6), round(-37.8285522450,6)]]

points = points+PlaceP
relation_dic = {'north':'n', 'northeast':'ne','northwest':'nw','south':'s','southeast':'se','southwest':'sw', 'east':'e', 'west':'w'}



### Generating simulated QSR questions


cardir = ['northwest', 'southeast']
cardir2 = ['northwest', 'north','northeast','southeast','south','southwest', 'east', 'west']

PlacePDir = [[i[0],i[1],i[2],i[3],finding_point_direction(i)] for i in PlaceP]


CertainEvidenceSet = []
answerQT1 = []
answerQT2 = []
answerQT3 = []
UncertainEvidenceSet = []
PlacesQ1 = []
PlacesQ3 = []
QT1 = []
QT2 =[]
QT3= []
relationslistQ2 = []
relationslistQ3 = []

for i in range(0,50):
    
    
    # Random selection of key places
    
    rmse = 0
    pointDist = []
    while (rmse < 0.038 or len(set(pointDist)) !=4):
    
        keyPlaces = random.sample(points[0:500], 4)
    
    
        pointsXY = [[x[2],x[3]] for x in keyPlaces]
    
        pointsXY_array = np.array(pointsXY)
    
        rmse = np.std(pointsXY_array - pointsXY_array.mean(axis=0))
    
        pointDist =[finding_point_direction(i) for i in keyPlaces]
        
     
        ########################### Simulating qualitative spatial questions
        
    keyPlacesDir =[i+[finding_point_direction(i)] for i in keyPlaces]    
        
    #Selecting NE and SW points to point P
        
    PointsToP = [i for i in keyPlacesDir if i[4]=='northeast' or i[4]=='southwest']
        
    #Selecting unknown points to point P
        
    UnknownToP = [ i for i in keyPlacesDir if i[0] !=PointsToP[0][0] and i[0] !=PointsToP[1][0]]
           
    
    ########## evidence database #########
    evidenceDB = qualification(points)
    
    #### CertainEvidence set for each configuration
    PlacePDist = qualification(PointsToP+PlacePDir)
    PlacePDist = [i for i in PlacePDist if i[0] ==501 or i[1] ==501]
    # PlacePDist = find_equivalent_relation(PlacePDist)

    
    CertainEvidenceSet.append(qualification(keyPlacesDir) + PlacePDist )
    
    #### UncertainEvidence set for each configuration
    
    
    

    for i in CertainEvidenceSet[-1]:
        
    
           
        deltaY = points[i[0]-1][3] - points[i[1]-1][3]
        deltaX = points[i[0]-1][2] - points[i[1]-1][2]
        
        if (deltaX ==0):
            
            if (deltaY > 0):
                
                UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                UncertainEvidenceSet.append((i[0],i[1],'0.1*northeast'))
                UncertainEvidenceSet.append((i[0],i[1],'0.1*northwest'))
            
            if (deltaY < 0):
                
                UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                UncertainEvidenceSet.append((i[0],i[1],'0.1*southeast'))
                UncertainEvidenceSet.append((i[0],i[1],'0.1*southwest'))
        
      
                
        if (deltaX !=0):
            
            
            alphaDegree = math.atan(deltaY/deltaX)*180/math.pi
           
           
            if (abs(alphaDegree) <= 5):
                
           
                if ( deltaY> 0 and deltaX>0 and abs(deltaY)<abs(deltaX)):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*east'))
               
                if ( deltaY< 0 and deltaX>0 and abs(deltaY)<abs(deltaX)):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*east'))
        
        
                if ( deltaY< 0 and deltaX>0 and abs(deltaY)>abs(deltaX)):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*south'))
               
                if ( deltaY< 0 and deltaX<0 and abs(deltaY)>abs(deltaX)):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*south'))
                   
                   
                if ( deltaY< 0 and deltaX<0 and abs(deltaY)<abs(deltaX) ):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*west'))
               
                if ( deltaY> 0 and deltaX<0 and abs(deltaY)<abs(deltaX)):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*west'))
                   
                if ( deltaY> 0 and deltaX<0 and abs(deltaY)>abs(deltaX) ):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*north'))
               
                if ( deltaY> 0 and deltaX>0 and abs(deltaY)>abs(deltaX)):
                   
                   UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                   UncertainEvidenceSet.append((i[0],i[1],'0.2*north'))
                   
                
            
            elif (abs(alphaDegree) ==0):
                
                if (deltaX > 0):
                
                    UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                    UncertainEvidenceSet.append((i[0],i[1],'0.1*northeast'))
                    UncertainEvidenceSet.append((i[0],i[1],'0.1*southeast'))
            
                if (deltaX < 0):
                
                    UncertainEvidenceSet.append((i[0],i[1],'0.8*'+i[2]))
                    UncertainEvidenceSet.append((i[0],i[1],'0.1*northwest'))
                    UncertainEvidenceSet.append((i[0],i[1],'0.1*southwest'))
            
            else:
                UncertainEvidenceSet.append(i)
                
    ## QT-1 template
    TemplateQT1 = "What's the spatial relation between the Place P and the"
    

    
    ## Randomly selecting One of the places which has unknown relation to P
    
    Place1 = random.sample(UnknownToP,1)
    PlacesQ1.append((Place1[0][0], 'the '+ Place1[0][1]))
    
    Place2= [i for i in UnknownToP if i[0] != Place1[0][0]]
    PlacesQ3.append((Place2[0][0], 'the '+Place2[0][1]))

    
    ## Randomly selecting One of the relations which have unknown to P
    
    relation1 = random.sample(cardir, 1)
    relationslistQ2.append(relation_dic[relation1[0]])
    
    relation2 = random.sample(cardir2,1)
    relationslistQ3.append((str(Place2[0][0]), str(PlacePDir[0][0]), relation_dic[relation2[0]]))
    
    
    QT1.append(TemplateQT1 + " "+ Place1[0][1]+"?")
    
    QT2.append("Which places are "+ relation1[0] + " of "+ PlacePDir[0][1]+"?")
    
    QT3.append("Is the " + Place2[0][1]+ " "+ relation2[0] + " of "+ PlacePDir[0][1] +"?")


    ############## Actual answers generation
    
    answerQT1.append(qualification(Place1+PlaceP))
    

    for  i in keyPlacesDir:
        
        
        
        # print(qualification(PlacePDir + [i]))
        
        a = qualification(PlacePDir + [i])[0][2]
        
        if (a == relation1[0]):
            
            answerQT2.append([i])
    
    answerQT3.append((Place2[0][0], PlacePDir[0][0], check_relation(Place2, PlacePDir,relation2[0])))
    



########################## Parsing step: extracting place instances from simulated questions ##############


### AllenNLP Implememntation

#from allennlp import pretrained
from allennlp.modules.elmo import Elmo, batch_to_ids
from allennlp_models.pretrained import load_predictor
#from ner import NER

import logging


logging.basicConfig(level=logging.INFO)
predictor = load_predictor("tagging-fine-grained-crf-tagger")

#model = pretrained.fine_grained_named_entity_recognition_with_elmo_peters_2018()
up_name_tags = ['U-GPE', 'U-LOC', 'U-FAC', 'U-ORG']
cp_name_tags = ['B-GPE', 'B-LOC', 'B-FAC', 'B-ORG', 'I-GPE', 'I-LOC', 'I-FAC', 'I-ORG', 'L-GPE', 'L-LOC', 'L-FAC',
                'L-ORG']

up_event_tags = ['U-EVENT']
cp_event_tags = ['B-EVENT', 'I-EVENT', 'L-EVENT']


class NER:
    @staticmethod
    def parse(sentence):
        res = predictor.predict(sentence=sentence)
        return res

    @staticmethod
    def extract_entities(sentence, u_list, cp_list):
        entities = []
        parsed = NER.parse(sentence)
        current = ''
        for i in range(0, len(parsed['tags'])):
            logging.debug('i: {} word: {} and tag: {}'.format(i, parsed['words'][i], parsed['tags'][i]))
            if parsed['tags'][i] in u_list:
                entities.append(parsed['words'][i])
            elif parsed['tags'][i] in cp_list:
                if parsed['tags'][i].startswith('B-'):
                    current = parsed['words'][i] + ' '
                elif parsed['tags'][i].startswith('L-'):
                    current += parsed['words'][i]
                    entities.append(current)
                else:
                    current += parsed['words'][i] + ' '
        return entities

    @staticmethod
    def extract_place_names_allenNLP(sentence):
        return NER.extract_entities(sentence, up_name_tags, cp_name_tags)

    @staticmethod
    def extract_events(sentence):
        return NER.extract_entities(sentence, up_event_tags, cp_event_tags)
    
PlacesQ1_1 = [(i[0],i[1].lstrip('the ')) for i in PlacesQ1]
PlacesQ3_1 = [(i[0],i[1].lstrip('the ')) for i in PlacesQ3]

# PlacesQ3 = ['the '+i for i in PlacesQ3]

Extracted_placesQ1_allen = [NER.extract_place_names_allenNLP(i) for i in QT1]
Extracted_placesQ3_allen = [NER.extract_place_names_allenNLP(i) for i in QT3]

# Extracted_placesQ1_allen1 = [i[0].lstrip('the ') for i in Extracted_placesQ1_allen if i !=[]]

Extracted_placesQ1_allen_pos= []

for i in Extracted_placesQ1_allen:
    
    if (i != []):
        a = []
        for j in i:
            a.append(j.lstrip('the '))
        
        Extracted_placesQ1_allen_pos.append(a)
    
    else:
        Extracted_placesQ1_allen_pos.append('')


Extracted_placesQ3_allen_pos= []

for i in Extracted_placesQ3_allen:
    
    if (i != []):
        a = []
        for j in i:
            a.append(j.lstrip('the '))
        
        Extracted_placesQ3_allen_pos.append(a)
    
    else:
        Extracted_placesQ3_allen_pos.append('')


    
correct_entitiesQ1_allen = []
correct_entitiesQ3_allen = []


for index,i in enumerate(Extracted_placesQ1_allen_pos):
    if (i != ''):
        
        if (PlacesQ1_1[index][1] in i):
            correct_entitiesQ1_allen.append(PlacesQ1_1[index][0])
        
        else:
            correct_entitiesQ1_allen.append('')
    
    else:
        correct_entitiesQ1_allen.append('')
        
# accuracy_detectionQ1_allen = len(correct_entitiesQ1_allen)/len(PlacesQ1_1)
query_sentencesQ1 = []
for i in correct_entitiesQ1_allen:
    
    if (i != ''):
        query_sentencesQ1.append((str(i),'501'))
    else:
        query_sentencesQ1.append('')
        
# query_sentencesQ1 = [(str(i),'501') for i in correct_entitiesQ1_allen]

for index, i in enumerate(Extracted_placesQ3_allen_pos):
    
    if (i != ''):
            
        if (PlacesQ3_1[index][1] in i):
            correct_entitiesQ3_allen.append(PlacesQ3_1[index][0])
        else:
            correct_entitiesQ3_allen.append('')
    else:
        correct_entitiesQ3_allen.append('')
    
    
# accuracy_detectionQ3_allen = len(correct_entitiesQ3_allen)/len(PlacesQ3_1)
query_sentencesQ3 = []
for i in correct_entitiesQ3_allen:
    
    if (i != ''):
        query_sentencesQ3.append((str(i),'501'))
    else:
        query_sentencesQ3.append('')

    

##############saving variable from allen's run#############
import pickle 
with open('QTs.pickle', 'wb') as f:
    pickle.dump([QT1, QT2, QT3], f)
    
with open('AnswerQTs.pickle', 'wb') as f:
    pickle.dump([answerQT1, answerQT2,answerQT3], f)

with open('EvidenceSet.pickle', 'wb') as f:
    pickle.dump([CertainEvidenceSet, UncertainEvidenceSet, evidenceDB], f)

# with open('relationlistsQ2Q3.pickle', 'wb') as f:
#     pickle.dump([relationslistQ2,relationslistQ3], f)

with open('placesQ1Q3.pickle', 'wb') as f:
    pickle.dump([PlacesQ1_1,PlacesQ3_1], f)

with open('querysentencesQ1Q3DP.pickle', 'wb') as f:
    pickle.dump([query_sentencesQ1,query_sentencesQ3],f, protocol=2)


with open('relationlistsQ2Q3.pickle', 'wb') as f:
    pickle.dump([relationslistQ2,relationslistQ3], f,protocol=2)

with open('KeyPlaces.pickle', 'wb') as f:
    pickle.dump([keyplaces], f,protocol=2)
    
with open('generatedrelationsProbcogQ1-Allen2.pickle', 'wb') as f:
    pickle.dump(m, f, protocol=2)

#Read
import pickle
with open('E:/sharefolder/QTs.pickle', 'rb') as f:
    QT1, QT2, QT3= pickle.load(f)

with open('E:/sharefolder/AnswerQTs.pickle', 'rb') as f:
    answerQT1, answerQT2,answerQT3 = pickle.load(f)

with open('E:/sharefolder/EvidenceSet.pickle', 'rb') as f:
    CertainEvidenceSet, UncertainEvidenceSet, evidenceDB= pickle.load(f)

with open('E:/sharefolder/relationlistsQ2Q3.pickle', 'rb') as f:
   relationslistQ2,relationslistQ3 = pickle.load(f)

with open('E:/sharefolder/placesQ1Q3.pickle', 'rb') as f:
   PlacesQ1_1,PlacesQ3_1 = pickle.load(f)
   

with open('E:/sharefolder/querysentencesQ1Q3Allen.pickle', 'rb') as f:
    query_sentencesQ1,query_sentencesQ3 = pickle.load(f)
   

with open('E:/sharefolder/generatedrelationsProbcogQ3-Allen.pickle', 'rb') as f:
   QT3_probcog_allen = pickle.load(f)

QT2_probcog_allen = QT2_probcog_allen[0]
QT2_probcog_allen = QT2_probcog_allen+QT2_probcog_allen144+QT2_probcog_allen147+QT2_probcog_allen852      
##########################################    

    
## DeepPavlov Implementation

from deeppavlov import configs, build_model
# from deeppavlov import configs, train_model

ner_model = build_model(configs.ner.ner_conll2003, download=True)


def extract_place_names_deepPavlov (sentence):
    
    
    parsed_entities = ner_model([sentence])
    parsed_entities = [i[0] for i in parsed_entities]
    # placeEntity = []
    current = ''
    extracted_places = []
    # k1 = 0
   
    for index, elem in enumerate(parsed_entities[-1]):
        if (index+1 < len(parsed_entities[-1]) and elem in cp_name_tags ):
        
            if (elem[0] =='B'):
                if (parsed_entities[-1][index+1][0] != 'I'):
                    extracted_places.append('the '+parsed_entities[0][index])
            
                else:
                    current += 'the ' +parsed_entities[0][index]
            else:
                current += " " +parsed_entities[0][index]

    if current !="":
        extracted_places.append(current)   
        
    return extracted_places

Extracted_placesQ1_DP = [extract_place_names_deepPavlov(i) for i in QT1]
Extracted_placesQ3_DP = [extract_place_names_deepPavlov(i) for i in QT3]


Extracted_placesQ1_DP_pos= []

for i in Extracted_placesQ1_DP:
    
    if (i != []):
        a = []
        for j in i:
            a.append(j.lstrip('the '))
        
        Extracted_placesQ1_DP_pos.append(a)
    
    else:
        Extracted_placesQ1_DP_pos.append('')


Extracted_placesQ3_DP_pos= []

for i in Extracted_placesQ3_DP:
    
    if (i != []):
        a = []
        for j in i:
            a.append(j.lstrip('the '))
        
        Extracted_placesQ3_DP_pos.append(a)
    
    else:
        Extracted_placesQ3_DP_pos.append('')


    
correct_entitiesQ1_DP = []
correct_entitiesQ3_DP = []


for index,i in enumerate(Extracted_placesQ1_DP_pos):
    if (i != ''):
        
        if (PlacesQ1_1[index][1] in i):
            correct_entitiesQ1_DP.append(PlacesQ1_1[index][0])
        
        else:
            correct_entitiesQ1_DP.append('')
    
    else:
        correct_entitiesQ1_DP.append('')
        
# accuracy_detectionQ1_allen = len(correct_entitiesQ1_allen)/len(PlacesQ1_1)
query_sentencesQ1 = []
for i in correct_entitiesQ1_DP:
    
    if (i != ''):
        query_sentencesQ1.append((str(i),'501'))
    else:
        query_sentencesQ1.append('')


for index, i in enumerate(Extracted_placesQ3_DP_pos):
    
    if (i != ''):
            
        if (PlacesQ3_1[index][1] in i):
            correct_entitiesQ3_DP.append(PlacesQ3_1[index][0])
        else:
            correct_entitiesQ3_DP.append('')
    else:
        correct_entitiesQ3_DP.append('')
    
    
# accuracy_detectionQ3_allen = len(correct_entitiesQ3_allen)/len(PlacesQ3_1)
query_sentencesQ3 = []
for i in correct_entitiesQ3_DP:
    
    if (i != ''):
        query_sentencesQ3.append((str(i),'501'))
    else:
        query_sentencesQ3.append('')







############ Preparing query sentences in the format of triple (Place, sr, place) for SparQ on Linux #############


certainset_sparq = []

for index, i in enumerate(CertainEvidenceSet):
    current = ''
    for j in i:
        current += '('+ str(j[0])+ " (" + relation_dic[j[2]] +') ' + str(j[1])+ ")" 
    
    certainset_sparq.append(['"('+current+')"'])
    


# import pickle 
with open('certainset_sparq.pickle', 'wb') as f:
    pickle.dump([certainset_sparq], f)



######################## Importing generated relations from Linux OS to Win OS

with open('GeneraatedRelations.pickle', 'rb') as f:
    generatedRelations= pickle.load(f)



################################### Answer Extraction stage ##############################################

generatedRelations_pos = []

for i in generatedRelations:
    for j in i:
        generatedRelations_pos.append(j)
        
generated_answersQ1 = []

generated_answersQ2 = [i for i in generatedRelations_pos if i[0] =='501' or i[1] =='501']
generated_answersQ3 = []

for index, i in enumerate(query_sentencesQ1):
    if (i != ''):
        for j in generatedRelations_pos[index*10: 10*(index+1)]:
            
        
            if (i[0] ==j[0] and i[1] ==j[1]):
                generated_answersQ1.append((j[0], j[1], j[2].replace(")", "").replace("(", "").rstrip()))
    else:
        generated_answersQ1.append('')


for index, i in enumerate(query_sentencesQ3):
    if (i != ''):
        for j in generatedRelations_pos[index*10: 10*(index+1)]:
            
        
            if (i[0] ==j[0] and i[1] ==j[1]):
                generated_answersQ3.append((j[0], j[1], j[2].replace(")", "").replace("(", "").rstrip()))
    else:
        generated_answersQ3.append('')

##################################### Evaluation ##########################################

Allrelations = 'e eq n ne nw s se sw w'


#### Question Type1 for SparQ - AllenNLP/DeepPavlov

answerQT1_equ1 = [find_equivalent_relation(i) for i in answerQT1]

answerQT1_equ = [(str(i[0][0]), str(i[0][1]), relation_dic[i[0][2]]) for i in answerQT1_equ1]


Exact_matchQ1 = [i for index, i in enumerate(generated_answersQ1) if i==answerQT1_equ[index]]

PartofAnswerQ1 = [i for index, i in enumerate(generated_answersQ1) if (i !='' and i !=answerQT1_equ[index]) if (i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and answerQT1_equ[index][2] in i[2].split()) and i[2] != Allrelations]

AllrelationsAnswerQ1= [i for index, i in enumerate(generated_answersQ1) if (i !='' and i !=answerQT1_equ[index]) if (i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and i[2] == Allrelations)]

NotMatchAnswerQ1 = [i for index, i in enumerate(generated_answersQ1) if (i !='' and i !=answerQT1_equ[index]) if (i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and answerQT1_equ[index][2] not in i[2].split())]

######## Question Type1 for Probcog - AllenNLP/DeepPavlov


def filterTheDict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            newDict[key] = value
    return newDict

GeneratedAnswers_QT1_probcog_DP = []
for  i in QT1_probcog_allen:
    

    if (i != ''):
        filterDic = filterTheDict(i, lambda elem : elem[1] >= 0.5)
        if filterDic != []:
        
            GeneratedAnswers_QT1_probcog_DP.append(filterDic)
        else:
            GeneratedAnswers_QT1_probcog_DP.append('')
    else:
        GeneratedAnswers_QT1_probcog_DP.append('')

correct_QT1_probcog_allen = []
incorrect_QT1_probcog_allen = []

for index, i in enumerate(GeneratedAnswers_QT1_probcog_DP):
    if (i != {} and i != ''):
        k=0
        for j in list(i.keys()):
                
            relation = j.strip('at').strip('(').strip(')').split(',')[2]
        
            if (relation == answerQT1_equ[index][2].upper() ):
                correct_QT1_probcog_allen.append(i)
                incorrect_QT1_probcog_allen.append('')
                k=k+1
        
        if (k < 1):
                correct_QT1_probcog_allen.append('')
                incorrect_QT1_probcog_allen.append(i)
    else:
        correct_QT1_probcog_allen.append('')
        incorrect_QT1_probcog_allen.append('')
            

#### Question Type2 for SparQ - AllenNLP/DeepPavlov

answerQT2_pos = [i[0] for i in answerQT2]
answerQT2_pos1 = [('Question '+ str(index+1), str(i[0])) for index, i in enumerate(answerQT2_pos)]

generared_answersQ2_1 = [(i[0], i[1], i[2].replace(")", "").replace("(", "").rstrip()) for i in generated_answersQ2]


PlacesAnswerQ2 = []

for index, i in enumerate(relationslistQ2):
    current = ''
    for j in generared_answersQ2_1[index*4: 4*(index+1)]:
        
        if ( i in j[2]):
            current +=  j[0] + ','
    current.rstrip(',')
    PlacesAnswerQ2.append(('Question ' + str(index+1), current))

PlacesAnswerQ2 = [(i[0], i[1].rstrip(',')) for i in PlacesAnswerQ2]         

ExactMatchAnswerQ2 = [i for index,i in enumerate(PlacesAnswerQ2) if i==answerQT2_pos1[index]]
PartofAnswerQ2 = [i for index,i in enumerate(PlacesAnswerQ2) if (i != answerQT2_pos1[index] and answerQT2_pos1[index][1] in i[1])]
NotMatchAnswerQ2 = [i for index,i in enumerate(PlacesAnswerQ2) if answerQT2_pos1[index][1] not in i[1]]


######## Question Type2 for ProbCog - AllenNLP/DeepPavlov

# def filterTheDict(dictObj, callback):
#     newDict = dict()
#     # Iterate over all the items in dictionary
#     for (key, value) in dictObj.items():
#         # Check if item satisfies the given condition then add to new dict
#         if callback((key, value)):
#             newDict[key] = value
#     return newDict

GeneratedAnswers_QT2_probcog_allen = []
for  i in QT2_probcog_allen:
    

    if (i != ''):
        filterDic = filterTheDict(i[0], lambda elem : elem[1] >= 0.5)
        if filterDic != []:
        
            GeneratedAnswers_QT2_probcog_allen.append(filterDic)
        else:
            GeneratedAnswers_QT2_probcog_allen.append('')
    else:
        GeneratedAnswers_QT2_probcog_allen.append('')

correct_QT1_probcog_allen = []
incorrect_QT1_probcog_allen = []

for index, i in enumerate(GeneratedAnswers_QT1_probcog_allen):
    if (i != {} and i != ''):
        k=0
        for j in list(i.keys()):
                
            relation = j.strip('at').strip('(').strip(')').split(',')[2]
        
            if (relation == answerQT1_equ[index][2].upper() ):
                correct_QT1_probcog_allen.append(i)
                incorrect_QT1_probcog_allen.append('')
                k=k+1
        
        if (k < 1):
                correct_QT1_probcog_allen.append('')
                incorrect_QT1_probcog_allen.append(i)
    else:
        correct_QT1_probcog_allen.append('')
        incorrect_QT1_probcog_allen.append('')
                 
#### Question Type3 for SparQ - AllenNLP/DeepPavlov


answerQT3_equ = [(str(i[0]), str(i[1]), i[2]) for i in answerQT3]

ExactMatchAnswerQ3 = []
correctAnswers_DP = []
ExactMatchAnswerQ3 = []
NotMatchAnswerQ3 = []
PartofAnswerQ3 = []
AllrelationsAnswerQ3 = []
incorrectasnwers = []

for index, i in enumerate(generated_answersQ3):
    
    if (i==relationslistQ3[index]):
        ExactMatchAnswerQ3.append((i[0],i[1], 'YES'))
        
        if ExactMatchAnswerQ3[-1] == answerQT3_equ[index]:
            correctAnswers_DP.append((i[0],i[1], 'YES'))
        
        else:
            correctAnswers_DP.append('')
            incorrectasnwers.append((i[0],i[1], 'YES'))
    
    elif (i !='' and i !=relationslistQ3[index]):
          if (i[0]==relationslistQ3[index][0] and i[1]==relationslistQ3[index][1] and relationslistQ3[index][2] in i[2].split() and i[2] != Allrelations):
              PartofAnswerQ3.append((i[0], i[1], 'YES'))
              
              if (PartofAnswerQ3[-1] ==answerQT3_equ[index]):
                  
                  
                  correctAnswers_DP.append((i[0],i[1], 'YES'))
              else:
                  correctAnswers_DP.append('')
                  incorrectasnwers.append((i[0],i[1], 'YES'))
                  
          elif (i[0]==relationslistQ3[index][0] and i[1]==relationslistQ3[index][1] and relationslistQ3[index][2] not in i[2].split()):
            
            NotMatchAnswerQ3.append((i[0], i[1], 'NO'))
            
            if NotMatchAnswerQ3[-1] ==answerQT3_equ[index]:
                  
                  correctAnswers_DP.append((i[0],i[1], 'NO'))
            else:
                
                correctAnswers_DP.append('')
                incorrectasnwers.append((i[0],i[1], 'NO'))
                  
                  
                  
          else:
              
              AllrelationsAnswerQ3.append((i[0], i[1], 'NA'))
              correctAnswers_DP.append('')
    else:
        
        correctAnswers_DP.append('')

########### #### Question Type3 for Probcog - AllenNLP/DeepPavlov



GeneratedAnswers_QT3_probcog_DP = []
for  i in QT3_probcog_DP:

    if (i != '' and i is not None):
        filterDic = filterTheDict(i, lambda elem : elem[1] >= 0.5)
        if ( filterDic != {}):
            GeneratedAnswers_QT3_probcog_DP.append((i,'YES'))
        else:
            GeneratedAnswers_QT3_probcog_DP.append((i,'NO'))

    else:
        GeneratedAnswers_QT3_probcog_DP.append('')

correct_QT3_probcog_DP = []
incorrect_QT3_probcog_DP = []

for index, i in enumerate(GeneratedAnswers_QT3_probcog_DP):
    if (i is not None and i != ''):
        
        if (i[1] == answerQT3_equ[index][2]):
            correct_QT3_probcog_DP.append(i)
        else:
            incorrect_QT3_probcog_DP.append(i)

    else:
        correct_QT3_probcog_DP.append('')
        incorrect_QT3_probcog_DP.append('')
        


########################################## Data preparation steps ####################################

################ converting sparq outputs to lists compatible with previous steps outputs

a = [['Modified network.\n((344 (s se sw) 501)(281 (sw) 501)(281 (nw) 344)(78 (nw sw w) 501)(78 (nw) 344)(78 (nw) 281)(38 (ne) 501)(38 (ne) 344)(38 (ne) 281)(38 (ne) 78))'], ['Modified network.\n((333 (ne) 501)(249 (sw) 501)(249 (sw) 333)(295 (se) 501)(295 (se) 333)(295 (se) 249)(139 (e eq n ne nw s se sw w) 501)(139 (sw) 333)(139 (ne) 249)(139 (nw) 295))'], ['Modified network.\n((274 (sw) 501)(438 (e eq n ne nw s se sw w) 501)(438 (ne) 274)(164 (e ne se) 501)(164 (ne) 274)(164 (se) 438)(226 (ne) 501)(226 (ne) 274)(226 (ne) 438)(226 (nw) 164))'], ['Modified network.\n((243 (sw) 501)(289 (e ne se) 501)(289 (ne) 243)(138 (nw sw w) 501)(138 (nw) 243)(138 (nw) 289)(254 (ne) 501)(254 (ne) 243)(254 (nw) 289)(254 (ne) 138))'], ['Modified network.\n((478 (e ne se) 501)(34 (sw) 501)(34 (sw) 478)(225 (ne) 501)(225 (nw) 478)(225 (ne) 34)(230 (nw sw w) 501)(230 (nw) 478)(230 (nw) 34)(230 (sw) 225))'], ['Unmodified network.\n((338 (ne) 501)(193 (sw) 501)(193 (sw) 338)(132 (e eq n ne nw s se sw w) 501)(132 (sw) 338)(132 (ne) 193)(264 (e eq n ne nw s se sw w) 501)(264 (sw) 338)(264 (ne) 193)(264 (se) 132))'], ['Modified network.\n((458 (sw) 501)(438 (e eq n ne nw s se sw w) 501)(438 (ne) 458)(228 (ne) 501)(228 (ne) 458)(228 (ne) 438)(164 (e ne se) 501)(164 (ne) 458)(164 (se) 438)(164 (se) 228))'], ['Modified network.\n((125 (n ne nw) 501)(420 (ne) 501)(420 (se) 125)(475 (se) 501)(475 (se) 125)(475 (se) 420)(436 (sw) 501)(436 (sw) 125)(436 (sw) 420)(436 (nw) 475))'], ['Modified network.\n((167 (n ne nw) 501)(407 (se) 501)(407 (se) 167)(480 (ne) 501)(480 (se) 167)(480 (nw) 407)(193 (sw) 501)(193 (sw) 167)(193 (nw) 407)(193 (sw) 480))'], ['Modified network.\n((378 (e eq n ne nw s se sw w) 501)(423 (nw sw w) 501)(423 (nw) 378)(262 (sw) 501)(262 (sw) 378)(262 (se) 423)(58 (ne) 501)(58 (ne) 378)(58 (ne) 423)(58 (ne) 262))']]

      
b = [i[0].split() for i in a]
p2 = []
p1 = []
test = []
rel = ''
for index, i in enumerate(b):
    for index, j in enumerate(i):
        
        if (index>1):
            if (re.findall(r'\d+', j) !=[]):
                
                if p1 == []:
                    p1 = re.findall(r'\d+', j)[0]
                    p2 = []
                elif (len(re.findall(r'\d+', j)) >1):
                    p2 = re.findall(r'\d+', j)[0]
                    # p1 = re.findall(r'\d+', i)[1]
                    test.append([p1, p2, rel])
                    rel = ''
                    p1 = re.findall(r'\d+', j)[1] 
                else:
                    p2 = re.findall(r'\d+', j)[0]
                    test.append([p1, p2, rel])
                    p1 = []
                    rel = ''
                    p2= []
                    
            else:
                rel +=j+' '


########### Probcog prepareation input dataset: uncertain evidence set

current = []
UncertainEvidenceSet1000 = []
for i in range(0, len(UncertainEvidenceSet)):
    
    if UncertainEvidenceSet[i][0] != 501: 
        current += [UncertainEvidenceSet[i]]
    
    elif UncertainEvidenceSet[i][0] == 501 and i==len(UncertainEvidenceSet)-1:
        current += [UncertainEvidenceSet[i]]
        UncertainEvidenceSet1000.append(current)
        current = []
        
    elif UncertainEvidenceSet[i][0] == 501 and UncertainEvidenceSet[i+1][0] ==501:
        current += [UncertainEvidenceSet[i]]
    
    
    else:
        current += [UncertainEvidenceSet[i]]
        UncertainEvidenceSet1000.append(current)
        current = []
    

ss = []
# current = ''
nn  =[list(dict.fromkeys(i)) for i in UncertainEvidenceSet1000 ]


### creating txt files for all 1000 configurations
for index, i in enumerate(nn):
    a = ''
    current = ''
    for j in i:
    
        if (j[2] in relation_dic.keys()):
            current += 'at'+ str((j[0], j[1], relation_dic[j[2]].upper()))+ '\n'
        else:
            # j[index][2].split('*')
            current += str(j[2].split('*')[0])+ ' at' + str((j[0], j[1], relation_dic[j[2].split('*')[1]].upper()))+ '\n'
    a = 'UncertainEvidenceSet' +str(index) +  '.txt'
    with open(a, 'w') as f:
        f.write(current)
      
### removing ' ' from created text files
for i in range(0,1000):

    db = 'UncertainEvidenceSet' + str(i) +'.txt'

    file = open(db, "rt")
    data = file.read()
    data = data.replace("'", '')
    file.close()
    # open the input file in write mode
    file = open(db, "wt")
    # overrite the input file with the resulting data
    file.write(data)
    file.close()


#### Key places for each configuration

keyplaces = []

for i in CertainEvidenceSet:
    current = []
    
    for index, j in enumerate(i):
        current.append(j[0])
        current.append(j[1])
    
    keyplaces.append(list(dict.fromkeys(current))[:-1])
 
    
 
########## converting QT1_probcog_allen into 1000    
m = []        
k=0
for index, i in enumerate(query_sentencesQ1):
    
    
    if (i ==''):
        m.append('')
    
    else:
        
        if (QT1_probcog_allen[k] is None):
            m.append('')
            k=k+1
            
        else:
            ans = list(QT1_probcog_allen[k].keys())[0].strip('at').strip('(').strip(')').split(',')
        
            if ( (ans[0],ans[1]) == i):
        
                m.append(QT1_probcog_allen[k])
            
                k = k+1
        
l =[]   
for i in relationslistQ2:
  l.append('('+"'"+'Places'+ "'"+', '+ "'"+i + "'"+ ','+ "'" + '501' + "'"+')')  

h = []
for index, i in enumerate(query_sentencesQ3):
    if (i !=''):
      h.append(relationslistQ3[index])
    else:
        h.append('')
      

Exact_matchQ1_edit = []
for index, i in enumerate(generated_answersQ1):
    if i==answerQT1_equ[index]:
        Exact_matchQ1_edit.append(i)
    else:
        Exact_matchQ1_edit.append('')

PartofAnswerQ1 = [i for index, i in enumerate(generated_answersQ1) if (i !='' and i !=answerQT1_equ[index]) if (i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and answerQT1_equ[index][2] in i[2].split()) and i[2] != Allrelations]

PartofAnswerQ1_edit = []
for index, i in enumerate(generated_answersQ1):
    if (i !='' and i !=answerQT1_equ[index]):
        if ((i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and answerQT1_equ[index][2] in i[2].split()) and i[2] != Allrelations):
            
            PartofAnswerQ1_edit.append(i)
            
        else:
            PartofAnswerQ1_edit.append('')
    else:
        PartofAnswerQ1_edit.append('')
    
    
correct_QT1_sparq_allen = []

for index,i in enumerate(PartofAnswerQ1_edit):
    if ( i =='' and  Exact_matchQ1_edit[index] !=''):
        correct_QT1_sparq_allen.append(Exact_matchQ1_edit[index])
    else:
        correct_QT1_sparq_allen.append(i)


correct_QT1_sparq_integrated = []
for index,i in enumerate(correct_QT1_sparq_DP):
    if ( i =='' and  correct_QT1_sparq_allen[index] !=''):
        correct_QT1_sparq_integrated.append(correct_QT1_sparq_allen[index])
    else:
        correct_QT1_sparq_integrated.append(i)    
    
    