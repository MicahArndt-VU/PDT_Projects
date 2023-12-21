import pandas as pd
import random
import datetime

#Helper Functions
def compute_Average(id, average):
    return average[id][0]/average[id][1]

#Read in a flat file
#DataStream = open("data.csv", 'r')
output = pd.DataFrame()

#Spoof Data for testing
ids = [101, 102, 103, 104]
possible_weather = ['sunny', 'overcast', 'rainy']
id_Stream = [random.choice(ids) for i in range(100)]
temperatures = [random.uniform(50,70) for i in range(100)]
ob_times = [datetime.datetime.now() + datetime.timedelta(minutes=random.randrange(-60, 60)) for i in range(100)]
weather = [random.choice(possible_weather) for i in range(100)]

#Process each line of the file
#Create a dictionary of max temperatures for a given region
maxTemp = {}
#Create a dictionary for computing average temperature for a region
avgTemp = {}
outputDict = {}
for record in range(100):
    #pull line from "file"
    id = id_Stream[record]
    temp = temperatures[record]
    ob = ob_times[record].time()
    w = weather[record]
    #Process the file
    #Check to update Max temp
    if (id in maxTemp):
        if maxTemp[id] < temp:
            maxTemp[id] = temp
            #print('Max Temperature for region ' + str(id) + ' is now ' + str(temp))
    else:
        maxTemp[id] = temp
    if (id not in avgTemp):
        avgTemp[id] = [temp, 1]
    else:
        avgTemp[id] = [avgTemp[id][0] + temp, avgTemp[id][1] + 1]
        #print('Average temp for region ' + str(id) + ' is currently ' + str(compute_Average(id, avgTemp)))

    #Check if id is in the data table
    if id not in outputDict:
        outputDict[id] = [temp, ob, w]
    else:
        print("Record currently exists. Current Observed time: " + str(outputDict[id][1]))
        print("New Observation time: " + str(ob))

        if (outputDict[id][1]) < ob:
            print("Data is newer- Updating table")
            print()
            outputDict[id] = [temp, ob, w]
        else:
            print()

output = pd.DataFrame(outputDict)
print(output.to_string())
print()

for region in ids:
    print('Max Temperature for region ' + str(region) + ' is ' + str(maxTemp[region]))
    print('Average temp for region ' + str(id) + ' is ' + str(compute_Average(id, avgTemp)))
    print()

