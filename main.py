import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from scraping_function import asn_object, org_link, org_object, poc_link, poc_object, net_object, net_link, net_resource_object
from bs4 import BeautifulSoup
from create_xlsx import create_asn_sheet, create_org_sheet, create_poc_sheet, create_net_resource_sheet
import pandas as pd

i = 0
while True:
    # prompting interval for asn
    interval_asn_1 = input("Input initial bound for ASN: ")
    interval_asn_2 = input("Input final bound for ASN: ")
    try:
        interval_asn_1 = int(interval_asn_1)
        interval_asn_2 = int(interval_asn_2)
    except ValueError:
        interval_asn_1 = interval_asn_1
        interval_asn_2 = interval_asn_2

    if isinstance(interval_asn_1, int) and isinstance(interval_asn_2, int):
        input_asn = []
        for i in range(interval_asn_1, interval_asn_2 + 1):
            input_asn.append("as" + f"{i}")
        break
    else:
        print("Input integers only.")
        i += 1
        if i == 3:
            break

print('Start...')

# setting the webdriver for chrome
service = Service(executable_path="./Driver/chromedriver.exe")  # Path for Chrome web driver
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # remove this if you want to see how the webdriver run.
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)  # set wait object
actions = ActionChains(driver)

data_asn = []
data_org = []
data_poc = []
data_net_resource = []
not_found = []
df = pd.DataFrame()

# calling webdriver
for i in range(len(input_asn)):
    driver.get('https://whois.arin.net/ui/')
    input_box = driver.find_element(By.XPATH, '//*[@id="queryinput"]')
    input_box.send_keys(input_asn[i])
    search_button = driver.find_element(By.XPATH, '//*[@id="whoisSubmitButton"]')
    search_button.click()
    try:
        #######################################################################################
        # ASN
        # Wait until the page source is loaded
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        page_source = driver.page_source
        # return a dictionary for asn object
        asn = asn_object(page_source)
        data_asn.append(asn_object(page_source))  # get ASN object
        create_asn_sheet(raw_data=data_asn)
        ##########################################################################################
        # ORG
        org_href = org_link(page_source)
        # go to org link
        driver.get(org_href)
        # Wait until the page source is loaded
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        page_source = driver.page_source
        # return a dictionary for org object
        dict1 = org_object(page_source, asn=input_asn[i])  # get Org object
        # get see also poc record link and go to the link
        soup = BeautifulSoup(page_source, 'html.parser')
        poc_record = soup.find('a', string='Related POC records.').get('href')
        net_record = soup.find('a', string='Related networks.').get('href')
        driver.get(poc_record)
        # Wait until the page source is loaded
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        page_source = driver.page_source
        dict2 = org_object(page_source, input_asn[i].upper())  # poc links
        dict1.update(dict2)
        data_org.append(dict1)
        create_org_sheet(raw_data=data_org)
        #######################################################################################################
        # POC
        # get all links
        poc_links = poc_link(page_source)
        # go to each poc links
        for link in poc_links:
            driver.get(link)
            # Wait until the page source is loaded
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
            page_source = driver.page_source
            poc_dict = poc_object(page_source, org_data=asn)
            data_poc.append(poc_dict)
            sleep(0.5)
        # create poc sheet
        create_poc_sheet(data_poc)
        ###############################################################################################
        # Net
        # go to net link
        driver.get(net_record)
        # Wait until the page source is loaded
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        page_source = driver.page_source
        net_dict = net_object(page_source, org_handle=asn)
        # Append data from the second dictionary to the DataFrame
        df = df._append(pd.DataFrame(net_dict), ignore_index=True)

        # Write the DataFrame to an Excel file
        df.to_excel('data/Net.xlsx', index=False, engine='openpyxl')

        ###############################################################################################
        # retrieve all asn links
        net_links = net_link(page_source)
        for link in net_links:
            driver.get(link)
            # Wait until the page source is loaded
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
            page_source = driver.page_source
            net_resource_dict = net_resource_object(page_source, org_data=asn)
            data_net_resource.append(net_resource_dict)
            sleep(0.2)
        # create net resource sheet
        create_net_resource_sheet(data_net_resource)

        print(f"{input_asn[i]}: success.")
    except:
        # create xlsx file for unavailable as number
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        not_found.append([input_asn[i]])

        for row_data in not_found:
            worksheet.append(row_data)

        xlsx_filename = "data/not_found.xlsx"
        workbook.save(xlsx_filename)
        print(f"{input_asn[i]}: not found.")

print("DONE.")

