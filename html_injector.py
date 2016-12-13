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

def inject_into_html(json, filename):
    contentHTML = json
    save_contentHTML(contentHTML)
    combine_and_save_to_html(filename)
