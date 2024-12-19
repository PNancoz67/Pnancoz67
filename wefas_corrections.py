from pathlib import Path
import json
import csv
from wefas_io import wefas_inbound
from wefas_io import wefas_outbound



def write_CSV(out_list):
    """write out the final CSV with all corrections"""
    with open('Output_of_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['Dispatch ID', 'All Charted Crew', 'Date Dispatched', 'Activity Response', 'Disposition (Outcome)',
                      'Scene Grid', 'Unit', 'Odometer - Start', 'Odometer - End']
        writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_ALL, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_list)

def build_crew(crew, call_crew, act_pend):
    """build out the crew dictionary when there was no valid activity"""      
    temp_act = '' 
    print(call_crew)
    for acts in act_pend:
        if acts.find('9-1') >= 0:
            temp_act = '9-1'
            break
        elif acts.find('9-2') >= 0:
            temp_act =  '9-2'
            break
        elif acts.find('9-3') >= 0: 
            temp_act =  '9-3'
            break
        elif acts.find('9') >= 0:
            temp_act =  '9'
            break
        elif acts.find('Event/Standby') >= 0:
            temp_act =  'Event/Standby'
            break
    for crew_member in call_crew:
        crew[crew_member] = temp_act
    print(crew)       

def correct_act(act_pend):
    """apply the text corrections to the pending activity records"""
    for i, item in enumerate(act_pend):
        for corrections in CorrectL:   
            if act_pend[i].find(corrections['Original']) >= 0:                   
                act_pend[i] = act_pend[i].replace(corrections['Original'], corrections['Updated'])
                break

def update_output(crew_line, act_pend):
    """apply the updates and corrections to the output records"""
    for acts in act_pend:
        # this section will apply the override for activity if the name matches
        if acts.find(call_line['All Charted Crew']) >= 0:     
            if acts.find('9-1') >= 0:
                call_line['Activity Response'] = '9-1'
            elif acts.find('9-2') >= 0:
                call_line['Activity Response'] = '9-2'
            elif acts.find('9-3') >= 0: 
                call_line['Activity Response'] = '9-3'
            elif acts.find('9') >= 0:
                call_line['Activity Response'] = '9'
            elif acts.find('Event/Standby') >= 0:
                call_line['Activity Response'] = 'Event/Standby'
            else:
                call_line['Activity Response'] = ''
            break
    call_line['All Charted Crew'] = reverse_name(call_line['All Charted Crew'])

def reverse_name(full_name):
    """Reverses the order of first and last name."""
    name_parts = full_name.split()
    if len(name_parts) == 2:
        rev_name = f"{name_parts[1]}, {name_parts[0]}"
    elif len(name_parts) == 3 and name_parts[2] in name_suffix:
        rev_name = f"{name_parts[1]} {name_parts[2]}, {name_parts[0]}"
    else:
        rev_name = f"{name_parts[1]} {name_parts[2]}, {name_parts[0]}"       
    return rev_name

def restore_name(full_name):
    """restore reversed name back to firstname-lastname order"""
    name_parts = full_name.split()
    if len(name_parts) == 2:
        rev_name = f"{name_parts[1].strip(',')} {name_parts[0].strip(',')}"
    elif len(name_parts) == 3 and name_parts[2].strip(',') in name_suffix:
        rev_name = f"{name_parts[2].strip(',')} {name_parts[0].strip(',')} {name_parts[1].strip(',')}"
    else:
        rev_name = f"{name_parts[2].strip(',')} {name_parts[0].strip(',')} {name_parts[1].strip(',')}"       
    return rev_name

def write_member_list():
    """maintains json list of all members"""
    for all_mem in all_crew:
        new_name = reverse_name(all_mem)
        sort_name.append(new_name)
    sort_name.sort()
    for sort_mem in sort_name:
        new_name = restore_name(sort_mem)
        resort_all_crew.append(new_name)  
    print(resort_all_crew)
    path = Path('WEFAS_members.json')
    contents = json.dumps(all_crew)
    path.write_text(contents)

valid_act = ['9', '9-1', '9-2', '9-3', 'Event/Standby', 'Event/Standby,Mixed', '']
name_suffix = ['Jr.', 'Sr.', 'III']
prev_CAD = ''
curr_date = ''
curr_dispostion = ''
curr_scene = ''
curr_unit = ''
curr_odo_end = ''
curr_odo_start = ''
call_line = {}
crew = {}
act_pend = []
out_list = []
all_crew = []
resort_all_crew = []
sort_name = []
call_crew = []
corrections = {}
path = Path('WEFAS_corrections.json')
contents = path.read_text()
CorrectL = json.loads(contents)

print(CorrectL)
filename = wefas_inbound()
#filename = 'Output_of_Peter_Nancoz_2024.csv'
#filename = 'Output_test.csv'
out_filename = wefas_outbound()
with open(filename,mode = 'r') as file:
    csvFile = csv.DictReader(file)
    csvSortedFile= sorted(csvFile, key=lambda x: x['Dispatch ID'])
    for lines in csvSortedFile:
        curr_CAD = lines['Dispatch ID']
        if curr_CAD == '' or lines['All Charted Crew'] == ' ':
            continue
        if curr_CAD != prev_CAD:
                #apply updates and move to output list
            if prev_CAD != '':
                if len(crew) == 0:
                    print(f'{prev_CAD} - no valid activity')
                    build_crew(crew, call_crew, act_pend)
                correct_act(act_pend)
                for k, v in crew.items():
                    call_line['All Charted Crew'] = k
                    call_line['Activity Response'] = v
                    update_output(call_line, act_pend)
                    out_list.append(call_line.copy())
            print(curr_CAD)

            act_pend = []
            crew = {}
            call_crew = []

            prev_CAD = curr_CAD
            curr_date = lines['Date Dispatched']
            curr_dispostion = lines['Disposition (Outcome)']
            curr_scene = lines['Scene Grid']
            curr_unit = lines['Unit']
            curr_odo_start = lines['Odometer - Start']
            curr_odo_end = lines['Odometer - End']
        curr_crew = lines['All Charted Crew']
        if curr_crew not in all_crew:
            all_crew.append(curr_crew)
        if curr_crew not in call_crew:
            call_crew.append(curr_crew)
        if lines['Activity Response'] == 'Event/Standby,Mixed':
            curr_activity = 'Event/Standby'
        else:
            curr_activity = lines['Activity Response']
        call_line = {'Dispatch ID': curr_CAD, 
                'All Charted Crew': curr_crew,
                'Date Dispatched': curr_date,
                'Activity Response': curr_activity,
                'Disposition (Outcome)': curr_dispostion,
                'Scene Grid': curr_scene,
                'Unit': curr_unit,
                'Odometer - Start': curr_odo_start,
                'Odometer - End': curr_odo_end }
        if curr_activity in valid_act:     
            crew[curr_crew] = curr_activity   
        else:
            if curr_activity not in act_pend:
                act_pend.append(curr_activity)   
if len(crew) == 0:
    print(f'{prev_CAD} - no valid activity')
    build_crew(crew, call_crew, act_pend)
correct_act(act_pend)

for k, v in crew.items():
    call_line['All Charted Crew'] = k
    call_line['Activity Response'] = v
    update_output(call_line, act_pend)
    out_list.append(call_line.copy()) 
write_member_list()
write_CSV(out_list)