#/bin/python3
"""
Date : 3/19/2021
Place : India
Author : Jayapraveen AR
Program aim : To generate downloadable video links at ITProtv website
Version : 1.0.2
"""
import requests,json

#Loggedin Token
login_data = "eyJxxxxxx.eyJxxxxxxxxo"

#Endpoints
iter_cert_course_url = "https://api.itpro.tv/api/mobile/v1/brand/ITProTV/tag_categories/certification/"
iter_category_course_url = "https://api.itpro.tv/api/mobile/v1/brand/ITProTV/tag_categories/course-library/"
login_url = "https://api.itpro.tv/api/urza/v3/mobile/android/login"
#Device details
brand = "ITProTV"
brand_itpro = "00002560-0000-3fa9-0000-1d61000035f3"
ua = "ItProTvApp/2.3.7 (7) (Ios 13; en)"

def list_categories(course_tags):
    categories = []
    for index,course in enumerate(course_tags):
        print("{0:} {1:}".format(index,course['name']))
        categories.append(course['name'])
    return categories

def list_iter_categories(iter_course):
    iter_categories = []
    for index,course in enumerate(iter_course):
        print("{0:} {1:}".format(index,course['name']))
        iter_categories.append(course['name'])
    return iter_categories

def get_episodes(episodes):
    episodes_url = []
    for index,value in enumerate(episodes):
        print("{0:} {1:}".format(index,value['title']))
        episodes_url.append(value['url'])
    print("Total= "+str(len(episodes_url)))
    return episodes_url

def get_link(episodes):
    links = []
    episode_url = "https://api.itpro.tv/api/consumer-web/v2/episode/"
    for i in episodes:
        link = episode_url + i
        links.append(link)
    errorlink = "https://api.itpro.tv/api/mobile/v1/episode/elbauto-scaling/sources"
    try:
        links.remove(errorlink)
    except:
        print("Error link does not exist")
    return links

def get_download_links(episode_links,data_auth):
    download_links = []
    for i in episode_links:
        req_data = requests.get(url = i, headers = data_auth)
        req_data = json.loads(req_data.text)
        print(req_data)
        download_links.append(req_data['episode']['jwVideo1080Embed'])
    print(download_links)
    return download_links


data_auth = {"Authorization":"Bearer "+login_data,"user-agent":ua}
course_data = requests.get('https://api.itpro.tv/api/mobile/v1/tag_categories/brand/ITProTV')
course_data = json.loads(course_data.text)
course_library_url = course_data['tagCategories'][0]['url']
course_tags = course_data['tagCategories'][0]['tags']
categories = list_categories(course_tags)
choice = int(input("\nEnter your choice: "))
iter_course = iter_category_course_url + course_tags[choice]['url'] + "/courses"
iter_course_data = requests.get(iter_course)
iter_course_data = json.loads(iter_course_data.text)
iter_course = list_iter_categories(iter_course_data['courses'])
choice = int(input("\nEnter your choice: "))
iter_course_data_url = "https://api.itpro.tv/api/urza/v3/consumer-web/course?url="+ iter_course_data['courses'][choice]['url'] +"&brand=" + brand_itpro
episodes = requests.get(iter_course_data_url,headers = data_auth)
episodes = json.loads(episodes.text)
episodes = get_episodes(episodes["course"]["episodes"])
episode_links = get_link(episodes)
episodes_download_links = get_download_links(episode_links,data_auth)
writer = open("download_links.txt",'a+')
for i in episodes_download_links:
    writer.write(str(i))
    writer.write("\n")
writer.close()