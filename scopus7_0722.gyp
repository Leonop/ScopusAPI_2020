if __name__ == '__main__':
    url_static ='/Users/leono1/OneDrive/Research_2019/Jared_Project/'
    data_Ori = pd.read_excel(url_static+'data_for_leo.xlsx')
    API_URL = 'https://api.elsevier.com/content/search/author?query=authlast({})%20and%20authfirst({})%20and%20affil({})&apiKey=891bea59463033deca36152d75882576'
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

    browser = webdriver.Chrome('/Users/leono1/Sync/Research/ScopusAPI/driver/chromedriver')
    k=1
    outcome=[]
    id_list=[]
    for lastName, firstName, aff in data_Ori[['last_name','first_name','school']].values[:]:
        print('[%d]:'%k, end=' ')
        k+=1
        aff = schoolMap[aff]
        itemURL = API_URL.format(lastName,firstName, aff)
        res = requests.get(itemURL, headers=header)
        resJSON = json.loads(res.content)
        try:
            if resJSON: #直接搜索last，first and aff有结果#
                num = len(resJSON['search-results']['entry'])
                if num ==1:# 如果有结果且唯一
                    authorID = resJSON['search-results']['entry'][0]['dc:identifier'].split(':')[-1]#直接保存ID
                elif num>1: # 如果有结果且不唯一
                    for item in resJSON['search-results']['entry']: #遍历每个结果
                        if  similar(aff.lower(), item['affiliation-current']['affiliation-name'].lower()) > 0.6:# 一旦发现aff的相似度高于60% 
                            authorID = item['dc:identifier'].split(':')[-1] #获取其ID 
                            break # 并退出循环
            elif resJSON =="": #如果搜索结果为空
                itemURL = API_URL.formal(lastName, aff) # 尝试搜索last 和aff
                res = requests.get(itemURL, headers=header)
                resJSON = json.loads(res.content)
                try: 
                    if resJSON:# 如果结果不为空
                        num = len(resJSON['search-results']['entry']) #结果数量
                        if num==1: #如果结果唯一
                            authorID = resJSON['search-results']['entry'][0]['dc:identifier'].split(':')[-1] #直接获取ID
                        elif num > 1: #如果结果不唯一
                            print('Too many author found%s %s(%s)'%(lastName, firstName, aff))
                            continue
                    else: #如果结果为空
                        raise ValueError #报错
                except Exception as e:
                     print('Not Found This Author:%s %s(%s)'%(lastName,firstName,aff))
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
                            print('Too many author found%s %s(%s)'%(lastName, firstName, aff))
                            continue
                    else: #如果结果为空
                        raise ValueError #报错
                except Exception as e:
                     print('Not Found This Author:%s %s(%s)'%(lastName,firstName,aff))
        except Exception as e:
            print('Not Found This Author:%s %s(%s)'%(lastName,firstName,aff))
            continue
        id_list.append([authorID,lastName, firstName])
        print('%s %s(%s): %s'%(lastName,firstName,aff,authorID))

        # authorURL = 'http://www.scopus.com/authid/detail.url?authorID=%s'%authorID
        # browser.get(authorURL)
        # time.sleep(2)
        # for tt in range(1,100):
        #     for articalDiv in browser.find_elements_by_xpath('//tr[starts-with(@id,"resultDataRow")]'):
        #         try:
        #             articalName = articalDiv.find_element_by_xpath('./td[position()=1]/a').text
        #             articalAuthors = articalDiv.find_element_by_xpath('./td[position()=2]').text
        #             articalYear = articalDiv.find_element_by_xpath('./td[position()=3]/span').text
        #             articalPub = articalDiv.find_element_by_xpath('./td[position()=4]').text
        #             articalCite = articalDiv.find_element_by_xpath('./td[position()=5]').text
        #             outcome.append([authorID,lastName,firstName,articalAuthors,
        #                     articalYear,articalName,articalPub,articalCite,aff,num])
        #         except Exception as e:
        #             print(e)
        #             continue
        #     pages = browser.find_elements_by_xpath('//ul[@class="pagination "]/li/a[@data-value]')
        #     for p in pages:  #自动翻页
        #         if int(p.get_attribute('data-value')) == tt + 1:
        #             p.click()
        #             time.sleep(5)
        #             break
        #     else:
        #         break



if __name__ == '__main__':
    url_static ='/Users/leono1/OneDrive/Research_2019/Jared_Project/'
    data_Ori = pd.read_excel(url_static+'data_for_leo.xlsx')
    API_URL = 'https://api.elsevier.com/content/search/author?query=authlast({})%20and%20authfirst({})%20and%20affil({})&apiKey=891bea59463033deca36152d75882576'
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

    browser = webdriver.Chrome('/Users/leono1/Sync/Research/ScopusAPI/driver/chromedriver')
    k=1
    outcome=[]
    for lastName, firstName, aff in data_Ori[['last_name','first_name','school']].values[:]:
        print('[%d]:'%k, end=' ')
        k+=1
        aff = schoolMap[aff]
        itemURL = API_URL.format(lastName,firstName, aff)
        res = requests.get(itemURL, headers=header)
        resJSON = json.loads(res.content)
        try:
            if resJSON: #直接搜索last，first and aff有结果#
                num = len(resJSON['search-results']['entry'])
                if num==1: # 如果有结果且唯一
                    authorID = resJSON['search-results']['entry'][0]['dc:identifier'].split(':')[-1] #直接保存ID
                    # print(authorID)
                elif num>1: # 如果有结果且不唯一
                    for item in resJSON['search-results']['entry']: #遍历每个结果
                        if  similar(aff.lower(), item['affiliation-current']['affiliation-name'].lower()) > 0.6:# 一旦发现aff的相似度高于60% 
                            authorID = item['dc:identifier'].split(':')[-1] #获取其ID 
                            break # 并退出循环
            else: #如果搜索结果为空
                itemURL = API_URL.formal(lastName, aff) # 尝试搜索last 和aff
                res = requests.get(itemURL, headers=header)
                resJSON = json.loads(res.content)
                try: 
                    if resJSON:# 如果结果不为空
                        num = resJSON['opensearch:totalResults'] #结果数量
                        if num ==1: #如果结果唯一
                            authorID = resJSON['search-results']['entry'][0]['dc:identifier'].split(':')[-1] #直接获取ID
                        elif num > 1: #如果结果不唯一
                            print('Too many author found')
                            continue
                    else: #如果结果为空
                        raise ValueError #报错
                except Exception as e:
                     print('Not Found This Author:%s %s(%s)'%(lastName,firstName,aff))
        except Exception as e:
            print('Not Found This Author:%s %s(%s)'%(lastName,firstName,aff))
            continue
        print('%s %s(%s): %s'%(lastName,firstName,aff,authorID))