#

from mlnQueryTool import MLNInfer
import pickle

cd = 'C:/Users/S3763411/Dropbox/Mohammad/RMIT - PhD Works/Papers/QSR journal paper/mln/probcog/rcc8/'
inf = MLNInfer()
mlnFiles = [cd + 'rule.mln']

##### Rcc-8 inference result - demonstration example

with open('C:/Users/S3763411/Dropbox/Mohammad/RMIT - PhD Works/Papers/QSR journal paper/Implementation/Demonstration examples/districts_list.pickle', 'rb') as f:
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

    with open('C:/Users/S3763411/Dropbox/Mohammad/RMIT - PhD Works/Papers/QSR journal paper/Implementation/Demonstration examples/generatedrelationsProbcogRcc.pickle', 'wb') as f:
        pickle.dump(generatedRelations, f, protocol=2)

    print('yes')
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



# keyplaces = keyplaces[0]
# nn = [(i[0].replace('u',''),i[1].replace('u',''),i[2].replace('u','')) for i in relationslistQ3]
# output_filename = cd + "results.txt"


#### QT1 Reasoning

###AllenNLP
# for i in range(0,1000):
#
#     db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(i) +'.txt'
#     Allresults = []
#     if (query_sentencesQ1[i] !=''):
#         queries = 'at(' + str(query_sentencesQ1[i][0]) +',' + str(query_sentencesQ1[i][1])+',' + 'rel)'
#         result = inf.run(mlnFiles, db, "MC-SAT", queries, "PyMLNs", output_filename,
#                          saveResults=True, maxSteps=20)
#         Allresults.append(result)

##Deeppavlov  QT1 reasoning
# QT1_probcog_DP =[]
#
# for i in range(0,1000):
#     if (query_sentencesQ1[i] !='' and QT1_probcog_allen[i] !=''):
#         QT1_probcog_DP.append(QT1_probcog_allen[i])
#     elif (query_sentencesQ1[i] !='' and QT1_probcog_allen[i] ==''):
#         db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(i) + '.txt'
#         queries = 'at(' + str(query_sentencesQ1[i][0]) +',' + str(query_sentencesQ1[i][1])+',' + 'rel)'
#         result = inf.run(mlnFiles, db, "MC-SAT", queries, "PyMLNs", output_filename,
#                                  saveResults=True, maxSteps=20)
#         if result is not None:
#             QT1_probcog_DP.append(result)
#         else:
#             QT1_probcog_DP.append('')
#     else:
#         QT1_probcog_DP.append('')
#
#     with open('E:/sharefolder/generatedrelationsProbcogQ1-DP.pickle', 'wb') as f:
#         pickle.dump(QT1_probcog_DP, f, protocol=2)
    # #### QT3 Reasoning
    # QT3results = []
    # for index, i  in enumerate(relationslistQ3):
    #
    #     db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(index) +'.txt'
    #     if (query_sentencesQ3[index] !=''):
    #         queries = 'at(' + str(query_sentencesQ3[index][0]) +',' + str(query_sentencesQ3[index][1])+',' + i[2].upper()+ ')'
    #         result = inf.run(mlnFiles, db, "MC-SAT", queries.encode('utf-8'), "PyMLNs", output_filename,
    #                          saveResults=True, maxSteps=20)
    #         QT3results.append(result)
    #     else:
    #         QT3results.append('')
###### QT3 reasoning Deeppavlov
# QT3_probcog_DP =[]
#
# for index, i in enumerate(relationslistQ3):
#     if (query_sentencesQ3[index] !='' and QT3_probcog_allen[index] !=''):
#         QT3_probcog_DP.append(QT3_probcog_allen[index])
#     elif (query_sentencesQ3[index] !='' and QT3_probcog_allen[index] ==''):
#         db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(index) + '.txt'
#         # queries = 'at(' + str(query_sentencesQ3[index][0]) +',' + str(query_sentencesQ3[index][1])+',' + 'rel)'
#         # result = inf.run(mlnFiles, db, "MC-SAT", queries, "PyMLNs", output_filename,
#         #                          saveResults=True, maxSteps=20)
#         queries = 'at(' + str(query_sentencesQ3[index][0]) + ',' + str(query_sentencesQ3[index][1]) + ',' + i[2].upper() + ')'
#         result = inf.run(mlnFiles, db, "MC-SAT", queries.encode('utf-8'), "PyMLNs", output_filename,
#                                  saveResults=True, maxSteps=20)
#         if result is not None:
#             QT3_probcog_DP.append(result)
#         else:
#             QT3_probcog_DP.append('')
#     else:
#         QT3_probcog_DP.append('')
#
#     with open('E:/sharefolder/generatedrelationsProbcogQ3-DP.pickle', 'wb') as f:
#         pickle.dump(QT3_probcog_DP, f, protocol=2)
#
#     ### QT2 reasoning
#     QT2results = []
#     k = 100
#     for index,i  in enumerate(relationslistQ2[148:]):
#         db = 'E:/sharefolder/test/' + 'UncertainEvidenceSet' + str(index+148) + '.txt'
#         result  ={}
#         for  j in keyplaces[index+148]:
#             queries = 'at(' + str(j) +',' + str(501)+',' + i.upper()+ ')'
#             test = inf.run(mlnFiles, db, "MC-SAT", queries.encode('utf-8'), "PyMLNs", output_filename,
#                              saveResults=True, maxSteps=20)
#             if test is not None:
#                 result.update(test)
#
#         if test is not None:
#             QT2results.append([result])
#         else:
#             QT2results.append('')
#
#         print('QT2 index:' + str(k))
#         k  = k+1
#     with open('E:/sharefolder/generatedrelationsProbcogQ2-148-Allen.pickle', 'wb') as f:
#         pickle.dump(QT2results, f, protocol=2)
#
#

#db = ["at(379, 18, SE)", "at(471, 18, SW)"]
#queries = "at(379, 18, rel)"

#allResults = {}

#tasks = (("MC-SAT", "PyMLNs"), ("MC-SAT", "J-MLNs"), ("MC-SAT", "Alchemy - August 2010 (AMD64)"))

#result = inf.run(mlnFiles, db, "MC-SAT", queries, "PyMLNs", output_filename,
                                           #   saveResults=True, maxSteps=5)


#
# for method, engine in tasks:
# 	allResults[(method,engine)] = inf.run(mlnFiles, db, method, queries, engine, output_filename,
#                                               saveResults=True, maxSteps=5000)
#
# for (method, engine), results in allResults.iteritems():
#
# 	print "Results obtained using %s and %s" % (engine, method)
# 	for atom, p in results.iteritems():
# 		print  "  %.6f  %s" % (p, atom)


############another approach
#from MLN import *
# cd = 'C:/Users/S3763411/Dropbox/Mohammad/RMIT - PhD Works/Papers/QSR journal paper/mln/probcog/cdc/'
# mlnFiles = [cd + 'cdc-full.mln']
# db = cd + 'query.db'
#
# mln = MLN(mlnFiles)
#
# mrf = mln.groundMRF(db)
#
# queries = ["at(A,D,rel)"]
# results = mrf.inferMCSAT(queries, verbose=False)
# for query, prob in zip(queries, results):
#     print "  %f  %s" % (prob, query)

