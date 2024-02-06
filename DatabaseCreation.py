# Webscraping Vehicle Safety Rating Data From NHTSA.gov

from splinter import Browser
from bs4 import BeautifulSoup
import numpy as np
import time
import pandas as pd

manufacturer_List = ['Acura','Audi','BMW','Buick','Cadillac', 'Chevrolet','Chrysler','Dodge','Ford','GMC','Honda','Hyundai','Infiniti','Jaguar','Jeep','Kia','Land Rover','Lexus', 'Lincoln', 'Mazda','Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Smart','Subaru','Tesla','Toyota','Volkswagen', 'Volvo']

# open chrome browser
browser = Browser('chrome')

# visit the url
url = 'https://www.nhtsa.gov/ratings'
browser.visit(url)

# locate the search bar and button icon
search_bar = browser.find_by_id('ratings-search-input')
search_button = browser.find_by_xpath('//*[@id="vehicle"]/div[2]/div[2]/div[1]/form/div/div/div/button')

# initiate list of dictionaries
dic_list = []

for make in manufacturer_List: 

    print(make)
    print('-----------------')

    # type manufacturer into search bar
    search_bar.fill(make)

    # click the search icon
    search_button.click()
    time.sleep(5)

    # get browser html
    html = browser.html

    # parse html with soup
    soup = BeautifulSoup(html, "html.parser")

    # find number of results for manufacturer
    table_results = soup.find_all('div', class_ = 'table-responsive')

    num = []
    for result in table_results:
        num.append(result.find_all('strong'))

    no_of_results = int(num[0][0].text.split()[0])
    no_of_pages = np.ceil(int(num[0][0].text.split()[0])/10)


    # create for loop from 0 to number of pages
    results_counter = 0
    not_rated = False
    for page in range(int(no_of_pages)):
        
        print(f'page #{page+1}')

        if not_rated:
            break
        
        time.sleep(5)
        # get browser html
        next_page_html = browser.html
        
        # parse html with soup
        next_page_soup = BeautifulSoup(next_page_html, "html.parser")

        next_page_elements_ratings = next_page_soup.find_all("tbody")
        
        # create for loop to number of results per page
        for result in range(1,11):

            if not_rated:
                break

            # initialize dictionary with ratings
            ratings_dict = {"overall_rating": 0, "frontal_crash": 0, "side_crash": 0, "rollover": 0}

            # vehicle saftey concerns
            vehicle_safety_concerns = False

            results_counter +=1

            # iterate through ratings dict and enumerate for indexing
            for num, rating in enumerate(ratings_dict):

                # grab rating
                ratings_lists = []
                for element in next_page_elements_ratings:
                    ratings_lists.append(element.find_all("img"))

                rate_num = str(ratings_lists[result+1][num])[-8:-7]

                if str(ratings_lists[result+1][num])[0:30] == '<img alt="Has safety concern."':
                    print("safety concern")
                    rate_num = str(ratings_lists[result+1][num+1])[-8:-7]
                    vehicle_safety_concerns = True
                    
                # break if non-digit is returned
                if rate_num.isdigit():

                    ratings_dict[rating] = (int(rate_num))
                    
                else:
                    not_rated = True
                    break
            
            if not_rated:
                break

            # add vehicle safety concern to dictionary
            ratings_dict['safety_concern'] = vehicle_safety_concerns

            # get make, model, year
            mmy_data = []
            for element in next_page_elements_ratings:
                mmy_data.append(element.find_all("a"))

            # split vehicle model to get make, model and year separately 
            mmy_list = mmy_data[result+1][0].text.split()

            ratings_dict['year'] = mmy_list.pop(0)
            ratings_dict['make'] = mmy_list.pop(0)
            ratings_dict['model'] = ' '.join(mmy_list)

            dic_list.append(ratings_dict)

        next_button = browser.find_by_xpath('//*[@id="ratings-2011-present"]/div/div/div[2]/div[2]/button[2]')
        next_button.click()

# put data into df
df = pd.DataFrame(dic_list)

# sort columns
df = df.iloc[:,[6,7,5,0,1,2,3,4]]

# convert df to csv file
df.to_csv('nhtsa_safety_ratings.csv', index = False)

### DATABASE CREATION DATA TABLE SETUP # Tanner
# Import Modules
import sqlite3
import requests
import json
import csv 
import os
import re

#Create connection

connection = sqlite3.connect('NHTSA.db')
cursor = connection.cursor()

#Use this to delete tables if needed

# cursor.execute("DROP TABLE IF EXISTS Ratings")
# cursor.execute("DROP TABLE IF EXISTS Recalls")
# cursor.execute("DROP TABLE IF EXISTS Complaints")
# cursor.execute("DROP TABLE IF EXISTS Vehicles")

#Create tables for Sqlite database

# Create Ratings Table

