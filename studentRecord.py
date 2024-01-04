#!/bin/python3

import sys
import os
import random
from datetime import datetime, timedelta

courseFile = "courses.txt"
studentFile = "students.txt"
passedFile = "passed.txt"


def menu():
    clear()
    choiceMap = {
        1: addStudent,
        2: searchStudent,
        3: searchCourse,
        4: addCourseCompletion,
        5: showStudentRecord,
        0: exit
    }

    while (True):
        print('''You may select one of the following:
                    1) Add student
                    2) Search student
                    3) Search course
                    4) Add course completion
                    5) Show student's record
                    0) Exit
What is your selection?''')
        while (True):
            choice = int(input())
            if (choice not in choiceMap):
                print("Please provide a valid input\n")
            else:
                return choiceMap[choice]


def addStudent():
    clear()
    while (True):
        print('Names should contain only letters and start with capital letters.')
        firstName = input(
            'Enter the first name of the student:\n').strip()
        secondName = input(
            'Enter the second name of the student:\n').strip()
        if (not (firstName.istitle() and secondName.istitle() and firstName.isalpha() and secondName.isalpha())):
            continue
        print(
            """
Select student's major:
            CE: Computational Engineering
            EE: Electrical Engineering
            ET: Energy Technology
            ME: Mechanical Engineering
            SE: Software Engineering
What is your selection?"""
        )
        while (True):
            choice = input()
            if (choice not in majorMap):
                print("Please provide a valid input!")
                continue
            else:
                break
        studentMajor = majorMap[choice]
        year = datetime.today().year
        email = firstName.lower()+"."+secondName.lower()+"@ioe.np"

        with open(studentFile, 'a') as f:
            f.write(
                f"{random.randint(10000,99999)},{firstName},{secondName},{year},{choice},{email}\n")
        print("Student added successfully!")
        input()
        return


def searchStudent():
    clear()
    found = 0
    while (True):
        searchTerm = input(
            "Give at least 3 characters of the students first or last name:\n").lower().strip()
        if (len(searchTerm) < 3):
            continue
        with open(studentFile, 'r')as file:
            for line in file:
                id, firstName, secondName, garbage = line.split(",", 3)
                if (searchTerm in firstName.lower() or searchTerm in secondName.lower()):
                    if (not found):
                        print("Matching students:")
                    print(
                        f"ID: {id}, First name: {firstName}, Last name: {secondName}")
                    found = 1
        if not found:
            print("Student not found!!")

        input()
        return


def searchCourse():
    clear()
    found = 0
    while (True):
        searchTerm = input(
            "Give at least 3 characters of the name of the course or the teacher:\n").lower().strip()
        if (len(searchTerm) < 3):
            continue
        with open(courseFile, "r") as file:
            for line in file:
                id, name, garbage, teachers = line.replace(
                    "\n", "").split(",", 3)
                if (searchTerm in line.lower()):
                    print(f"ID: {id}, Name:{name}, Teacher(s):{teachers}")
                    found = 1
        if not found:
            print("Record not found!")
        input()
        return


def addCourseCompletion():
    found = 0
    latestObtainedGrade =0
    clear()
    while (True):
        print('Give the course ID:')
        courseId = input().upper()
        with open(courseFile, "r")as file:

            for line in file:
                if courseId in line:
                    _, _, credit, _ = line.split(",")
                    found = 1
                    break
                else:
                    continue
        if not found:
            print("Course not found for the given course ID")
            input()
            continue
        print("Get the student ID:")
        studentId = input()
        with open(studentFile, "r")as file:
            found = 0
            for line in file:
                if studentId in line:
                    found = 1
                    break
                else:
                    continue
        if not found:
            print("Student not found with the given student ID")
            input()
            continue
        print("Give the grade:")
        grade = input()
        if (grade > credit and grade < 0):
            print("Grade is not a correct grade.")
        with open(passedFile, "r")as file:
            for line in file:
                if (studentId in line and courseId in line):
                    _, _, date, obtainedGrade = line.replace(
                        " ", '').split(',')
                    date=str(date)
                    if int(grade) < int(obtainedGrade):
                        print(
                            f"Student has passed this course earlier with grade {obtainedGrade}")
                        input()
                        return
                    
                    


        while True:
            passedDate = input("Enter a date (DD/MM/YYYY): ")
            try:
                passedDate = datetime.strptime(passedDate, "%d/%m/%Y")
            except ValueError:
                print("Invalid date format.Use DD/MM/YYYY.Try again!")
                continue

            if passedDate < datetime.today()-timedelta(days=30):
                print('Input date is older than 30 days. Contact "opinto".')
                input()
                return

            if passedDate > datetime.today():
                print("Input date is later than today. Try again!")
                input()
                return
            print("Input date is valid.")
            with open(passedFile, "a")as file:
                file.write(f"{courseId},{studentId},{passedDate.strftime('%d/%m/%Y')},{grade}\n")
            print("Record added!")
            input()
            return


def showStudentRecord():
    clear()
    found = 0
    totalCredits = 0
    obtainedGrade = 0

    while True:
        searchTerm = input('Please Enter the ID of the student:').strip()
        if not searchTerm:
            continue
        with open(studentFile, 'r') as file:
            for line in file:
                id, firstName, secondName, startingYear, major, email = line.replace(
                    "\n", "").split(",")
                if searchTerm == id:
                    found = 1
                    print(f"""
Student ID: {id}
Name: {firstName}, {secondName}
Starting year: {startingYear}
Major: {majorMap[major]}
Email: {email}
""")

        if not found:
            print("Student not found with the provided ID")
            input()
            return
        else:
            # Checking the passed file for records of the passed programs
            found = 0
            with open(passedFile, "r") as file:
                for line in file:
                    if searchTerm in line:
                        courseId, id, date, grade = line.replace(
                            "\n", "").split(",")
                        with open(courseFile, "r") as newFile:
                            for line in newFile:
                                if courseId in line:
                                    found += 1
                                    courseId, name, credits, teachers = line.replace(
                                        "\n", "").split(",", 3)
                                    totalCredits += int(credits)
                                    obtainedGrade += int(grade)
                                    print(f"""
Course ID: {courseId}, Name: {name}, Credits: {credits}
Date: {date}, Teacher(s): {teachers}, grade: {grade}""")
            if found:
                print(
                    f"\nTotal credits:{totalCredits}, average grade:{obtainedGrade/found}")
            input()
        return


def clear():
    os.system('cls') if os.name == 'nt' else os.system("clear")


def exit():
    sys.exit()


if __name__ == '__main__':
    majorMap = {
        "CE": "Computational Engineering",
        "EE": "Electrical Engineering",
        "ET": "Energy Technology",
        "ME": "Mechanical Engineering",
        "SE": "Software Engineering"
    }
    while (True):
        choice = menu()
        choice()
