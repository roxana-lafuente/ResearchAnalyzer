from loginfo import LogInfo
from html_injector import *
from mixed_parser import *
import os
import json
import datetime
from dateutil import parser
import numpy as np

class UE4_JSON_Factory():
    def __init__(self, specific_index=-5, recalculate = True):
        self.clustering_options = [((x * 5) ** 3) * 200 for x in range(1, 11)]
        self.standard_cluster = self.clustering_options[
            int(len(self.clustering_options) / 2)]

    def reject_outliers(self, data, m = 5.):
        '''
        WHY FILTER THE OUTLIERS
        The outliers generate problems during normalization, most of the elements
        receive a number close to zero while the outliers receive a number close to 1.
        Normalization means giving the elements a percentaje divided by 100, thus the 0 to 1 scale.
        This percentaje is the time at which they are in the timeline, the X dimension.
        Because most of the element receive a number close to zero, they lack precision,
        0.0000000010134012 gets truncated by floating point presicion.
        By removing the outliers, the elements receive bigger percentajes.
        0.1013401223456789<--- winning 8 valuable bits of numerical presicion.
        '''
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d/mdev if mdev else 0.
        return data[s<m]

    def normalizeXandZ(self, necessary_sentences_information):
        XCoordinates = []
        YCoordinates = []
        ZCoordinates = []
        for index,x in enumerate(necessary_sentences_information):
            XCoordinates.append(int(necessary_sentences_information[index]["X"]))
            YCoordinates.append(int(necessary_sentences_information[index]["Y"]))
            ZCoordinates.append(int(necessary_sentences_information[index]["Z"]))
        FilteredXCoordinates = self.reject_outliers(np.array(XCoordinates))
        #print str(len(XCoordinates) - len(FilteredXCoordinates)) + " outliers filtered"
        Xnorm = [float(i)/sum(FilteredXCoordinates) for i in FilteredXCoordinates]
        minXNorm = Xnorm[0]
        maxXNorm = Xnorm[-1]
        from math import log
        def f(X):
            return (2**(X*0.1)-1)*(log((X*(-1)+1),0.8))
        ZNorm = [f(float(i)/sum(ZCoordinates)) for i in ZCoordinates]
        parsed_coordinates = [coord["coordinates"].split() for coord in necessary_sentences_information]
        for index,coordinate in enumerate(FilteredXCoordinates):
            necessary_sentences_information[index]["X"] = str(Xnorm[index])
            necessary_sentences_information[index]["Y"] = str(YCoordinates[index])
            necessary_sentences_information[index]["Z"] = str(1-ZNorm[index])
        return str(minXNorm),str(maxXNorm), necessary_sentences_information


    def save_UE4_data(self):
        for clustering_option_index in range(0, 10):
            self.save_UE4_data_by_cluster_option(clustering_option_index)
            print str((clustering_option_index+1)*10) + "% complete"

    def save_UE4_data_by_cluster_option(self, clustering_option_index = -1):
        '''
        X is time
        Y is resource index, resource is the combo of the processname and the windowname
        Z is the length of the clustered sentence, and so it is too the ammout of key events grouped together
        Z represents the importance of a sphere by distance, judging it by the ammount of events it has grouped together
        '''
        if clustering_option_index == -1: clustering_option_index = self.standard_cluster
        clustering_option = self.clustering_options[clustering_option_index]

        necessary_sentences_information = []
        stylized_group_names = {}

        first_X = -1
        path = os.getcwd() + "/example_log/"
        li = LogInfo(path + "click_images/clickimagelogfile_zxysp.txt", # Your click data file here
                     path + "detailed_log/detailedlogfile_zxysp.txt", # Your detailed log file here
                     path + "timed_screenshots/timedscreenshootlogfile_zxysp.txt", # Your timed screenshot log file here
                     path + "system_log/system_log_zxysp.txt") # Your system log data here
        clustered_keys = li.get_clustered_keys(clustering_option)
        group_names = []
        for index,sentence_info in enumerate(clustered_keys):

            start_timestamp = parser.parse(sentence_info[1])
            end_timestamp = sentence_info[2]
            process_name = sentence_info[3]
            if process_name not in group_names:
                group_names.append(process_name)
                stylized_group_names[process_name] = "" if process_name == "|"  else process_name

            necessary_sentence_information = {}
            epoch = datetime.datetime.utcfromtimestamp(0)
            def unix_time_millis(dt):
                return (dt - epoch).total_seconds() * 1000.0
            X = str(int(unix_time_millis(start_timestamp )))
            if (index == 0):
                first_X = int(X)
            else:
                X = str(int(unix_time_millis(start_timestamp )) - first_X)
            Y = str(group_names.index(process_name))
            Z = str(len(sentence_info[0]))

            necessary_sentence_information["sentence"] = sentence_info[0]

            necessary_sentence_information["coordinates"] = (X + " " + Y + " " + Z)
            necessary_sentence_information["X"] = X
            necessary_sentence_information["Y"] = Y
            necessary_sentence_information["Z"] = Z
            necessary_sentences_information.append(necessary_sentence_information)

        wrapper = {}
        wrapper["minXNorm"],wrapper["maxXNorm"],wrapper["data"] = self.normalizeXandZ(necessary_sentences_information)
        wrapper["maxY"] = str(len(group_names) - 1)
        wrapper["number_of_groups"] = str(len(group_names))
        wrapper["groups_names"] = group_names

        with open("../data/UE4Ready_"+str(clustering_option_index + 1)+ ".json", 'w') as outfile:
            json.dump(wrapper, outfile)

        with open("../data/HumanReadableJSON.json", 'w') as outfile:
            json.dump(necessary_sentences_information, outfile)

if __name__ == "__main__":

    ue4_JSON_Factory = UE4_JSON_Factory()
    ue4_JSON_Factory.save_UE4_data()
