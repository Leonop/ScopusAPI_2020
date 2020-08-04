# -*- coding: utf-8 -*-
"""
Created on Sun August  8 12:40:02 2020

@author: leo
"""

import pandas as pd
import requests,json,time
import selenium 
from selenium import webdriver
from difflib import SequenceMatcher
import os
from openpyxl.workbook import Workbook
from webdriver_manager.chrome import ChromeDriverManager


url_static = "/Users/leono1/OneDrive/Research_2019/Jared_Project/"
data = pd.read_excel(url_static+'scopusIDs_for_Leo080220.xlsx')
k=1
browser=webdriver.Chrome(ChromeDriverManager().install())
outcome=[]
for authorID,firstName,lastName in data[['ScopusID','first_name','last_name']].values[:]:
    print('[%d]: '%k, end=' ')
    k+=1
    authorURL = 'https://www.scopus.com/authid/detail.uri?authorId=%s'%authorID
    browser.get(authorURL)
    time.sleep(2)
    for tt in range(1,100):
            for articalDiv in browser.find_elements_by_xpath('//tr[starts-with(@id,"resultDataRow")]'):
                try:
                    articalName = articalDiv.find_element_by_xpath('./td[position()=1]/a').text
                    articalAuthors = articalDiv.find_element_by_xpath('./td[position()=2]').text
                    articalYear = articalDiv.find_element_by_xpath('./td[position()=3]/span').text
                    articalPub = articalDiv.find_element_by_xpath('./td[position()=4]').text
                    articalCite = articalDiv.find_element_by_xpath('./td[position()=5]').text
                    outcome.append([authorID,lastName,firstName,articalAuthors,
                            articalYear,articalName,articalPub,articalCite])
                except Exception as e:
                    print(e)
                    continue
            pages = browser.find_elements_by_xpath('//ul[@class="pagination "]/li/a[@data-value]')
            for p in pages:
                if int(p.get_attribute('data-value')) == tt + 1:
                    p.click()
                    time.sleep(5)
                    break
            else:
                break

outcome = pd.DataFrame(outcome,columns=['AuthorID','Last Name','First Name','All Authors','Year','Title','Journal Name','Citation'])
path = '/Users/leono1/OneDrive/Research_2019/Jared_Project/'
outcome.to_csv(path+'outcome20200802.csv')

    