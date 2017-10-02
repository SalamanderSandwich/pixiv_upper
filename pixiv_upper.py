#!/usr/bin/python
#Goes thru a directory and redownloads images that match pixiv's downsized filenames
from pixivpy3 import *
import sys,os

_USERNAME=""
_PASSWORD=""

api = AppPixivAPI()
api.login(_USERNAME, _PASSWORD)

if len(sys.argv)<1:
    print("Usage: pixiv_upper.py PATH_TO_YOUR_IMAGES'")
    sys.exit()

libPath=sys.argv[1]

for subdir, dirs, files in os.walk(libPath):
    for file in files:
        filename = subdir + os.sep + file
        splitFilename=file.split("_")
        if len(splitFilename)>=3: #you might be a pixiv image
            illustrationID="blank"
            pageNumber="blank"
            if splitFilename[1][:1]=='p' and (splitFilename[2].find("master") != -1 or splitFilename[2].find("square") != -1):
                print("Found pixiv image "+filename+"...", end='')
                illustrationID=splitFilename[0]
                pageNumber=splitFilename[1][1:]
            if splitFilename[0] == "illust" and len(splitFilename) == 4:
                print("Found pixiv image "+filename+"...", end='')
                illustrationID=splitFilename[1]
            if illustrationID != "blank":
                json_result = api.illust_detail(illustrationID,req_auth=True)
                if pageNumber == "blank" and len(json_result.illust['meta_pages']) != 0:
                    print(" downloaded from app")
                    print("!!!WARN!!!")
                    print("Found app image that is part of album, please download image from pixiv")
                    print(filename)
                    print("https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+illustrationID)
                    print("!!!WARN!!!")
                else:
                    try:
                        api.download(json_result.illust['meta_pages'][int(pageNumber)]['image_urls']['original'],path=subdir)
                        print("downloaded")
                    except:
                        api.download(json_result.illust['meta_single_page']['original_image_url'],path=subdir)
                        print("downloaded")
                    else:
                        print("!!!ERROR!!!")
                        print("You shouldn't be seeing this, please submit a bug report and include the illustrationID: "+illustrationID)
                        print("!!!ERROR!!!")