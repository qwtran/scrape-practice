import time

from random import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

sleep_min_sec = 5
sleep_max_sec = 10

one_way              = False
input_depart_airport = "BWI"
input_arrive_airport = "LAX"
input_departure_date = "4/1"
input_arrival_date   = "4/4"
input_passengers     = 5


def parse_flight_table(flight_table_elem):
    tabledata = []

    row_elems = flight_table_elem.find_elements_by_xpath(".//tr[contains(@id, 'flightRow')]")

    for row in row_elems:
        rowdata = []

        # Get depart time
        flight_depart_time_elem = row.find_element_by_xpath(".//td[contains(@class, 'depart_column')]")
        rowdata.append(str(flight_depart_time_elem.text).split('\n')[0])

        # Get arrive time
        flight_arrive_time_elem = row.find_element_by_xpath(".//td[contains(@class, 'arrive_column')]")
        rowdata.append(str(flight_arrive_time_elem.text).split('\n')[0])

        # Get number of stops
        flight_routes_elem = row.find_element_by_xpath(".//td[contains(@class, 'routing_column')]")
        rowdata.append(str(flight_routes_elem.text).split('\n')[0])

        # Get duration
        flight_duration_elem = row.find_element_by_xpath(".//span[contains(@class, 'duration')]")
        rowdata.append(flight_duration_elem.text)

        # Get prices
        flight_business_price_elems = row.find_elements_by_xpath(".//td[contains(@class, 'price_column')]")
        for elem in flight_business_price_elems:
            try:
                rowdata.append(elem.find_element_by_xpath(".//label[contains(@class, 'product_price')]").text)
            except NoSuchElementException:
                rowdata.append('Sold Out')

        # Append row to tabledata
        tabledata.append(rowdata)

    return tabledata


def scrape():
    browser = webdriver.Firefox()
    browser.get("https://www.southwest.com/")

    # Set one way trip with click event.
    if one_way:
        one_way_elem = browser.find_element_by_id("trip-type-one-way")
        one_way_elem.click()

    # Set the departing airport.
    depart_airport_elem = browser.find_element_by_id("air-city-departure")
    depart_airport_elem.send_keys(input_depart_airport)

    # Set the arrival airport.
    arrive_airport_elem = browser.find_element_by_id("air-city-arrival")
    arrive_airport_elem.send_keys(input_arrive_airport)

    # Set departure date.
    depart_date_elem = browser.find_element_by_id("air-date-departure")
    depart_date_elem.clear()
    depart_date_elem.send_keys(input_departure_date)

    # Set return date.
    if not one_way:
        return_date_elem = browser.find_element_by_id("air-date-return")
        return_date_elem.clear()
        return_date_elem.send_keys(input_arrival_date)

    # Clear the readonly attribute from the passenger elem
    passengers_elem = browser.find_element_by_id("air-pax-count-adults")
    passengers_elem.click()

    # Set passenger count.
    passengers_elem_add = browser.find_element_by_id("jb-number-selector-more")
    for x in range(0, input_passengers - 1):
        passengers_elem_add.click()

    # Wait a random amount of time sec
    time.sleep(randint(sleep_min_sec, sleep_max_sec))

    # Submit
    search_elem = browser.find_element_by_id("jb-booking-form-submit-button")
    search_elem.click()

    # Web driver might be too fast. Tell it to slow down.
    wait = WebDriverWait(browser, 120)
    wait.until(EC.element_to_be_clickable((By.ID, "faresOutbound")))

    result = []

    outbound_fares_table_elem = browser.find_element_by_id("faresOutbound")
    result.append(parse_flight_table(outbound_fares_table_elem))

    if not one_way:
        return_fares_table_elem = browser.find_element_by_id("faresReturn")
        result.append(parse_flight_table(return_fares_table_elem))

    print(result)


scrape()

# browser.quit()
