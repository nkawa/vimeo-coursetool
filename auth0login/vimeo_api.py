#import vimeo
import os
from dotenv import load_dotenv, find_dotenv
from vimeo import VimeoClient  #from PyVimeo

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

v = VimeoClient(
    token=  os.environ.get('VIMEO_ACCESS_TOKEN'),
    key=  os.environ.get('VIMEO_CLIENT_ID'),
    secret=  os.environ.get('VIMEO_CLIENT_SECRET')
)

#pict = v.get('/videos/506063480/pictures')

#print(pict.json()['data'][0]['sizes'][3]['link'])
def GetVimeoThummnail(id):
    query="/videos/"+id+"/pictures"
#    print("Get:",query)
    pict = v.get(query)
 #   print(pict.text)
    pjson = pict.json()
  #  print(pjson)
    dt= pjson['data'][0]['sizes']
#    print(dt[3]['width'],dt[3]['link'])
    return (dt[3]['link'])




