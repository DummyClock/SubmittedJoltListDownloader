from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import os
import time

from auth import EMAIL, PASSWORD

def downloadCSVs(listNames, startDate=None, endDate=None):
    #Get the default one-week-period dates
    if startDate == None and endDate == None:
        endDate = str(date.today())
        startDate = str(date.today() - timedelta(days=7))
    print("StartDate:"+startDate+"!")

    driver = webdriver.Chrome()
    driver.get("https://app.joltup.com/account#/login")
    time.sleep(3)            # Give time for dynamic elements to load  

    driver.find_element(By.ID, "emailAddress").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD, Keys.ENTER)
    time.sleep(4)

    driver.get("https://app.joltup.com/review/review/listResultsReporting/gridView")
    time.sleep(6)           # Give time for dynamic elements to load 

    dateRange(driver, startDate, endDate)

    lowercaseNames = [name.lower() for name in listNames]       #Turns desired lists' names lowercase
    list_of_titles = driver.find_elements(By.CLASS_NAME, "left-column-item-title")  #Gathers all list titles

    #Find desired list and download the CSV file
    for t in list_of_titles:
        title = t.find_element(By.TAG_NAME, "span").text.lower()
        if title in lowercaseNames: 
            t.click()
            time.sleep(3)

            driver.find_element(By.CLASS_NAME, "list-download").click()
            time.sleep(5)

    driver.get("https://app.joltup.com/site/logout")

    time.sleep(1.5)
    driver.close()

#ISSUE: Correct value is entered, but site does not store it, leaving it to reset
def dateRange(driver, startDate, endDate):
    driver.find_element(By.CLASS_NAME, "date-range-filter").click() #Open up date range picker
    time.sleep(2)

    #Put in the start date
    start_field = driver.find_element(By.ID, "input-start")
    start_field.clear()
    start_field.send_keys(startDate)

    #Put in the end date
    end_field = driver.find_element(By.ID, "input-end")
    end_field.clear()
    end_field.send_keys(endDate)
    time.sleep(2)

    #Find and click on "Done" in the Date-Range picker menu
    buttons = driver.find_element(By.CLASS_NAME, "date-range-menu").find_element(By.CLASS_NAME, "button-row").find_elements(By.CLASS_NAME, "button")
    for button in buttons:
        span_text = button.find_element(By.TAG_NAME, "span").text
        if span_text.lower() == "done":
            button.click()
    time.sleep(5)

#Testing the functions.
listName = ["BOH Closing Checklist".lower()]
downloadCSVs(listName)
