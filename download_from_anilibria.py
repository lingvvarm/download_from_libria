import requests
import math
import os

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

name = input("Search anime: ")
response = requests.get(f'https://api.anilibria.tv/v2/searchTitles?search={name}')

if response:
    pass
else:
    print('Connection error. Code: ' + str(response.status_code))
    exit()



if len(response.text) > 2:
    print("")
else:
    print("Title not found.")
    exit()

json_response = response.json()
json = json_response

for i in range(len(json)):
    print(f'[{i + 1}]', end=" ")
    print(json[i]['names']["ru"])

print("")
number = int(input("Enter number: ")) - 1

if number >= len(json):
    print("Error: wrong number.")
    exit()

torrent_list = json[number]["torrents"]["list"]

for i in range (len(torrent_list)):
    print(f'[{i + 1}]', end=" ")
    print("Episodes" + " " + torrent_list[i]["series"]["string"], end=" ")
    print(torrent_list[i]["quality"]["string"], end=" ")
    print(convert_size(torrent_list[i]["total_size"]), end=" ")
    print("seeds: " + str(torrent_list[i]["seeders"]))

print("")
torrent_num = int(input("Choose torrent: ")) - 1

if torrent_num >= len(torrent_list):
    print("Error: wrong torrent chosen.")
    exit()

url = "http://anilibria.tv" + torrent_list[torrent_num]["url"]

r = requests.get(url, allow_redirects=True)

filename = json[number]["names"]["en"].replace(" ", "_") + "-Anilibria.TV" +  "[" + torrent_list[torrent_num]["quality"]["string"].replace(" ", "_") + "]" + "[" + torrent_list[torrent_num]["series"]["string"].replace(" ", "_") + "]" + ".torrent"

filepath = "/home/lingvvarm/Загрузки/" + filename

open(filepath, 'wb').write(r.content)

command = "transmission-gtk" + " " + filepath
os.system(command)