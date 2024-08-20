#

from mlnQueryTool import MLNInfer
import pickle

cd = '~/rcc8/'
inf = MLNInfer()
mlnFiles = [cd + 'rule.mln']

# with open('E:/sharefolder/querysentencesQ1Q3DP.pickle', 'rb') as f:
#    query_sentencesQ1,query_sentencesQ3 = pickle.load(f)
# 
# with open('E:/sharefolder/generatedrelationsProbcogQ3-Allen.pickle', 'rb') as f:
#    QT3_probcog_allen = pickle.load(f)
# 
# with open('E:/sharefolder/relationlistsQ2Q3.pickle', 'rb') as f:
#    relationslistQ2,relationslistQ3 = pickle.load(f)
# 
# with open('E:/sharefolder/KeyPlaces.pickle', 'rb') as f:
#    keyplaces = pickle.load(f)

##### Rcc-8 inference result - demonstration example

with open('districts_list.pickle', 'rb') as f:
   districts_list = pickle.load(f)

output_filename = cd + 'results.txt'

generatedRelations = []
for i in districts_list[0]:

    db = cd + 'evidence-rcc8.txt'
        # queries = 'at(' + str(query_sentencesQ3[index][0]) +',' + str(query_sentencesQ3[index][1])+',' + 'rel)'
        # result = inf.run(mlnFiles, db, "MC-SAT", queries, "PyMLNs", output_filename,
        #                          saveResults=True, maxSteps=20)
    queries = 'at(22785, rel, ' + str(i[0]) + ')'
    result = inf.run(mlnFiles, db, "MC-SAT", queries.encode('utf-8'), "J-MLNs", output_filename,
                                 saveResults=True, maxSteps=10)
    generatedRelations.append(result)

    with open('generatedrelationsProbcogRcc.pickle', 'wb') as f:
        pickle.dump(generatedRelations, f, protocol=2)

    print('yes')


#### QT1 Reasoning


##Deeppavlov  QT1 reasoning
QT1_probcog_DP =[]

for i in range(0,1000):
    if (query_sentencesQ1[i] !='' and QT1_probcog_allen[i] !=''):
        QT1_probcog_DP.append(QT1_probcog_allen[i])
    elif (query_sentencesQ1[i] !='' and QT1_probcog_allen[i] ==''):
        db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(i) + '.txt'
        queries = 'at(' + str(query_sentencesQ1[i][0]) +',' + str(query_sentencesQ1[i][1])+',' + 'rel)'
        result = inf.run(mlnFiles, db, "MC-SAT", queries, "PyMLNs", output_filename,
                                 saveResults=True, maxSteps=20)
        if result is not None:
            QT1_probcog_DP.append(result)
        else:
            QT1_probcog_DP.append('')
    else:
        QT1_probcog_DP.append('')

    with open('E:/sharefolder/generatedrelationsProbcogQ1-DP.pickle', 'wb') as f:
        pickle.dump(QT1_probcog_DP, f, protocol=2)

###### QT3 reasoning Deeppavlov
QT3_probcog_DP =[]

for index, i in enumerate(relationslistQ3):
    if (query_sentencesQ3[index] !='' and QT3_probcog_allen[index] !=''):
        QT3_probcog_DP.append(QT3_probcog_allen[index])
    elif (query_sentencesQ3[index] !='' and QT3_probcog_allen[index] ==''):
        db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(index) + '.txt'
        # queries = 'at(' + str(query_sentencesQ3[index][0]) +',' + str(query_sentencesQ3[index][1])+',' + 'rel)'
        # result = inf.run(mlnFiles, db, "MC-SAT", queries, "PyMLNs", output_filename,
        #                          saveResults=True, maxSteps=20)
        queries = 'at(' + str(query_sentencesQ3[index][0]) + ',' + str(query_sentencesQ3[index][1]) + ',' + i[2].upper() + ')'
        result = inf.run(mlnFiles, db, "MC-SAT", queries.encode('utf-8'), "PyMLNs", output_filename,
                                 saveResults=True, maxSteps=20)
        if result is not None:
            QT3_probcog_DP.append(result)
        else:
            QT3_probcog_DP.append('')
    else:
        QT3_probcog_DP.append('')

    with open('E:/sharefolder/generatedrelationsProbcogQ3-DP.pickle', 'wb') as f:
        pickle.dump(QT3_probcog_DP, f, protocol=2)

    ### QT2 reasoning
    QT2results = []
    k = 100
    for index,i  in enumerate(relationslistQ2[148:]):
        db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(index+148) + '.txt'
        result  ={}
        for  j in keyplaces[index+148]:
            queries = 'at(' + str(j) +',' + str(501)+',' + i.upper()+ ')'
            test = inf.run(mlnFiles, db, "MC-SAT", queries.encode('utf-8'), "PyMLNs", output_filename,
                             saveResults=True, maxSteps=20)
            if test is not None:
                result.update(test)

        if test is not None:
            QT2results.append([result])
        else:
            QT2results.append('')

        print('QT2 index:' + str(k))
        k  = k+1
    with open('E:/sharefolder/generatedrelationsProbcogQ2-148-Allen.pickle', 'wb') as f:
        pickle.dump(QT2results, f, protocol=2)
