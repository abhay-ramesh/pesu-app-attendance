# Correct any Incorrect data in attendence.json of a subject
import json
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def correct():
    # Get attendence data from csv file
    attendence_data = json.load(open("attendence.json", "r"))

    # Get all subject code
    all_subject_code = [i['subject_code'] for i in attendence_data]
    # print(all_subject_code)

    # Get data of subject using subject code
    # Ask user to enter subject code
    for idx, i in enumerate(all_subject_code):
        print(f'{idx+1}. {i}')
    subject_code = input("Enter Subject Code Number: ")
    subject_data = attendence_data[int(subject_code)-1]

    # Go through all attendence data of subject
    for idx, i in enumerate(subject_data['attendance']):
        print(f'Date: {i["date"]}, Time: {i["time"]}, Status: {i["status"]}')
        # Ask user if it is correct or not
        # If Correct press enter
        # If Incorrect press x
        status = input(f'Correct(Enter)/Incorrect(x): ')
        if status == 'x':
            # If incorrect check the status of attendence and toggle it to opposite of ✓ or X
            if i['status'] == '✓':
                i['status'] = 'X'
            else:
                i['status'] = '✓'
            print(f'Corrected Status: {i["status"]}')

    print(subject_data)

    # Save the data to attendence.json
    with open('attendence.json', 'w') as f:
        json.dump(attendence_data, f, indent=4)


if __name__ == "__main__":
    correct()
