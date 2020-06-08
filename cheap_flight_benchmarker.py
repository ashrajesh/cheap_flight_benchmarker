from selenium import webdriver
import time
import csv
import datetime
from csv import writer
from webdriver_manager.chrome import ChromeDriverManager
from apscheduler.schedulers.blocking import BlockingScheduler

global current_time     # used for timestamp

def append_row_csv(file_name, elements):
    with open(file_name, 'a+', newline='') as towrite:
        csvwriter = writer(towrite)
        csvwriter.writerow(elements)

def task():
    finalurl = "https://www.google.com/flights?hl=en#flt=AUS.DFW.2020-06-21;c:USD;e:1;sd:1;t:f;tt:o" # change this link depending on the flight price you would like to track
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(finalurl)
    time.sleep(1.5)
    print("\n"+driver.find_element_by_css_selector(".gws-flights-results__cheapest-price").text)
    price = driver.find_element_by_css_selector(".gws-flights-results__cheapest-price").text
    print("\n"+"Airline with best fare: "+driver.find_element_by_css_selector(".gws-flights-results__carriers").text)
    airline = driver.find_element_by_css_selector(".gws-flights-results__carriers").text
    print("Flight time: "+driver.find_element_by_css_selector(".gws-flights-results__times-row").text)
    driver.quit()
    current_time = datetime.datetime.now()
    row = [price, airline, current_time]
    append_row_csv('output_file.csv', row)

task()
scheduler = BlockingScheduler()
scheduler.add_job(task, 'interval', hours=1.5) # time interval set to check price every 1.5 hours
scheduler.start()