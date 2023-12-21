import datetime

#Helper function used to fetch all score records
def extractScores():
    scoreInput = []
    file = open("scores.txt", 'r')

    for line in file:
        scoreInput.append(line)
    return scoreInput

"""

Begin with a prototype to simulate batch processing

Bare Bones - No windowing

"""
def bareBatch():
    #Create an array of strings to work with input
    scoreInput = extractScores()

    #Now, we do transformations to extract
    #Create a list of key-value tuples
    KV_score = []
    for record in scoreInput:
        datapoints = record.split(",")
        KV_score.append((datapoints[1], datapoints[2]))

    totals = {}
    #Now add to totals dict
    for item in KV_score:
        if (item[0] in totals.keys()):
            totals[item[0]] += (int) (item[1])
        else:
            totals[item[0]] = (int) (item[1])

    #Print our Batch input
    for key in totals.keys():
        print("Team: ", key, "Point Total: ", totals[key])

"""

Batch Process with windowing. Windows are based in two minute increments on event time

"""
def determineBucket(time, windows):
    for i in range(len(windows)):
        window = windows[i]
        if (time > window[0].time() and time < window[1].time()):
            return i

def windowedBatch():
    scoreInput = extractScores()
    baseTime = datetime.datetime.strptime('12:00:00', "%H:%M:%S")
    maxTime = datetime.datetime.strptime('12:10:00', "%H:%M:%S").time()
    windows = []

    #Set up our window Function
    for i in range(5):
        if len(windows) == 0:
            windows.append((baseTime, (baseTime + datetime.timedelta(0,2))))
        else:
            windows.append((windows[i - 1][1], (windows[i - 1][1] + datetime.timedelta(0,0,0,0,2))))
    KV_score = {}
    #Now, we process our Scores
    for line in scoreInput:
        data = line.split(',')
        score = (int) (data[2])
        team = data[1]
        eventTime = datetime.datetime.strptime(data[3], "%H:%M:%S").time()
        windowIndex = determineBucket(eventTime, windows)
        if (windows[windowIndex] in KV_score.keys()):
            if team in KV_score[windows[windowIndex]].keys():
                KV_score[windows[windowIndex]][team] += score
            else:
                KV_score[windows[windowIndex]][team] = score
        else:
            KV_score[windows[windowIndex]] = {team: score}

    #Print Output
    for key in KV_score.keys():
        for teamKey in KV_score[key].keys():
            print("Event Time Window: ", key[0].time(), " - ", key[1].time(), "\tTeam: ", teamKey, "\tScore: ", KV_score[key][team])

"""

Building off of the above funciton, we are transitioning to a simple streaming process.
We will use triggers for each window so when a new record in the window is found, we then create a new pane

"""
def parseRawData(scoreInput):
    processingData = []
    for line in scoreInput:
        data = line.split(',')
        procTime = datetime.datetime.strptime(data[4].strip(), "%H:%M:%S").time()
        eventTime = datetime.datetime.strptime(data[3].strip(), "%H:%M:%S").time()

        # Create a list of dictionaries with the procTime as the key
        processingData.append({procTime: (data[1], data[2], eventTime, procTime)})
    return processingData

def orderData(dataSet):
    orderedTimeData = []
    for i in range(len(dataSet)):
        item = dataSet[i]
        keys = (list)(item.keys())
        orderedTimeData.append(keys[0])
    orderedTimeData = sorted(orderedTimeData)
    return orderedTimeData

def createWindows(baseTime):
    windows = []
    for i in range(5):
        if len(windows) == 0:
            windows.append((baseTime, (baseTime + datetime.timedelta(0,0,0,0,2))))
        else:
            windows.append((windows[i - 1][1], (windows[i - 1][1] + datetime.timedelta(0,0,0,0,2))))
    return windows

def triggerStreaming():
    #Set up our data
    scoreInput = extractScores()
    processingData = parseRawData(scoreInput)
    #Now sort the processing data by process Time
    orderedKeys = orderData(processingData)
    #Sort our processing data to be in the correct order
    pipeline = []
    for key in orderedKeys:
        for record in processingData:
            if key in record.keys():
                pipeline.append(record[key])
                break

    #Set up windows for our pipeline
    windows = createWindows(datetime.datetime.strptime('12:00:00', "%H:%M:%S"))
    KV_Score = {}

    #Process Our Data
    for line in pipeline:
        team = line[0]
        score = (int)(line[1])
        windowIndex = determineBucket(line[2], windows)
        if (windows[windowIndex] in KV_Score.keys()):
            if team in KV_Score[windows[windowIndex]].keys():
                KV_Score[windows[windowIndex]][team] += score
                key = windows[windowIndex]
                #When a change occurs, trigger an update
                print("Bucket: ", windowIndex, "\tEvent Time Window: ", windows[windowIndex][0].time(), " - ", windows[windowIndex][1].time(),
                      "\tTeam: ", team, "\tScore: ", KV_Score[key][team])
            else:
                KV_score[windows[windowIndex]][team] = score
                key = windows[windowIndex]
                print("Bucket: ", windowIndex, "\tEvent Time Window: ", windows[windowIndex][0], " - ",
                      windows[windowIndex][1],
                      "\tTeam: ", team, "\tScore: ", KV_Score[key][team])
        else:
            KV_Score[windows[windowIndex]] = {team: score}
            key = windows[windowIndex]
            print("Bucket: ", windowIndex, "\tEvent Time Window: ", windows[windowIndex][0].time(), " - ",
                  windows[windowIndex][1].time(),
                  "\tTeam: ", team, "\tScore: ", KV_Score[key][team])
    print()
    print("Pipeline has finished processing")
    print()
    for key in KV_Score.keys():
        for teamKey in KV_Score[key].keys():
            print("Event Time Window: ", key[0].time(), " - ", key[1].time(), "\tTeam: ", teamKey, "\tScore: ", KV_Score[key][team])


