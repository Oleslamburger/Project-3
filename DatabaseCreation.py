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