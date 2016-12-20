from loginfo import LogInfo
from html_injector import *
from mixed_parser import *
import os
import json
import datetime
import webbrowser
from text_reconstruction import TextReconstructor

class Visualizer():
    def __init__(self):

        self.global_id = 0
        self.group_names = []

        self.content_style = "color: #7c795d;"
        self.clustering_options = [((x * 5) ** 3)*200 for x in range(1, 11)]
        print len(self.clustering_options)
        print self.clustering_options
        self.path = os.getcwd() + "/example_log/"
        # Data from one subject.
        # LogInfo needs: - Detailed log file path.
        #                - Click images file path.
        #                - Timed screenshot file path.
        #                - System log file path.

        self.li = LogInfo(self.path + "click_images/clickimagelogfile_zxysp.txt", # Your click data file here
                     self.path + "detailed_log/detailedlogfile_zxysp.txt", # Your detailed log file here
                     self.path + "timed_screenshots/timedscreenshootlogfile_zxysp.txt", # Your timed screenshot log file here
                     self.path + "system_log/system_log_zxysp.txt") # Your system log data here

        self.injector = HTML_Injector()
        self.parse_and_inject_clicks_into_HTML()
        for clustering_option in self.clustering_options:
            self.parse_and_inject_sentences_into_HTML(clustering_option)
        self.injector.injectIntoHTML()

        webbrowser.open("visualization/index.html",new=2)


    def parse_and_inject_clicks_into_HTML(self):

        stylized_group_names = {}
        stylized_click_names = {"left":"Left Click", "right":"Right"}

        neccesary_clicks_information = []
        for clickinfo in self.li.get_click_info_for_visualization():
            self.global_id += 1

            click_type = clickinfo[0]
            process_name = clickinfo[7]

            if process_name not in self.group_names:
                self.group_names.append(process_name)
                stylized_group_names[process_name] = "" if process_name == "|"  else process_name

            splitted_image_title = clickinfo[2].split('_')
            date = datetime.datetime.strptime(splitted_image_title[0], "%Y%m%d").date()
            hour = str(datetime.datetime.strptime(splitted_image_title[1], "%H%M%S")).split(' ')[1]
            start_timestamp = str(date) + ' ' + hour
            end_timestamp = start_timestamp
            neccesary_click_information = {}
            neccesary_click_information["id"] = self.global_id
            neccesary_click_information["content"] =  ' <span style="' + self.content_style + '">' + stylized_click_names[click_type] + '</span>'
            neccesary_click_information["start"] = start_timestamp
            neccesary_click_information["end"] = end_timestamp
            neccesary_click_information["group"] = self.group_names.index(process_name)
            neccesary_click_information["type"] = "box"
            neccesary_click_information["click_image"] =  self.path + "click_images/" + clickinfo[2]
            neccesary_clicks_information.append(neccesary_click_information)

        #reuse the parsed clicks for all of the clustering options
        for clustering_option in self.clustering_options:
            vis_index = self.clustering_options.index(clustering_option)
            self.injector.prepareForHTML(json.dumps(neccesary_clicks_information),stylized_group_names.values(),"clicks",vis_index)

    def parse_and_inject_sentences_into_HTML(self, clustering_option = 5000000):
        neccesary_sentences_information = []
        stylized_group_names = {}

        for sentence_info in self.li.get_clustered_keys(clustering_option):
            self.global_id += 1

            start_timestamp = sentence_info[1]
            end_timestamp = sentence_info[2]
            process_name = sentence_info[3]
            if process_name not in self.group_names:
                self.group_names.append(process_name)
                stylized_group_names[process_name] = "" if process_name == "|"  else process_name

            neccesary_sentence_information = {}
            neccesary_sentence_information["id"] = self.global_id
            neccesary_sentence_information["content"] = ' <span style="' + self.content_style + '">' + sentence_info[0] + '</span>'
            neccesary_sentence_information["start"] = start_timestamp
            neccesary_sentence_information["end"] = end_timestamp
            neccesary_sentence_information["group"] = self.group_names.index(process_name)
            neccesary_sentence_information["type"] = "box"
            neccesary_sentences_information.append(neccesary_sentence_information)

        vis_index = self.clustering_options.index(clustering_option)
        self.injector.prepareForHTML(json.dumps(neccesary_sentences_information),stylized_group_names.values(),"sentences",vis_index)

if __name__ == "__main__":
    vis = Visualizer()
