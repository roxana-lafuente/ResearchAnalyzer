from loginfo import LogInfo
from html_injector import *
from mixed_parser import *
import os
import json
import datetime


class Visualizer():
    #TODO When recalculate is True
    #use a baked timeline content instead of computing it
    def __init__(self, specific_index=-5, recalculate = True):
        self.specific_index = specific_index
        self.show_all = True
        if self.specific_index == -5:
            self.show_all = False

        self.global_id = 0
        self.group_names_by_clustering_index = [ [] for i in range(10) ]
        self.log_classes = ["sentences", "clicks"]
        self.start = ""
        self.end = ""
        self.options = ""
        self.content_style = "color: #7c795d;"
        self.clustering_options = [((x * 5) ** 3) * 200 for x in range(1, 11)]
        self.standard_cluster = self.clustering_options[
            int(len(self.clustering_options) / 2)]
        self.path = str(os.getcwd()).replace('\\','/') + "/example_log/"
        # Data from one subject.
        # LogInfo needs: - Detailed log file path.
        #                - Click images file path.
        #                - Timed screenshot file path.
        #                - System log file path.

        self.li = LogInfo(self.path + "click_images/clickimagelogfile_zxysp.txt",  # Your click data file here
                          self.path + "detailed_log/detailedlogfile_zxysp.txt",  # Your detailed log file here
                          # Your timed screenshot log file here
                          self.path + "timed_screenshots/timedscreenshootlogfile_zxysp.txt",
                          self.path + "system_log/system_log_zxysp.txt")  # Your system log data here

        self.injector = HTML_Injector()
        self.general_parse_into_HTML(self.log_classes.index("clicks"))
        for index,clustering_option in enumerate(self.clustering_options):
            self.general_parse_into_HTML(
                self.log_classes.index("sentences"), clustering_option)
            print str((index+1)*10) + "% complete"
        self.injector.injectIntoHTML()

    def prepare_options(self):
        if self.options == "":
            self.options = "var options = {\nstart: '"
            self.options += self.start
            self.options += "',\nend: '"
            self.options += self.end
            self.options += "',\neditable: false\n};"
        return self.options


    def check_if_valid_and_set_option(self, index = 0):
        start = self.specific_index - 1
        end = self.specific_index + 1
        is_valid = index >= start and index <= end
        is_start = index == start
        is_end = index == end
        return is_valid, is_start, is_end

    def general_parse_into_HTML(self, clicks, clustering_option=0):

        if not clustering_option:
            clustering_option = self.standard_cluster
        clustering_option_index = self.clustering_options.index(clustering_option)
        array_to_parse = []
        stylized_group_names = {}
        stylized_click_names = {}
        neccesary_information_array = []
        if clicks:
            stylized_click_names = {"left": "Left Click", "right": "Right", "middle": "Middle"}
        if clicks:
            array_to_parse = self.li.get_click_info_for_visualization()
        else:
            array_to_parse = self.li.get_clustered_keys(clustering_option)
        for index, info in enumerate(array_to_parse):
            self.global_id += 1
            is_valid, is_start, is_end = self.check_if_valid_and_set_option(index)
            if (is_valid or self.specific_index == -5):
                if clicks:
                    process_name = info[7]
                else:
                    process_name = info[3]
                process_name = process_name.replace("|", "|<br>")
                if process_name not in self.group_names_by_clustering_index[clustering_option_index]:
                    self.group_names_by_clustering_index[clustering_option_index].append(process_name)
                if clicks:
                    neccesary_information = self.parse_click_info(
                        info, stylized_click_names, clustering_option_index, is_start, is_end)
                else:
                    neccesary_information = self.parse_sentence_info(info, clustering_option_index, is_start, is_end)
                neccesary_information_array.append(neccesary_information)
        if clicks:
            # reuse the parsed clicks for all of the clustering options
            for clustering_option in self.clustering_options:
                vis_index = self.clustering_options.index(clustering_option)
                if neccesary_information_array:
                    self.injector.prepareForHTML(
                    json.dumps(neccesary_information_array),
                    self.group_names_by_clustering_index,
                    self.prepare_options(),
                    "clicks",
                    vis_index)
        else:
            vis_index = self.clustering_options.index(clustering_option)
            if neccesary_information_array:
                self.injector.prepareForHTML(
                json.dumps(neccesary_information_array),
                self.group_names_by_clustering_index,
                self.prepare_options(),
                "sentences",
                vis_index)

    def parse_sentence_info(self, sentence_info, clustering_option_index, is_start = False, is_end = False):
        start_timestamp = sentence_info[1]
        end_timestamp = sentence_info[2]
        process_name = sentence_info[3].replace("|", "|<br>")
        neccesary_sentence_information = {}
        neccesary_sentence_information["id"] = self.global_id
        neccesary_sentence_information[
            "content"] = ' <span style="' + self.content_style + '">' + sentence_info[0] + '</span>'
        neccesary_sentence_information["start"] = start_timestamp
        if is_start: self.start = start_timestamp
        neccesary_sentence_information["end"] = end_timestamp
        if is_end: self.end = end_timestamp
        neccesary_sentence_information[
            "group"] = self.group_names_by_clustering_index[clustering_option_index].index(process_name)
        neccesary_sentence_information["type"] = "box"
        return neccesary_sentence_information

    def parse_click_info(self, click_info, stylized_click_names, clustering_option_index, is_start = False, is_end = False):
        click_type = click_info[0]
        process_name = click_info[7].replace("|", "|<br>")

        splitted_image_title = click_info[2].split('_')
        date = datetime.datetime.strptime(
            splitted_image_title[0], "%Y%m%d").date()
        hour = str(datetime.datetime.strptime(
            splitted_image_title[1], "%H%M%S")).split(' ')[1]
        start_timestamp = str(date) + ' ' + hour
        end_timestamp = start_timestamp
        neccesary_click_information = {}
        neccesary_click_information["id"] = self.global_id
        neccesary_click_information["content"] = ' <span style="' + \
            self.content_style + '">' + \
            stylized_click_names[click_type] + '</span>'
        neccesary_click_information["start"] = start_timestamp
        if is_start: self.start = start_timestamp
        neccesary_click_information["end"] = end_timestamp
        if is_end: self.end = end_timestamp
        neccesary_click_information[
            "group"] = self.group_names_by_clustering_index[clustering_option_index].index(process_name)
        neccesary_click_information["type"] = "box"
        neccesary_click_information[
            "click_image"] = "file:///" + self.path + "click_images/" + click_info[2]
        return neccesary_click_information


if __name__ == "__main__":

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    if len(sys.argv) == 2:
        vis = Visualizer(int(sys.argv[1]))
    else:
        vis = Visualizer()
