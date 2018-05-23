from datetime import datetime
from time import sleep
import pandas as pd
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
browser.set_window_size(1410,803)
browser.get("https://oaklawnmazda.dominioncrm.com/")
username = browser.find_element_by_xpath("//input[@type='text']")
username.send_keys('dantrinidad')
sleep(2)
password = browser.find_element_by_xpath("//input[@type='password']")
password.send_keys('2025DMdf!')
login_attempt = browser.find_element_by_xpath("//button[@class='b b-success clickable']")
login_attempt.click()
result_sold = {}
result_leads = {}
sleep(2)
browser.find_element_by_xpath("//a[@title='Reports']").click()
sleep(2)
browser.execute_script("document.getElementsByClassName('reports--menu--report clickable')[5].click()")
sleep(2)
date_fields = browser.find_elements_by_class_name("field--input")
date_fields[0].send_keys('3/01/2018')
date_fields[1].send_keys('3/31/2018')
sleep(2)
browser.find_element_by_xpath("//button[@class='report--refresh clickable']").click()
sleep(2)
table = browser.find_elements_by_class_name("report--table")
rows = table[0].find_elements_by_class_name("report--table--body--row")
num_rows = len(rows)
unique_customers = []

for i in range(0,num_rows-1):
    source = ''
    customer_name = rows[i].find_elements_by_tag_name("td")[0].text.split('\n')[0]
    if customer_name in unique_customers:
        continue
    unique_customers.append(customer_name)
    date_from = rows[i].find_elements_by_tag_name("td")[4].text.split('\n')[0]
    datetime_object = datetime.strptime(date_from, '%m-%d-%y')
    date_input = datetime_object.strftime('%Y-%m-%d')
    source_detail = rows[i].find_elements_by_tag_name("td")[5].text
    source_detail = source_detail.split('\n')

    if len(source_detail) == 1:
        if source_detail[0] == 'Internet':
            source = 'Dealer Website'
        elif 'Walk' in source_detail[0]:
            source = 'Showroom'
        elif 'Phone' in source_detail[0]:
            source = 'Phone'
    elif len(source_detail) == 2:
        if 'Billboard' in source_detail[1] or 'Live Local' in source_detail[1] or 'Not Listed' in source_detail[1] or 'Referral' in source_detail[1]:
            source = 'Showroom'
        elif 'Search Engine' in source_detail[1]:
            source = 'oaklawnmazda.com'
        else:
            source = source_detail[-1]
    if date_input not in result_sold.keys():
        result_sold[date_input] = {}
        result_leads[date_input] = {}
    if source not in result_sold[date_input].keys():
        result_sold[date_input][source] = {'C': 1}
        result_leads[date_input][source] = {'L':0}
    else:
        result_sold[date_input][source]['C'] += 1
    #print(date_input, source, 'count',i)

browser.quit()
count = -1
df = pd.DataFrame(columns=['Date', 'source_detail', 'C'])
for date_input in result_sold:
    for src in result_sold[date_input]:
        count += 1
        df.loc[count] = [date_input,
                         src,
                         result_sold[date_input][src]['C']]
count =-1
df_leads = pd.DataFrame(columns=['Date', 'source_detail', 'L'])
for date_input in result_leads:
    for src in result_leads[date_input]:
        count += 1
        df_leads.loc[count] = [date_input,
                         src,
                         result_leads[date_input][src]['L']]
print(result_leads)
print(result_sold)
# print(df)
# print(df_leads)
#-------------------------- SQL INSERT and UPDATE ---------------------------------#

from sqlalchemy import create_engine
engine = create_engine(
    "mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/Dominion")
df.to_sql(con=engine, name='Sold', if_exists='append', index=False)
df_leads.to_sql(con=engine, name='Leads', if_exists='append', index=False)
print('inserted successfully')

