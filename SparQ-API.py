
import subprocess
import pickle
import re


with open('certainset_sparq.pickle', 'rb') as f:
    certainset_sparq= pickle.load(f)

certainE = certainset_sparq

sparqC = "/home/mohammad/Desktop/SparQ-master/sparq constraint-reasoning cardir algebraic-closure"
sparq_outputs = []
for index, i in  enumerate(certainE[0]):

	
	sparq_command = sparqC+ i[0]

	sparq_run= subprocess.Popen (sparq_command, shell=True, stdout=subprocess.PIPE).communicate()[0].rstrip().decode("utf-8")
	sparq_outputs.append([sparq_run])
	#print(sparq_command)

#print(test)	

sparq_outputs_split= [i[0].split() for i in sparq_outputs]
p2 = []
p1 = []
generatedRelations = []
rel = ''
for index, i in enumerate(sparq_outputs_split):
    for index, j in enumerate(i):
        
        if (index>1):
            if (re.findall(r'\d+', j) !=[]):
                
                if p1 == []:
                    p1 = re.findall(r'\d+', j)[0]
                    p2 = []
                elif (len(re.findall(r'\d+', j)) >1):
                    p2 = re.findall(r'\d+', j)[0]
                    # p1 = re.findall(r'\d+', i)[1]
                    generatedRelations.append([p1, p2, rel])
                    rel = ''
                    p1 = re.findall(r'\d+', j)[1] 
                else:
                    p2 = re.findall(r'\d+', j)[0]
                    generatedRelations.append([p1, p2, rel])
                    p1 = []
                    rel = ''
                    p2= []
                    
            else:
                rel +=j+' '

#print(generatedRelations)

with open('/home/mohammad/Desktop/SparQ-master/GeneraatedRelations.pickle', 'wb') as f:
    pickle.dump([generatedRelations], f)
	 
	 
#a ='/home/mohammad/Desktop/SparQ-master/sparq constraint-reasoning cardir algebraic-closure "((B ne A) (C ne A) (D se A) (E  se A) (C se B) (D se B) (E sw B) (D sw C) (E sw D) (P sw B) (P sw C) (P nw D) (P ne E))"'

#stream = os.popen(a)
#output = stream.read()
#print(output)

