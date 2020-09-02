from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import math
import matplotlib.pyplot as plt
import random

def main():
    data = []
    segNames = []
    timeSave = []
    pbSplitTime = []
    bestSplitTime = []
    segAttempt = []
    percentReset = []

    #reading the data inside teh xml file to a variable under the name data
    #fileName = "Super Mario 64 - 16 Star.lss"
    fileName = "Pingus Full.lss"

    with open(fileName, 'r') as f:
        data = f.readlines()
        data = "".join(data)

    #passing the stored data inside the beautifulsoup parser, storing the returned object
    bs_data = BeautifulSoup(data, "lxml")

    #passing the path of the xml document to enable the parsing process
    tree = ET.parse(fileName)

    #getting the parent tag of the xml document
    root = tree.getroot()

    segmentCount = 0 #total number of segments
    prevSegTime = 0 #storing the previous segment time to calc current segment time
    sumOfBest = 0 #sum of best time in seconds
    attemptCount = int(root[5].text) #get the total number of attemps
    segAttemptCount = 0 #store the number of completed attempts for each split

    #count the number of segments in the file
    for i in range(0,len(data)):
        if(data[i:i+9] == "<Segment>"):
            segmentCount+=1
            if(segAttemptCount != 0): #to prevent the first instance of segment to add a zero to the start
                segAttempt.append(segAttemptCount)
                segAttemptCount = 0
        if(data[i:i+5] == "<Time"):
            segAttemptCount+=1
    segAttempt.append(segAttemptCount) #to add the last split since no Segment tag following

    #calculate reset percentage for each split
    for r in range(0, segmentCount):
        resetPercent = 0
        if(r == 0):
            resetPercent = (attemptCount-segAttempt[r])/attemptCount
        else:
            resetPercent = (segAttempt[r-1]-segAttempt[r])/attemptCount

        percentReset.append(round_up(resetPercent*100, 3))
            
    print("Total Attempts:",attemptCount)
    print("Total Number of Segments:", segmentCount)

    #calculate the sum of best before calculating the rest of the values
    for j in range(0, segmentCount):
        bestSeg = toSeconds(root[7][j][3][0].text)
        sumOfBest = round_up(sumOfBest + bestSeg, 3)
    
    finalTime = toSeconds(root[7][segmentCount-1][2][0][0].text)
    totalTimeSave = round_up(finalTime-sumOfBest, 3)
    print("Sum Of Best:", sumOfBest)
    print("Total Time Save:", totalTimeSave)

    #get all of the data values
    for x in range(0, segmentCount):
        bestSeg = toSeconds(root[7][x][3][0].text)
        pbSeg = toSeconds(root[7][x][2][0][0].text)
        currSegTime = round_up(pbSeg-prevSegTime, 3)
        segTimeSave = round_up(currSegTime-bestSeg, 3)
        percentTimeSave = round_up((segTimeSave/totalTimeSave)*100, 3)

        segNames.append(root[7][x][0].text)
        timeSave.append(percentTimeSave)
        pbSplitTime.append(pbSeg)
        bestSplitTime.append(bestSeg)
        
        print("Segment Name: " + root[7][x][0].text)
        print("\tBest Time:", bestSeg)
        print("\tPB Time:", currSegTime)
        print("\tTime Save:", segTimeSave)
        print("\t% Time Save:", percentTimeSave, "%")
        print("\tCompleted Attempts:", segAttempt[x])
        print("\t% of Reset:", percentReset[x], "%")
        
        prevSegTime = pbSeg

    #calculate best segment split times overall
    for y in range(1, segmentCount):
        bestSplitTime[y] = round_up(bestSplitTime[y-1]+bestSplitTime[y], 3)

    #create data for best vs pb split time comparison
    bestValues = []
    pbValues = []
    for a in range(0, segmentCount):
        bestValues.append((segNames[a], bestSplitTime[a]))
        pbValues.append((segNames[a], pbSplitTime[a]))

    data = (bestValues, pbValues)

    #display the PB run time
    singleScatterPlotDisplay(segNames, pbSplitTime, "PB Run Time", "Segments", "Time")
    #display the best run time
    singleScatterPlotDisplay(segNames, bestSplitTime, "Best Run Time", "Segments", "Time")
    #display the percentage of time save throughout the Run
    pieChartDisplay(segNames, timeSave, "Percentage Time Save")
    #display the percentage of time resets occur
    pieChartDisplay(segNames, percentReset, "Percentage Reset")
    #display the best splits vs the PB splits on the same plot
    #multipleScatterPlotDisplay(data, ("yellow", "blue"), ("Best", "PB"), "Best vs PB Comparison", "Segments", "Time")

#convert the time as a string into the number of seconds as an int
def toSeconds(string):
    #00:00:05.2960000 is the format of the time as a string
    hours = float(string[0:2])*360
    minutes = float(string[3:5])*60
    seconds = float(string[6:])
    return round_up((hours + minutes + seconds), 3)

#round up float values to three decimal places
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

#display a pie chart
def pieChartDisplay(labels, values, title):
    colors = []
    for item in labels:
        rgb = (random.random(), random.random(), random.random())
        colors.append(rgb)

    #reverse the lists so the values appear clockwise
    values.reverse()
    labels.reverse()

    #plot
    plt.pie(values, labels = labels, colors = colors, startangle = 90)

    plt.axis('equal')
    plt.title(title)
    plt.show()

    #reverse the lists back to original
    values.reverse()
    labels.reverse()

#display one set of data points as a scatterplot
def singleScatterPlotDisplay(labels, values, title, xLab, yLab):
    plt.scatter(labels, values) #put the points on the plot
    plt.plot(labels, values) #put the line on the plot
    plt.title(title)
    plt.xlabel(xLab)
    plt.ylabel(yLab)
    
    plt.show()

#display multiple groups of data on one scatterplot
def multipleScatterPlotDisplay(data, colors, groups, title, xLab, yLab):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for data, color, group in zip(data, colors, groups):
        x, y = data
        ax.scatter(x, y, c=color, label=group)
        
    plt.title(title)
    plt.xlabel(xLab)
    plt.ylabel(yLab)
    plt.show()

if __name__ == "__main__":
    main()
    




