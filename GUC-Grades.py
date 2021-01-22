# IMPORTS
from __future__ import print_function, unicode_literals
import os
import sys
import getpass
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from alive_progress import alive_bar
from PyInquirer import prompt, print_json

def getDataFromTable(table):
    ''' Extact Data from html table of grades '''
    table_soup = bs(table, 'html.parser')
    datasets = []
    for row in table_soup.find_all("tr")[1:]:
        element = []
        for item in row.find_all('td'):
            element.append(item.text.strip())
        datasets.append(element)

    # fix grades formate
    for element in datasets:
        grades = element[2].split()
        element[2] = ''
        for grade in grades:
            element[2] = element[2] + grade
    return datasets

def getMedtermGradesFromTable(table):
    ''' get Midterm Grades from html table'''
    table_soup = bs(table, 'html.parser')
    datasets = []
    for row in table_soup.find_all("tr")[1:]:
        element = []
        for item in row.find_all('td'):
            element.append(item.text.strip())
        datasets.append(element)
    return datasets

def getUpdatesDictionary(last_courses_grades, courses_grades):
    '''getting new updates in grades if there are any and return them as a dictionary'''
    updates = {}
    for course, elements in courses_grades.items():
        elements = sorted(elements)
        last_courses_grades[course] = sorted(last_courses_grades[course])
        course_updates = []
        for element in elements:
            try:
                last_courses_grades[course].index(element)
            except:
                course_updates.append(element)
        if len(course_updates) != 0:
            updates[course] = course_updates
    return updates


def displayUpdates(updates_dictionary):
    for index, element in enumerate(updates_dictionary):
        if list(updates_dictionary.keys())[index] == 'Midterms Grades':
            displayMidtermGrades(updates_dictionary, index)
        else:
            displayCourse(updates_dictionary, index)


def displayCourse(courses_grades, i):
    ''' Display Courses on the terminal'''
    os.system('cls' if os.name == 'nt' else 'clear')
    course_name = list(courses_grades.keys())[i]
    lines = courses_grades.get(course_name)

    print('-' * len(course_name))
    print(course_name)
    print('-' * len(course_name))
    print('\n')

    if len(lines) != 0:
        for line in lines:
            element = line[0] + ' ' + line[1]
            grade = line[2]
            ta = line[3]
            print ("{:<40} {:<15} {:<20}".format(element, grade, ta))
    else:
        print('## No Grades Appeared till now ##')
    print('\n')


def displayMidtermGrades(courses_grades, i):
    ''' Display Midterm Grades'''
    os.system('cls' if os.name == 'nt' else 'clear')
    key = list(courses_grades.keys())[i]
    lines = courses_grades.get(key)
    print('-' * len(key))
    print(key)
    print('-' * len(key))
    print('\n')
    if len(lines) != 0:
        for line in lines:
            course = line[0]
            grade = line[1]
            print ("{:<70} {:<10}".format(course, grade))
    else:
        print('## No Grades Appeared till now ##')

    print('\n')

# Display interactive menu

def displayCourseInteractive(courses_grades):
    os.system('cls' if os.name == 'nt' else 'clear')
    shift_in_case_of_update = 0
    options = list(courses_grades.keys())
    if len(updates_dictionary) != 0:
        options = ['There are new updates in grades check now'] + options
        shift_in_case_of_update = 1
    questions = {
        'type': 'list',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': options
    }
    terminal_menu = prompt(questions)
    choice_index = options.index(list(terminal_menu.values())[0])
    if options[choice_index] == 'There are new updates in grades check now':
        displayUpdates(updates_dictionary)
    elif options[choice_index] == 'Midterms Grades':
        displayMidtermGrades(courses_grades, 0)
    else:
        displayCourse(courses_grades, choice_index - shift_in_case_of_update)

