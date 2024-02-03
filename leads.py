import csv
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('https://crm.dmbgroup.online/login')
print('page opened')
email_input = driver.find_element(By.ID, 'email')
password_input = driver.find_element(By.ID, 'password-input')
signin_button =  driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[2]/div/div[2]/form/div[4]/button')

email_input.send_keys('r.nsiah@gmail.com')
password_input.send_keys('Zanovia1@')
signin_button.click()


prospects_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="navbar-nav"]/li[8]/a'))
)
prospects_menu.click()

prospect_list_submenu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebarProspect"]/ul/li[1]'))
)
prospect_list_submenu.click()
print('got to table')

time.sleep(4)
# Wait for table containing leads to load
leads_table = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//table[@class="table align-middle table-nowrap mb-0"]')))
print('found table')
rows = leads_table.find_elements(By.TAG_NAME, 'tr')

leads_data = []
print('got to before the loop')
for row in rows[1:]:
    time.sleep(1.5)
    try:
        edit_button = row.find_element(By.XPATH, './/ul[@class="list-inline hstack gap-2 mb-0"]/li[1]//i[@class="ri-pencil-fill align-bottom text-muted"]')
        print('found edit button')
        print('edit button located ')
        actions = ActionChains(driver)
        actions.move_to_element(edit_button).perform()
    
        edit_button.click()
        print('edit button clicked')
    
    except StaleElementReferenceException:
    # If the element is stale, re-locate and click it again
        edit_button = row.find_element(By.XPATH, './/ul[@class="list-inline hstack gap-2 mb-0"]/li[1]//i[@class="ri-pencil-fill align-bottom text-muted"]')
        actions = ActionChains(driver)
        actions.move_to_element(edit_button).perform()
        edit_button.click()
        
    
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, 'agentModal'))
    )
    
    time.sleep(.7)
  
    first_name = driver.find_element(By.ID, 'editFirstName').get_attribute('value')
    print(first_name)
    last_name = driver.find_element(By.ID, 'editLastName').get_attribute('value')
    print(last_name)
    phone = driver.find_element(By.ID, 'editPhoneNumber').get_attribute('value')
    print(phone)
    address = driver.find_element(By.ID, 'editAddress').get_attribute('value')
    print(address)
    state = driver.find_element(By.ID, 'editState').get_attribute('value')
    city = driver.find_element(By.ID, 'editCity').get_attribute('value')
    zip_code = driver.find_element(By.ID, 'editPostalCode').get_attribute('value') 
    
    age_element = driver.find_element(By.XPATH, '//p[contains(text(), "Age is:")]')
    age_text = age_element.text
    
    age = age_text.split(' ')[-1]
    
    lead_data = {
            'First Name': first_name,
            'Last Name': last_name,
            'Phone': phone,
            'Address': address,
            'State': state,
            'City': city,
            'Zip Code': zip_code,
            'Age': age
        }
    
    leads_data.append(lead_data)
    print({'lead_data':len(leads_data)})
    close_button = driver.find_element(By.ID, 'close-modal')
    print('found close button')
    close_button.click()
    
csv_filename = 'leads_data.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['First Name','Last Name','Phone', 'Address', 'State', 'City', 'Zip Code', "Age"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for lead in leads_data:
        writer.writerow(lead)
        

driver.quit()





