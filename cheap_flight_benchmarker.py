from selenium import webdriver
import time
import csv
import datetime
from csv import writer
from webdriver_manager.chrome import ChromeDriverManager
from apscheduler.schedulers.blocking import BlockingScheduler

global current_time     # used for timestamp

def welcome():
    print("\nWelcome to Cheap Flight Benchmarker\n")
    endurl = ";c:USD;e:1;sc:b;sd:1;t:f;tt:o"    #business class
    endurltwo = ";c:USD;e:1;sd:1;t:f;tt:o"      #economy class
    print("Are you looking to track Economy or Business Tickets? (e/b) : ")
    global classed
    classed = input()
    global urlclass
    if classed == "b":
        urlclass = endurl
    else:
        urlclass = endurltwo

def search():
    print("\nEnter origin airport code: ")
    global origin
    origin = input()
    print("\nEnter destination airport code: ")
    global destination
    destination = input()
    print("\nEnter desired date: ")
    print("Year (YYYY): ")
    global year
    year = input()
    #year = str(2020)
    print("\nMonth (MM): ")
    global month
    month = input()
    print("\nDay (DD): ")
    global day
    day = input()
    baseurl = "https://www.google.com/flights?hl=en#flt="
    originurl = origin + "."
    destinurl = destination + "."
    date = year + "-" + month + "-" + day
    global finalurl
    finalurl = baseurl + originurl + destinurl + date + urlclass

def confirm():
    x = 0
    while (x==0):
        welcome()
        search()
        print("\n\nTracking flights matching the following specifications: \nOrigin: " + origin + "\nDestination: " + destination + "\nClass: " + classed + "\nDate: " + month + "/" + day + "/" + year)
        print("\n\nWould you like re-do search criteria? (y/n)")
        answer = input()
        if answer == "y":
            x = 0
        else:
            x = 1

def append_row_csv(file_name, elements):
    with open(file_name, 'a+', newline='') as towrite:
        csvwriter = writer(towrite)
        csvwriter.writerow(elements)

def task():
    #finalurl = "https://www.google.com/flights?hl=en#flt=AUS.DFW.2020-06-21;c:USD;e:1;sd:1;t:f;tt:o" # change this link depending on the flight price you would like to track
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(finalurl)
    time.sleep(1.5)
    p = driver.find_element_by_css_selector(".gws-flights-results__cheapest-price").text
    price = p[2:] #remove first two elements of string
    print("\n"+price)
    print("\n"+"Airline with best fare: "+driver.find_element_by_css_selector(".gws-flights-results__carriers").text)
    airline = driver.find_element_by_css_selector(".gws-flights-results__carriers").text
    print("Flight time: "+driver.find_element_by_css_selector(".gws-flights-results__times-row").text)
    driver.quit()
    current_time = datetime.datetime.now()
    row = [price, airline, current_time]
    append_row_csv('outputted_file.csv', row)

confirm()
task()
scheduler = BlockingScheduler()
scheduler.add_job(task, 'interval', hours=1.5) # time interval set to check price every 1.5 hours
scheduler.start()