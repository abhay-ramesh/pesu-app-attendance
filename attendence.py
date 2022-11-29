# Get all Attendence data from all txt file from text folder

import os
import re
import pandas as pd
import json


# Get all txt file from text folder


def get_all_txt_file():
    path = 'data'
    all_txt_file = []
    for file in os.listdir(path):
        if file.endswith('.txt'):
            all_txt_file.append(file)
    return all_txt_file

# Get all Attendence data from all txt file


def attendence_data(file_name):
    attendance_data = []
    print('Processing file: ', file_name)
    path = 'data'
    text = []
    subject = ""
    subject_code = ""
    attendance = []
    # Get text from all txt file
    with open(os.path.join(path, file_name), 'r', encoding="utf-16") as f:
        text = f.readlines()

    # Remove all empty line
    text = [x.strip() for x in text if x.strip()]
    # Check line starting with letter U
    for line in text:
        status = []
        times = []
        if line.startswith('U'):
            # print(line)
            # Split line by hyphen
            line = line.split('-')
            # Get first element of line and remove spaces and anything other than alphabets or numbers and add it to subject_code
            subject_code = re.sub('[^A-Za-z0-9]+', '', line[0])
            # Get second element of line and remove starting spaces and add it to subject
            subject = line[1]
            subject = subject.lstrip()
        # Check line starting with Date Format 14-Sep-2019 after removing spaces
        elif re.match(r'\d{2}-\w{3}-\d{4}', line.replace(" ", "")):
            # print(line)
            date = line.replace(" ", "")
            # Get next line
            nextLine = text[text.index(line) + 1]
            # print(nextLine)
            # Remove all spaces and hyphen from next line
            nextLine = nextLine.replace(' ', '')
            nextLine = nextLine.replace('-', '')
            # Print next line if its length is not divisible by 5
            if len(nextLine) % 5 != 0:
                print(nextLine)
            # Split next line by 10 characters then by 5 characters
            nextLine = [nextLine[i:i + 10]
                        for i in range(0, len(nextLine), 10)]
            # For each 10 characters split it by 5 characters
            for i in nextLine:
                times.append([i[j:j + 5] for j in range(0, len(i), 5)])
            # print(times)
            # Get next line and check it has X or ✓
            nextLine2 = text[text.index(line) + 2]
            if 'X' in nextLine2 or '✓' in nextLine2:
                # Split next line by 13 characters and remove spaces
                nextLine2 = [nextLine2[i:i + 13]
                             for i in range(0, len(nextLine2), 13)]
                nextLine2 = [x.strip() for x in nextLine2 if x.strip()]
                status = nextLine2
            # Add everything to attendance list
            attendance.append({
                'date': date,
                'times': times,
                'status': status
            })
            # print(subject_code, subject, date, times, status)
            # print('---------------------------------')
    # # Check if attendance list has equal number of times and status
    # print("Subject Code: ", subject_code)
    # for i in attendance:
    #     if len(i['times']) != len(i['status']):
    #         print("Date: ", i['date'])
    #         for j in i['times']:
    #             print(f"Time: {j[0]}-{j[1]}")
    #             # Get Input from user as Y or N irrespective of case and add it to status
    #             # status = input("Status(Y/N): ")
    #             # status = status.upper()
    #             # i['status'].append(status)

    # Check if attendance list has equal number of times and status
    # Convert attendance list to json
    attendance_formated = []
    print("Subject Code: ", subject_code)
    for i in attendance:
        for j in i['times']:
            if len(i['status']) != len(i['times']):
                # print("Date: ", i['date'])
                # print(f"Time: {j[0]}-{j[1]}")
                # status = input("Status(Y/N): ") # Found that all status are Y
                # status = status.upper()
                # if status == 'Y':
                #     status = '✓'
                # else:
                #     status = 'X'
                status = '✓'
                i['status'].append(status)
            template = {
                'date': i['date'],
                'time': f"{j[0]}-{j[1]}",
                'from-time': j[0],
                'to-time': j[1],
                'status': i['status'][i['times'].index(j)]
            }
            print(template)
            attendance_formated.append(template)
    # print(attendance_formated)

    # Add everything to attendance_data list
    attendance_data.append({
        'subject_code': subject_code,
        'subject': subject,
        'attendance': attendance_formated
    })
    return attendance_data


demo_attendence_data_format = [
    {
        "subject": "Design Of Machine Element",
        "subject_code": "UE20ME301",
        "attendence": [
            {
                "date": "29-11-2022",
                "from-time": "10:45",
                "to-time": "11:45",
                "status": "Present"
            },
            {
                "date": "30-11-2022",
                "from-time": "10:45",
                "to-time": "11:45",
                "status": "Present"
            }
        ]
    },
    {
        "subject": "Pricniple Of Energy Conversion",
        "subject_code": "UE20ME302",
        "attendence": [
            {
                "date": "29-11-2022",
                "from-time": "10:45",
                "to-time": "11:45",
                "status": "Present"
            },
            {
                "date": "30-11-2022",
                "from-time": "10:45",
                "to-time": "11:45",
                "status": "Present"
            }
        ]
    }
]


if __name__ == "__main__":

    # get_attendence_data()
    all_txt_file = get_all_txt_file()
    # print(all_txt_file)

    # Get all attendence data from all txt file
    all_attendence_data = []
    for file in all_txt_file:
        data = attendence_data(file)
        all_attendence_data.append(data[0])

    # print(all_attendence_data)

    # Save all attendence data to json file
    with open('attendence.json', 'w') as f:
        json.dump(all_attendence_data, f)

    # Convert to csv
    # Columns
    columns = ['subject', 'subject_code',
               'date', 'from-time', 'to-time', 'status']
    # Create a dataframe
    df = pd.DataFrame(columns=columns)
    # Dataframe data
    data = []
    # Add data to dataframe
    for i in all_attendence_data:
        for j in i['attendance']:
            data.append([i['subject'], i['subject_code'],
                         j['date'], j['from-time'], j['to-time'], j['status']])
    # Add data to dataframe
    df = pd.concat([df, pd.DataFrame(data, columns=columns)])
    # Save to csv
    df.to_csv('attendence.csv', index=False)
