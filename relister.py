# relister.py
#! /usr/bin/python
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import sys, os
from helper import supersecretusername, supersecretpassword

import time

def get_chrome_driver():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    
    
    chrome_driver_path = base_path + "/chromedriver.exe"
    
    return webdriver.Chrome(chrome_driver_path)

def relist():

    # get the browser
    browser = get_chrome_driver() #webdriver.Chrome(chrome_driver_path)
    browser.get('https://accounts.craigslist.org/login/home')

    try:
        WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_id('inputPassword'))
    except TimeoutException:
        browser.quit()


    # log in
    username = browser.find_element_by_name('inputEmailHandle')
    username.send_keys(supersecretusername)

    password = browser.find_element_by_name('inputPassword')
    password.send_keys(supersecretpassword)

    browser.find_element_by_class_name('accountform-btn').click()


    # wait for elements to load
    try:
        WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_xpath("//*[text()[contains(., 'log out')]]"))
    except TimeoutException:
        browser.quit()
        print ("COULD NOT FIND MAIN SCREEN")

    moreToRenew = True

    while moreToRenew:
        try:
            WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_xpath("//*[@class='managebtn'][@value='renew']"))
        except TimeoutException:
            browser.quit()
            moreToRenew = False
            break
            print("ERROR 2")
        print("in while")    
            
        renew_button = browser.find_element_by_xpath("//*[@class='managebtn'][@value='renew']")
        renew_button.click()
        try:
            WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_xpath("//*[@class='postingtitle']"))
        except TimeoutException:
            browser.quit()
            print("ERROR 3")
        
        browser.get('https://accounts.craigslist.org/login/home')
        
        print("Waiting ten seconds.");
        time.sleep(10)


    print("outside while")
    browser.quit()
    
