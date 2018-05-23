from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import xmltodict

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
browser.get("https://oaklawnmazda.cdkcrm.com")
username = browser.find_element_by_id("UsernameTextBox")
username.send_keys('dtrinidad')
sleep(1)
password = browser.find_element_by_id("PasswordTextBox")
password.send_keys('123456')
login_attempt = browser.find_element_by_id("LogInLink")
login_attempt.click()

#****************************8 ------- User Input --------- **************************************#
start_month = 'Apr'
start_date = '1'
end_month = 'Apr'
end_date = '30'

###################################################################################################
sleep(1)
try:
    browser.find_element_by_xpath("//button[@class='walkme-custom-balloon-button walkme-custom-balloon-normal-button walkme-custom-balloon-ok-button walkme-action-ok walkme-click-and-hover']").click()
except:
    pass
sleep(1)
try:
    browser.find_element_by_id('messageBox_button_0').click()
except:
    pass
sleep(3)
WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.ID,"menu-item-desk-log")))
browser.find_element_by_id('menu-item-desk-log').click()
sleep(1)

#************************* -------- Date Filter Logic ----------**********************************#
sleep(2)
span_click = browser.find_element_by_xpath("//span[@class='input-group-addon']")
span_click.click()
month_sel = browser.find_elements_by_class_name('monthselect')
month_sel[0].click()
selected_month = month_sel[0].find_element_by_xpath("//option[text()='{}']".format(start_month))
selected_month.click()
date_sel_left = browser.find_element_by_xpath("//td[contains(@class,'available') and text() = '{}']".format(start_date))
date_sel_left.click()
month_sel = browser.find_elements_by_class_name('monthselect')
month_sel[1].click()
selected_month = month_sel[1].find_elements_by_xpath("//option[text()='{}']".format(end_month))
selected_month[1].click()
date_sel_left = browser.find_elements_by_xpath("//td[contains(@class,'available') and text() = '{}']".format(end_date))
date_sel_left[-1].click()
apply_dates = browser.find_element_by_xpath("//button[text()='Apply']")
apply_dates.click()
sleep(2)
num_customers = browser.find_element_by_xpath("//div[@class='total-result-count ng-binding']").text.split(' ')[0]
num_customers = int(num_customers)
customers = browser.find_elements_by_xpath("//div[@class='lead-row ng-scope']")
unique_customers = []
result_leads = {}
sleep(1)
#print(num_customers)
for i in range(0,num_customers):
    if (i+1)%50 == 0:
        sleep(4)
        print(i)
        browser.execute_script(" var a = document.getElementsByClassName('lead-row ng-scope'); a[{}].scrollIntoView();".format(i))

for i in range(0,num_customers):
    sleep(1)
    if (i + 1) % 50 == 0:
        sleep(3)
        browser.execute_script(
            " var a = document.getElementsByClassName('lead-row ng-scope'); a[{}].scrollIntoView();".format(i))
    customer_name = browser.execute_script("return document.getElementsByClassName('lead-customer-name hidden-xs ng-binding')[{}].innerHTML".format(i))
    if customer_name in unique_customers:
        continue
    print(customer_name)
    unique_customers.append(customer_name)
    start_date = browser.execute_script("var a = document.getElementsByClassName('lead-row ng-scope'); b = a[{}].getElementsByClassName('lead-col lead-col-status hidden-xs ng-binding'); return b[1].innerText;".format(i))
    datetime_object = datetime.strptime(start_date, '%m/%d/%Y')
    date_input = datetime_object.strftime('%Y-%m-%d')
    source_detail = browser.execute_script("var a = document.getElementsByClassName('lead-row ng-scope'); b = a[{}].getElementsByClassName('lead-col lead-col-source hidden-sm hidden-xs ng-binding'); return b[0].innerText;".format(i))
    source_detail = source_detail.strip('')
    source = source_detail
    if 'Phone Call' in source_detail:
        source = 'Phone'
    if source_detail != 'F&I' and source!= 'Phone' and source_detail!= 'Showroom':
        sleep(2)
        browser.execute_script("var a = document.getElementsByClassName('lead-customer-name hidden-xs ng-binding'); a[{}].click(); ".format(i))
        sleep(4)
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='View Source']")))
            source_click = browser.find_element_by_xpath("//span[text()='View Source']")
            source_click.click()
            sleep(2)
            try:
                xml_text = browser.execute_script(
                    "var a = document.getElementsByTagName('textarea'); return a[0].value;")
                jsonString = json.dumps(xmltodict.parse(xml_text), indent=4)
                jsonData = json.loads(jsonString)
                try:
                    source_detail = jsonData['adf']['prospect']['provider']['name']['#text']
                except:
                    source_detail = jsonData['adf']['prospect']['provider']['name']
                if 'DealerTrack' in source_detail:
                    source_detail = 'DealerTrack'
                try:
                    vendor = jsonData['adf']['prospect']['vendor']['vendorname']
                except:
                    vendor = jsonData['adf']['prospect']['vendor']['contact']['name']['#text']
                vendor = vendor.lower()
                vendor = vendor.replace('ultimo motors northshore', 'ULN')
                vendor = vendor.replace('ultimo motorsports', 'UMS')
                vendor = vendor.replace('ultimo motors', 'ULT')
                source_detail = source_detail.split('/')[0].strip()
                source = source_detail + ' ' + vendor
            except:
                source = 'Internet Other'
        except:
            source = 'Internet Other'
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//i[text()='close']")))
        close_button = browser.find_element_by_xpath("//i[text()='close']")
        close_button.click()
    if date_input not in result_leads.keys():
        result_leads[date_input] = {}
        result_leads[date_input] = {}
    if source not in result_leads[date_input].keys():
        result_leads[date_input][source] = {'L': 1}
    else:
        result_leads[date_input][source]['L'] += 1
    print(date_input, source, i)
browser.quit()
count =-1
df_leads = pd.DataFrame(columns=['Date', 'source_detail', 'L'])
for date_input in result_leads:
    for src in result_leads[date_input]:
        count += 1
        df_leads.loc[count] = [date_input,
                         src,
                         result_leads[date_input][src]['L']]
print(result_leads)
#-------------------------- SQL INSERT and UPDATE ---------------------------------#
from sqlalchemy import create_engine
engine = create_engine("mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/CDK")
df_leads.to_sql(con=engine, name='Leads', if_exists='append', index=False)
print('inserted successfully')