Table1= """CREATE TABLE IF NOT EXISTS
Ratings(ymm Text PRIMARY KEY,year_make_model Text, make Text ,model Text ,model_year INTEGER, base_model Text, overall_rating INTEGER,
frontal_crash INTEGER, side_crash INTEGER, rollover INTEGER, safety_concerns Text)"""

#Create Recalls Table

Table2="""CREATE TABLE IF NOT EXISTS
Recalls(year_make_model Text, manufacturer Text, make Text ,base_model Text, model_year INTEGER, NHTSTA_campaign_number Text,
parkIt BOOLEAN, parkOutside BOOLEAN, NHTSA_action_number Text,report_received_date DATE, component Text, summary Text,
consequence Text, remedy Text, notes Text)"""

#Create Complaints Table

Table3="""CREATE TABLE IF NOT EXISTS
Complaints(year_make_model Text, manufacturer Text, make Text ,base_model Text, model_year INTEGER, type Text,
ODI_number INTEGER, crash BOOLEAN, fire BOOLEAN, number_of_injuries INTEGER, number_of_deaths INTEGER, date_of_incident DATE,
date_complaint_filed DATE, vin Text, components Text, summary Text)"""

#Create Vehicles Table

Table4="""CREATE TABLE IF NOT EXISTS
Vehicles(year_make_model Text PRIMARY KEY, make Text, base_model Text, model_year INTEGER)"""

# Execute the variables above

cursor.execute(Table1)
cursor.execute(Table2)
cursor.execute(Table3)
cursor.execute(Table4)

#create csv path to NHTSA Ratings web scrape

csvpath = os.path.join(".", "nhtsa_safety_ratings.csv")

