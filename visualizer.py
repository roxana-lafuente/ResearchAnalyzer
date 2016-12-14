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
# Print clicks summary info.
neccesary_clicks_information = []
for id,clickinfo in  enumerate(li.get_click_info()):
    #TODO fix the timestamps, for some reason they give me dates like 1969 when the current year is 2016! I feel like I am taking crazy pills!
    start_timestamp = str(datetime.datetime.fromtimestamp(float(clickinfo[1][0])/1000.0))
    end_timestamp = str(datetime.datetime.fromtimestamp(float(clickinfo[2])/1000.0))

    neccesary_click_information = {}
    neccesary_click_information["id"] = id
    neccesary_click_information["content"] = "item " + str(id) #+ ' <span style="color:#97B0F8;">(' + names[id % 2] + ')</span>'
    neccesary_click_information["start"] = start_timestamp
    neccesary_click_information["end"] = end_timestamp
    neccesary_click_information["group"] = id % 2
    #neccesary_click_information["type"] = "box"
    neccesary_clicks_information.append(neccesary_click_information)
group_names = ["First", "Second", "Third", "Fourth"]
inject_into_html(json.dumps(neccesary_clicks_information),group_names,"clicks")
webbrowser.open("visualization/clicks.html",new=2)
