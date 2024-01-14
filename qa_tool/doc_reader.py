# -- DOCX reader class
from docx import Document
from docx.shared import RGBColor
import pandas as pd

from qa_tool.report_gen import ReportGen
from qa_tool.qa_utils import get_day_index, getcolor, append_location

class DocReader():
    """Reads a docx file and extracts the table information
    """

    def __init__(self, file_path: str, report_gen_object: ReportGen) -> None:
        """
        Args:
            file_path: path to the docx file to read
            report_gen_object: For logging and reporting
        """
        doc_file = Document(file_path)
        self.table = self._make_table(doc_file.tables[0])  # Access the first table in the document

    def get_entity(self, date_item: str) -> list:
        """For a given date, computes and returns an entity
           An entity is a list of dictionary
           each dictionary contains elements of one row of the table
           
          Args:
                date_item: a date in format yyyyddmm
           Returns:
                A list of dictionaries
        """
        day_ind = get_day_index(date_item)
        table_entry = self.table[day_ind]
        entity = list()
        for item in table_entry:
            entity_item = self._get_entity_item(item)
            if entity_item is not None:
                entity.append(entity_item)
        
        return entity
            
    def _get_entity_item(self, item: str) -> dict:
        """Checks if an item is an entry and splits and stores in a dict and returns.

            Args:
                item: string that may or maynot contain data for an entity_item
            Return:
                dict or None 
        """
        entity_item = dict()
        if "\n" in item and len(item) > 1:
                splitted_item = item.split("\n")
                entity_item["time_slot"] = splitted_item[0]
                entity_item["class_name"] = splitted_item[1]
                entity_item["location"] = splitted_item[-1]
                entity_item["instructor_name"] = splitted_item[2]
                return entity_item
        else:
            return None


    def _make_table(self, table: "doc_file_table") -> pd.DataFrame:
        """Takes in Docx table and converts into dataframe
        
            Args:
                table: doc file table
            Returns:
                table as pandas dataframe
        """  

        data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                cell_color = getcolor(cell)
                #if cell_color is not None:
                #    print(cell.text + " " + cell_color)
                text = cell.text
                if cell_color is not None:
                    text = append_location(text, cell_color)
                row_data.append(text)
            data.append(row_data)

        return pd.DataFrame(data)