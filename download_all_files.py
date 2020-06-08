from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import shutil
import time


def get_groups():
    return [[('К01-121', '2014'), ('К03-121', '2015'), ('Б14-503', '2016')],
            [('К01-122', '2014'), ('К03-122', '2015'), ('Б14-504', '2016')],
            [('К01-121', '2015'), ('Б15-502', '2016'), ('Б15-502', '2017')],
            [('Б16-503', '2016'), ('Б16-503', '2017'), ('Б16-503', '2018')],
            [('Б16-513', '2016'), ('Б16-513', '2017'), ('Б16-513', '2018')]]

def get_old_groups():
    return [[('К01-121', '2012'), ('К03-121', '2013'), ('К05-121', '2014')],
            [('К01-122', '2012'), ('К03-122', '2013'), ('К05-122', '2014')],
            [('К01-123', '2012'), ('К03-123', '2013'), ('К05-123', '2014')],
            [('К01-121', '2013'), ('К03-121', '2014'), ('К05-121', '2015')],
            [('К01-122', '2013'), ('К03-122', '2014'), ('К05-122', '2015')],
            [('К01-123', '2013'), ('К03-123', '2014'), ('К05-123', '2015')]]



def run_browser():
    browser = webdriver.Chrome()
    browser.get('https://eis.mephi.ru/ReportServer_SQL2008/Pages/ReportViewer.aspx?%2fStudAtt%2fsvodSession&rs%3aCommand=Render&year=2018&semn=1')
    return browser

def make_automatic_download(browser):
    groups = get_groups()
    for full_group_data in groups:
        true_name = full_group_data[-1][0] if full_group_data[-1][0][0] == 'Б' else \
            f'Б{full_group_data[0][1][-2:]}-50{2+int(full_group_data[0][0][-1])}'
        for idx, group_data in enumerate(full_group_data):
            group = group_data[0]
            year = group_data[1]
            get_one_svod(browser, year, 'осенний', group, true_name, 2 * idx + 1)
            if 'К' in group:
                group = f"{group[:2]}{int(group[2])+1}{group[3:]}"
            get_one_svod(browser, year, 'весенний', group, true_name, 2 * idx + 2)

def get_one_svod(browser, year, term_feature, group, true_group_name, term_number=0):
    browser.refresh()
    name = browser.find_element_by_css_selector('#ReportViewerControl_ctl00_ctl05_txtValue')
    name.clear()
    name.send_keys(group) # now we put group_name in input field
    name.send_keys(Keys.RETURN) # press Enter
    year_choice = browser.find_element_by_css_selector('#ReportViewerControl_ctl00_ctl03_ddValue')
    year_choice.send_keys(year) # we chose the year
    term = browser.find_element_by_css_selector('#ReportViewerControl_ctl00_ctl07_ddValue')
    term.send_keys(term_feature) # now we chose if the term is autumm or spring
    look_report_button = browser.find_element_by_css_selector('#ReportViewerControl_ctl00_ctl00')
    look_report_button.click() # now we will see the table report
    file_type_choice = browser.find_element_by_css_selector('#ReportViewerControl_ctl01_ctl05_ctl00')
    file_type_choice.send_keys('CSV') # we chose CSV type and now we can download it
    download_button = browser.find_element_by_css_selector('#ReportViewerControl_ctl01_ctl05_ctl01')
    download_button.click() # download the file
    browser.get('https://eis.mephi.ru/ReportServer_SQL2008/Pages/ReportViewer.aspx?%2fStudAtt%2fsvodSession&rs%3aCommand=Render&year=2018&semn=1')
    time.sleep(0.5)
    file_path = f"{os.getenv('HOME')}/Загрузки"
    file_name = max([file_path +"/"+ f for f in os.listdir(file_path)], key=os.path.getctime)
    new_path = f"{os.getenv('HOME')}/Diploma/new_svod/{file_name.split('/')[-1]}"
    shutil.move(file_name, new_path)
    os.rename(new_path, f"{'/'.join(new_path.split('/')[:-1])}/SvodSession_{true_group_name}_{term_number}.csv")
    print(f'{group} {year}_{term_feature}')