def login_credenalties ():
    ''' loin to GUC portal'''
    if not os.path.isfile(".credenalites"):
        username = input("Enter your username : ")
        password = getpass.getpass(prompt="Enter Your Password : ")
        remember_me = input("Remember me ? [yes / no] : ")
        if remember_me[0].lower() == 'y':
            f = open(".credenalites", "w")
            f.write(username+"\n"+password)
            f.close()
    else:
        f = open(".credenalites", "r")
        lines = f.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        f.close()
    return username, password    

offline_mode = False

# CREDENALITES
username, password = login_credenalties()
# selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
browser = webdriver.Chrome(options=chrome_options)

while True:
    try:
        browser.get(f'http://{username}:{password}@student.guc.edu.eg/external/student/grade/CheckGrade.aspx/1')
        break
    except :
        options = ['Try again', 'Get grades from last session', 'Exit']
        print('Sorry there is a problem in connecting with GUC server')
        questions = {
            'type': 'list',
            'name': 'theme',
            'message': 'What do you want to do?',
            'choices': options
        }
        terminal_menu = prompt(questions)
        choice_index = options.index(list(terminal_menu.values())[0])
        if choice_index == 0:
            continue
        elif choice_index == 1:
            offline_mode = True
            browser.quit()
            break
        else:
            browser.quit()
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()

# fill the dictionary with courses and grades
courses_grades = {}

if offline_mode:
    with open('.courses_grades.json') as json_file:
        courses_grades = json.load(json_file)
else:
    # Get available courses names
    select = Select(browser.find_element_by_xpath('//*[@id="smCrsLst"]'))
    courses = [x.text for x in browser.find_elements_by_tag_name("option")]


    # Get midterm grades
    courses_grades['Midterms Grades'] = getMedtermGradesFromTable(browser.find_element_by_xpath('//*[@id="midDg"]').get_attribute('outerHTML'))

    while True:
        try:
            # Get courses grades
            with alive_bar(len(courses) - 1, title='getting grades', bar='circles') as bar:
                for i in range(1, len(courses)):
                    select = Select(browser.find_element_by_xpath('//*[@id="smCrsLst"]'))
                    select.select_by_index(i)
                    courses_grades[courses[i]] = getDataFromTable(browser.find_element_by_xpath('//*[@id="nttTr"]/td/table').get_attribute('outerHTML'))
                    bar()
                # Close the driver
                browser.quit()
                break
        except:
            print('Sorry a problem occurred when we get your grades from GUC server')
            options = ['Try again', 'Get grades from last session', 'Exit']
            questions = {
                'type': 'list',
                'name': 'theme',
                'message': 'What do you want to do?',
                'choices': options
            }
            terminal_menu = prompt(questions)
            choice_index = options.index(list(terminal_menu.values())[0])
            if choice_index == 1:
                with open('.courses_grades.json') as json_file: 
                    courses_grades = json.load(json_file)
                browser.quit()
                break
            else:
                browser.quit()
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit() 
updates_dictionary = {}

if not os.path.isfile(".courses_grades.json"):
    with open('.courses_grades.json', 'w') as file:
        file.write(json.dumps(courses_grades))
else:
    with open('.courses_grades.json') as json_file: 
        last_courses_grades = json.load(json_file) 
    updates_dictionary = getUpdatesDictionary(last_courses_grades, courses_grades)
    if len(updates_dictionary) != 0:
        with open('.courses_grades.json', 'w') as file:
            file.write(json.dumps(courses_grades))

# TODO Welcoming the user
# TODO handle error (if there is an error user can choose to get grades locally or try again)


def main():    
    while True:
        displayCourseInteractive(courses_grades)
        options = ['Choose another', 'Exit', 'Log out']
        questions = {
            'type': 'list',
            'name': 'theme',
            'message': 'What do you want to do?',
            'choices': options
        }
        terminal_menu = prompt(questions)
        choice_index = options.index(list(terminal_menu.values())[0])
        if choice_index == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()
        elif choice_index == 2:
            if os.path.isfile(".credenalites"):
                os.remove('.credenalites')
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()
if __name__ == "__main__":
    main()
