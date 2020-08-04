# -*- coding: utf-8 -*-
"""
Created on Wed July  8 12:40:02 2020

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
import re

def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()
    
if __name__ == '__main__':
    url_static ='/Users/leono1/OneDrive/Research_2019/Jared_Project/'
    data_Ori = pd.read_excel(url_static+'data_for_leo.xlsx')
    API_URL = 'https://api.elsevier.com/content/search/author?query=authlast({})%20and%20authfirst({})%20and%20affil({})&apiKey=891bea59463033deca36152d75882576'
    non_found_count=0
    found_count=0
    header = {
            'Accept': 'application/json'
            }
    schoolMap = [['FAMU', 'Florida Agriculture and Mechanical University'],
        ['FAU', 'Florida Atlantic University'],
        ['FGCU', 'Florida Gulf Coast University'],
        ['FIU', 'Florida International University'],
        ['FSU', 'Florida State University'],
        ['UCF', 'University of Central Florida'],
        ['UF', 'University of Florida'],
        ['UNF', 'University of North Florida'],
        ['USF', 'University of South Florida'],
        ['UWF', 'University of West Florida']]
    schoolMap = {i:j for i,j in schoolMap}

    browser = webdriver.Chrome(ChromeDriverManager().install())
    k=1
    outcome=[]
    id_list=[]
    for lastName, firstName, aff, subj in data_Ori[['last_name','first_name','school', 'discipline']].values[:]:
        print('[%d]:'%k, end=' ')
        k+=1
        aff = schoolMap[aff]
        itemURL = API_URL.format(lastName,firstName, aff, subj)
        res = requests.get(itemURL, headers=header)
        resJSON = json.loads(res.content)
        try:
            if resJSON: #直接搜索last，first and aff有结果#
                num = len(resJSON['search-results']['entry'])
                if num==1: # 如果有结果且唯一
                    authorID = resJSON['search-results']['entry'][0]['dc:identifier'].split(':')[-1] #直接保存ID
                elif num>1: # 如果有结果且不唯一
                    for item in resJSON['search-results']['entry']: #遍历每个结果
                        if  similar(aff.lower(), item['affiliation-current']['affiliation-name'].lower()) > 0.8:# 一旦发现aff的相似度高于80% 
                            authorID = item['dc:identifier'].split(':')[-1] #获取其ID 
                            break # 并退出循环
            elif resJSON=="": #如果搜索结果为空
                itemURL = API_URL.formal(lastName, aff) # 尝试搜索last 和aff
                res = requests.get(itemURL, headers=header)
                resJSON = json.loads(res.content)
                try: 
                    if resJSON:# 如果结果不为空
                        num = len(resJSON['search-results']['entry']) #结果数量
                        if num ==1: #如果结果唯一
                            authorID = resJSON['search-results']['entry'][0]['dc:identifier'].split(':')[-1] #直接获取ID
                            # authorURL = 'https://www.scopus.com/authid/detail.uri?authorId=%s'%authorID                               browser.get(authorURL)
                            # subject = browser.find_elements_by_xpath('//*[@id="subjectAreaBadges"]/span')                      
                        elif num > 1: #如果结果不唯一
                            print('Too many author found')
                            non_found_count+=1
                            id_list.append(["",lastName, firstName])
                            continue
                    else: #如果结果为空
                        raise ValueError #报错
                except Exception as e:
                     print('Not Found This Author:  :%s  :%s  :%s'%(lastName,firstName,aff))
            else:
                itemURL = API_URL.format(lastName, firstName)
                res = requests.get(itemURL, headers=header)
                resJSON = json.loads(res.content)
                try:
                    if resJSON:
                        num = len(resJSON['search-results']['entry']) #结果数量
                        if num==1: #如果结果唯一
                            authorID = resJSON['search-results']['entry'][0]['dc:identifier'].split(':')[-1] #直接获取ID
                        elif num > 1: #如果结果不唯一
                            print('Too many author found    :%s  :%s  :%s'%(lastName, firstName, aff))
                            non_found_count+=1
                            id_list.append(["",lastName, firstName])
                            continue
                    else: #如果结果为空
                        raise ValueError #报错
                except Exception as e:
                     print('Not Found This Author:  :%s  :%s  :%s'%(lastName,firstName,aff))
                     non_found_count+=1
                     id_list.append(["",lastName, firstName])
        except Exception as e:
            print('Not Found This Author:   :%s  :%s  :%s'%(lastName,firstName,aff))
            non_found_count+=1
            id_list.append(["",lastName, firstName])
            continue
        print('%s:   :%s  :%s   :%s'%(lastName,firstName,aff,authorID))
        found_count+=1
        id_list.append([authorID,lastName, firstName])
    print('Total data has '+str(k)+' scopus IDs.\n'+'There '+str(found_count)+' ids were found\n'+'There '+str(non_found_count)+' cannot be found')
    id_df = pd.DataFrame(id_list)
    id_df.to_csv(url_static+'/scopusID_list20200723.csv')