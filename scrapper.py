# Using selenium to scrap terrains from inmuebles24.com from the City Puebla
import random
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# This are the initial variables needed to start the scrapper
url= 'https://www.inmuebles24.com/terrenos-en-venta-q-puebla.html'
url2= 'https://www.inmuebles24.com/terrenos-en-venta-pagina-25-q-puebla.html'
all_terrains= []
df_header = ['Location', 'Price', 'Zone', 'City', 'Area']
df_error = ['Error', 'Error', 'Error', 'Error', 'Error']
df = pd.DataFrame(columns=df_header)
file_name_prefix = 'terrains'

#This function opens the browser and the url
def open_browser(url):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    return driver

# this function is the main scrapper on the page
def scrapper(driver):
    mis_terrenos = []
    terrain = driver.find_element(By.CLASS_NAME, 'postings-container')
    terrains = terrain.find_elements(By.XPATH, '//div[@data-qa="posting PROPERTY"]')
    for element in terrains:
        #print(element.text)
        mis_terrenos.append(element.text)
    return mis_terrenos

# this function obtains the next page info
def next_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    next_button= driver.find_element(By.XPATH, '//a[@data-qa="PAGING_NEXT"]')
    print(next_button.get_attribute('href'))
    next_page = next_button.get_attribute('href')
    return next_page

#This function is to save the info in a csv file
def save_csv(all_terrains):
    df = pd.DataFrame(all_terrains)
    df.to_csv('terrains.csv', index=False, header=False)

#This function cleans individual records to insert into the dataframe

def clean_record(iterable_record):
    temporal_list = iterable_record.split('\n')
    try:
        record_cleaned = [temporal_list[1],temporal_list[0].strip(),temporal_list[2].split(',')[0],temporal_list[2].split(',')[1],temporal_list[3]]
    except:
        record_cleaned = df_error
    return record_cleaned

#This function adds the individual records to the dataframe
def add_record_to_df(df, temporal_list2):
    df.loc[len(df)] = temporal_list2
    return df

# This function is the main function that calls the other functions
if __name__ == '__main__':
    driver = open_browser(url)
    time.sleep(random.uniform(7.0,11.0))
    mis_terrenos = scrapper(driver)
    all_terrains += mis_terrenos
    print(len(all_terrains))
    next_page_url = str(next_page(driver))
    time.sleep(random.uniform(7.0,11.0))
    driver.close()

    # this loop is to get the info from the next pages

    while next_page != None:
        try:
            driver = open_browser(next_page_url)
            time.sleep(random.uniform(7.0,11.0))
            mis_terrenos = scrapper(driver)
            all_terrains += mis_terrenos
            print(len(all_terrains))
            next_page_url = str(next_page(driver))
            time.sleep(random.uniform(7.0,11.0))
            driver.close()
        except:
            driver.close()
            break


    #print(len(all_terrains))
    print("all terrains scrapped")

    #this portion of code transforms every row from the extracted data into a pandas dataframe
    print("\n")
    print("cleaning data")
    for i in all_terrains:
        # If there are more than 5 spaces in the record, then it this record matches our logic.
        # In the future, it is necessary to change the scrapping function to avoid this logic
        print(i)
        count_spaces = i.count('\n')
        if count_spaces > 5:
            record_cleaned = clean_record(i)
            df = add_record_to_df(df, record_cleaned)
        else:
            pass


    print(df)

    # create the csv filename with timestamp
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    str_current_datetime = str(current_datetime)
    file_name = file_name_prefix + str_current_datetime + '.csv'

    # save the dataframe to csv
    df.to_csv(file_name, index=False, header=df_header)
    print("csv saved")
    print("end of program")















