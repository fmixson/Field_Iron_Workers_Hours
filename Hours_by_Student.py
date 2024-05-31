import pandas as pd
from bs4 import BeautifulSoup
# from selenium.webdriver.android import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

global df_raw_section_data


class Hours_by_Student:
    global df_raw_section_data

    def __init__(self, section, course2, driver):
        self.section = section
        self.course2 = course2
        self.driver = driver

    def raw_data_hours(self):

        def table3_function():
            table3 = table.find_all('tr')[1:]
            for j in table3:
                raw_section_data = j.find_all('td')
                row = [tr.text for tr in raw_section_data]
                row.append(self.section)
                row.append(self.course2)
                try:
                    length = len(df_raw_section_data)
                    df_raw_section_data.loc[length] = row
                except:
                    continue
            self.driver.back()
            self.driver.back()

        headers = ['NO', 'Name', 'ID', 'Grade', 'Hours', 'Other', 'Section', 'Course']
        df_raw_section_data = pd.DataFrame(columns=headers)
        final_hours = self.driver.find_element_by_xpath('//*[@id="FinalGrades_form"]/a').click()
        course = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[3]').text
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'Roster_form')))
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        table = soup.find('table', {'bgcolor': 'white', 'cellpadding': '5', 'cellspacing': '0'})
        try:
            table2 = table.find_all('th')
            table3_function()
        except:
            self.driver.back()
            self.driver.back()

        return df_raw_section_data
