from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

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

sleep(2)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Leads']")))
leads = browser.find_element_by_xpath("//a[text()='Leads']")
leads.click()
sleep(5)
opportunity_module = browser.find_element_by_xpath(
    "//div[@class='report--module report--module--ungrouped report--module--opportunitysourcing report--module--series--count--4 report--module--bg--undefined report--module--text--undefined report--module--text--accent--undefined']")
table_rows_opp_module = opportunity_module.find_elements_by_tag_name('tr')
customers = table_rows_opp_module[1].find_elements_by_tag_name('td')
meets = customers[3]
meets.click()
result_appts = {}
result_leads = {}
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='drilldowns--body']")))
articles_panel = browser.find_elements_by_xpath("//div[@class='drilldowns--body']")
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='drilldowns--count']")))
articles_count = articles_panel[0].find_elements_by_xpath("//span[@class='drilldowns--count']")
num_customers = articles_count[-1].text
num_customers = int(num_customers)
scroll_times = -(-num_customers // 30) - 1
if num_customers >=30:
    for i in range(1,scroll_times+1):
        browser.execute_script(" var a =document.getElementsByTagName('article'); a[{} * 30].scrollIntoView(); ".format(i))
        sleep(3)

for i in range(0,num_customers):
    sleep(1)
    browser.execute_script("document.getElementsByClassName('drilldown--header clickable')[{}].click();".format(i))
    date_input = browser.execute_script(
        "var ele = document.getElementsByClassName('drilldown--header clickable'); var date_input = ele[{}].getElementsByClassName('drilldown--h2  drilldown--date')[0].innerHTML ; return date_input".format(
            i))
    date_input = date_input.replace(',', '')
    datetime_object = datetime.strptime(date_input, '%a %b %d %Y %I:%M%p')
    date_input = datetime_object.strftime('%Y-%m-%d')
    sleep(5)
    browser.execute_script("document.getElementsByClassName('activity--history--right')[0].scrollIntoView();")
    source_detail = ''
    sleep(1)
    try:
        leads = browser.find_element_by_xpath("//span[@class='activity--history--filter--label' and text()='Lead']")
        leads.click()
        div_activities = browser.find_elements_by_class_name('activity--history--summaries')
        WebDriverWait(div_activities[0], 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='activity--history--summary activity--history--110 clickable']")))
        div_tags = div_activities[0].find_elements_by_xpath(
            "//div[@class='activity--history--summary activity--history--110 clickable']")
        div_tags_len = len(div_tags)
        for j in range(0, div_tags_len):
            sales_lead = div_tags[j].find_element_by_tag_name('h1').text
            if 'Sales Lead' in sales_lead:
                sleep(3)
                div_tags[j].click()
                sleep(1)
                break
        try:
            sleep(2)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='activity--history--detail--body']")))
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tbody[@data-label='Provider']/tr")))
            row = browser.find_elements_by_xpath("//tbody[@data-label='Provider']/tr")[0]
            value = row.find_elements_by_tag_name('td')
            source_detail = value[-1].text
        except:
            pass
        if source_detail == '':
            try:
                sleep(2)
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='View Raw Lead']")))
                raw_click = browser.find_element_by_xpath("//a[text()='View Raw Lead']")
                raw_click.click()
                sleep(2)
                special_requests = browser.find_element_by_tag_name('xmp').text
                special_requests = special_requests.split('Special Requests:')[1]
                special_requests = special_requests.split('.com')[0]
                source_detail = special_requests.split('.')[-1]
            except:
                pass
    except:
        pass
    if source_detail == '':
        source_detail = 'Internet Other'
    if date_input not in result_appts.keys():
        result_appts[date_input] = {}
        result_leads[date_input] = {}
    if source_detail not in result_appts[date_input].keys():
        result_appts[date_input][source_detail] = {'A': 1}
        result_leads[date_input][source_detail] = {'L': 0}
    else:
        result_appts[date_input][source_detail]['A']+=1
        result_leads[date_input][source_detail]['L'] = 0
    print(date_input, source_detail, 'count',i)
browser.quit()
count = -1
df = pd.DataFrame(columns=['Date', 'source_detail', 'A'])
for date_input in result_appts:
    for src in result_appts[date_input]:
        count += 1
        df.loc[count] = [date_input,
                         src,
                         result_appts[date_input][src]['A']]
count =-1
df_leads = pd.DataFrame(columns=['Date', 'source_detail', 'L'])
for date_input in result_leads:
    for src in result_leads[date_input]:
        count += 1
        df_leads.loc[count] = [date_input,
                         src,
                         result_leads[date_input][src]['L']]
# print(result_leads)
# print(result_appts)
# print(df)
# print(df_leads)
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/Dominion")
df.to_sql(con=engine, name='Appointments', if_exists='append', index=False)
df_leads.to_sql(con=engine, name='Leads', if_exists='append', index=False)
print('inserted successfully')

