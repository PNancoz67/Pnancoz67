from pathlib import Path
import json
import csv
from wefas_io import wefas_inbound

valid_act = ['9', '9-1', '9-2', '9-3', 'Event/Standby', 'Event/Standby,Mixed', '']
no_act = []
total = 0

path = Path('WEFAS_corrections.json')
contents = path.read_text()
CorrectL = json.loads(contents)

path = Path('WEFAS_members.json')
contents = path.read_text()
members = json.loads(contents)

filename = wefas_inbound()
#filename = 'Output_of_Peter_Nancoz_2024.csv'


with open(filename,mode = 'r') as file:
    csvFile = csv.DictReader(file)
    csvSortedFile= sorted(csvFile, key=lambda x: x['Dispatch ID'])
    for lines in csvSortedFile:
        if lines['Activity Response'] in valid_act:
            continue
        found = False
        for  member in members:
            if lines['Activity Response'].find(member) != -1:
  #              print(f'found member - {member} activity - {lines['Activity Response']}')
                found = True
                break
        if found:
            continue   
        else:
  #          print(f'not found - {lines["Activity Response"]}') 
            no_act.append(lines['Activity Response'])
    for acts in no_act:
        found = False
        for Correct in CorrectL:
 #           print(Correct['Original'])
            if acts.find(Correct['Original']) != -1:
                found = True
                break
        if found:
            continue
        else:
            print(f'Found an activity that needs to be added - {acts}')
            total += 1


print(f'Total number activities not found - {total}')