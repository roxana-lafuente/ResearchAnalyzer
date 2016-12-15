
class HTML_Injector:
    def __init__(self):
        self.group_names = []
        self.data = {}

    def combine_and_save_to_html(self,filename):
        header = ""
        footer = ""
        content = ""
        with open ("visualization/header.html", 'r') as f:
            header = f.read()

        with open ("visualization/footer.html", 'r') as f:
            footer = f.read()

        with open ("visualization/content.html", 'r') as f:
            content = f.read()
        filepath_complete = "visualization/" + filename + ".html"
        text_file = open(filepath_complete, "w")
        text_file.write(header)
        text_file.write(content)
        text_file.write(footer)
        text_file.close()


    def save_contentHTML(self,text):
        text_file = open("visualization/content.html", "w")
        text_file.write(text)
        text_file.close()

    def add_at(self,at, to_add, contentHTML):
        starts_at = contentHTML.rfind(at)
        contentHTML = contentHTML[:starts_at] + to_add + contentHTML[starts_at:]
        return contentHTML

    def prepare_group_names(self,group_names):
        #given ["First","Second","Third",Fourth]
        #returns var names = ['First', 'Second', 'Third', 'Fourth'];
        pre = "var names = ["
        post = "];"
        middle = ""
        for group_name in group_names:
            middle += "'" +  group_name + "'" + ","
        return pre + middle[:-1] + post

    def prepareForHTML(self,json, group_names, filename):
        for group_name in group_names:
            self.group_names.append(group_name)
        self.data [filename] = json

    def injectIntoHTML(self):
        filename = "index"
        #inject group names
        with open ("visualization/footer_template.html", 'r') as f:
            footer = f.read()
        footer = self.add_at("<!--group names start here. ",self.prepare_group_names(self.group_names), footer)
        #inject data
        contentHTML = ""
        for id,content in enumerate(self.data.values()):
            if id != 0:
                content = "," + content[1:]
            #if id != len(self.data.values())-1:
                #content = content [:-1]#remove all but the last bracket
            content = content [:-1]#remove all right brackets
            contentHTML += content + "\n"
        #placeholder until real phases info can be used
        contentHTML+= ',{"id": "orange", "start": "2014-01-31", "end": "2019-02-02", "type": "background", "className": "orange"}'
        contentHTML+= ',{"id": "brownish", "start": "2000-01-31", "end": "2014-01-31", "type": "background", "className": "brownish"}'
        contentHTML+= ',{"id": "yellowish", "start": "1900-01-31", "end": "2000-01-31", "type": "background", "className": "yellowish"}'
        contentHTML+= ',{"id": "aqua", "start": "1900-01-31", "end": "2000-01-31", "type": "background", "className": "aqua"}'
        contentHTML+= ',{"id": "green", "start": "1850-01-31", "end": "1900-01-31", "type": "background", "className": "green"}]'
        self.save_contentHTML(contentHTML)
        #combine content with header and footer
        with open ("visualization/content.html", 'r') as f:
            content = f.read()
        filepath_complete = "visualization/" + filename + ".html"
        text_file = open("visualization/footer.html", "w")
        text_file.write(footer)
        text_file.close()
        self.combine_and_save_to_html(filename)
