from loginfo import LogInfo
from html_injector import *
import os
import json
import datetime
import webbrowser

path = os.getcwd() + "/example_log/"
# Data from one subject.
# LogInfo needs: - Detailed log file path.
#                - Click images file path.
#                - Timed screenshot file path.
#                - System log file path.
li = LogInfo(path + "click_images/clickimagelogfile_zxysp.txt", # Your click data file here
             path + "detailed_log/detailedlogfile_zxysp.txt", # Your detailed log file here
             path + "timed_screenshots/timedscreenshootlogfile_zxysp.txt", # Your timed screenshot log file here
             path + "system_log/system_log_zxysp.txt") # Your system log data here

stylized_group_names = {"left":"Left Clicks","right":"Right Clicks"}
group_names = ["right", "left"]

neccesary_clicks_information = []
for id,clickinfo in  enumerate(li.get_click_info_for_visualization()):

    click_type = clickinfo[0]

    splitted_image_title = clickinfo[2].split('_')
    start_relative_timestamp = float(clickinfo[1][0])
    print splitted_image_title
    date = datetime.datetime.strptime(splitted_image_title[0], "%Y%m%d").date()
    hour = str(datetime.datetime.strptime(splitted_image_title[1], "%H%M%S")).split(' ')[1]
    print date, hour
    start_timestamp = str(date) + ' ' + hour
    end_timestamp = start_timestamp

    neccesary_click_information = {}
    neccesary_click_information["id"] = id
    neccesary_click_information["content"] = "item " + str(id) #+ ' <span style="color:#97B0F8;">(' + names[id % 2] + ')</span>'
    neccesary_click_information["start"] = start_timestamp
    neccesary_click_information["end"] = end_timestamp
    neccesary_click_information["group"] = group_names.index(click_type)
    neccesary_click_information["type"] = "box"
    neccesary_click_information["click_image"] =  path + "click_images/" + clickinfo[2]
    neccesary_clicks_information.append(neccesary_click_information)


inject_into_html(json.dumps(neccesary_clicks_information),stylized_group_names.values(),"clicks")
webbrowser.open("visualization/clicks.html",new=2)
