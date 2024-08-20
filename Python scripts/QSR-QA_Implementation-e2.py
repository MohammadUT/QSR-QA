# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 00:23:30 2022

@author: S3763411
"""

import pandas as pd
import random
import time
import pickle



######### 2. Reading footprints relations 

cd_pickle = 'Stored pickle variables'
cd_evidence = 'Evidence sets'

cd1 = '~/Input dataset/'
uk_gazetter_all = pd.read_csv(cd1+ 'zoi_data/ukgaz.csv',encoding = "ISO-8859-1")
place_types = pd.read_csv(cd1+ 'zoi_data/counties.csv',encoding = "ISO-8859-1")       
    

uk_gazetter_all_list = uk_gazetter_all.values.tolist()
place_types_list = place_types.values.tolist()


with open(cd_pickle + 'zoi_relations_extracted.pickle' , 'rb') as f:
        footprints_relations = pickle.load(f)
        
footprints_relations = footprints_relations[0]



######### 3. Reading extracted footprints relations and random selection of 4 footprints for 1000 configurations
   
zoi_relations_list_filter = [i for i in footprints_relations if i[2] !='dr']


footprint_list = list(set([i[0] for i in zoi_relations_list_filter]))



evidence_sets = []
selected_footprints2 = []

while (len(list(set(map(lambda i: tuple(sorted(i)), evidence_sets)))) < 1000):
    
    first_pair = random.sample(zoi_relations_list_filter, 1)
    
    
    
        
    selected_first_pair = [i for i in zoi_relations_list_filter if (first_pair[0] != i) if (first_pair[0][0] in i) or (first_pair[0][1] in i)]
    
    if (selected_first_pair != []):
        second_pair = random.sample(selected_first_pair, 1)
        
        two_pairs = first_pair + second_pair
        
        
        
        selected_second_pair = [i for i in zoi_relations_list_filter if (second_pair[0] != i and first_pair[0] !=i and i not in selected_first_pair) if (second_pair[0][0] in i) or (second_pair[0][1] in i)]
        
        if (selected_second_pair !=[]):
            selected_first_sec_pairs = selected_first_pair+selected_second_pair
            
            # selected_first_sec_pairs2 =  [i for i in selected_first_sec_pairs if (i not in two_pairs)]
            
            
            # if (selected_first_sec_pairs2 != []):
                
            third_pair = random.sample(selected_first_sec_pairs, 1)
            
            selected_pairs = two_pairs + third_pair
            
            selected_footprints = list(set([i[0] for i in selected_pairs]+[i[1] for i in selected_pairs]))
            
            
            
            if (len(selected_footprints)> 3):                
                
                evidence_sets.append(selected_pairs)
                selected_footprints2.append(selected_footprints)
                
                
with open(cd+ 'selected_footprints.pickle', 'wb') as f:
    pickle.dump([selected_footprints2], f,protocol=2)

                
######### 4. Obtaining all 6 relations in each configurations with 4 footprints.

# footprints_relations6 = full_evidencesets
selected_footprints2 = selected_footprints2[0]
footprints_relations6 = []

for i in selected_footprints2:
    sets = []

    for index,j in enumerate(i):
        for k in i[index+1:]:
            sets.append(find_zoi_relation(j,k))
    
    footprints_relations6.append(sets)

#footprints_relations6 = full_evidencesets

######## 5. Finding relations between generated incidents and footprints 



with open(cd_pickle + 'footprint_incident_rel.pickle', 'rb') as f:
    footprint_incident_rel = pickle.load(f)

footprint_incident_rel = footprint_incident_rel[0]


incident_relations2 = []
incident_relations_check = []

for index,i in enumerate(footprint_incident_rel):
    
    #random_incident_relations_known = random.sample(i, 2)
    a = random.sample(i, 2)
    incident_relations2.append([(i[0], i[1], i[-1], i[-2]) for i in a])
    
    incident_relations_check.append([(m[0],m[1],m[-1],m[-2]) for m in i if m not in a])
    

# incident_relations_check = []
# for index,i in enumerate(footprint_incident_rel):
#     s = []
#     for j in i:
        
#         a = (j[0],j[1], j[-1],j[-2])
#         if a not in  incident_relations2[index]:
            

#             s.append(a)
            
#     incident_relations_check.append(s)
    
        
        
    
    


with open(cd_pickle+ 'incident_relations2.pickle', 'wb') as f:
    pickle.dump([incident_relations2], f,protocol=2)
    
######## 5. Extracting relations between footprints and counties, ua, districts, and countries in pyQGIS


######## 6. Assigning IDs to counties, ua, districts, and countries.

with open(cd_pickle+ 'countries_footprints_rel.pickle' , 'rb') as f:
        countries_footprints_rel = pickle.load(f)


countries_footprints_rel  = countries_footprints_rel[0]

   
countries_footprints_rel_id = []

for i in countries_footprints_rel:
    b = []
    for j in i:
        
        m = [s[-1] for s in place_types_list if s[3] == j[0]]
        
        if (m !=[]):
            b.append((m[0], j[1], j[2]))
        else:
            b.append(j)
    
    countries_footprints_rel_id.append(b)



    

ccud_relations4 = []

for index, i in enumerate(counties_footprints_rel_id):

    m = [k for k in i if type(k[0]) != str]
    
    random_sample_county = random.sample(m, 1)
    
    
    
    m = [k for k in ua_footprints_rel_id[index] if type(k[0]) != str and k[-1] !='dr' and k[1] != random_sample_county[0][1]]
    if ( m != []):
        random_sample_ua = random.sample(m, 1)

    else:
        m = [k for k in ua_footprints_rel_id[index] if type(k[0]) != str and k[1] != random_sample_county[0][1]]
        random_sample_ua = random.sample(m, 1)

        
        
    m = [k for k in districts_footprints_rel_id[index] if type(k[0]) != str and k[-1] !='dr' 
         and k[1] != random_sample_ua[0][1] and k[1] != random_sample_county[0][1]]
    
    if ( m != []):
        random_sample_districts = random.sample(m, 1)
        
    else:
         m = [k for k in districts_footprints_rel_id[index] if type(k[0]) != str 
              and k[1] != random_sample_ua[0][1] and k[1] != random_sample_county[0][1]]
         
         random_sample_districts = random.sample(m, 1)

    
    m = [k for k in countries_footprints_rel_id[index] if type(k[0]) != str and k[-1] != 'dr' 
         and k[1] != random_sample_districts[0][1] and k[1] != random_sample_ua[0][1] and k[1] != random_sample_county[0][1]]
    
    random_sample_country = random.sample(m, 1)
    
    ccud_relations4.append(random_sample_county+random_sample_ua+random_sample_districts+random_sample_country)  
    
    

######## 7. Preparing evidence DB (12 relations)
        # 6 relations for footprints : footprints_relations6
        # 4 random relations between footprints and counties/countries/ua/districts: ccud_relations4
        # 2 random relations between incident point and two random footprints: incident_relations2


############## Mapping NL expressions to RCC5 relations

# NL expressions -  RCC5 relations
# --------------------------------
# in/inside      - PP, PPi
# within/part of -
# --------------------------------               
# disjoint/border- DC               
# intersect      - PO                 
# equal          - EQ                  


# 9IM -  RCC5 relations
# --------------------------------
# cb/vb    - PP
# cs/vs    - PPi
# di       - DC               
# ov       - PO                 
# eq       - EQ    

####### 8. Evidence_db = footprints_relations6 + ccud_relations4 + incident_relations2

rcc5_9im_map = {'pp':['vb','cb'], 'ppi':['vs','cs'] , 'dr':'di','po':'ov','eq':'eq'}
r9im_rcc5_map = {'cs':'ppi', 'vs':'ppi','cb':'pp','vb':'pp', 'di':'dr','eq':'eq','ov':'po'}


Evidence_db = [footprints_relations6[i] + ccud_relations4[i] + incident_relations2[i] for i in range(0,1000)]

with open(cd_pickle+ 'Evidence_db.pickle', 'wb') as f:
    pickle.dump([Evidence_db], f,protocol=2)


for index, i in enumerate(Evidence_db):
    a = ''
    current = ''
    for j in i:
        if (j[-1] not in rcc5_9im_map.keys()):

            current += 'rcc('+ str(j[0]) + ','+ str(j[1]) + ','+ r9im_rcc5_map[j[-1]].upper()+ ')'+ '\n'
        
        else:
            current += 'rcc('+ str(j[0]) + ','+ str(j[1]) + ','+ j[-1].upper()+ ')'+ '\n'

    a = cd_evidence + 'EvidenceSet_ProbCog' +str(index) +  '.txt'
    with open(a, 'w') as f:
        f.write(current)
        
#### uncertain probability
cd_uncertain_evidencetset = '/Users/mkazemi/PhD /RMIT - PhD Works/Papers/QSR journal paper/Implementation/Stage 2 - Made up questions and real evidence sets/Uncertain evidence sets/'  
for index, i in enumerate(Evidence_db):
    a = ''
    current = ''
    for j in i:
        if (j[-1] not in rcc5_9im_map.keys()):
            

            current += 'rcc('+ str(j[0]) + ','+ str(j[1]) + ','+ r9im_rcc5_map[j[-1]].upper()+ ')'+ '\n'
        
        else:
            if (j[1] != 260000 ):
                current += 'rcc('+ str(j[0]) + ','+ str(j[1]) + ','+ j[-1].upper()+ ')'+ '\n'
            else:
                current += '0.7 rcc('+ str(j[0]) + ','+ str(j[1]) + ','+ j[-1].upper()+ ')'+ '\n'

    a = cd_uncertain_evidencetset + 'Uncertain_EvidenceSet_ProbCog' +str(index) +  '.txt'
    with open(a, 'w') as f:
        f.write(current)        
      
############################# Stage 2: Question Genertation (4Types)  #####################################

######## 1. QType1 questions

## mapping rcc8 relations to natural language expressions
NL = ['in', 'inside','within','part of','border','disjoint from','intersect','equal']
SR_to_NL = {'TPP':{'in', 'inside','within','part of'}, 'NTPP':{'in', 'inside','within','part of'},'EC':'border','DC':'disjoint','PO':'intersect','EQ':'equal'}


        
QType1 = []                 

Q1_places_list = []
Q2_places_list = []
Q3_places_list = []
Q4_places_list = []

Extracted_placesQ1_DP= []
Extracted_placesQ2_DP = []
Extracted_placesQ3_DP = []
Extracted_placesQ4_DP = []

correct_entities_Q1 = []
correct_entities_Q2 = []
correct_entities_Q3 = []
correct_entities_Q4 = []


for index,i in enumerate(Evidence_db):
    

    
    ### Qtype1
    Q1_places = random.sample(incident_relations_check[index],1)
    place1_name = [i[1] for i in uk_gazetter_all_list if i[0] ==Q1_places[0][0]][0]
    Q1_places_list.append(Q1_places)
    
    QType1.append('What is the spatial relation between incident and ' + \
                  place1_name + '?')
    

                
with open(cd_pickle+ 'Q1_places_list.pickle', 'wb') as f:
    pickle.dump([Q1_places_list], f,protocol=2)


######## 2. Geoparser over QType1
correct_places_Q1 = []

for index, i in enumerate(Q1_places_list):
    a = [m[1] for m in uk_gazetter_all_list if m[0] ==i[0][0] ][0]
    
    correct_places_Q1.append(a)

# correct_places_Q1 = [i[0][2] for i in Q1_places_list]

correct_entities_Q1 = []


with open(cd_pickle+ 'Extracted_placesQ1_DP.pickle' , 'rb') as f:
        Extracted_placesQ1_DP = pickle.load(f)

Extracted_placesQ1_DP = Extracted_placesQ1_DP[0]

    # ## Extract places: DeepPavlov

    # Extracted_placesQ1_DP.append(extract_place_names_deepPavlov(QType1[-1]))
    
    ## post-process and Check detection accuracy
for index,i in enumerate(Extracted_placesQ1_DP):
    
    if (i != []):
        
        Extracted_placesQ1_DP_pos = i[0].lstrip('the ')
        
        if (Extracted_placesQ1_DP_pos == correct_places_Q1[index]):
            
                
            correct_entities_Q1.append(Extracted_placesQ1_DP_pos)
            
        else:
            correct_entities_Q1.append('')
        
    
    else:
        correct_entities_Q1.append('')
        

for i in correct_entities_Q1: 
    
    with open(cd_pickle + 'correct_entities_Q1.txt', 'w') as f:
        f.write(i)   

        
        
#############  3. Run ProbCog over Q1 questions
cd_certain = '/Users/mkazemi/PhD /RMIT - PhD Works/Papers/QSR journal paper/Implementation/Stage 2 - Made up questions and real evidence sets/Results/ProbCog_Q1_CertainEvidence/'
cd_uncertain = '/Users/mkazemi/PhD /RMIT - PhD Works/Papers/QSR journal paper/Implementation/Stage 2 - Made up questions and real evidence sets/Results/ProbCog_Q1_UncertainEvidence/generatedrelationsProbcogQ1-RCC5-uncertain.pickle'

with open(cd_certain +'AnswersQ1-RCC-ProbCog.pickle' , 'rb') as f:
        inference_results_probcog_Q1_certain = pickle.load(f)



#############  3.1. Postprocess probcog results in the form of (place1, place2, SR, probability)

inference_results_probcog_Q1_certain2 = []

for i in inference_results_probcog_Q1_certain:
    test = []
    for j in i:
        
        a = j[0].replace('rcc','').replace('(','').replace(')','').split(',')
        
        test.append(a + [j[1]])
        
    inference_results_probcog_Q1_certain2.append(test)
    

#############  3.2. Retunrning highest probabiliy value relation 

max_inference_results_probcog_Q1_certain2 =[max(i, key=lambda x: x[-1]) for i in inference_results_probcog_Q1_certain2]
    
b = []
for index, i in enumerate(a):
    if i[-2] != Q1_places_list[index][0][-1].upper() :
        b.append(i)
    else:
        b.append('')   
        
        

############ 4. SparQ reasoning 


############ 4.1. Preparing query sentences in the format of triple (Place, sr, place) for SparQ on Linux #############


evidenceset_sparq = []

for index, i in enumerate(Evidence_db):
    current = ''
    
    for j in i:
        
        if (j[-1] in rcc5_9im_map.keys()):
            current += '('+ str(j[0])+ ' (' + j[-1]+ ') ' + str(j[1])+ ")" 

        elif (j[-1] in rcc5_9im_map['pp']):
            current += '('+ str(j[0])+ ' (pp) ' + str(j[1])+ ")" 
        
        elif (j[-1] in rcc5_9im_map['ppi']):
            current += '('+ str(j[0])+ ' (ppi) ' + str(j[1])+ ")" 
            
        elif ( j[-1] == rcc5_9im_map['dr']):
            current += '('+ str(j[0])+ ' (dr) ' + str(j[1])+ ")" 
        
        elif ( j[-1] == rcc5_9im_map['po']):
            current += '('+ str(j[0])+ ' (po) ' + str(j[1])+ ")" 
            
        elif ( j[-1] == rcc5_9im_map['eq']):
            current += '('+ str(j[0])+ ' (eq) ' + str(j[1])+ ")" 
        
        else:
            current += ''

    evidenceset_sparq.append(['"('+current+')"'])


with open(cd_pickle+ 'evidenceset_sparq.pickle', 'wb') as f:
    pickle.dump([evidenceset_sparq], f,protocol=2)

############# 4.2. Run SparQ over evidence sets


############## 4.3. Postprocess sparq results in the form of (place1, place2, SR)

with open(cd_pickle + 'sparq_outputs_RCC.pickle', 'rb') as f:
    sparq_outputs= pickle.load(f)
    
rcc5_relation = ['pp','ppi','dr','eq','po']


# a1 = [['Modified network.\n((74C (pp) Sc)(En (dr eq po pp ppi) Sc)(En (dr eq po pp ppi) 74C)(156C (dr eq po pp ppi) Sc)(156C (dr eq po pp ppi) 74C)(156C (pp) En)(49410 (dr eq po pp ppi) Sc)(49410 (dr eq po pp ppi) 74C)(49410 (pp) En)(49410 (pp) 156C)(246632 (dr eq po pp ppi) Sc)(246632 (dr eq po pp ppi) 74C)(246632 (dr eq po pp ppi) En)(246632 (dr eq po pp ppi) 156C)(246632 (dr eq po pp ppi) 49410)(135181 (pp) Sc)(135181 (pp) 74C)(135181 (dr eq po pp ppi) En)(135181 (dr eq po pp ppi) 156C)(135181 (dr eq po pp ppi) 49410)(135181 (dr eq po pp ppi) 246632)(247 (po pp) Sc)(247 (po pp) 74C)(247 (po pp) En)(247 (po pp) 156C)(247 (po) 49410)(247 (po) 246632)(247 (po) 135181))']]
inference_results_sparq = []
for index1, m in enumerate(sparq_outputs[0]):
        
    b = [i.split() for i in m]
    p2 = []
    p1 = []
    
    rel = ''
    for index, i in enumerate(b):
        for index, j in enumerate(i):
            
            if (index>1):
                if (j.replace("(", "").replace(")","") not in rcc5_relation):
                    
                    if p1 == []:
                        p1 = j.replace("(", "")
                        p2 = []
                    elif (len([i for i in j.split("(") if  i !='']) > 1):
                        p2 = j.split("(")[0].replace(")","")
                        
                        # p1 = re.findall(r'\d+', i)[1]
                        inference_results_sparq.append([p1, p2, rel.rstrip(' '),index1+1])
                        rel = ''
                        p1 = j.split("(")[1]
                    else:
                        p2 = [i for i in j.split(")") if  i !=''][0]
                        inference_results_sparq.append([p1, p2, rel.rstrip(' '),index1+1])
                        p1 = []
                        rel = ''
                        p2= []
                        
                else:
                    rel +=j.replace("(", "").replace(")","")+' '
                    

inference_results_sparq_probability = []
for i in inference_results_sparq:
    
    probability = round(1/len(i[2].split(' ' )),2)
    
    inference_results_sparq_probability.append(i + [probability])



############## 4.4. Assigning cardinal probabilities to SparQ answers

inference_results_sparq_Q1_probability = []

for index,i in enumerate(Q1_places_list):
    
    
    a = [m for m in inference_results_sparq_probability if m[-2] ==index+1 and (m[0] == str(i[0][0])) and (m[1] == str(i[0][1]))][0]
    
    inference_results_sparq_Q1_probability.append(a)
    

######## 5. Comparision SparQ and ProbCog for Qtype1


#### output: (place 1, place 2, correct relation, probcog probability, sparq probability)


comparison_results_Q1 = []

for index, i in  enumerate(Q1_places_list):
    
    if ( i[0][-1] in inference_results_sparq_Q1_probability[index][2].split(' ')):
        
        sparq_probability = inference_results_sparq_Q1_probability[index][-1]
        
    else:
        
        sparq_probability = 0
    
    probcog_probablility = [m[-1] for m in inference_results_probcog_Q1_certain2[index] if 
                            m[0] == str(i[0][0]) and m[1] == str(i[0][1]) and m[2] == i[0][-1].upper() ][0]
    
    comparison_results_Q1.append((i[0][0], i[0][1], i[0][-1], probcog_probablility,sparq_probability))


import csv

# cd = '/Users/mkazemi/PhD /RMIT - PhD Works/Papers/QSR journal paper/Implementation/Stage 2 - Made up questions and real evidence sets/Results/ProbCog_Q1_UncertainEvidence/'
with open(cd_certain + 'Comparison_Q1_certain2.csv', "wt") as fp:
    
    writer = csv.writer(fp, delimiter=",")
    # writer.writerow(["your", "header", "foo"])  # write header
    writer.writerows(comparison_results_Q1)


    
######## 2. QType2 questions

    
# Q2_places = [i for index, i in enumerate(incident_relations_check) if Q1_places_list[index] not in i[0]]

QType2 = []


Q2_SR_list = []

for index, i in enumerate(Q1_places_list):
    
    Q2_SR = random.sample([i for i in NL if i not in  ['part of', 'equal']], 1)
    Q2_SR_list.append(Q2_SR[0])
    
    #Q2_places = [i for i in  incident_relations_check[index] if i not in Q1_places_list[index]]


   
    #Q2_places_list.append(Q2_places)


    if (Q2_SR[0] == 'border' or Q2_SR[0] == 'intersect'):
    
        QType2.append('Which regions '+  Q2_SR[0] + ' with the incident?')
     
        
   
    elif (Q2_SR[0] =='in' or Q2_SR[0] =='inside' or Q2_SR[0] =='within'):
        
        QType2.append('In which regions the incident is located in?')
    
    else:
        
        QType2.append('Which regions are '+  Q2_SR[0] + ' the incident?')



with open(cd_pickle+ 'Q2_SR_list.pickle', 'wb') as f:
    pickle.dump([Q2_SR_list], f,protocol=2)
    
######## 2. Run ProbCog over QType2


######## 3. ProbCog post_processing

cd_q2_certain = '/Users/mkazemi/PhD /RMIT - PhD Works/Papers/QSR journal paper/Implementation/Stage 2 - Made up questions and real evidence sets/Results/ProbCog_Q2_Certain/AnswersQ2-RCC-ProbCog-Certain.pickle'

with open(cd_q2_certain , 'rb') as f:
        inference_results_probcog_Q2_certain = pickle.load(f)
    


#############  3.1. Postprocess probcog results in the form of (place1, place2, SR, probability)

inference_results_probcog_Q2_certain2 = []

for i in inference_results_probcog_Q2_certain:
    test = []
    for j in i:
        
        b = [(k,v) for k,v in j.items()][0]
        a = b[0].replace('rcc','').replace('(','').replace(')','').split(',')
        
        test.append(a + [b[1]])
    test1 = [(int(i[0]),int(i[1]),i[2],i[3]) for i in test]    
    inference_results_probcog_Q2_certain2.append(test1)


inference_results_probcog_Q2_certain3 = []



for index, i in enumerate(inference_results_probcog_Q2_certain2):

    
    a = []
    for j in i:
        
        if (j[0] in evidence_places_unique_unknown[index] and
            j[-2] ==Q2_SR_list_rcc[index]):
            
            a.append(j)
    
    if (len(a) > 6):
        
        n = len(a) - 6
        inference_results_probcog_Q2_certain3.append(a[n:])
    else:
        inference_results_probcog_Q2_certain3.append(a)



#############  4. Postprocess SparQ results for QType2

aaa = []
evidence_places_unique_unknown = []
for index,i in enumerate(Evidence_db):
    evidence1 = []
    evidence2 = []
    for j in i:
        
        evidence1.append(j[0])
        evidence2.append(j[1])
        
    evidence12 = list(set(evidence1+evidence2))
    
    evidence_places_unique_unknown1 = [i for i in evidence12 if i not in [m[0] for m in incident_relations2[index]] and i != 260000]

    evidence_places_unique_unknown.append(evidence_places_unique_unknown1)

      

inference_results_sparq_Q2_probability = []
for index,i in enumerate(evidence_places_unique_unknown):
    
    b = []
    for j in i:
        
        b += [m for m in inference_results_sparq_probability if (m[-2] == index+1)
                     and m[0] == str(j) and m[1] == '260000'
                     or m[1] == str(j) and m[0] == '260000' ]
        
        
    inference_results_sparq_Q2_probability.append(b)
    

#############  5. calculating magnitude of difference

magnitude_q2 = []
for index, i in enumerate(inference_results_probcog_Q2_certain3):
    mag = 0
    for index1, j in enumerate(i):
        
        mag += j[-1] - inference_results_sparq_Q2_probability[index][index1][-1]
    
    
    magnitude_q2.append(mag/6)

    
    
################ 5. Extracting actual answers for QType2

with open(cd_pickle + 'countries_incident_rel.pickle', 'rb') as f:
    countries_incident_rel= pickle.load(f)
    
countries_incident_rel = countries_incident_rel[0]

countries_incident_rel_id = []

for i in countries_incident_rel:
    b = []
    for j in i:
        
        m = [s[-1] for s in place_types_list if s[3] == j[0]]
        
        if (m !=[]):
            b.append((m[0], j[1], j[2]))
        else:
            b.append(j)
    
    countries_incident_rel_id.append(b)
    
    



def find_actual_relation (place1_id, place2_id, config_index):
    
    
    all_relations = counties_incident_rel_id+ districts_incident_rel_id+countries_incident_rel_id +ua_incident_rel_id +incident_relations_check
    
    test = all_relations[index:index+1] + all_relations[(index+1000):(index+1001)] +all_relations[(index+2000):(index+2001)] + all_relations[(index+3000):(index+3001)] + all_relations[(index+4000):(index+4001)]  
          
    for i in test:
        
        for j in i:
            
            if ( place1_id == j[0] and place2_id ==j[1]) or ( place1_id == j[1] and place2_id == j[0]):
                return j
                break
            
            
NL_rcc = {'in': 'PPI', 'inside': 'PPI', 'within':'PPI', 'part of':'PPI','border':'DR', 'disjoint from':'DR',
     'intersect':'PO', 'equal':'EQ'}   

Q2_SR_list_rcc = [NL_rcc[i] for i in Q2_SR_list]         
        
actual_places_Q2 = []       
for index,i in enumerate(evidence_places_unique_unknown):
    a = []
    for j in i:
        
        if (find_actual_relation(j, 260000,index)[-1].upper() == Q2_SR_list_rcc[index]):
            a.append(find_actual_relation(j, 260000,index))
    
    actual_places_Q2.append(a)
    
with open(cd_pickle+ 'actual_places_Q2.pickle', 'wb') as f:
    pickle.dump([actual_places_Q2], f,protocol=2)
    
    
comparison_results_Q2 = []

for index,i in enumerate(actual_places_Q2):
    a = []
    if i !=[]:
        for j in i:
            
            sparq_probability =[m[-1] for m in inference_results_sparq_Q2_probability[index] if j[-1] in m[2].split(' ') and  m[0] ==str(j[0]) and m[1] ==str(j[1])]
            probcog_probability = [m[-1] for m in inference_results_probcog_Q2_certain3[index] if m[0] ==j[0] and m[1] ==j[1]]

            if sparq_probability !=[] :
                
                a.append((str(j[0]),str(j[1]),Q2_SR_list_rcc[index], probcog_probability[0],sparq_probability[0]))
            
            else:
                a.append((str(j[0]),str(j[1]),Q2_SR_list_rcc[index], probcog_probability[0],0))

        comparison_results_Q2.append(a)
    else:
        
        comparison_results_Q2.append('')
        

comparison_metric_Q2 = []

for index,i in enumerate(comparison_results_Q2):
    a = []
    if i != '':
            
        probcog=[m for m in i if m[-2] > m[-1] and m[-2] != m[-1]]
        sparq = [m for m in i if m[-2] < m[-1] and m[-2] != m[-1]]
        
        if (probcog == [] and sparq == []):
            comparison_metric_Q2.append('')
            
        else:
            
            magnitude = [i[-2] -i[-1] for i in probcog +sparq]
            magnitude_avg = sum(magnitude)/len(magnitude)
            
            lenSP = len(probcog) +len(sparq)
        
            comparison_metric_Q2.append((round(len(probcog)/lenSP,2), round(len(sparq)/lenSP,2), round(magnitude_avg,2)))
    
    else:

        
        for j in inference_results_probcog_Q2_certain3[index]:
            
            sparq_find = [i for i in inference_results_sparq_Q2_probability[index] if 
                          i[0] ==str(j[0]) and j[2].lower() in i[2].split(' ')]
            
            if sparq_find !=[]:
                
                a.append((j[0], j[1], j[-1], sparq_find[0][-1]))
                
            else:
                
                a.append((j[0], j[1], j[-1], 0))
        
        probcog=[m for m in a if m[-2] < m[-1] and m[-2] != m[-1]]
        sparq = [m for m in a if m[-2] > m[-1] and m[-2] != m[-1]]
        
        if (probcog == [] and sparq == []):
            comparison_metric_Q2.append('')
            
        else:
            
            magnitude = [i[-1] -i[-2] for i in probcog +sparq]
            magnitude_avg = sum(magnitude)/len(magnitude)
            
            lenSP = len(probcog) +len(sparq)
        
            comparison_metric_Q2.append((round(len(probcog)/lenSP,2), round(len(sparq)/lenSP,2),round(magnitude_avg,2)))
            
        
        # comparison_metric_Q2.append('')
            
            

        
    
######## 3. QType3 questions
 

Q3_place_list = []
QType3 = []
Q3_SR_list = []
actual_answers_Q3 = []

for index, i in enumerate(Q1_places_list):
    
    Q3_SR = random.sample([i for i in NL if i not in  ['part of', 'equal']], 1)
    Q3_SR_list.append(Q3_SR[0])
    
    
    Q3_places = [i for i in  incident_relations_check[index] if i not in Q1_places_list[index]]
    Q3_place_list.append(Q3_places)

    Q3_place_name = [i[1] for i in uk_gazetter_all_list if i[0] ==Q3_places[0][0]][0]
    #Q2_places_list.append(Q2_places)
    
    if Q3_places[0][-1].upper() == NL_rcc[Q3_SR[0]] :
        
        actual_answers_Q3.append((Q3_places[0][0],Q3_places[0][1],Q3_places[0][-1],Q3_SR[0],'YES'))
    else:
        actual_answers_Q3.append((Q3_places[0][0],Q3_places[0][1],Q3_places[0][-1],Q3_SR[0],'NO'))


    if (Q3_SR[0] == 'border' or Q3_SR[0] == 'intersect'):
    
        QType3.append('Does ' + Q3_place_name + ' '+ Q3_SR[0] + ' with the incident?')
        
    elif (Q3_SR[0] =='in' or Q3_SR[0] =='inside' or Q3_SR[0] =='within'):
        
    
        QType3.append('Is the incident ' + Q3_SR[0] + ' '+ Q3_place_name +'?')
     
    
    else:
        
        QType3.append('Is ' + Q3_place_name +' '+ Q3_SR[0] + ' the incident?')

Q3_SR_list_rcc = [NL_rcc[i] for i in Q3_SR_list]         



with open(cd_pickle+ 'Q3_SR_list.pickle', 'wb') as f:
    pickle.dump([Q3_SR_list], f,protocol=2)
    
    


with open(cd_pickle+ 'Q3_place_list.pickle', 'wb') as f:
    pickle.dump([Q3_place_list], f,protocol=2)



######## 2. Geoparser over QType3
correct_places_Q3 = []

for index, i in enumerate(Q3_place_list):
    a = [m[1] for m in uk_gazetter_all_list if m[0] ==i[0][0] ][0]
    
    correct_places_Q3.append(a)

# correct_places_Q1 = [i[0][2] for i in Q1_places_list]

correct_entities_Q3 = []


with open(cd_pickle+ 'Extracted_placesQ3_DP.pickle' , 'rb') as f:
        Extracted_placesQ3_DP = pickle.load(f)

Extracted_placesQ3_DP = Extracted_placesQ3_DP[0]

    # ## Extract places: DeepPavlov

    # Extracted_placesQ1_DP.append(extract_place_names_deepPavlov(QType1[-1]))
    
    ## post-process and Check detection accuracy
for index,i in enumerate(Extracted_placesQ3_DP):
    
    if (i != []):
        
        Extracted_placesQ3_DP_pos = i[0].lstrip('the ')
        
        if (Extracted_placesQ3_DP_pos == correct_places_Q3[index]):
            
                
            correct_entities_Q3.append(Extracted_placesQ3_DP_pos)
            
        else:
            correct_entities_Q3.append('')
        
    
    else:
        correct_entities_Q3.append('')
        

for i in correct_entities_Q3: 
    
    with open(cd_pickle + 'correct_entities_Q3.txt', 'w') as f:
        f.write(i)   

        
        

######## 3.2 Run Probcog over questions
cd_q3_certain = '/Users/mkazemi/PhD /RMIT - PhD Works/Papers/QSR journal paper/Implementation/Stage 2 - Made up questions and real evidence sets/Results/ProbCog_Q3_Certain/AnswersQ3-RCC-ProbCog-Certain.pickle'

with open(cd_q3_certain, 'rb') as f:
    inference_results_probcog_Q3_certain = pickle.load(f)
    

inference_results_probcog_Q3_certain2 = []

for i in inference_results_probcog_Q3_certain:
    test = []
    for j in i:
        
        a = j[0].replace('rcc','').replace('(','').replace(')','').split(',')
        
        test.append(a + [j[1]])
        
    inference_results_probcog_Q3_certain2.append(test)
        
        

######## 3.3 Extracting SparQ generated answers


inference_results_sparq_Q3_probability = []

for index,i in enumerate(Q3_place_list):

        
    b = [m for m in inference_results_sparq_probability if (m[-2] == index+1)
                     and m[0] == str(i[0][0]) and m[1] == '260000'
                     or m[1] == str(i[0][0]) and m[0] == '260000' ]
        
        
    inference_results_sparq_Q3_probability.append(b[0])
    


######## 3.4 Comparision SparQ and ProbCog for Qtype3


comparison_results_Q3 = []

for index, i in  enumerate(Q3_place_list):
    
    if ( Q3_SR_list_rcc[index].lower() in inference_results_sparq_Q3_probability[index][2].split(' ')):
        
        sparq_probability = inference_results_sparq_Q3_probability[index][-1]
        
    else:
        
        sparq_probability = 0
    
    probcog_probablility = [m[-1] for m in inference_results_probcog_Q3_certain2[index] if m[2] == Q3_SR_list_rcc[index] ][0]
    
    
    if (actual_answers_Q3[index][-1] =="YES" and (probcog_probablility> sparq_probability)):
        
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Probcog"))
        
    elif(actual_answers_Q3[index][-1] =="YES" and (probcog_probablility< sparq_probability)):
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Sparq"))
    
    elif(actual_answers_Q3[index][-1] =="YES" and (probcog_probablility==sparq_probability==1)):
        
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Equal 1"))
        
    elif(actual_answers_Q3[index][-1] =="YES" and (probcog_probablility==sparq_probability==0)):
        
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Zero Incorrect"))
    
    elif (actual_answers_Q3[index][-1] =="NO" and (probcog_probablility> sparq_probability)):
        
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Sparq"))
        
    elif(actual_answers_Q3[index][-1] =="NO" and (probcog_probablility< sparq_probability)):
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Probcog"))
    
    elif(actual_answers_Q3[index][-1] =="NO" and (probcog_probablility==sparq_probability==1)):
        
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Equal 1 Incorrect"))
        
    elif(actual_answers_Q3[index][-1] =="NO" and (probcog_probablility==sparq_probability==0)):
        
        comparison_results_Q3.append((i[0][0], i[0][1], Q3_SR_list_rcc[index],
                                  i[0][-1], probcog_probablility,sparq_probability
                                  ,actual_answers_Q3[index][-1], "Zero"))



   
# # comparison_results_Q3 = []

# # for index, i in enumerate(Q3_place_list):
    
    
# #     probcog = [m for m in inference_results_probcog_Q2_certain2[index] if m[0] == str(i[0][0])]
# #     sparq = [m for m in inference_results_sparq_Q2_probability[index] if m[0] == str(i[0][0])]
    
# #     comparison_results_Q3.append((i[0][0],i[0][1],i[0][-1],probcog[0][2:],sparq[0][2:] ))

# # 3.1 Generating Actual answers


# correct_places_Q3 = [i[1] for i in uk_gazetter_all_list if i[0] == Q3_places[0][0] or i[0] == Q3_places[0][1]]

# ## Extract places: DeepPavlov

# Extracted_placesQ3_DP.append(extract_place_names_deepPavlov(QType3[-1]))

# ## post-process and Check detection accuracy
    
# if (Extracted_placesQ3_DP[-1] != []):
    
#     Extracted_placesQ3_DP_pos = [i.lstrip('the ') for i in Extracted_placesQ3_DP[-1]]
    
#     if (len(Extracted_placesQ3_DP_pos)>1):
        
#         if (Extracted_placesQ3_DP_pos[0] in correct_places_Q3 and Extracted_placesQ3_DP_pos[1] in correct_places_Q3):
            
#             correct_entities_Q3.append((correct_places_Q3[0],correct_places_Q3[1]))
        
#         else:
#             correct_entities_Q3.append('')
    
#     else:
#         correct_entities_Q3.append('')

# else:
#     correct_entities_Q3.append('')    

#     ### Qtype4
    
    
#     Q4_random_uknownRelation = random.sample([i for i in unknown_added_relations[index]],1)
    
#     if (Q4_random_uknownRelation[0][1][0] != ''):
#         Q4_random_scale = random.sample([Q4_random_uknownRelation[0][1], Q4_random_uknownRelation[0][2]],1)
#         QType4.append('Which regions are part of ' + Q4_random_scale[0][1] + ' ' + Q4_random_scale[0][0]+'?')
    
#         Q4_places_list.append(Q4_random_scale[0][0])
   

#         correct_places_Q4 = Q4_random_scale[0]
        
#         ## Extract places: DeepPavlov
    
#         Extracted_placesQ4_DP.append(extract_place_names_deepPavlov(QType4[-1]))
        
#         ## post-process and Check detection accuracy
            
#         if (Extracted_placesQ4_DP[-1] != []):
            
#             Extracted_placesQ4_DP_pos = [i.lstrip('the ') for i in Extracted_placesQ4_DP[-1]]
                
#             if (Extracted_placesQ4_DP_pos[0] in correct_places_Q4):
                
#                 correct_entities_Q4.append(Extracted_placesQ4_DP_pos[0])
            
#             else:
#                 correct_entities_Q4.append('')
        
#         else:
#             correct_entities_Q4.append('')
    
#     else:
#          QType4.append('')
#          correct_entities_Q4.append('')


# ##### Storing variables

# # import pickle 
# # with open('QTypes.pickle', 'wb') as f:
# #     pickle.dump([QType1, QType2, QType3,QType4], f




# # with open('Extracted_placesQ.pickle', 'wb') as f:
# #     pickle.dump([Extracted_placesQ1_DP, Extracted_placesQ2_DP, Extracted_placesQ3_DP,Extracted_placesQ4_DP], f)
    
# # with open('correct_entitiesQ.pickle', 'wb') as f:
# #     pickle.dump([correct_entities_Q1, correct_entities_Q2, correct_entities_Q3,correct_entities_Q4], f)


# ##### Reading variables
# # with open('QTypes.pickle', 'rb') as f:
# #     QType1, QType2, QType3, QType4= pickle.load(f)
    
# # with open('Extracted_placesQ.pickle', 'rb') as f:
# #     Extracted_placesQ1_DP, Extracted_placesQ2_DP, Extracted_placesQ3_DP, Extracted_placesQ4_DP= pickle.load(f)

# # with open('correct_entitiesQ.pickle', 'rb') as f:
# #     correct_entities_Q1, correct_entities_Q2, correct_entities_Q3, correct_entities_Q4= pickle.load(f)


# #### Geoparser tool - Deeppavlov


# # Extracted_placesQ1_DP = [extract_place_names_deepPavlov(i) for i in QType1]
# # Extracted_placesQ3_DP = [extract_place_names_deepPavlov(i) for i in QType2]


# # Extracted_placesQ1_DP_pos= []

# # for i in Extracted_placesQ1_DP:
    
# #     if (i != []):
# #         a = []
# #         for j in i:
# #             a.append(j.lstrip('the '))
        
# #         Extracted_placesQ1_DP_pos.append(a)
    
# #     else:
# #         Extracted_placesQ1_DP_pos.append('')


# # Extracted_placesQ3_DP_pos= []

# # for i in Extracted_placesQ3_DP:
    
# #     if (i != []):
# #         a = []
# #         for j in i:
# #             a.append(j.lstrip('the '))
        
# #         Extracted_placesQ3_DP_pos.append(a)
    
# #     else:
# #         Extracted_placesQ3_DP_pos.append('')





# import pickle 
# with open('evidenceset_sparq.pickle', 'wb') as f:
#     pickle.dump([evidenceset_sparq], f)

# # with open('evidenceset_sparq.pickle', 'wb') as f:
# #     pickle.dump(evidenceset_sparq, f, protocol=2)


# with open('evidenceset_sparq.pickle', 'rb') as f:
#     evidenceset_sparq = pickle.load(f)

# ### Answer Extraction


# ### QType-1
# # relation_map = {'pp':['cs','cb','vs','vb'] , 'dr':'di','po':'ov','eq':'eq'}

# answers_Q1 = []
# correct_relations_Q1 = []

# for index, k in enumerate(correct_entities_Q1):
    
#     correct_relations_Q1.append([i for i in zoi_relations_list \
#                                   if (i[0] ==Q1_places_list[index][0][0]\
#                                  and i[1] ==Q1_places_list[index][0][1]) or \
#                                      (i[0] ==Q1_places_list[index][0][1]\
#                                     and i[1] ==Q1_places_list[index][0][0])][0][-1])
#     if ( k != ''):
#         # p1 = [i[0] for i in uk_gazetter_all_list if i[1] == k[0][0]]
#         # p2 = [i[0] for i in uk_gazetter_all_list if i[1] == k[0][1]]
        
        
        
#         extracted_relation_Q1 = [i for i in inference_results \
#                                   if (i[0] ==str(Q1_places_list[index][0][0]) \
#                                     and i[1] ==str(Q1_places_list[index][0][1])\
#                                     and i[3] == index+1) or \
#                                     (i[0] ==str(Q1_places_list[index][0][1]) \
#                                       and i[1] ==str(Q1_places_list[index][0][0])\
#                                       and i[3] == index+1)]
   
    
#         if (r9im_rcc5_map[correct_relations_Q1[index]] == extracted_relation_Q1[0][2]):
#             answers_Q1.append((extracted_relation_Q1[0][0],extracted_relation_Q1[0][1],\
#                                k[0], k[1],extracted_relation_Q1[0][2],\
#                                extracted_relation_Q1[0][3],\
#                             r9im_rcc5_map[correct_relations_Q1[index]],'correct_exact match'))
                
#         elif (len(extracted_relation_Q1[0][2].split()) >3):
#             answers_Q1.append((extracted_relation_Q1[0][0],extracted_relation_Q1[0][1],\
#                                k[0], k[1],extracted_relation_Q1[0][2],\
#                                extracted_relation_Q1[0][3],\
#                             r9im_rcc5_map[correct_relations_Q1[index]] , 'uninformative'))
                
#         elif (r9im_rcc5_map[correct_relations_Q1[index]] in extracted_relation_Q1[0][2] and \
#              len(extracted_relation_Q1[0][2].split()) <4 ):
#             answers_Q1.append((extracted_relation_Q1[0][0],extracted_relation_Q1[0][1],\
#                                k[0], k[1],extracted_relation_Q1[0][2],\
#                                extracted_relation_Q1[0][3],\
#                             r9im_rcc5_map[correct_relations_Q1[index]] , 'correct_partially match'))
                
#         else:
#             answers_Q1.append((extracted_relation_Q1[0][0],extracted_relation_Q1[0][1],\
#                                k[0], k[1],extracted_relation_Q1[0][2],\
#                                extracted_relation_Q1[0][3],\
#                             r9im_rcc5_map[correct_relations_Q1[index]] , 'incorrect'))
            
                
#     else:
#         answers_Q1.append('')
        

# ### QType-2
# # NL = ['in', 'inside','within','part of','border','disjoint from','intersect','equal']

# NL_rcc5_relation = {'in':'pp','inside':'pp', 'within':'pp','part of':'pp',\
#                     'border':'dr','intersect':'po','disjoint from':'dr','equal':'eq'}

# answers_Q2 = []

# for index, k in enumerate(correct_entities_Q2):
    

#     if ( k !=''):
        

#         if ( NL_rcc5_relation[Q2_SR_list[index]] == 'pp'):
            
#             extracted_placesQ2 = [i for i in inference_results if \
#                                   ((i[0] ==str(Q2_places_list[index][0])\
#                                    and 'ppi' in i[2].split() \
#                                    and i[3] == index+1\
#                                    and len(i[2])<4) or 
                                      
#                                    (i[1] ==str(Q2_places_list[index][0])\
#                                       and 'pp' in i[2].split() \
#                                       and i[3] == index+1\
#                                       and len(i[2]) < 4))]
               
             
#         elif  ( NL_rcc5_relation[Q2_SR_list[index]] == 'po'):
            
#             extracted_placesQ2 = [i for i in inference_results if \
#                                   (i[0] ==str(Q2_places_list[index][0]) or \
#                                    i[1] ==str(Q2_places_list[index][0])) and \
#                                    'po' in i[2].split() and \
#                                    i[3] == index+1]
                
#         elif  ( NL_rcc5_relation[Q2_SR_list[index]] == 'dr'):
            
#             extracted_placesQ2 = [i for i in inference_results if \
#                                   (i[0] ==str(Q2_places_list[index][0]) or \
#                                    i[1] ==str(Q2_places_list[index][0])) and \
#                                    'dr' in i[2].split() and \
#                                    i[3] == index+1]
                
#         else:
             
#             extracted_placesQ2 = [i for i in inference_results if \
#                                    (i[0] ==str(Q2_places_list[index][0]) or \
#                                     i[1] ==str(Q2_places_list[index][0])) and \
#                                     'eq' in i[2].split() and \
#                                     i[3] == index+1]       
        
#         for i in extracted_placesQ2:
            
#             if ( i !=[]):
                
#                 if len(i[2].split()) < 4:
                
#                     answers_Q2.append((i, Q2_places_list[index][0], NL_rcc5_relation[Q2_SR_list[index]],index+1 ))
#                 else:
                
#                     answers_Q2.append((i, Q2_places_list[index][0], NL_rcc5_relation[Q2_SR_list[index]],index+1, 'uninformative'))
#             else:
#                 answers_Q2.append('')
# a=  []
# for m in range(0,1000):
#     s = [i[0] for i in answers_Q2 if i[0][3] == m+1]        
#     a.append(s)

# correct_placesQ2 = []
# for index,m in enumerate(correct_entities_Q2):
    
    
#     if  (NL_rcc5_relation[Q2_SR_list[index]] =='pp'):
        
        
#         s = [i for i in evidence_sets2[index] if (i[3]==m) and (i[5]=='cb' or i[5] =='vb') \
#              or (i[2]==m) and (i[5]=='cs' or i[5] == 'vs')]
                
#     elif (NL_rcc5_relation[Q2_SR_list[index]] =='dr'):
       
#         s = [i for i in evidence_sets2[index] if (i[2]==m or i[3]==m) and i[5] =='di']
       
#     elif (NL_rcc5_relation[Q2_SR_list[index]] =='po'):
       
#         s = [i for i in evidence_sets2[index] if (i[2]==m or i[3]==m) and i[5] == 'ov']
       
#     else:           
#         s = [i for i in evidence_sets2[index] if (i[2]==m or i[3]==m) and i[5] =='eq']
           
#     correct_placesQ2.append(s)
    
    
    
    