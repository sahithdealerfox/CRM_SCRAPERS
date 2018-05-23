import time
from datetime import date
from functools import reduce
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

'''browser = webdriver.Remote(command_executor="http://sandel153:b1eb82d6-e29a-4ee0-a29f-a8a82ffa56d6@ondemand.saucelabs.com:80/wd/hub",
   desired_capabilities={"browserName" : "chrome",
       "platform": "Windows 10",
       "version" : "65.0",
        })'''
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
desklog_click = browser.find_element_by_xpath("//span[@id='tdDeskLogImage']")
desklog_click.click()
iframe1 = browser.find_element_by_xpath('//iframe[contains(@id, "Main")]')
browser.switch_to_frame(iframe1)
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

time.sleep(5)
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="results"]')))
num_customers = browser.find_elements_by_xpath('//table[@id="results"]/tbody/tr')
num_customers = len(num_customers)
print(num_customers)

result = {}
month = int(date.today().strftime("%m"))
day = int(date.today().strftime("%d"))
year = int(date.today().strftime("%y"))
month_of_year = date.today().strftime("%b")
day_of_week = date.today().strftime("%a")
today = "{}/{}/{}".format(month, day, year)

for record in range(0, num_customers):
    if record > 0:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, 'Main')))
        iframe_child = browser.find_element_by_xpath('//iframe[contains(@id, "Main")]')
        browser.switch_to.frame(iframe_child)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'DataPanel_ContentMain_CustomerName_{}'.format(record))))
    script = "document.getElementById('DataPanel_ContentMain_CustomerName_{}').scrollIntoView();".format(record)
    browser.execute_script(script)
    temp_table = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='DataPanel_ContentMain_CustomerName_{}']".format(record))))
    temp_table.click()
    if len(browser.window_handles) > 0:
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(5)
        browser.execute_script(
            "var i = document.getElementById('OpportunityPanel_ViewPrevOpptyLink'); if (i != null) {i.click()};")
        source_type_panel = browser.find_elements_by_xpath(
            "//*[@id='OpportunityPanel_ActiveOpptyPanel']/table/tbody/tr[6]/td")
        source_type = source_type_panel[1].text.strip()
        rep_row = browser.find_elements_by_xpath(
            "//*[@id='OpportunityPanel_ActiveOpptyPanel']/table/tbody/tr[5]/td")
        rep_name = rep_row[1].text.split('-')[0].strip()
        source_detail_panel = browser.find_elements_by_xpath(
            "//*[@id='OpportunityPanel_ActiveOpptyPanel']/table/tbody/tr[7]/td")
        source_detail = source_detail_panel[1].text.strip()

        if 'Online Shopper' in source_detail:
            source_detail = 'Online Shopper'
        if 'Repeat' in source_detail:
            source_detail = 'Previous Customer'
        elif '|' in source_detail:
            source_detail = source_detail.split('|')
            source_detail = source_detail[-1].strip()
        if source_detail == 'Dealer Website':
            source_detail = 'Online Shopper'

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
                import operator

                flat_list = reduce(operator.add, t)
                flat_list = [x for x in flat_list if x]
                if today in flat_list and ('View' in flat_list[-2] or 'View' in flat_list[-3]):
                    if 'Appointment' in s[1] :
                        result[source_type][source_detail]['A'] += 1
                        print(' Appointment : ',s)

                if today in flat_list and 'Complete' in flat_list[-2] and 'Edit' in flat_list[-1]:
                    if 'Appointment' in s[1]:
                        result[source_type][source_detail]['A'] += 1
                        print(' Appointment : ',s)

                if today in flat_list and ('View' in flat_list[-2] or 'View' in flat_list[-3]):
                    if 'Show' in flat_list[4] or 'Show' in flat_list[5]:
                        result[source_type][source_detail]['S'] += 1
                        print(' Shown : ',s)

        for i in evenRows:
            s = i.text
            s = s.split('\n')
            s = [x for x in s if x]
            t = [i.split(' ') for i in s]
            if len(t) > 0:
                import operator
                flat_list = reduce(operator.add, t)
                flat_list = [x for x in flat_list if x]
                if today in flat_list and ('View' in flat_list[-2] or 'View' in flat_list[-3]):
                    if 'Appointment' in s[1]:
                        result[source_type][source_detail]['A'] += 1
                        print(' Appointment : ', s)
                if today in flat_list and 'Complete' in flat_list[-2] and 'Edit' in flat_list[-1]:
                    if 'Appointment' in s[1]:
                        result[source_type][source_detail]['A'] += 1
                        print(' Appointment : ', s)

                if today in flat_list and ('View' in flat_list[-2] or 'View' in flat_list[-3]):
                    if ('Show' in flat_list[3]) and ('No Show' not in flat_list[3]):
                        result[source_type][source_detail]['S'] += 1
                        print(' Shown : ', s)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'gvOpptyHistory')))
        div_comp_contacts = browser.find_element_by_id('gvOpptyHistory')
        rows_cch = div_comp_contacts.find_elements_by_tag_name('tr')
        if 'Sold - CRM Sold' in rows_cch[0].text or 'Sold - DMS Sold' in rows_cch[0].text and date.today().strftime("%m/%d/%y") in rows_cch[0].text:
            result[source_type][source_detail]['C'] += 1
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
browser.quit()
count = -1
df = pd.DataFrame(columns=['Date', 'month', 'Day of week', 'source_type', 'source_detail', 'L', 'A', 'S', 'C'])
for src_type in result:
    for src in result[src_type]:
        count += 1
        df.loc[count] = [today, month_of_year, day_of_week, src_type.strip(), src.strip(), result[src_type][src]['L'],
                         result[src_type][src]['A'], result[src_type][src]['S'], result[src_type][src]['C']]
today = "{}-{}-{}".format(month, day, year)
df.to_csv('LASC_{}.csv'.format(today))
# time.sleep(1)
# import boto3
#
# s3 = boto3.resource('s3')
# data = open('LASC_{}.csv'.format(today), 'rb')
# s3.Bucket('eleads-scraper-data').put_object(Key='LASC/LASC_{}.csv'.format(today), Body=data)