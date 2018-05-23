import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

option = webdriver.ChromeOptions()
# option.add_argument(" — incognito")
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

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'MenuSections_SectionLabel_11')))
telephony = browser.find_element_by_id('MenuSections_SectionLabel_11').click()

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Car Wars Pro: Staff Activity')))
staff_activity = browser.find_element_by_link_text('Car Wars Pro: Staff Activity').click()

iframe = browser.find_element_by_xpath('//iframe[contains(@id, "Main")]')
browser.switch_to_frame(iframe)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'go_username')))
go_username = browser.find_element_by_id("go_username").send_keys("dealerfox")
go_password = browser.find_element_by_id("go_password").send_keys("2017ELdf1")
go_login = browser.find_element_by_xpath("//*[@type='submit']").click()
time.sleep(5)
#WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'mobile_a')))
browser.execute_script("document.getElementsByClassName('mobile_a')[0].click();")
time.sleep(4)
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Day')))
date_select = browser.find_element_by_link_text('Month')
browser.execute_script("arguments[0].click();",date_select)

#################################################################################

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'table1')))
table_rep = browser.find_element_by_id("table1")
time.sleep(2)
table_rows = table_rep.find_elements_by_tag_name("tr")

import pandas as pd

month = int(date.today().strftime("%m"))
day = int(date.today().strftime("%d"))
year = int(date.today().strftime("%y"))
day_of_week = date.today().strftime("%a")
today = "{}/{}/{}".format(month, day, year)
month_of_year = date.today().strftime("%b")
df = pd.DataFrame(columns=['Date', 'mon','Day of week', 'Names', 'Total Outbound', 'Live Conversations', 'Booked Appointments Firm','Average talk Time'])
for i in range(1, len(table_rows) - 1):
    WebDriverWait(table_rows[i], 10).until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
    table_data = table_rows[i].find_elements_by_tag_name('td')
    df.loc[i - 1] = [today, month_of_year,day_of_week, table_data[0].text, table_data[1].text, table_data[4].text,
                     table_data[8].text.split('|')[0], table_data[10].text]
df.to_csv('carwarsbdc_{}-{}.csv'.format(month,year))
browser.quit()

time.sleep(1)
import boto3

s3 = boto3.resource('s3')
data = open('carwarsbdc_{}-{}-{}.csv'.format(month, day,year), 'rb')
s3.Bucket('eleads-scraper-data').put_object(Key='CARWARS_BDC/carwarsbdc_{}-{}.csv'.format(month,year), Body=data)