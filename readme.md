# PES University Mobile App - Android Attendance Data Scraper/Analyzer

This is a simple python script that scrapes the attendance data from the PES University Mobile App and analyzes it.

## PESU Attendance Report Done Better

## Requirements

- Python 3.6+
- Python modules: `requests`, `pandas`, `matplotlib`, `numpy`

## Instructions

1. Take Screenshot of Attendance Page for each subject as a long screenshot from PESU Mobile App.
2. Upload the screenshots to [Online OCR](https://onlineocr.net/), now process the image and download the output as a text file
3. Save the text files in the `data` folder
4. pip install any missing modules
5. Run `python attendance.py` to process the raw text files and generate the attendance data into json and csv file.
6. Run `python analysis.py` to generate the attendance analysis reports in terminal.
7. Check if the % attendance matches with the PESU Mobile App.
8. If the % attendance doesn't match, then run `python correction.py` and enter the correct attendance data.
9. Now run `python analysis.py` again to generate the attendance analysis reports in terminal.
10. Enjoy!
