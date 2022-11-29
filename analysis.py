# Do Analysis on attendence csv file
#
# Path: analysis.py

import csv
import os
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import ceil

required_percentage = 75

# Subject Data JSON Format
# {
#     "subject_code": "UE20CS323",
#     "subject": "Graph Theory, and its Applications",
#     "attendance": [
#         {
#             "date": "25-Nov-2022",
#             "time": "13:30-14:30",
#             "from-time": "13:30",
#             "to-time": "14:30",
#             "status": "X"
#         },
#         {
#             "date": "23-Nov-2022",
#             "time": "10:45-11:45",
#             "from-time": "10:45",
#             "to-time": "11:45",
#             "status": "\u2713"
#         },
#     ]
# }

# Get attendence data from csv file
attendence_data = json.load(open("attendence.json", "r"))
# print(attendence_data)

# Get Subject Based Attendence Data
for subject_data in attendence_data:
    # Print Summary of Subject
    subject = subject_data['subject']
    subject_code = subject_data['subject_code']
    total_lectures = len(subject_data['attendance'])
    total_present = len(
        [i for i in subject_data['attendance'] if i['status'] == '✓'])
    total_absent = len(
        [i for i in subject_data['attendance'] if i['status'] == 'X'])
    percentage = round((total_present/total_lectures)*100, 2)

    print("Subject: ", subject)
    print("Subject Code: ", subject_code)
    print("Total Classes: ", total_lectures)
    print("Total Present: ", total_present)
    print("Total Absent: ", total_absent)
    print("Percentage of Present: ", round(
        (total_present/total_lectures)*100, 2), "%")
    print("Percentage of Absent: ", round(
        (total_absent/total_lectures)*100, 2), "%")
    print("--------------------------------------------")
    if percentage < required_percentage:
        print("You should attend more classes")
        # Calculate the number of classes which was needed to attend to get allow% attendance
        min_classes = ceil((required_percentage*total_lectures)/100)
        print(
            f"You should have attended {min_classes-total_present} more classes to get {required_percentage}% attendance")
        # Calculate the number of classes which is needed to attend to get 75% in future
        needed_new_classes = ceil(
            (((total_present)-((required_percentage/100)*total_lectures))/((required_percentage/100)-1)))
        print(
            f"You should attend {needed_new_classes} more classes to get {required_percentage}% attendance in future")
        print("--------------------------------------------")
    else:
        print("You are doing good")
        print("--------------------------------------------")

# Get All Attendence data from all subjects
all_attendence_data = []
for subject_data in attendence_data:
    for i in subject_data['attendance']:
        all_attendence_data.append(i)

# Get All Dates
all_dates = [i['date'] for i in all_attendence_data]

# Get Unique Dates
unique_dates = list(set(all_dates))
# Custom Sort using 00-AUG-2021 format
unique_dates.sort(key=lambda date: datetime.datetime.strptime(
    date, '%d-%b-%Y'))

# print("Unique Dates: ", unique_dates)

# Find the number of classes on each date
# Get the number of classes on each date
classes_on_each_date = []
for i in unique_dates:
    # Classes Absent on each date
    classes_absent_on_each_date = len(
        [j for j in all_attendence_data if j['date'] == i and j['status'] == 'X'])
    # Classes Present on each date
    classes_present_on_each_date = len(
        [j for j in all_attendence_data if j['date'] == i and j['status'] == '✓'])
    # Total Classes on each date
    total_classes_on_each_date = classes_absent_on_each_date + \
        classes_present_on_each_date
    # Percentage of classes present on each date
    percentage_classes_present_on_each_date = round(
        (classes_present_on_each_date/total_classes_on_each_date)*100, 2)
    # Percentage of classes absent on each date
    percentage_classes_absent_on_each_date = round(
        (classes_absent_on_each_date/total_classes_on_each_date)*100, 2)
    # Append the data to classes_on_each_date list
    classes_on_each_date.append({
        "date": i,
        "total_classes": total_classes_on_each_date,
        "classes_present": classes_present_on_each_date,
        "classes_absent": classes_absent_on_each_date,
        "percentage_classes_present": percentage_classes_present_on_each_date,
        "percentage_classes_absent": percentage_classes_absent_on_each_date
    })

absent_day = {
    "Monday": 0,
    "Tuesday": 0,
    "Wednesday": 0,
    "Thursday": 0,
    "Friday": 0,
    "Saturday": 0,
    "Sunday": 0
}
for i in classes_on_each_date:
    if i['percentage_classes_present'] == 0:
        # Check what day of the week it is
        day_of_the_week = datetime.datetime.strptime(
            i['date'], '%d-%b-%Y').strftime('%A')
        print(
            f"Classes Absent on {i['date']}: {i['classes_absent']}")
        absent_day[day_of_the_week] += 1
    # print("Date: ", i['date'])
    # print("Total Classes: ", i['total_classes'])
    # print("Classes Present: ", i['classes_present'])
    # print("Classes Absent: ", i['classes_absent'])
    # print("Percentage of Classes Present: ",
    #       i['percentage_classes_present'])
    # print("Percentage of Classes Absent: ", i['percentage_classes_absent'])
    # print("--------------------------------------------")

print("Absent Day: ", absent_day)

# Plot the data
# Get the dates
dates = [i['date'] for i in classes_on_each_date]
# # Get the percentage of classes present
# percentage_classes_present = [
#     i['percentage_classes_present'] for i in classes_on_each_date]
# # Get the percentage of classes absent
# percentage_classes_absent = [
#     i['percentage_classes_absent'] for i in classes_on_each_date]

# # Plot the data
# plt.figure(figsize=(20, 10))
# plt.plot(dates, percentage_classes_present, label="Present")
# plt.plot(dates, percentage_classes_absent, label="Absent")
# plt.xlabel("Dates")
# plt.ylabel("Percentage of Classes")
# plt.title("Attendence")
# plt.legend()
# plt.show()

# Get the number of classes present on each date
classes_present_on_each_date = [i['classes_present']
                                for i in classes_on_each_date]
# Get the number of classes absent on each date
classes_absent_on_each_date = [i['classes_absent']
                               for i in classes_on_each_date]

# Get the total number of classes on each date
total_classes_on_each_date = [i['total_classes']
                              for i in classes_on_each_date]

# # Plot the data as bar graph
# plt.figure(figsize=(20, 10))
# plt.bar(dates, classes_present_on_each_date, label="Present")
# plt.bar(dates, classes_absent_on_each_date, label="Absent")
# plt.xlabel("Dates")
# plt.ylabel("Number of Classes")
# plt.title("Attendence")
# plt.legend()
# plt.show()
