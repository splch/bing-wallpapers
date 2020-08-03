#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os import system, getcwd, path
import requests
import urllib.request

from platform import system as sys
sys = sys()
print(sys)
if sys == 'Darwin':
    from appscript import app, mactypes
else:
    import ctypes


# In[2]:


# Get current directory
folder = getcwd()+'/'

print(folder)


# In[3]:


# URL in json format with latest wallpaper
url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"

# Get json output
resp = requests.get(url)
data = resp.json()

# Form image url from json
img = "http://www.bing.com" + data['images'][0]['url']#.replace("1080", "1200")

print(img)


# In[4]:


img_path = folder+'daily_wallpaper'+img[-11:-7]
run = path.exists(img_path) # check if first run

urllib.request.urlretrieve(img, img_path)
print('Downloaded wallpaper')


# In[5]:


# Set mac/win/linux wallpaper
if sys == 'Darwin':
    system('osascript -e \'tell application "Finder" to set desktop picture to "'+img_path+'" as POSIX file\'')
else:
    ctypes.windll.user32.SystemParametersInfoA(20, 0, img_path , 0)
print('Set wallpaper')


# In[6]:


# automatically change wallpaper (mac/linux)
if not run:
    system('crontab -l | { cat; echo "0 */2 * * * cd '+folder+' && $(which python3) '+folder+'wallpaper.py >> cron.log 2>&1"; } | crontab -')
    print('Scheduled cron job.')

