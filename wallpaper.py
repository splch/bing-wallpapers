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
    import win32api
    import win32gui
    import win32con


# In[2]:


# Get current directory
folder = getcwd()+'/'

print(folder)


# In[3]:


# URL in json format with latest wallpaper
url = 'https://www.bing.com/HPImageArchive.aspx?format=js&n=1'

# Get json output
resp = requests.get(url)
data = resp.json()

# Form image url from json

img = 'https://www.bing.com' + data['images'][0]['url'].replace('1080', '1200')

print(img)


# In[4]:


img_path = folder+'daily_wallpaper'+img[-11:-7]
run = path.exists(img_path) # check if first run

try:
    urllib.request.urlretrieve(img, img_path)
except:
    urllib.request.urlretrieve(img.replace('1200', '1080'), img_path)
print('Downloaded wallpaper')


# In[5]:


# Set mac/win/linux wallpaper
if sys == 'Darwin':
    system('osascript -e \'tell application "Finder" to set desktop picture to "'+img_path+'" as POSIX file\'')
else:
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path.replace('\\', '/'), 1+2)
    
print('Set wallpaper')


# In[6]:


# automatically change wallpaper (mac/linux)
if not run:
    system('crontab -l | { cat; echo "0 */2 * * * cd '+folder+' && $(which python3) '+folder+'wallpaper.py"; } | crontab -')
    print('Scheduled cron job.')

