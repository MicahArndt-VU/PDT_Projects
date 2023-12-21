#Goal of this is to do the same work as the CH2 Workbook, just using the apache beam engine
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam.transforms.trigger as trigger
import pandas
import datetime
import time

#Pipeline function to demonstrate basic Batch Processing with Apache Beam
def basicBatch():
    def print_out(pane):
        print(pane)
    options = PipelineOptions()
    p = beam.Pipeline(options=options)

    #Organize our pipeline Steps
    lines = (p
             | "Read Lines" >> beam.io.ReadFromText('scores.txt')
             | "Map Lines" >> beam.Map(lambda record: record.split(','))
            | "Map to KV" >> beam.Map(lambda record: (record[1], (int)(record[2])))
            | "Sum Scores" >> beam.CombinePerKey(sum)
            | "Output Pane" >> beam.Map(print_out)
            )
    results = p.run()
    return

#Pipeline function to demonstrate Windowed Batch Processing with Apache Beam
def windowedBatch():
    def print_out(pane):
        print(pane)
    #Create a class for timestamping our records
    class AddTimestampDoFn(beam.DoFn):
        def process(self, element):
            ts = datetime.datetime.strptime(element[3], "%H:%M:%S")
            ts = ts.replace(year=2023, month=1, day=1)  # Set arbitrary date
            ts = ts.timestamp()  # Turn into seconds since epoch
            yield beam.window.TimestampedValue(element, ts)

    options = PipelineOptions()
    p = beam.Pipeline(options=options)
    lines = (p
             |"Read Lines" >> beam.io.ReadFromText('scores.txt')
             |"Map Lines" >> beam.Map(lambda record: record.split(','))
             |"Window Lines" >> beam.WindowInto(beam.window.FixedWindows(120)) #Window into 2 minute windows
            |"Add Timestamps" >> beam.ParDo(AddTimestampDoFn())
            |"Map to KV" >> beam.Map(lambda record: (record[1],  (int)(record[2]))) #Now we are using the bucket as the key
             | "Sum Scores" >> beam.CombinePerKey(sum)
             | "Output Pane" >> beam.Map(print_out)
             )
    results = p.run()

    return

def repeatedTriggers():
    def print_out(pane):
        print(pane)
    #Create a class for timestamping our records
    class AddTimestampDoFn(beam.DoFn):
        def process(self, element):
            ts = datetime.datetime.strptime(element[3], "%H:%M:%S")
            ts = ts.replace(year=2023, month=1, day=1)  # Set arbitrary date
            ts = ts.timestamp()  # Turn into seconds since epoch
            yield beam.window.TimestampedValue(element, ts)

    options = PipelineOptions()
    p = beam.Pipeline(options=options)
    lines = (p
             |"Read Lines" >> beam.io.ReadFromText('scores.txt')
             |"Map Lines" >> beam.Map(lambda record: record.split(','))
             |"Window Lines" >> beam.WindowInto(beam.window.FixedWindows(120), trigger=trigger.Repeatedly(trigger.AfterCount(1)), accumulation_mode=trigger.AccumulationMode.ACCUMULATING) #Window into 2 minute windows
            |"Add Timestamps" >> beam.ParDo(AddTimestampDoFn())
            |"Map to KV" >> beam.Map(lambda record: (record[1],  (int)(record[2]))) #Now we are using the bucket as the key
             | "Sum Scores" >> beam.CombinePerKey(sum)
             | "Output Pane" >> beam.Map(print_out)
             )
    results = p.run()

print("Results from Basic Batching: ")
basicBatch()
print("Results from Windowed Batching: ")
windowedBatch()
print("Results from Repeated Trigger Batching: ")
repeatedTriggers()
