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
        
############################# Stage 2: Question Genertation (4Types)  #####################################

######## 1. finding relation questions

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

   