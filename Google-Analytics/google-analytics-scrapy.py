import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from datetime import datetime
df = pd.DataFrame(
columns=['Month', 'Type', 'New_Users','Bounce_Rate', 'Average_Session','Total_Users' , 'Local_Users'])
count = 0

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
browser.get("https://analytics.google.com")
username = browser.find_element_by_id("identifierId")
username.send_keys('dan@dealerfox.com')
next_button = browser.find_element_by_id("identifierNext").click()
time.sleep(3)
password = browser.find_element_by_xpath("//input[@type='password']")
password.send_keys('2025DFdf!2')
next_button = browser.find_element_by_id("passwordNext").click()
WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.TAG_NAME, 'suite-universal-picker')))
time.sleep(3)
univ_button = browser.find_element_by_tag_name('suite-universal-picker')
univ_button.click()
time.sleep(2)
a = browser.find_elements_by_class_name('md-virtual-repeat-offsetter')
a[3].find_elements_by_tag_name('li')[-2].click()
time.sleep(2)
WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.XPATH, "//li[@value='138549011']")))
oaklawnmazda = browser.find_element_by_xpath("//li[@value='138549011']").click()
time.sleep(1)
WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.XPATH, "//li[@value='142861518']")))
all_website_data = browser.find_element_by_xpath("//li[@value='142861518']").click()
# WebDriverWait(browser, 50).until(
#     EC.presence_of_element_located((By.XPATH, "//li[@aria-label='Ultimo Motors Dealer Inspire']")))
# ultimo = browser.find_element_by_xpath("//li[@aria-label='Ultimo Motors Dealer Inspire']").click()
# time.sleep(1)
# WebDriverWait(browser, 50).until(EC.presence_of_element_located(
#     (By.XPATH, "//li[@aria-label='Ultimo Motors Dealer Inspire' and @value='96400243']")))
# ultimo_sub = browser.find_element_by_xpath(
#     "//li[@aria-label='Ultimo Motors Dealer Inspire' and @value='96400243']").click()
# time.sleep(1)
# WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.XPATH, "//li[@value='100550847']")))
# all_website_data = browser.find_element_by_xpath("//li[@value='100550847']").click()
time.sleep(5)
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[3].click()")
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[4].click()")
time.sleep(2)
browser.switch_to.frame('galaxyIframe')
time.sleep(2)
date_picker = browser.find_element_by_id('ID-reportHeader-dateControl').click()
from_date = '5/1/2018'
to_date = '5/20/2018'
b = datetime.strptime(from_date, '%m/%d/%Y')
b = b.strftime('%Y-%m-%d')
time.sleep(1)
from_date_fill = browser.find_element_by_xpath(
    "//input[@type='text'][@class='ID-datecontrol-primary-start _GATg ACTION-daterange_input TARGET-primary_start _GAfl']")
from_date_fill.clear()
from_date_fill.send_keys(from_date)
to_date_fill = browser.find_element_by_xpath(
    "//input[@type='text'][@class='ID-datecontrol-primary-end _GATg ACTION-daterange_input TARGET-primary_end']")
to_date_fill.clear()
to_date_fill.send_keys(to_date)
apply_date = browser.find_element_by_xpath("//input[@type='button'][@value='Apply']").click()
time.sleep(2)
x = browser.find_element_by_id('ID-overview-sparkline')
y = x.find_elements_by_class_name('_GAGu')

all_users = y[0].text.replace(',','')
new_users = y[1].text.replace(',','')
avg_session = y[6].text
bounce_rate = y[7].text
time.sleep(2)
browser.switch_to.default_content()
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[12].click()")
time.sleep(2)
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[14].scrollIntoView()")
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[14].click()")
browser.switch_to.frame('galaxyIframe')
time.sleep(3)
country = browser.find_element_by_id("ID-geo-table-dataTable-key-0-0").click()
local_list = ['Illinois', 'Wisconsin', 'Michigan', 'Indiana']
time.sleep(4)
local_states = browser.find_elements_by_xpath("//table[@id='ID-rowTable']/tbody/tr")
all_local_users = 0
for i in range(len(local_states)):
    if local_states[i].text.split('\n')[0].split(' ')[1] in local_list:
        all_local_users += int(local_states[i].text.split('\n')[1].split('(')[0].replace(',', ''))
df.loc[count]= [b, 'Website', new_users, bounce_rate,avg_session,all_users,all_local_users]
browser.switch_to.default_content()
mobile_list = ['mobile', 'desktop']
time.sleep(2)
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[17].scrollIntoView()")
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[17].click()")
time.sleep(1)
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[18].click()")
time.sleep(4)
browser.switch_to.frame('galaxyIframe')
mob_desk_elements = browser.find_elements_by_xpath("//table[@id='ID-rowTable']/tbody/tr")
for i in range(len(mob_desk_elements)):
    if mob_desk_elements[i].text.split('\n')[0].split(' ')[1] in mobile_list:
        count +=1
        df.loc[count] = [b, mob_desk_elements[i].text.split('\n')[0].split(' ')[1],mob_desk_elements[i].text.split('\n')[2].split('(')[0].replace(',',''),mob_desk_elements[i].text.split('\n')[4],mob_desk_elements[i].text.split('\n')[6],0,0]
time.sleep(2)
browser.switch_to.default_content()
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[3].click()")
time.sleep(1)
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[4].click()")
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[6].click()")
browser.execute_script("document.getElementsByClassName('ga-nav-link-label ng-binding ng-scope')[7].click()")
time.sleep(1)
organic_list = ['Paid Search', 'Organic Search']
browser.switch_to.frame('galaxyIframe')
org_paid_elements = browser.find_elements_by_xpath("//table[@id='ID-rowTable']/tbody/tr")
# for i in range(len(org_paid_elements)):
#     if org_paid_elements[i].text.split('\n')[0].split('.')[1].strip() in organic_list:
#         print(org_paid_elements[i].text.split('\n')[0].split('.')[1].strip(),
#               org_paid_elements[i].text.split('\n')[2].split('(')[0], org_paid_elements[i].text.split('\n')[4],
#               org_paid_elements[i].text.split('\n')[6])
browser.switch_to.default_content()
print(df)
browser.quit()
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/Dominion")
df.to_sql(con=engine, name='Google_Analytics', if_exists='append', index=False)
print('inserted successfully')

