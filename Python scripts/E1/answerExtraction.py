
# import extracted outputs from SparQ

with open('GeneraatedRelations.pickle', 'rb') as f:
    generatedRelations= pickle.load(f)


## post-process conventional reasoner answers

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

## Evaluation of answers

Allrelations = 'e eq n ne nw s se sw w'


## Finding relation in conventional reasoner

answerQT1_equ1 = [find_equivalent_relation(i) for i in answerQT1]

answerQT1_equ = [(str(i[0][0]), str(i[0][1]), relation_dic[i[0][2]]) for i in answerQT1_equ1]


Exact_matchQ1 = [i for index, i in enumerate(generated_answersQ1) if i==answerQT1_equ[index]]

PartofAnswerQ1 = [i for index, i in enumerate(generated_answersQ1) if (i !='' and i !=answerQT1_equ[index]) if (i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and answerQT1_equ[index][2] in i[2].split()) and i[2] != Allrelations]

AllrelationsAnswerQ1= [i for index, i in enumerate(generated_answersQ1) if (i !='' and i !=answerQT1_equ[index]) if (i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and i[2] == Allrelations)]

NotMatchAnswerQ1 = [i for index, i in enumerate(generated_answersQ1) if (i !='' and i !=answerQT1_equ[index]) if (i[0]==answerQT1_equ[index][0] and i[1]==answerQT1_equ[index][1] and answerQT1_equ[index][2] not in i[2].split())]

## Finding relation in probabilistic reasoner


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
            

## Finding features in conventional reasoner


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


## Finding features in probabilistic reasoner


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
                 
## Yes/no in conventional reasoner


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

## Yes/no in probabilistic reasoner

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
        
