import pandas as pd


class TotalSectionHours:
    headers2 = ['Course', 'Section', 'Total', 'End Date']
    df_sections = pd.DataFrame(columns=headers2)
    length = 0

    def __init__(self, df_raw_section_data, course_date):
        self.df_raw_section_data = df_raw_section_data
        self.course_date = course_date

    def total_section_hours(self):
        course = 0
        section = 0
        total_hours = 0
        section_hours = []

        for i in range(len(self.df_raw_section_data)):
            section = self.df_raw_section_data.loc[i, 'Section']
            course = self.df_raw_section_data.loc[i, 'Course']
            hours = self.df_raw_section_data.loc[i, 'Hours']
            hours = hours.split()
            hours = hours[0]
            if hours == 'hours':
                hours = 0
            hours = float(hours)
            total_hours = total_hours + hours

        section_hours.append(course)
        section_hours.append(section)
        section_hours.append(total_hours)
        section_hours.append(self.course_date)
        TotalSectionHours.df_sections.loc[TotalSectionHours.length] = section_hours
        TotalSectionHours.length = TotalSectionHours.length + 1
        print('df sections', TotalSectionHours.df_sections)
        TotalSectionHours.df_sections.to_csv('C:/Users/fmixson/Desktop/IWPA_Section_Totals.csv')