def alignedDelayTriggerStreaming():
    # Set up our data
    scoreInput = extractScores()
    processingData = parseRawData(scoreInput)
    # Now sort the processing data by process Time
    orderedKeys = orderData(processingData)
    # Sort our processing data to be in the correct order
    pipeline = []
    for key in orderedKeys:
        for record in processingData:
            if key in record.keys():
                pipeline.append(record[key])
                break

    # Set up windows for our pipeline
    windows = createWindows(datetime.datetime.strptime('12:00:00', "%H:%M:%S"))
    KV_Score = {}
    delayBase = datetime.datetime.strptime('12:00:00', "%H:%M:%S")
    # Process Our Data
    for line in pipeline:
        delayNext =  (delayBase + datetime.timedelta(0,0,0,0,2))
        team = line[0]
        score = (int)(line[1])
        procTime = (datetime.datetime.combine(datetime.datetime.now().date(), line[3]))
        windowIndex = determineBucket(line[2], windows)
        if (windows[windowIndex] in KV_Score.keys()):
            if team in KV_Score[windows[windowIndex]].keys():
                KV_Score[windows[windowIndex]][team] += score
                key = windows[windowIndex]

            else:
                KV_score[windows[windowIndex]][team] = score
                key = windows[windowIndex]

        else:
            KV_Score[windows[windowIndex]] = {team: score}
            key = windows[windowIndex]
        #Check to see if we need to fire an aligned delay trigger
        if (procTime.time() >= delayNext.time()):
            print("Trigger Window: " + (str) (delayBase.time()) + ' - ' + (str) (delayNext.time()))
            #Set Delay base to new base
            delayBase = delayNext
            #Print our windows
            for key in KV_Score.keys():
                for teamKey in KV_Score[key].keys():
                    print("Event Time Window: ", key[0].time(), " - ", key[1].time(),
                          "\tTeam: ", teamKey, "\tScore: ", KV_Score[key][team])
            print()

    print()
    print("Pipeline has finished processing")
    print()
    for key in KV_Score.keys():
        for teamKey in KV_Score[key].keys():
            print("Event Time Window: ", key[0].time(), " - ", key[1].time(),
                  "\tTeam: ", teamKey, "\tScore: ", KV_Score[key][team])

def unalignedTriggerStreaming():
    # Set up our data
    scoreInput = extractScores()
    processingData = parseRawData(scoreInput)
    # Now sort the processing data by process Time
    orderedKeys = orderData(processingData)
    # Sort our processing data to be in the correct order
    pipeline = []
    for key in orderedKeys:
        for record in processingData:
            if key in record.keys():
                pipeline.append(record[key])
                break

    # Set up windows for our pipeline
    windows = createWindows(datetime.datetime.strptime('12:00:00', "%H:%M:%S"))
    KV_Score = {}
    #Establish base times for unaligned delays
    delayBases = []
    for i in range(4):
        delayBases.append(-1)
    for line in pipeline:
        team = line[0]
        score = (int)(line[1])
        procTime = (datetime.datetime.combine(datetime.datetime.now().date(), line[3]))
        windowIndex = determineBucket(line[2], windows)
        procWindow = delayBases[windowIndex]
        if type(procWindow) == int:
            procWindowMax = procTime + datetime.timedelta(0,0,0,0,2)
        else:
            procWindowMax = delayBases[windowIndex] + datetime.timedelta(0,0,0,0,2)
        if (windows[windowIndex] in KV_Score.keys()):
            if team in KV_Score[windows[windowIndex]].keys():
                KV_Score[windows[windowIndex]][team] += score
                key = windows[windowIndex]

            else:
                KV_score[windows[windowIndex]][team] = score
                key = windows[windowIndex]

        else:
            KV_Score[windows[windowIndex]] = {team: score}
            key = windows[windowIndex]
        #Now, do triggers
        if (type(procWindow) == int):
            #Establish a base
            delayBases[windowIndex] = procTime
        else:
            #Check to see if our procTime is greater than our max
            if procTime.time() >= procWindowMax.time():
                delayBases[windowIndex] = procTime
                #Print Trigger
                print("Event Time Window: ", windows[windowIndex][0].time(), " - ", windows[windowIndex][1].time(),
                  "\tTeam: ", team, "\tScore: ", KV_Score[key][team])
    print()
    print("Pipeline has finished processing")
    print()
    for key in KV_Score.keys():
        for teamKey in KV_Score[key].keys():
            print("Event Time Window: ", key[0].time(), " - ", key[1].time(),
                  "\tTeam: ", teamKey, "\tScore: ", KV_Score[key][team])

    #Process data in our pipeline
    pass

print("Results from Basic Batching: ")
bareBatch()
print()

print("Results from Windowed Batching: ")
windowedBatch()
print()

print("Results from Repeated Trigger Streaming: ")
triggerStreaming()
print()

print("Results from Aligned Delay Trigger Streaming: ")
alignedDelayTriggerStreaming()
print()

print("Results from unaligned Delay Trigger Streaming: ")
unalignedTriggerStreaming()
print()