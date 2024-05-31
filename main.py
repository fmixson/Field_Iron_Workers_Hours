import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import lxml


import pandas as pd

from Hours_by_Student import Hours_by_Student
from Select_Course_Section import SelectSection
from Select_Semester import SelectSemester
from Total_Hours_by_Section import TotalSectionHours


def calculate_apprecticeship_hours(year, semester):
    global section_and_course
    global tr_table
    global df_sections
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    table = soup.find('select', {'onchange': 'New_Term(this.form)', 'name': 'term_code'})
    option_table = table.find_all('option')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    # for i in range(len(option_table)):
    s = SelectSemester(session=year + ' ' + semester, soup=soup, driver=driver)
    section_table = s.select_session()
    # section_table = soup.find('table', {'bgcolor': 'white'})
    tr_table = section_table.find_all('tr')
    for i in range(len(tr_table)):
        s = SelectSection(P_Period=p_period, driver=driver)
        section, course, course_date = s.selection_process(i + 1)
        if section == None:
            continue
        r = Hours_by_Student(section=section, course2=course, driver=driver)
        df_raw_section_data = r.raw_data_hours()
        df_empty = df_raw_section_data.empty
        if df_empty == True:
            continue
        t = TotalSectionHours(df_raw_section_data, course_date=course_date)
        t.total_section_hours()


s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get('https://secure.cerritos.edu/rosters/login.cgi')
login = driver.find_element(By.NAME,'login')
login.send_keys('gvasquez')
login = driver.find_element(By.NAME, 'passwd')
login.send_keys('Frankie29Lee!')
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clform')))
button = driver.find_element(By.XPATH, '//*[@id="login_form"]/table/tbody/tr[3]/td[2]/input').click()

# This waits for list of courses to load
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clform')))
# headers = ['NO', 'Name', 'ID', 'Grade', 'Hours', 'Other', 'Section', 'Course']
# df = pd.DataFrame(columns=headers)
pd.set_option('display.max_columns', None)
p_period = input("For what period would you like totals, P1, P2, P3, or Grand Total? ")
if p_period == "P1":
    year = input("Please provide the P1 year,e.g. 2020: ")
    calculate_apprecticeship_hours(year=year, semester='Summer')
    calculate_apprecticeship_hours(year=year, semester='Fall')
if p_period == "P2":
    year = input("Please provide the P2 year,e.g. 2020: ")
    calculate_apprecticeship_hours(year=year, semester='Spring')
if p_period == "P3":
    year = input("Please provide the P3 year,e.g. 2020: ")
    calculate_apprecticeship_hours(year=year, semester='Spring')
    calculate_apprecticeship_hours(year=year, semester='Summer')
if p_period == "Grand Total":
    p_period = "P1"
    year = input("Please provide the P1 year,e.g. 2020: ")
    year2 = input("Please provide the P3 year, e.g. 2020: ")
    calculate_apprecticeship_hours(year=year, semester='Summer')
    calculate_apprecticeship_hours(year=year, semester='Fall')
    p_period = "P3"
    calculate_apprecticeship_hours(year=year2, semester='Spring')
    calculate_apprecticeship_hours(year=year2, semester='Summer')

# df_raw_section_data.to_csv('C:/Users/family/Desktop/IWPA_Raw_Data.csv')
# df_sections.to_csv('C:/Users/family/Desktop/IWPA_Section_Totals.csv')

