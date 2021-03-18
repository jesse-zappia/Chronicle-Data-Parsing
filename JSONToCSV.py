#Chronicle CSV parser
#Version 0.1.1
#Written by Jesse Zappia
#Last Update: 3/18/2021

import json
import csv
import sys
import argparse
import os

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", required = True, type = str, help = "Input CSV file from Chonicle Export")
parser.add_argument("--output", default = "output.csv", help = "Output CSV file")

args = parser.parse_args()

#Set input and output files
input_file = args.input
output_file = args.output

json_target = open('temp.json', mode='w')

with open(input_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            json_target.write("{ \"data\": [")
        elif line_count==1:
            json_target.write(row["Log data"])
            line_count += 1
        else:
            json_target.write(",")
            json_target.write(row["Log data"])
            line_count += 1
    json_target.write("] }")
    print(f'Processed {line_count} lines into JSON file.')

json_target.close()

print('Writing data to CSV file...')

with open('temp.json') as json_file:
    data = json.load(json_file)

log_record = data['data']

csv_output = open(output_file, mode='w', newline='') # Newline requried for Windows compatability

csv_writer = csv.writer(csv_output)

count = 0

for log in log_record:
    if count == 0:
        header = log.keys()
        csv_writer.writerow(header)
        count += 1

    csv_writer.writerow(log.values())

print('Done!')
csv_output.close()

print('Cleaning up temp files...')
os.remove("temp.json")
print('Done!')
