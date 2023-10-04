from bs4 import BeautifulSoup
from urllib.parse import urlparse

whitelist = ["rstyle.me","go.skimresources.com","click.linksynergy.com","go.magik.ly",'shopstyle.it','fave.co','c.klarna.com']

def append_script(source_file_name, source_url, link_bucket_file_name, altered_file_location):

    f = open(source_file_name, 'r')
    file_data = f.read()
    f.close()

    soup = BeautifulSoup(file_data,features="html.parser")

    link_count = 0
    for link in soup.findAll('a'):
        link_count += 1
        link['class'] = link.get('class', []) + ['annotate_'+str(link_count)]
        try:
            link['onclick'] = "return annotation_function('"+str(link['href'])+"','annotate_"+str(link_count)+"');"
        except:
            print()
            print("Annotation Function Error with following object: ")
            print(link)
            print()
            link['onclick'] = "annotation_function('#');"
        #del link['href']
        try:
            if urlparse(link['href']).hostname in whitelist:
                color = "grey"
            else:
                color = 'red'
        except:
            color = 'red'
        try:
            link['style'] = link['style'] + ';;border: solid '+color+' 5px;'
        except:
            link['style'] = 'border:solid '+color+' 5px;'
        link['onMouseOver'] = 'this.style.cursor="pointer"'

    script_string = "var a = document.createElement('a');\na.download = 'links.txt';\na.onclick = 'return false';\n"

    f = open(link_bucket_file_name,"r")
    links_data = f.readlines()
    f.close

    links_string = str()
    for link in links_data:
        links_string += link.split('\n')[0] + "\\n"

    script_string += "\nvar listing = ['"+links_string+"'];\n"

    script_string += "console.log(listing);\n"
    script_string += "function annotation_function(url,id){\n"
    script_string += "console.log(id);\n"
    script_string += "var container = document.getElementsByClassName(id)[0];\nconsole.log(container);\n"
    script_string += "annotation_response = confirm('Annotate ' + url + '?');\n"
    script_string += "console.log(annotation_response);\n"
    script_string += "if (annotation_response == true) {\nlisting = [listing[0]+url+'\\n'];\nconsole.log(listing);\na.href = window.URL.createObjectURL(new Blob(listing, {type: 'text/plain'}));\na.click();\n"
    script_string += "container.style.borderColor = 'grey';}\nreturn false; \n}"

    new_tag = soup.new_tag("script", id="annotation_script")
    new_tag.string = script_string

    soup.html.append(new_tag)
    html_string = str(soup)

    f = open(altered_file_location,"w")
    f.write(html_string)
    f.close()
