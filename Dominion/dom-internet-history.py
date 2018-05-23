from datetime import datetime
from time import sleep
import pandas as pd
from selenium import webdriver
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
sleep(1)
password = browser.find_element_by_xpath("//input[@type='password']")
password.send_keys('2025DMdf!')
login_attempt = browser.find_element_by_xpath("//button[@class='b b-success clickable']")
login_attempt.click()
sleep(1)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Leads']")))
leads = browser.find_element_by_xpath("//a[text()='Leads']")
leads.click()
sleep(5)
opportunity_module = browser.find_element_by_xpath("//div[@class='report--module report--module--ungrouped report--module--opportunitysourcing report--module--series--count--4 report--module--bg--undefined report--module--text--undefined report--module--text--accent--undefined']")
table_rows_opp_module = opportunity_module.find_elements_by_tag_name('tr')
customers = table_rows_opp_module[1].find_element_by_tag_name('td')
customers.click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='drilldowns--body']")))
articles_panel = browser.find_elements_by_xpath("//div[@class='drilldowns--body']")
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='drilldowns--count']")))
articles_count = articles_panel[0].find_elements_by_xpath("//span[@class='drilldowns--count']")
num_customers = articles_count[-1].text
num_customers = int(num_customers)
print(num_customers)
scroll_times = -(-num_customers // 30) - 1
if num_customers >=30:
    for i in range(1,scroll_times+1):
        browser.execute_script(" var a =document.getElementsByTagName('article'); a[{} * 30].scrollIntoView(); ".format(i))
        sleep(3)
result_la = {}
for i in range(0,num_customers):
    sleep(1)
    browser.execute_script("document.getElementsByClassName('drilldown--header clickable')[{}].click();".format(i))
    date_input = browser.execute_script("var ele = document.getElementsByClassName('drilldown--header clickable'); var date_input = ele[{}].getElementsByClassName('drilldown--h2  drilldown--date')[0].innerHTML ; return date_input".format(i))
    raw_date = date_input
    date_input = date_input[0:16].strip().replace(',','')
    datetime_object = datetime.strptime(date_input, '%a %b %d %Y')
    date_input = datetime_object.strftime('%Y-%m-%d')
    sleep(5)
    browser.execute_script("document.getElementsByClassName('activity--history--right')[0].scrollIntoView();")
    source_detail = ''
    try:
        sleep(3)
        WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='activity--history--detail--body']")))
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@data-label='Provider']/tr")))
        row = browser.find_elements_by_xpath("//tbody[@data-label='Provider']/tr")[0]
        value = row.find_elements_by_tag_name('td')
        source_detail = value[-1].text
    except:
        pass
    if source_detail == '':
        try:
            sleep(2)
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//a[text()='View Raw Lead']")))
            raw_click = browser.find_element_by_xpath("//a[text()='View Raw Lead']")
            raw_click.click()
            sleep(2)
            special_requests = browser.find_element_by_tag_name('xmp').text
            special_requests = special_requests.split('Special Requests:')[1]
            special_requests = special_requests.split('.com')[0]
            source_detail = special_requests.split('.')[-1]
        except:
            pass
    if source_detail == '':
        source_detail = 'Internet Other'
    if date_input not in result_la.keys():
        result_la[date_input] = {}
    if source_detail not in result_la[date_input].keys():
        result_la[date_input][source_detail] = {'L': 1}
    else:
        result_la[date_input][source_detail]['L'] += 1
    print(date_input, source_detail, 'count',i)
browser.quit()
count = -1
df = pd.DataFrame(columns=['Date', 'source_detail', 'L'])
for date_input in result_la:
    for src in result_la[date_input]:
        count += 1
        df.loc[count] = [date_input,
                         src,
                         result_la[date_input][src]['L']]
print(df)
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/Dominion")
df.to_sql(con=engine, name='Leads', if_exists='append', index=False)
print('inserted successfully')
