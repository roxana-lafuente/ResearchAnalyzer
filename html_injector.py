
class HTML_Injector:

    def __init__(self):
        self.options = ""
        self.group_names = []
        self.visualizations = [dict() for x in range(10)]

    def add_at(self, at, to_add, contentHTML):
        starts_at = contentHTML.rfind(at)
        contentHTML = contentHTML[:starts_at] + \
            to_add + contentHTML[starts_at:]
        return contentHTML

    def prepare_group_names(self, group_names):
        #given ["First","Second","Third",Fourth]
        # returns var names = ['First', 'Second', 'Third', 'Fourth'];
        pre = "var names = ["
        post = "];"
        middle = ""

        for clustering_index, group_name_list in enumerate(group_names):
            group_names_per_clustering_index = ""
            for group_name in group_name_list:
                group_names_per_clustering_index += "'" + group_name + "'" + ","
            group_names_per_clustering_index = "["+group_names_per_clustering_index[:-1]+"]"
            middle += group_names_per_clustering_index + ","
        return pre + middle[:-1] + post

    def prepareForHTML(self, json, group_names, options, filename, vis_index):
        self.group_names = group_names
        self.options = options
        self.visualizations[vis_index][filename] = json

    def append_groups_to_content(self, contentHTML):
        # the dates used are placeholders until real phases info can be used
        contentHTML += ',{"id": "orange", "start": "2014-01-31", "end": "2019-02-02", "type": "background", "className": "orange"}'
        contentHTML += ',{"id": "brownish", "start": "2000-01-31", "end": "2014-01-31", "type": "background", "className": "brownish"}'
        contentHTML += ',{"id": "yellowish", "start": "1900-01-31", "end": "2000-01-31", "type": "background", "className": "yellowish"}'
        contentHTML += ',{"id": "aqua", "start": "1900-01-31", "end": "2000-01-31", "type": "background", "className": "aqua"}'
        contentHTML += ',{"id": "green", "start": "1850-01-31", "end": "1900-01-31", "type": "background", "className": "green"}]'
        contentHTML += "\n</textarea>"
        return contentHTML

    def injectIntoHTML(self):
        filename = "index"
        # inject group names
        with open("visualization/footer_template.html", 'r') as f:
            footer = f.read()

        footer = self.add_at("<!--options start here. ",self.options, footer)
        footer = self.add_at("<!--group names start here. ",
                             self.prepare_group_names(self.group_names), footer)

        # inject data
        contentHTML = ""
        for vis_index, visualization in enumerate(self.visualizations):
            if visualization:
                contentHTML += '\n<textarea id="vis_index' + \
                    str(vis_index) + '" style="display: none;">'
                for id, content in enumerate(visualization.values()):
                    if id != 0:
                        content = "," + content[1:]
                    # if id != len(self.visualizations.values())-1:
                       # content = content [:-1]#remove all but the last
                       # bracket
                    content = content[:-1]  # remove all right brackets
                    contentHTML += content + "\n"
                contentHTML = self.append_groups_to_content(contentHTML)

        with open("visualization/orange_style.html", 'r') as f:
            orange_style = f.read()
        orange_style = self.add_at(
            "<!--TIMELINE start here. ", contentHTML + footer, orange_style)
        text_file = open("visualization/index.html", "w")
        text_file.write(orange_style)
        text_file.close()
