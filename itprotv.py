#/bin/python3
"""
Date : 5/15/2021
Place : India
Author : Jayapraveen AR
Program aim : To download course videos from ITProtv website
Version : 1.0.5
ToDo:
1.Download Attachments
2.Download subtitles
"""
import requests,json,os,shutil

#Endpoints
tags_url = "https://api.itpro.tv/api/mobile/v1/tag_categories/brand/ITProTV"
iter_cert_course_url = "https://api.itpro.tv/api/mobile/v1/brand/ITProTV/tag_categories/certification/"
iter_category_course_url = "https://api.itpro.tv/api/mobile/v1/brand/ITProTV/tag_categories/course-library/"
iter_course_url = "https://api.itpro.tv/api/urza/v3/consumer-web/course?url="
user_info_url = "https://api.itpro.tv/api/urza/v3/consumer-web/user-config"
#Device details
brand = "ITProTV"
brand_itpro = "00002560-0000-3fa9-0000-1d61000035f3"
ua = "ItProTvApp/2.3.7 (7) (Ios 13; en)"
# Retry times
retry = 3

def token_validation():
    out_data = requests.get(user_info_url, headers = data_auth)
    if(out_data.status_code) == 200:
        return True
    else:
        return False


resolution_data = {"1080p": "jwVideo1080Embed", "720p": "jwVideo720Embed", "480p": "jwVideo480Embed"}
def list_categories(course_tags):
    categories = []
    for index,course in enumerate(course_tags):
        print("{0:} {1:}".format(index,course["name"]))
        categories.append(course["name"])
    return categories

def get_episodes(episodes):
    episodes_url = []
    for index,value in enumerate(episodes):
        print("{0:} {1:}".format(index,value['title']))
        episodes_url.append(value['url'])
    print("Total= "+str(len(episodes_url)))
    return episodes_url

def download_video(url,filename,epoch = 0):
    if(os.path.isfile(filename)):
        video_head = requests.head(url, allow_redirects = True)
        if video_head.status_code == 200:
            video_length = int(video_head.headers.get("content-length"))
            if(os.path.getsize(filename) >= video_length):
                print("Video already downloaded.. skipping Downloading..")
            else:
                print("Redownloading faulty download..")
                os.remove(filename) #Improve removing logic
                download_video(url,filename)
        else:
            if (epoch > retry):
                exit("Server doesn't support HEAD.")
            download_video(url,filename,epoch + 1)
    else:
        video = requests.get(url, stream=True)
        video_length = int(video.headers.get("content-length"))
        if video.status_code == 200:
            if(os.path.isfile(filename) and os.path.getsize(filename) >= video_length):
                print("Video already downloaded.. skipping write to disk..")
            else:
                try:
                    with open(filename, 'wb') as video_file:
                        shutil.copyfileobj(video.raw, video_file)
                except:
                    print("Connection error: Reattempting download of video..")
                    download_video(url,filename, epoch + 1)

            if os.path.getsize(filename) >= video_length:
                pass
            else:
                print("Error downloaded video is faulty.. Retrying to download")
                download_video(url,filename, epoch + 1)
        else:
            if (epoch > retry):
                exit("Error Video fetching exceeded retry times.")
            print("Error fetching video file.. Retrying to download")
            download_video(url,filename, epoch + 1)

def get_link(episodes):
    links = []
    episode_url = "https://api.itpro.tv/api/consumer-web/v2/episode/"
    for i in episodes:
        link = episode_url + i
        links.append(link)
    return links

def get_download_links(episode_links,data_auth,resolution):
    download_links = {}
    for i in episode_links:
        req_data = requests.get(url = i, headers = data_auth)
        req_data = json.loads(req_data.text)
        if (req_data["episode"][resolution] == None):
            resolution = next_resolution
        download_links[req_data["episode"]["title"]] = req_data["episode"][resolution] # Add the episode url corresponding to the resolution selected
    return download_links

os.path.join(os.getcwd())
if os.path.isfile("itprodownloaderConfig.json"):
    with open("itprodownloaderConfig.json",'r') as config:
        config_data = config.read()
    config_data = json.loads(config_data)
else:
    exit("Configuration File is missing..\nCheck out Readme.md to find Instructions.")

session_token = config_data.get("token",None)
download_location = config_data.get("downloadLocation",".")
data_auth = {"Authorization":"Bearer "+session_token,"user-agent":ua}
print("Token is Valid!\n") if token_validation() else exit("Token Error! Recheck and fix token in the configuration")
os.chdir(download_location)
resolution = config_data.get("downloadQuality",None)
next_resolution = resolution_data.get(str(int(resolution.split('p')[0])-360) + 'p')
resolution = resolution_data.get(resolution,None)
exit("Download Quality entered is invalid..") if(resolution == None) else 1
method = config_data.get("method","download")
course_data = requests.get(tags_url)
course_data = json.loads(course_data.text)
course_library_url = course_data['tagCategories'][0]['url']
course_tags = course_data['tagCategories'][0]['tags']
categories = list_categories(course_tags)
choice = int(input("\nEnter your choice: "))
iter_course = iter_category_course_url + course_tags[choice]["url"] + "/courses"
iter_course_data = requests.get(iter_course)
iter_course_data = json.loads(iter_course_data.text)
iter_course = list_categories(iter_course_data['courses'])
choice = int(input("\nEnter your choice: "))
iter_course_data_url = iter_course_url + iter_course_data['courses'][choice]['url'] +"&brand=" + brand_itpro
episodes = requests.get(iter_course_data_url,headers = data_auth)
episodes = json.loads(episodes.text)
episodes = get_episodes(episodes["course"]["episodes"])
episode_links = get_link(episodes)
episodes_download_links = get_download_links(episode_links,data_auth,resolution)
if(method == "download"):
    for index,data in enumerate(episodes_download_links.items()):
        filename = str(index) + '.' +data[0] + ".mp4"
        url = data[1]
        download_video(url,filename)
else:
    writer = open("download_links.txt",'w')
    for filename,url in episodes_download_links.items():
        writer.write(url)
        writer.write("\n")
    writer.close()
