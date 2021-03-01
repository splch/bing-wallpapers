from os import system, getcwd, path
import requests
import urllib.request

from platform import system as _sys
sys = _sys()
print(sys)

if sys == 'Windows':
    import win32api
    import win32gui
    import win32con

# Get current directory
folder = getcwd()+'/'

print(folder)

# URL in json format with latest wallpaper
url = 'https://www.bing.com/HPImageArchive.aspx?format=js&n=1'

# Get json output
resp = requests.get(url)
data = resp.json()

# Form image url from json

img = 'https://www.bing.com' + data['images'][0]['url']

print(img)

img_path = folder+'daily_wallpaper'+img[-11:-7]
run = path.exists(img_path) # check if first run

try:
    urllib.request.urlretrieve(img.replace('1080', '1200'), img_path)
except:
    urllib.request.urlretrieve(img, img_path)

print('Downloaded wallpaper')

# Set mac/win/linux wallpaper
if sys == 'Darwin':
    system('osascript -e \'tell application "System Events" to tell every desktop to set picture to "'+img_path+'"\'')
elif sys == 'Linux':
    system('gsettings set org.gnome.desktop.background picture-uri '+img_path)
elif sys == 'Windows':
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel/Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path.replace('\\', '/'), 1+2)

print('Set wallpaper')

# automatically change wallpaper
if not run:
    if sys == 'Darwin' or sys == 'Linux':
        system('crontab -l | { cat; echo "0 */2 * * * cd '+folder+' && $(which python3) '+folder+'wallpaper.py"; } | crontab -')
    elif sys == 'Windows':
        system('schtasks /create /sc hourly /mo 2 /tn "Daily Paper" /tr python3.exe '+folder+'wallpaper.py')

    print('Scheduled Daily Paper.')