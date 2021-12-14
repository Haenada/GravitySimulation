from SystemLibrary import *
import matplotlib.animation as animation
from ForceGravityCalculators import *
import operator
import matplotlib.pyplot as plt
import numpy as np


from concurrent.futures import ThreadPoolExecutor, as_completed

timeStep = 3600 * 12
runLength = 365*timeStep*2*165

def forceRun(system):
    counter = 0
    savePlots = False
    saveData = True
    for currentTime in np.arange(0, runLength, timeStep):
        if currentTime == 0:
            systemForceList = totalForce(system)
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(kickDriftKick, bdy, system, fList, timeStep) for fList,
                           bdy in systemForceList]
        elif currentTime != 0:
            systemForceList = totalForce(currentSystem)
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(kickDriftKick, bdy, currentSystem, fList, timeStep) for fList,
                           bdy in systemForceList]
            
        currentSystem = []

        for future in as_completed(futures):
            currentSystem.append(future.result())

        if saveData:
            if currentTime == 0:
                storage = [np.zeros((1,8))]*len(currentSystem) #list of arrays
            currentSystem.sort(key=operator.attrgetter("name"))  
            for i in range(len(currentSystem)):
                storage[i] = np.vstack((storage[i], np.array([[currentSystem[i].mass,                     currentSystem[i].loc[0], currentSystem[i].loc[1], currentSystem[i].loc[2],                     currentSystem[i].velocity[0], currentSystem[i].velocity[1]                            , currentSystem[i].velocity[2], currentTime]])))
                    
        if savePlots: 
            if (counter/2 % 182.5) == 0: # for number of imgs 
                colours = ["orange","brown","violet","blue","red","darkred","cyan","green","darkblue","maroon"]
                currentSystem.sort(key=operator.attrgetter("name"))           
                fig = plt.figure(figsize=(7,7))
                ax = fig.add_subplot(projection="3d")
                ax.set_xlim(-6*10**9, 6*10**9)
                ax.set_xlabel("x")
                ax.set_ylim(-6*10**9, 6*10**9)
                ax.set_ylabel("y")
                ax.set_zlim(-6*10**9, 6*10**9)
                ax.set_zlabel("z")
                for i in range(len(currentSystem)):
                    ax.scatter(currentSystem[i].loc[0], currentSystem[i].loc[1], currentSystem[i].loc[2],
                                color=colours[i], label = currentSystem[i].name)
                ax.legend()
                plt.savefig("TestRunForce2/run2_" + str(counter/2) + ".png")
                plt.close()
        counter +=1
    if saveData:
        for i in range(len(currentSystem)):    
            np.savetxt("runData/11_12_21/"+currentSystem[i].name+".txt", storage[i][1:,])    
    return
        
def txtToListOfBodies(fileLocation):
    import os
    bodiesData = os.listdir(fileLocation)
        
    arrayList = []
    for file in bodiesData:
        with open(fileLocation+file) as data:
            array = np.array([[float(digit) for digit in line[1:-1].split()] for line in data])
        arrayList.append(array) 
    return arrayList, bodiesData
      

#Controls   
runForceRun = True
loadTxt = False
animateData = False
    
if runForceRun:
    forceRun(basicSolarSystem())
if loadTxt:
    arrayList, bodiesData = txtToListOfBodies("runData/11_12_21/")
    if animateData:
        fig, ax = plt.subplots()
        ax.set(xlim=(-6E9, 6E9), ylim=(-6E9, 6E9))
        line, = ax.plot([], [], "o", markersize = 5)
        
        def animate(i):
            xList=[]
            yList=[]
            for body in range(len(bodiesData)):
                xList.append(arrayList[body][:,1][i])
                yList.append(arrayList[body][:,2][i])
            line.set_data(xList, yList)  
            return line,
        
        ani = animation.FuncAnimation(fig, animate, np.arange(1, len(arrayList[0])),
            interval=1, save_count=720, blit=True)
        plt.show()


