import time, sys, operator
import pandas as pd
from datetime import date, datetime
from functools import reduce
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
browser.get("https://www.eleadcrm.com/evo2/fresh/login.asp")
browser.implicitly_wait(10)
browser.maximize_window()
browser.get("https://www.eleadcrm.com/evo2/fresh/login.asp")
username = browser.find_element_by_id("user")
password = browser.find_element_by_id("password")
username.send_keys("Dealerfox")
password.send_keys("2017eldf1")
login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
login_attempt.click()
time.sleep(4)
if len(browser.window_handles) == 2:
    browser.switch_to.window(browser.window_handles[-1])
    browser.close()
time.sleep(2)
browser.switch_to.window(browser.window_handles[0])
desklog_click = browser.find_element_by_xpath("//span[@id='tdDeskLogImage']")
desklog_click.click()
iframe_child = browser.find_element_by_xpath('//iframe[contains(@id, "Main")]')
browser.switch_to.frame(iframe_child)
date_input = sys.argv[1]  # '3/31/18'
month = int(date_input.split('/')[0])
day = int(date_input.split('/')[1])
year = int(date_input.split('/')[2])
date_input_final = "{}/{}/{}".format(month, day, year)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Calendar')))
browser.execute_script(
    "var date_start = document.getElementById('Calendar'); date_start.readOnly = false; date_start.value = '{}'".format(
        date_input_final))
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Calendar2')))
browser.execute_script(
    "var date_end = document.getElementById('Calendar2'); date_end.readOnly = false; date_end.value = '{}'".format(
        date_input_final))
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'btnRefresh')))
refresh = browser.find_element_by_id('btnRefresh')
refresh.click()
time.sleep(2)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Filters_chkWebUps')))
check_internet = browser.find_element_by_xpath("//input[@id='Filters_chkWebUps']")
check_internet.click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Filters_chkPhoneUps')))
check_phone = browser.find_element_by_xpath("//input[@id='Filters_chkPhoneUps']")
check_phone.click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Filters_chkCampaignUps')))
check_campaign = browser.find_element_by_xpath("//input[@id='Filters_chkCampaignUps']")
check_campaign.click()
time.sleep(2)
num_customers = 0
table_var = "results"
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="results"]/tbody/tr')))
time.sleep(10)
num_customers = browser.find_elements_by_xpath('//table[@id="results"]/tbody/tr')
num_customers = len(num_customers)
print(num_customers)
result = {}
unique_customers = []
for record in range(0, num_customers):
    if record > 0:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'Main')))
        iframe_child = browser.find_element_by_xpath('//iframe[contains(@id, "Main")]')
        browser.switch_to.frame(iframe_child)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'DataPanel_ContentMain_CustomerName_{}'.format(record))))
    script = "document.getElementById('DataPanel_ContentMain_CustomerName_{}').scrollIntoView();".format(record)
    browser.execute_script(script)
    temp_table = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='DataPanel_ContentMain_CustomerName_{}']".format(record))))
    temp_table.click()
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(3)
    try:
        wait = WebDriverWait(browser, 10)
        opn_panel = wait.until(EC.presence_of_element_located((By.ID, 'OpportunityPanel_ViewPrevOpptyLink')))
        opn_panel.click()
        time.sleep(2)
    except:
        pass
    time.sleep(2)
    WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.ID, 'OpportunityPanel_ActiveOpptyPanel')))
    WebDriverWait(browser,40).until(EC.presence_of_element_located((By.ID,'CustomerInfoPanel_lblPersonID')))
    customer_id = browser.find_element_by_id('CustomerInfoPanel_lblPersonID').text
    if customer_id in unique_customers:
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        continue
    unique_customers.append(customer_id)
    source_type_panel = browser.find_elements_by_xpath(
        "//*[@id='OpportunityPanel_ActiveOpptyPanel']/table/tbody/tr[6]/td")
    rep_row = browser.find_elements_by_xpath(
        "//*[@id='OpportunityPanel_ActiveOpptyPanel']/table/tbody/tr[5]/td")
    source_type = source_type_panel[1].text.strip()
    source_detail_panel = browser.find_elements_by_xpath(
        "//*[@id='OpportunityPanel_ActiveOpptyPanel']/table/tbody/tr[7]/td")
    source_detail = source_detail_panel[1].text.strip()
    if 'Online Shopper' in source_detail:
        source_detail = 'Online Shopper'.lower()
    if 'Repeat' in source_detail:
        source_detail = 'Previous Customer'.lower()
    elif '|' in source_detail:
        source_detail = source_detail.split('|')
        source_detail = source_detail[0].strip().replace(' com', '.com').lower()
    if source_type not in result.keys():
        result[source_type] = {}
    if source_detail not in result[source_type].keys():
        result[source_type][source_detail] = {'L': 1, 'A': 0, 'S': 0, 'C': 0}
    else:
        result[source_type][source_detail]['L'] += 1
    iframe1 = browser.find_element_by_id('tabsTargetFrame')
    browser.switch_to.frame(iframe1)
    oddRows = browser.find_elements_by_class_name("odd")
    evenRows = browser.find_elements_by_class_name("even")
    for i in oddRows:
        s = i.text
        s = s.split('\n')
        s = [x for x in s if x]
        t = [i.split(' ') for i in s]
        if len(t) > 0:
            flat_list = reduce(operator.add, t)
            flat_list = [x for x in flat_list if x]
            if date_input in flat_list and 'Appointment' in s[1]:
                result[source_type][source_detail]['A'] += 1
                if 'Show' in s[2] and 'No Show' not in s[2]:
                    result[source_type][source_detail]['S'] += 1
    for i in evenRows:
        s = i.text
        s = s.split('\n')
        s = [x for x in s if x]
        t = [i.split(' ') for i in s]
        if len(t) > 0:
            flat_list = reduce(operator.add, t)
            flat_list = [x for x in flat_list if x]
            if date_input in flat_list and 'Appointment' in s[1]:
                result[source_type][source_detail]['A'] += 1
                if 'Show' in s[2] and 'No Show' not in s[2]:
                    result[source_type][source_detail]['S'] += 1
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'gvOpptyHistory')))
    div_comp_contacts = browser.find_element_by_id('gvOpptyHistory')
    headerRows = browser.find_elements_by_class_name('PageHeader')
    for rows_cch in headerRows:
        if ('Sold - CRM Sold' in rows_cch.text or 'Sold - DMS Sold' in rows_cch.text) and date_input in rows_cch.text:
            #print("Sold")
            result[source_type][source_detail]['C'] += 1
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
browser.quit()
format_str = '%m/%d/%y'
datetime_obj = datetime.strptime(date_input, format_str)
day_of_week = datetime_obj.date().strftime("%a")
month_of_year = datetime_obj.date().strftime("%b")
count = -1
df = pd.DataFrame(columns=['Date', 'month', 'Day of week', 'source_type', 'source_detail', 'L', 'A', 'S', 'C'])
for src_type in result:
    for src in result[src_type]:
        count += 1
        df.loc[count] = [datetime_obj.date().strftime('%Y-%m-%d'), month_of_year, day_of_week, src_type.strip(),
                         src.strip(),
                         result[src_type][src]['L'],
                         result[src_type][src]['A'], result[src_type][src]['S'], result[src_type][src]['C']]
date_input_final = date_input_final.replace('/', '-')
print('inserted {} succesfully'.format(date_input))
# df.to_csv('LASC_{}.csv'.format(date_input_final))
# import boto3
# s3 = boto3.resource('s3')
# data = open('LASC_{}.csv'.format(date_input_final), 'rb')
# s3.Bucket('eleads-scraper-data').put_object(Key='LASC/LASC_{}.csv'.format(date_input_final), Body=data)
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/CRM")
df.to_sql(con=engine, name='Eleads1', if_exists='append', index=False)
