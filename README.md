# ITPro.Tv Courses downloader

## How to use
1. Download the python script.
2. Login to the ITPro.tv site on a web browser after opening the network tab on the developer tools
3. Click dashboard and search for "passedToken" and copy the token starting with "eyJ" completely to clipboard
![Token Instructions](https://i.imgur.com/gCrSSnQ.png)
4. Open the itProDownloaderConfig.json in an text editor of your choice.
5. paste the token by replacing the "eyJxxxx.eyJxxxxx0" in token string
6. Run the script using python. eg. python3 itprotv.py
7. It should list all the Categories in the site.
8. Enter the number corresponding to the title.
9. Wait till the script finishes downloading.

## NOTE: 
1.To get the download links instead of downloading the videos, change the method in the config file to "list". "download_links.txt" file on the same directory where the script is located will appear having the download links of all the videos files. Use any downloading softwares such as IDM/Aria2 to download the videos files.
2. To Get Aria2c compatible url list set the method to "aria2c"

## Usage Disclaimer
1. Intended for Educational purposes only.

## Happy Learning! :-)

