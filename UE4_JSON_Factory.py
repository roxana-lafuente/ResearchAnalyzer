from loginfo import LogInfo
from html_injector import *
from mixed_parser import *
import os
import json
import datetime
from dateutil import parser



def normalizeXandZ(necessary_sentences_information):
    XCoordinates = []
    ZCoordinates = []
    for index,x in enumerate(necessary_sentences_information):
        XCoordinates.append(int(necessary_sentences_information[index]["X"]))
        ZCoordinates.append(int(necessary_sentences_information[index]["Z"]))
    Xnorm = [float(i)/sum(XCoordinates) for i in XCoordinates]
    from math import log
    def f(X):
        return (2**(X*0.1)-1)*(log((X*(-1)+1),0.8))
    ZNorm = [f(float(i)/sum(ZCoordinates)) for i in ZCoordinates]
    parsed_coordinates = [coord["coordinates"].split() for coord in necessary_sentences_information]
    for index,coordinate in enumerate(parsed_coordinates):
        necessary_sentences_information[index]["X"] = str(Xnorm[index])
        necessary_sentences_information[index]["Y"] = coordinate[1]
        necessary_sentences_information[index]["Z"] = str(1-ZNorm[index])
    return necessary_sentences_information



def save_UE4_data(clustering_option = 5400000):
    '''
    X is time
    Y is resource index, resource is the combo of the processname and the windowname
    Z is the length of the clustered sentence, and so it is too the ammout of key events grouped together
    Z represents the importance of a sphere by distance, judging it by the ammount of events it has grouped together
    '''
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
    wrapper["data"] = normalizeXandZ(necessary_sentences_information)
    wrapper["maxY"] = str(len(group_names) - 1)
    wrapper["number_of_groups"] = str(len(group_names))

    with open("UE4Ready.json", 'w') as outfile:
        json.dump(wrapper, outfile)

    with open("events.json", 'w') as outfile:
        json.dump(wrapper, outfile)

    with open("HumanReadableJSON.json", 'w') as outfile:
        json.dump(necessary_sentences_information, outfile)

if __name__ == "__main__":
    save_UE4_data()
