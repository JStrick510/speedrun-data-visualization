from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import math

def main():
    data = []

    #reading the data inside teh xml file to a variable under the name data
    fileName = "Super Mario 64 - 16 Star.lss"
    #fileName = "Pingus Full.lss"

    with open(fileName, 'r') as f:
        data = f.readlines()
        data = "".join(data)

    #passing the stored data inside the beautifulsoup parser, storing the returned object
    bs_data = BeautifulSoup(data, "lxml")

    #passing the path of the xml document to enable the parsing process
    tree = ET.parse(fileName)

    #getting the parent tag of the xml document
    root = tree.getroot()

    countSegs = 0
    segmentCount = 0
    prevSegTime = 0
    sumOfBest = 0

    for i in range(0,len(data)):
        if(data[i:i+9] == "<Segment>"):
            segmentCount+=1

    print("Total Number of Segments:", segmentCount)

    for j in range(0, segmentCount):
        bestSeg = toSeconds(root[7][j][3][0].text)
        sumOfBest = round_up(sumOfBest + bestSeg, 3)

    finalTime = toSeconds(root[7][segmentCount-1][2][0][0].text)
    totalTimeSave = round_up(finalTime-sumOfBest, 3)
    print("Sum Of Best:", sumOfBest)
    print("Total Time Save:", totalTimeSave)

    for x in range(0, segmentCount):
        bestSeg = toSeconds(root[7][x][3][0].text)
        pbSeg = toSeconds(root[7][x][2][0][0].text)
        currSegTime = round_up(pbSeg-prevSegTime, 3)
        segTimeSave = round_up(currSegTime-bestSeg, 3)
        percentTimeSave = round_up((segTimeSave/totalTimeSave)*100, 3)
        
        print("Segment Name: " + root[7][x][0].text)
        print("\tBest Time:",bestSeg)
        print("\tPB Time:",currSegTime)
        print("\tTime Save:", segTimeSave)
        print("\t% Time Save:", percentTimeSave, "%")
        
        prevSegTime = pbSeg

def toSeconds(string):
    #00:00:05.2960000
    hours = float(string[0:2])*360
    minutes = float(string[3:5])*60
    seconds = float(string[6:])
    return round_up((hours + minutes + seconds), 3)

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

if __name__ == "__main__":
    main()
    




