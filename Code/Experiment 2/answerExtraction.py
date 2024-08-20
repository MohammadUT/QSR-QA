
import pandas as pd
import random
import time
import pickle


   
#############  3. Run ProbCog over FR questions
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
    

######## 5. Comparision SparQ and ProbCog for finding relation


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


    
######## 2. finding features question

    
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



#############  4. Postprocess SparQ results for finding features

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

    
    
################ 5. Extracting actual answers for finding features questions

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
            
            

        
    
######## 3. yes/no questions
 

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



######## 3.2 Run Probcog over yes/no questions
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
    


######## 3.4 Comparision SparQ and ProbCog for yes/no questions


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


