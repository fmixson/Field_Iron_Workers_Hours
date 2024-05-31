from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# from AED import driver


class SelectSection:

    def __init__(self, P_Period, driver):
        self.P_Period = P_Period
        self.driver = driver

    def selection_process(self, i):

        def _completion_date_formatting():
            button2 = self.driver.find_element_by_xpath(
                '//*[@id="clform"]/table/tbody/tr[' + str(i) + ']/td[1]/input').click()
            # This waits until roster open to run
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'college')))
            # This clicks on final grades link
            course_date = self.driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[4]/td[3]').text
            course_date_split = course_date.split()
            return course_date_split

        def _section_number_formatting():
            global section_and_course
            course = self.driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[3]').text
            cutup = course.split()
            for word in cutup:
                if "(" in word:
                    section = word
                    # section = cutup[4]
                    section = section[1:]
            course2 = cutup[0] + ' ' + cutup[1][:5]
            return section, course2

        global section_and_course
        counted_course = self.driver.find_element_by_xpath('//*[@id="clform"]/table/tbody/tr[' + str(i) + ']/td[2]').text
        if (counted_course != "AED 40.01") and ("IWAP" not in counted_course):
            section = None
            course = None
            course_date = None
            pass
        else:
            course_date_split = _completion_date_formatting()
            P1_eligible_months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            P2_eligible_months = ['Jan', 'Feb', 'Mar', 'Apr']
            P3_eligible_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

            if self.P_Period == "P1":
                eligible = P1_eligible_months
            elif self.P_Period == "P2":
                eligible = P2_eligible_months
            elif self.P_Period == "P3":
                eligible = P3_eligible_months

            if course_date_split[9] in eligible:
                section, course = _section_number_formatting()
                course_date = course_date_split[9]
            elif course_date_split[10] in eligible:
                section, course = _section_number_formatting()
                course_date = course_date_split[10]
            elif course_date_split[11] in eligible:
                section, course = _section_number_formatting()
                course_date = course_date_split[11]
            else:
                self.driver.back()
                section = None
                course = None
                course_date = None
        return section, course, course_date