#Loop through the NHTSA CSV and create Vehicles table and Ratings table
with open(csvpath, encoding='UTF-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    header = next(csvreader)
    for row in csvreader:
        #get attributes as they relate to table headers in the Ratings and Vehicles tables
        if row[0]=='Acura' or row[0]=='Honda' or row[0]=='Kia' or row[0]=='Nissan' or row[0]=='Volvo': 
            base_model = (row[1]).split(' ')[0].upper()
            ymm = str(row[2])+row[0]+row[1]
            model = row[1].upper()
            make = row[0].upper()
            year = row[2]
            overall_rating = row[3]
            frontal_crash = row[4]
            side_crash = row[5]
            rollover = row[6]
            safety_concerns = row[7].upper()
            year_make_model = year+make+base_model
            

            #Insert values directly into Ratings
            
            insertRatings = '''INSERT OR IGNORE INTO Ratings (ymm,year_make_model, make, model, base_model, model_year, overall_rating, frontal_crash,
                                side_crash, rollover, safety_concerns) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
            valuesRatings = (ymm, year_make_model, make, model, base_model, year, overall_rating, frontal_crash, side_crash, rollover, safety_concerns)
            cursor.execute(insertRatings,valuesRatings)
            #Insert only unique values into Vehicles
            
            insertVehicles = '''INSERT OR IGNORE INTO Vehicles (year_make_model,make,base_model,model_year) VALUES (?,?,?,?)'''
            valuesVehicles = (year_make_model, make, base_model, year)
            cursor.execute(insertVehicles,valuesVehicles)
            #commit changes
            connection.commit()

        ##### Use Regex to get models with unique naming conventions

        #get names of vehicles where models only occupy the first word of a string
            
        elif row[0]=='Jeep' or row[0] == 'Hyundai' or row[0] == 'Volkswagen':
            ymm = str(row[2])+row[0]+row[1]
            model = row[1].upper()
            make = row[0].upper()
            year = row[2]
            overall_rating = row[3]
            frontal_crash = row[4]
            side_crash = row[5]
            rollover = row[6]
            safety_concerns = row[7].upper()
            base_model_pattern = re.compile(r'(.*?\b(?:(Cherokee|Fe|R|GTI|GLI|Sportwagen|Sport))\b)')
            match = base_model_pattern.search(row[1])
            if match:
                base_model = str(match.group()).upper()
                year_make_model = str(row[2])+row[0].upper()+base_model.replace(" ","")
            else:
                base_model = row[1].split(' ')[0].upper()
                year_make_model = str(row[2])+row[0].upper()+base_model.replace(" ","")
            
            #Insert values directly into Ratings
            
            insertRatings = '''INSERT OR IGNORE INTO Ratings (ymm,year_make_model, make, model, base_model, model_year, overall_rating, frontal_crash,
                                side_crash, rollover, safety_concerns) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
            valuesRatings = (ymm, year_make_model, make, model, base_model, year, overall_rating, frontal_crash, side_crash, rollover, safety_concerns)
            cursor.execute(insertRatings,valuesRatings)
            #Insert only unique values into Vehicles
            
            insertVehicles = '''INSERT OR IGNORE INTO Vehicles (year_make_model,make,base_model,model_year) VALUES (?,?,?,?)'''
            valuesVehicles = (year_make_model, make, base_model, year)
            cursor.execute(insertVehicles,valuesVehicles)
            #commit changes
            connection.commit()

#delete brands from db that have not been properly cleaned yet

cursor.execute("DELETE FROM Ratings WHERE make IN ('BMW', 'Cadillac', 'Ford', 'GMC', 'Lexus', 'Mercedes-Benz', 'Subaru', 'Tesla', 'Toyota')")
cursor.execute("DELETE FROM Vehicles WHERE make IN ('BMW', 'Cadillac', 'Ford', 'GMC', 'Lexus', 'Mercedes-Benz', 'Subaru', 'Tesla', 'Toyota')")
connection.commit()

#Query into Vehciles to get makes and models to loop through

cursor.execute("SELECT * FROM Vehicles")
recallsrows = cursor.fetchall()
recallsrows = list(set(recallsrows))

#Loop through makes and models to dump into NHTSA recalls URL

for row in recallsrows:
    APImake = row[1]
    APImodel = row[2]
    APIyear = row[3]
    recalls_url = f'https://api.nhtsa.gov/recalls/recallsByVehicle?make={APImake}&model={APImodel}&modelYear={APIyear}'
    response = requests.get(recalls_url).json()

#if the API call has data, loop through it and grab the information

    if response['Count'] > 0:
        records = response['results']
        for record in records:
            manufacturer = record.get('Manufacturer','N/A')
            NHTSACampainNumber = record.get('NHTSACampaignNumber','N/A')
            parkIT = record.get('parkIt', 'N/A')
            parkOutSide = record.get('parkOutSide', 'N/A')
            NHTSAActionNumber = record.get('NHTSAActionNumber', 'N/A')
            ReportReceivedDate = record.get('ReportReceivedDate','N/A')
            Component = record.get('Component', 'N/A')
            Summary = record.get('Summary','N/A')
            Consequence = record.get('Consequence', 'N/A')
            Remedy = record.get('Remedy','N/A')
            Notes = record.get('Notes','N/A')
            ModelYear = record.get('ModelYear','N/A')
            Make = record.get('Make','N/A')
            Model = record.get('Model','N/A')
            year_make_model_recalls = ModelYear+Make+Model

            #Prep data to insert into the recalls database

            insertRecalls = '''INSERT OR IGNORE INTO Recalls (year_make_model, manufacturer, make,base_model, model_year,
                            NHTSTA_campaign_number, parkIt, parkOutside, NHTSA_action_number,report_received_date, 
                             component, summary, consequence, remedy, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            valuesRecalls = (year_make_model_recalls, manufacturer,Make,Model, ModelYear, NHTSACampainNumber, parkIT, parkOutSide,
                             NHTSAActionNumber ,ReportReceivedDate, Component, Summary, Consequence, Remedy, Notes)
            
#enter the data into the recalls table and commit the changes
            
            cursor.execute(insertRecalls, valuesRecalls)
            connection.commit()

#Query into Vehciles to get makes and models to loop through

cursor.execute("SELECT * FROM Vehicles")
vehiclesrows = cursor.fetchall()
vehiclesrows = list(set(vehiclesrows))

#Loop through makes and models to dump into NHTSA complaints URL
for row in vehiclesrows:
    APImake = row[1]
    APImodel = row[2]
    APIyear = row[3]
    complaints_url = f'https://api.nhtsa.gov/complaints/complaintsByVehicle?make={APImake}&model={APImodel}&modelYear={APIyear}'
    response = requests.get(complaints_url).json()
    
    #if the API call has data, loop through it and grab the information

    if response['count'] > 0:
        records = response['results']
        for record in records:
            odiNumber = record['odiNumber']
            manufacturer = record['manufacturer']
            crash = record['crash']
            fire = record['fire']
            numberOfInjuries = record['numberOfInjuries']
            numberOfDeaths = record['numberOfDeaths']
            dateOfIncident = record['dateOfIncident']
            dateComplaintFiled = record['dateComplaintFiled']
            vin = record['vin']
            components = record['components']
            summary = record['summary']
            product_type = record['products'][0]['type']
            product_Year = record['products'][0]['productYear']
            product_Make = record['products'][0]['productMake']
            product_Model = record['products'][0]['productModel']
            year_make_model_complaints = product_Year+product_Make+product_Model

            #Prep data to insert into the complaints database

            insertComplaints = '''INSERT INTO Complaints (year_make_model, manufacturer, make,base_model, model_year, type, ODI_number, crash,
            fire, number_of_injuries, number_of_deaths, date_of_incident, date_complaint_filed, vin, components, summary) VALUES 
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
            valuesComplaints = (year_make_model_complaints, manufacturer, product_Make,product_Model, product_Year, product_type, odiNumber, crash,
            fire, numberOfInjuries, numberOfDeaths, dateOfIncident, dateComplaintFiled, vin, components, summary)

            cursor.execute("")

            #enter the data into the complaints table and commit the changes

            cursor.execute(insertComplaints,valuesComplaints)
            connection.commit()

#close off the connection
connection.close()