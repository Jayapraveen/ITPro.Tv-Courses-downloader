'''
Date : 2/29/2020
Place : India
Author : Jayapraveen AR
Program aim : To generate downloadable video links at ITProtv website
Time : 3:18 IST
Version : 1.0.1 working
Method : Bruteforce
'''


import requests
import json
import ast

ua = "ItProTvApp/2.3.7 (7) (Ios 13; en)"

def login():
    username = "" #Enter your username inside the quotes
    password = "" #Enter your password inside the quotes
    endpoint = "https://api.itpro.tv/api/mobile/v1/login"
    brand = "ITProTV"
    contentPlatform = "IOS"
    device = "Iphone 11"
    device_name = "yuabbfbdfcdafd-efga dfh-iafdajk-lmd5675jk-2656" #Randomiseable
    header = ast.literal_eval(json.dumps({"user-agent":ua,"Content-Type":"application/json; charser=UTF-8","Connection":"keep-Alive"}))
    serial_data = json.dumps({"username":username,"password":password,"brand":brand,"contentPlatform":contentPlatform,"device":device,"deviceName":device_name})
    out = requests.post(url = endpoint,data = serial_data,headers = header)
    return json.loads(out.text)

def list_categories(course_tags):
    x = 0
    categories = []
    for i in course_tags:
        print("{0:} {1:}".format(x,i['name']))
        categories.append(i['name'])
        x = x+1
    return categories

def list_iter_categories(iter_course):
    x = 0
    iter_categories = []
    for i in iter_course:
        print("{0:} {1:}".format(x,i['name']))
        iter_categories.append(i['name'])
        x = x+1
    return iter_categories

def get_episodes(episodes):
    x = 0
    count_obj = len(episodes['topics'])
    episodes_url = []
    for j in range(0,count_obj):
        for i in episodes['topics'][j]['episodes']:
            print("{0:} {1:}".format(x,i['title']))
            episodes_url.append(i['url'])
            x = x+1
    print("Total= "+str(len(episodes_url)))
    return episodes_url

def get_link(episodes):
    links = []
    episode_url = "https://api.itpro.tv/api/mobile/v1/episode/"
    for i in episodes:
        link = episode_url + i + "/sources"
        links.append(link)
    return links

def get_download_links(episode_links,data_auth):
    download_links = []
    for i in episode_links:
        req_data = requests.get(url = i, headers = data_auth)
        req_data = json.loads(req_data.text)
        download_links.append(req_data['sources']['videos'][0]['url'])
        print(download_links)
    return download_links


login_data = login()
data_auth = ast.literal_eval(json.dumps({"Authorization":"Bearer "+login_data['token'],"user-agent":ua}))
course_data = requests.get('https://api.itpro.tv/api/mobile/v1/tag_categories/brand/ITProTV')
course_data = json.loads(course_data.text)
course_library_url = course_data['tagCategories'][0]['url']
course_tags = course_data['tagCategories'][0]['tags']
categories = list_categories(course_tags)
iter_cert_course_url = "https://api.itpro.tv/api/mobile/v1/brand/ITProTV/tag_categories/certification/"
iter_category_course_url = "https://api.itpro.tv/api/mobile/v1/brand/ITProTV/tag_categories/course-library/"
choice = int(input("\nEnter your choice: "))
iter_course = iter_category_course_url + course_tags[choice]['url'] + "/courses"
iter_course_data = requests.get(iter_course)
iter_course_data = json.loads(iter_course_data.text)
iter_course = list_iter_categories(iter_course_data['courses'])
choice = int(input("\nEnter your choice: "))
iter_course_url = "https://api.itpro.tv/api/mobile/v1/course/"
iter_course_url = iter_course_url + iter_course_data['courses'][choice]['url'] + "/"
episodes = requests.get(iter_course_url,headers = data_auth)
episodes = json.loads(episodes.text)
episodes = get_episodes(episodes)
episode_links = get_link(episodes)
episodes_download_links = get_download_links(episode_links,data_auth)
writer = open("download_links.txt",'a+')
for i in episodes_download_links:
    writer.write(str(i))
    writer.write("\n")
writer.close()