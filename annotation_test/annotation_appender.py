from bs4 import BeautifulSoup
f = open("Alan McKay.html",'r')
data = f.read()
f.close()

soup = BeautifulSoup(data,features="html.parser")
for link in soup.findAll('a'):
    link['onclick'] = "annotation_function('"+str(link['href'])+"');"
    del link['href']
    try:
        link['style'] = link['style'] + ';;border: solid red 5px;'
    except:
        link['style'] = 'border:solid red 5px;'
    link['onMouseOver'] = 'this.style.cursor="pointer"'


script_string = "var a = document.createElement('a');\na.download = 'links.txt';\n"

f = open("links.txt","r")
links_data = f.readlines()
f.close

links_string = str()
for link in links_data:
    links_string += link.split('\n')[0] + "\\n"

print(links_string)

script_string += "\nvar listing = ['"+links_string+"'];\n"

script_string += "console.log(listing);\nfunction annotation_function(url){\nannotation_response = prompt('Please enter annotation value for ' + url);\nconsole.log(annotation_response);\nif (annotation_response == 'yes') {\nlisting = [listing[0]+url+'\\n'];\nconsole.log(listing);\na.href = window.URL.createObjectURL(new Blob(listing, {type: 'text/plain'}));\na.click();\n} \n}"

new_tag = soup.new_tag("script", id="annotation_script")
new_tag.string = script_string

soup.html.append(new_tag)
html_string = str(soup)



f = open("Alan McKay edited.html","w")
f.write(html_string)
f.close()
