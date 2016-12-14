# a very C reminicent style, lets see how it plays out! here's hope they dont tell me to rewrite it
def combine_and_save_to_html(filename):
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


def save_contentHTML(text):
    text_file = open("visualization/content.html", "w")
    text_file.write(text)
    text_file.close()

def add_at(at, to_add, contentHTML):
    starts_at = contentHTML.rfind(at)
    contentHTML = contentHTML[:starts_at] + to_add + contentHTML[starts_at:]
    return contentHTML

def prepare_group_names(group_names):
    #given ["First","Second","Third",Fourth]
    #returns var names = ['First', 'Second', 'Third', 'Fourth'];
    pre = "var names = ["
    post = "];"
    middle = ""
    for group_name in group_names:
        middle += "'"+  group_name + "'" + ","
    return pre + middle[:-1] + post

def inject_into_html(json, group_names, filename):
    contentHTML = json
    save_contentHTML(contentHTML)

    with open ("visualization/footer_template.html", 'r') as f:
        footer = f.read()
    footer = add_at("<!--group names start here. ",prepare_group_names(group_names), footer)
    with open ("visualization/content.html", 'r') as f:
        content = f.read()
    filepath_complete = "visualization/" + filename + ".html"
    text_file = open("visualization/footer.html", "w")
    text_file.write(footer)
    text_file.close()
    combine_and_save_to_html(filename)
