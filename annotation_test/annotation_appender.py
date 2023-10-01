from bs4 import BeautifulSoup
f = open("Alan McKay.html",'r')
data = f.read()
f.close()

soup = BeautifulSoup(data,features="html.parser")
for link in soup.findAll('a'):
    link['href'] = None
    link['onclick'] = "annotation_prompt("+str(link['href'])+")"

html_string = str(soup)

f = open("Alan McKay edited.html","w")
f.write(html_string)
f.close()s
