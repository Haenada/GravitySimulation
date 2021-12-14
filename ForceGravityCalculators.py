from SystemLibrary import *
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed


# Working in kg and KM
class CelestialObject:
    def __init__(self, name, mass, loc, velocity):
        self.name = name 
        self.mass = mass #kg
        self.loc = loc # km
        self.velocity = velocity  #km/s
        
  
def newtonsLawComponents(massOne, massTwo, distanceList):
    G = 6.67*10**(-11)*(1000)**-3 
    distanceMagnitude = np.sqrt(distanceList[0]**2 + distanceList[1]**2 + distanceList[2]**2)
    xUnitVector = distanceList[0]/distanceMagnitude
    yUnitVector = distanceList[1]/distanceMagnitude
    zUnitVector = distanceList[2]/distanceMagnitude
    
    forceList = [0,0,0]
    forceList[0] = -((G*massOne*massTwo)/(distanceMagnitude**2))*xUnitVector #x
    forceList[1] = -((G*massOne*massTwo)/(distanceMagnitude**2))*yUnitVector #y
    forceList[2] = -((G*massOne*massTwo)/(distanceMagnitude**2))*zUnitVector #z
    return forceList

def totalForceBody(body, bodyList):
    totalForceList = [0,0,0]
    for i in bodyList:    
        if i.name==body.name:
            continue
        distanceList = [body.loc[0] - i.loc[0], body.loc[1] - i.loc[1], body.loc[2] - i.loc[2]]
        forceList = newtonsLawComponents(body.mass,i.mass,distanceList)
        totalForceList[0] += forceList[0]
        totalForceList[1] += forceList[1]
        totalForceList[2] += forceList[2]
    return [totalForceList, body]

    
def totalForce(bodiesList): 
    rangeLimit = False
    forceList = []
    
    if rangeLimit:
        pass
    else:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(totalForceBody, x, bodiesList) for x in bodiesList]
            
    for future in as_completed(futures):
        forceList.append(future.result())
#returns [[[xforce,yforce,zforce],body1],[[..], body2]] i.e a list of lists, containing a list        
    return forceList


def kickDriftKick(body, bodyList, forceList, timeStep):
    velocityKickInitial = [0,0,0]
    velocityKickInitial[0] = forceList[0]/body.mass * timeStep/2 + body.velocity[0]
    velocityKickInitial[1] = forceList[1]/body.mass * timeStep/2 + body.velocity[1]
    velocityKickInitial[2] = forceList[2]/body.mass * timeStep/2 + body.velocity[2]
    
    positionalDrift = [0,0,0]
    positionalDrift[0] = velocityKickInitial[0] * timeStep
    positionalDrift[1] = velocityKickInitial[1] * timeStep
    positionalDrift[2] = velocityKickInitial[2] * timeStep
    
    intermediateBody = body
    intermediateBody.loc[0] += positionalDrift[0]
    intermediateBody.loc[1] += positionalDrift[1]
    intermediateBody.loc[2] += positionalDrift[2]
    totalForceBodyKick, oldBody = totalForceBody(intermediateBody, bodyList)
    
    velocityKickFinal = [0,0,0]
    velocityKickFinal[0] = totalForceBodyKick[0]/body.mass * timeStep/2 + velocityKickInitial[0]
    velocityKickFinal[1] = totalForceBodyKick[1]/body.mass * timeStep/2 + velocityKickInitial[1]
    velocityKickFinal[2] = totalForceBodyKick[2]/body.mass * timeStep/2 + velocityKickInitial[2]
    
    return CelestialObject(body.name, body.mass,
                           intermediateBody.loc,
                               [velocityKickFinal[0], velocityKickFinal[1], velocityKickFinal[2]])
    

                    
def test():
    totalForce(basicSolarSystem())
    return
def test2():
    totalForceSystem = totalForce(basicSolarSystem())
    for i in totalForceSystem:
        if i[1].name == "Earth":
            forceTest = i
    print("force", forceTest)
    bodyObject = kickDriftKick(basicSolarSystem()[3], basicSolarSystem(), forceTest[0], 3600)
    print(bodyObject.name, bodyObject.loc, bodyObject.velocity)
    return




