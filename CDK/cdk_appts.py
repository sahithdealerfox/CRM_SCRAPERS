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

appointments = browser.find_element_by_xpath("//a[@title = 'Appointments']")
appointments.click()

#**************************** ------- User Input --------- **************************************#
start_month = 'Apr'
start_date = '1'
end_month = 'Apr'
end_date = '30'

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
result_appts = {}
sleep(1)
print(num_customers)
for i in range(0,num_customers):
    if (i+1)%50 == 0:
        sleep(4)
        browser.execute_script(" var a = document.getElementsByClassName('lead-row ng-scope'); a[{}].scrollIntoView();".format(i))

for i in range(0,num_customers):
    sleep(1)
    if (i + 1) % 50 == 0:
        sleep(3)
        browser.execute_script(
            " var a = document.getElementsByClassName('lead-row ng-scope'); a[{}].scrollIntoView();".format(i))
    customer_name = browser.execute_script(
        "return document.getElementsByClassName('lead-customer-name ng-binding')[{}].innerHTML".format(i))
    if customer_name in unique_customers:
        continue
    unique_customers.append(customer_name)
    app_status = browser.execute_script("var a = document.getElementsByClassName('lead-row ng-scope'); var b = a[{}].getElementsByClassName('lead-col lead-col-status hidden-xs'); var c = b[0].innerText; return c;".format(i))
    app_status =app_status.split('\n')[0].strip()
    print(i)
    start_date = browser.execute_script("var a= document.getElementsByClassName('lead-body'); var b = a[0].getElementsByClassName('lead-col lead-col-date hidden-xs');var c = b[{}].getElementsByClassName('ng-binding'); return c[0].innerText".format(i))
    datetime_object = datetime.strptime(start_date, '%m/%d/%Y')
    date_input = datetime_object.strftime('%Y-%m-%d')
    browser.execute_script("var a = document.getElementsByClassName('lead-customer-name ng-binding'); a[{}].click(); ".format(i))
    sleep(4)
    source_label = browser.execute_script("var a = document.getElementsByClassName('crm-lead-details-value ng-binding'); return a[1].innerText; ")
    source = source_label.strip('\n')
    sleep(3)
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"//button[@ng-click= 'dismiss()']")))
    close_appt = browser.find_element_by_xpath("//button[@ng-click= 'dismiss()']").click()
    sleep(2)
    if 'Phone' in source:
        source = 'Phone'
    if 'Internet' in source:
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='View Source']")))
            source_click = browser.find_element_by_xpath("//span[text()='View Source']")
            source_click.click()
            sleep(2)
            try:
                xml_text = browser.execute_script("var a = document.getElementsByTagName('textarea'); return a[0].value;")
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
                source = 'Other'
        except:
            source = 'Other'
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//i[text()='close']")))
    close_button = browser.find_element_by_xpath("//i[text()='close']")
    close_button.click()
    if date_input not in result_appts.keys():
        result_appts[date_input] = {}
        result_appts[date_input] = {}
    if source not in result_appts[date_input].keys():
        result_appts[date_input][source] = {'A': 1, 'S': 0}
    else:
        result_appts[date_input][source]['A'] += 1
    if app_status == 'Show':
        result_appts[date_input][source]['S']+=1
browser.quit()
print(result_appts)
count =-1
df = pd.DataFrame(columns=['Date', 'source_detail', 'A', 'S'])
for date_input in result_appts:
    for src in result_appts[date_input]:
        count += 1
        df.loc[count] = [date_input,
                         src,
                         result_appts[date_input][src]['A'],
                         result_appts[date_input][src]['S']]
print(df)
from sqlalchemy import create_engine
engine = create_engine("mysql+mysqldb://Dealerfox:" + 'Temp1234' + "@dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com/CDK")
df.to_sql(con=engine, name='Appointments_Shown', if_exists='append', index=False)
print('inserted successfully')
