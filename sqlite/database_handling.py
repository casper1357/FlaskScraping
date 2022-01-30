import cmath
from twitchAPI.twitch import Twitch
import time
import json
import matplotlib.pyplot as plt
import sqlite3

from pprint import pprint
start_time = time.time()
time_to_update=10 # time in seconds
twitch = Twitch('uowsdxh0nb3h4qqgk8v8oxkvl4tlqh', 'pvyjt5qkfuoe4fyzeuzzy4zlhyd357') # Twitch key/secret
#game_ID of poe is 29307
#pprint(twitch.get_users(logins=['Zizaran']))
#pprint(twitch.get_games(names=['Path of Exile']))
#pprint(twitch_data_lst[0])

def spec_key_data(d_key):
    twitch_data = twitch.get_streams(first=10, game_id=['29307'])  # first parameter has max of 100, can also take game_id that specifies specific game
    #pprint(twitch_data)
    twitch_data_lst = twitch_data['data']
    #pprint(twitch_data_lst)
    data = []
    for i in twitch_data_lst:
        data.append(i[d_key])
    return data

def get_viewer_data():
    print("Fetching viewer data")
    graph1_data = []
    graph2_data = []
    view_count = spec_key_data('viewer_count')
    titles = spec_key_data('title')
    user_names = spec_key_data('user_name')
    ascii_user_names = get_users_ascii(user_names)
    total_view_count = []
    for i in ascii_user_names:
        users_data = twitch.get_users(logins=i)  # Passing in multiple users will result in it randomising the order, which we do not want and therefore pass 1 at a time
        total_view_count.append(users_data['data'][0]['view_count'])
    #print(type(total_view_count[0]))
    for i in range(len(user_names)):
        graph1_data.append([user_names[i], int(view_count[i]), titles[i]])
    for i in range(len(ascii_user_names)):
        graph2_data.append([ascii_user_names[i], int(total_view_count[i])])
    #return [graph1_data, graph2_data]


def get_users_ascii(users):
    users_ascii = []
    for i in users:  # Checks if streamers have ascii name otherwise won't work with .get_users
        try:
            i.encode('ascii')
            # print(f"{i} was ascii")
            users_ascii.append(i)
        except UnicodeEncodeError:
            pass
            # print(f"User {i} was not ascii")
    return users_ascii

conn = sqlite3.connect("twitch.db")

# Creates the cursor
cursor = conn.cursor()

#Destroy a table
#cursor.execute("DROP TABLE streamers")


all_streamers = [("Zizaran", 5000, 1, '30/1/2022'), ("Steelmage", 2000, 1, '30/1/2022'), ("Aceu", 10000, 1, '30/1/2022')]
#cursor.execute("""UPDATE streamers SET user_name = 'MONKE' WHERE user_name = 'Zizaran' AND view_count = 4000""")
#cursor.execute("SELECT rowid, * FROM streamers ORDER BY user_name LIMIT 1")
#cursor.execute("""UPDATE streamers SET user_name = 'MONKE' WHERE rowid = 1""")
#cursor.execute("DELETE from streamers WHERE rowid = 6")
#cursor.execute("SELECT rowid, * FROM streamers")
#cursor.execute("SELECT rowid, * FROM streamers WHERE user_name = 'Zizaran'")
#print(cursor.fetchall())
#cursor.executemany("INSERT INTO streamers VALUES (?,?,?,?)", all_streamers)
print("Command executed succesfully...")
'''
# Create table
cursor.execute("""CREATE TABLE view_count_streamers (
        user_name text,
        view_count integer,
        time text
    )""")

# Create table
cursor.execute("""CREATE TABLE total_view_count_streamers (
        user_name text,
        total_views integer,
        time text
    )""")
'''
conn.commit()
conn.close()

#while True:
    #get_viewer_data()
