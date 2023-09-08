import sqlite3 as lite
from bs4 import BeautifulSoup

class DataInterface(object):
    #db_object = DataInterface("./crawl-data.sqlite")
    def __init__(self,path,file_name):
        self.db_location = path + file_name
        self.connection = lite.connect(self.db_location)

    def get_url_from_source(self,file_name):
        try:
            cursor = self.connection.cursor()
            visit_id = file_name.split('-')[0]
            query = 'select url from navigations where visit_id = '+visit_id
            result = cursor.execute(query)
            return result.fetchone()[0]
        except:
            log_str = "Error with following file: \n"
            log_str += file_name + "\n"
            log_str += query + '\n\n\n\n'
            f = open('error_logs/get_url_from_source_log.txt','a')
            f.write(log_str)
            f.close()



class SourceInterface(object):
    def __init__(self, path = 'datadir/sources/'):
        self.path = path

    def set_html_file(self,file_name):
        f = open(self.path+file_name, 'r')
        self.file_name = file_name
        self.file_data = f.read()
        f.close()

    def get_visit_id(self):
        return self.file_name.split('-')[0]

    def get_anchor_hrefs(self):
        soup = BeautifulSoup(self.file_data,features="html.parser")
        anchors = list()
        for anchor in soup.findAll('a'):
            try:
                anchors.append(anchor['href'])
            except:
                log_str = "Error within page: " + self.file_name + "\n"
                log_str += 'Tried to access href of the following element: \n'
                log_str += str(anchor)
                log_str += '\n\n\n\n'
                f = open('error_logs/get_anchor_hrefs_log.txt','a')
                f.write(log_str)
                f.close()
        return anchors

    def get_anchor_info(self):
        #tool a function which grabs *all* anchor info
        pass


if __name__ == "__main__":
    test_file_name = '3571936341707252-c001159620014cf3dd33a0f41016184f.html'
    data_object = DataInterface('datadir/','crawl-data.sqlite')
    print(data_object.get_url_from_source(test_file_name))
    source_object = SourceInterface()
    source_object.set_html_file(test_file_name)
    print(source_object.get_visit_id())
    #print(source_object.get_anchor_hrefs())
