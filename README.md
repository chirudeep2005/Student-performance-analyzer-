# Student Performance Analyzer

A beginner-friendly Python command-line project that stores student marks in a CSV file and generates a performance report.

## Features
- Add student records for Maths, Science, and English
- Validate marks from 0 to 100
- Calculate each student's percentage and grade
- Show the class average and top performer
- Save records in `students.csv` so they remain available after restarting

## Requirements
- Python 3.9 or newer
- No external packages required

## Run the project
1. Download or clone this repository.
2. Open a terminal in this folder.
3. Run:

   ```bash
   python main.py
   ```

## CSV format
The app creates `students.csv` automatically when you add the first student. Example:

```csv
name,maths,science,english
Asha,92,88,95
Rahul,75,81,79
```

## Ideas for a live interview feature
- Search for a student by name
- Sort the report by percentage
- Show students who scored below a chosen threshold
- Add another subject

## Interview preparation
Read the code, run it yourself, and practise explaining the functions `load_students`, `calculate_percentage`, `get_grade`, and `show_report`. Only describe the project as your own work to the extent that you understand, modify, and can honestly explain your contribution.
