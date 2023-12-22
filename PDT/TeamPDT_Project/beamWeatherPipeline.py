import pandas as pd
import random
import datetime
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam.transforms.trigger as trigger

#Our sink that we write to
df = pd.DataFrame(columns=['id', 'temperature', 'weather', 'timestamp'])
#Function to handle data processing
def append_to_df(element):
    global df
    #Define dict to append
    appendDF = pd.DataFrame(columns=['id', 'temperature', 'weather', 'timestamp'])
    id = [(int)(element[0])]
    weather = [element[1][1]]
    temperature = [element[1][0]]
    timestamp = [element[1][2]]
    #Test to see if we need to append (Based on time)
    if id[0] in df['id'].values:
        #Check if the timestamp is newer
        if datetime.datetime.strptime(timestamp[0].split(".")[0],"%H:%M:%S").time()  > datetime.datetime.strptime(df.loc[df['id'] == id[0], 'timestamp'][0].split('.')[0], "%H:%M:%S").time():
            #Update the record
            df.loc[df['id'] == id[0], 'temperature'] = temperature[0]
            df.loc[df['id'] == id[0], 'weather'] = weather[0]
            df.loc[df['id'] == id[0], 'timestamp'] = timestamp[0]
            print("Updating Record")
            return
        else:
            print("Record is older. Not updating")
            return
    else:
        appendDF['id'] = id
        appendDF['temperature'] = temperature
        appendDF['weather'] = weather
        appendDF['timestamp'] = timestamp
        df = pd.concat([df, appendDF])
    #print(df.to_string())
    return
#Helper Functions
def printout(element):
    print("In Printout")
    print(element)

ids = [101, 102, 103, 104]
possible_weather = ['sunny', 'overcast', 'rainy']
id_Stream = [random.choice(ids) for i in range(100)]
temperatures = [random.uniform(50,70) for i in range(100)]
ob_times = [datetime.datetime.now() + datetime.timedelta(minutes=random.randrange(-60, 60)) for i in range(100)]
weather = [random.choice(possible_weather) for i in range(100)]

"""
#Write this data to a file for processing
for i in range(len(ids)):
    with open('weather_data.txt', 'a') as f:
        f.write(str(ids[i]) + ',' + str(temperatures[i]) + ',' + str(ob_times[i].time()) + ',' + str(weather[i]) + '\n')
        f.close()
"""
#Define class to add timestamp to our record
class AddTimestampDoFn(beam.DoFn):
        def process(self, element):
            ts = datetime.datetime.strptime(element[2].split('.')[0], "%H:%M:%S")
            ts = ts.replace(year=2023, month=1, day=1)  # Set arbitrary date
            ts = ts.timestamp()  # Turn into seconds since epoch
            yield beam.window.TimestampedValue(element, ts)

#Begin Creating our pipeline
options = PipelineOptions()
p = beam.Pipeline(options=options)

pipeline = (p
            |"Read Lines" >> beam.io.ReadFromText('weather_data.txt')
            |"Map Lines" >> beam.Map(lambda record: record.split(','))
            |"Add Timestamps" >> beam.ParDo(AddTimestampDoFn())
            |"Window Lines" >> beam.WindowInto(beam.window.FixedWindows(120)) #Window into 2 minute windows
            |"Map to KV" >> beam.Map(lambda record: (record[0],  ((float)(record[1]), record[3], record[2]))) #Use the id as a key, mapping weather and temperature to a tuple
            |"Output Pane" >> beam.Map(append_to_df) #Write this to a dataframe
            )
results = p.run()
print(df.to_string())