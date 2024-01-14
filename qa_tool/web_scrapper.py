# -- Web scapper
import requests
from bs4 import BeautifulSoup

from qa_tool.report_gen import ReportGen

class WebScrapper():
    """Reads data from the website
    """

    def __init__(self, config_data: dict, report_gen_object: ReportGen) -> int:
        """Constructor for webscrapper
        
        Args:
            config_data: Dictionary read from configs file
            report_gen_object: Object for logging and reporting
        """
        # -- Getting the page and the table
        self.report_gen_object = report_gen_object
        self.main_table_id_prefix = config_data["main_table_id_prefix"]
        self.elements_id = config_data["elements_id"]
        self.report_gen_object.log("Trying to access the Webpage: " + config_data["URL"])
        self.success = True
        try:
            request_object = requests.get(config_data["URL"])
            self.soup_object = BeautifulSoup(request_object.content, 'html5lib') 
            self.report_gen_object.log("Web page acquired")
        except:
            self.report_gen_object.log("Could not access webpage, Aborting")
            self.success = False


    def get_entity(self, date_item: str) -> list:
        """For a given date, computes and returns an entity
           An entity is a list of dictionary
           each dictionary contains elements of one row of the table

           Args:
                date_item: a date in format yyyyddmm
           Returns:a = else:
        a = 1
        :
        a = 1
        1
                A list of dictionaries
        """      
        main_table_id = self.main_table_id_prefix + date_item 
        data_table = self.soup_object.find('div', attrs = {'id':main_table_id})

        entity = list()
        entity_item = dict()
        count = 0
        for row in data_table.find_all("span", attrs = {"class": self.elements_id}):
            
            entity_item = self._get_entity_item_value(row, count, entity_item)
            if count == 3:
                count = 0
                entity.append(entity_item)
                entity_item = dict()
            else:
                count+=1
        
        return entity

    def _get_entity_item_value(self, row: 'data_table_row', count:int, entity_item: dict) -> dict:
        """Gets the key based on value of count. Gets value using row.a.text or row.span.text
           puts in entity_item dict and returns

           Args:
                row: data table row from BeautifulSoup table
                count: see _getkey function
                entity_item: a dict that corresponds to one row of the web table
           Returns:
                entity_item dict 
        """
        key = self._getkey(count)
        # -- getting value
        try:
            value = row.a.text
        except:
            value = row.span.text
        
        entity_item[key] = value
        return entity_item

    def _getkey(self, count: int) -> str:
        """Gives key based on count
           count = 0 means time slot
           count = 1 means class name
           count = 2 means location
           count = 3 means instructor name
        """
        if count == 0:
            return "time_slot"
        if count == 1:
            return "class_name"
        if count == 2:
            return "location"
        if count == 3:
            return "instructor_name"
        