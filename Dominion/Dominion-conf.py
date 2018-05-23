from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

option = webdriver.ChromeOptions()
#option.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
browser.get("https://oaklawnmazda.dominioncrm.com/")
username = browser.find_element_by_xpath("//input[@type='text']")
username.send_keys('dantrinidad')
sleep(1)
password = browser.find_element_by_xpath("//input[@type='password']")
password.send_keys('2025DMdf!')
login_attempt = browser.find_element_by_xpath("//button[@class='b b-success clickable']")
login_attempt.click()
sleep(1)
WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//a[text()='Leads']")))
leads = browser.find_element_by_xpath("//a[text()='Leads']")
leads.click()
sleep(2)
opportunity_module = browser.find_element_by_xpath("//div[@class='report--module report--module--ungrouped report--module--opportunitysourcing report--module--series--count--4 report--module--bg--undefined report--module--text--undefined report--module--text--accent--undefined']")
start_date = opportunity_module.find_elements_by_tag_name('h2')
start_date = start_date[0].text
start_date = start_date.split('-')[0].strip()
table_rows_opp_module = opportunity_module.find_elements_by_tag_name('tr')
phone_in = table_rows_opp_module[2].find_elements_by_tag_name('td')
walk_in = table_rows_opp_module[3].find_elements_by_tag_name('td')

datetime_object = datetime.strptime(start_date, '%m/%d/%y')
date_input = datetime_object.strftime('%Y-%m-%d')

df = pd.DataFrame(columns=['Date', 'source_detail', 'L', 'A', 'S', 'C'])
df.loc[0] = [date_input,'Phone', phone_in[0].text,phone_in[3].text,phone_in[1].text,phone_in[4].text]
df.loc[1] = [date_input, 'Walk in',walk_in[0].text,walk_in[3].text,walk_in[1].text,walk_in[4].text ]

browser.quit()

print(df)
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/Dominion")
df.to_sql(con=engine, name='Traditional', if_exists='append', index=False)
print('inserted successfully')