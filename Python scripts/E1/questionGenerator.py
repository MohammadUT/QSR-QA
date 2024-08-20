
import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math



#################### Question generation step: generating three QSR questions types: Qtypes 1,2,3 #################

## transfor quantitave data to qualitative knowledge

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
    
    
    
    
pd = pd.read_csv('PlaceNames-500.csv')
points = pd.values.tolist()

## incident point
PlaceP = [[501, 'Place P', round(144.9448852500,6), round(-37.8285522450,6)]]

points = points+PlaceP
relation_dic = {'north':'n', 'northeast':'ne','northwest':'nw','south':'s','southeast':'se','southwest':'sw', 'east':'e', 'west':'w'}


### Generating simulated cardinal questions with their actual answers


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
    


