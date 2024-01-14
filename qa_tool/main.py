# -- Main file
import yaml

from qa_tool.web_scrapper import WebScrapper
from qa_tool.report_gen import ReportGen
from qa_tool.doc_reader import DocReader
from qa_tool.qa_utils import date_list_generator, get_day_index
from qa_tool.compare_entity import CompareEntity

def main():
    # -- Reading configs
    yaml_file = "configs.yml"

    # Open and read the YAML file
    with open(yaml_file, 'r') as file:
        # Parse the YAML content
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    # -- Making the report generator object
    report_gen_object = ReportGen(config_data["report_file_path"])
    
    # -- Making the web scapper object
    web_scrapper_object = WebScrapper(config_data, report_gen_object)
    if not web_scrapper_object.success:
        report_gen_object.store_report()
        exit()
    
    # -- Making the doc reader object
    report_gen_object.log("Trying to access the docx file")
    try:
        doc_reader_object = DocReader(config_data["docx_file_path"], report_gen_object)
        report_gen_object.log("Docx file opened succesfully")
    except:
        report_gen_object.log("Could not open docx file. Aborting")
        report_gen_object.store_report()
        exit()

    # -- generating the date list
    report_gen_object.log("Creating a list of dates")
    try:
        date_list = date_list_generator(config_data["start_date"], config_data["end_date"])
        report_gen_object.log("List of dates created")
    except:
        report_gen_object.log("There seems to be some issue with date formatting. Aborting")
        report_gen_object.store_report()
        exit()
    
    # -- Looping through dates
    for date_item in date_list:
        
        report_gen_object.log("*" * 10)
        # -- Getting entity from Web. A schedule for a day is an entity
        # -- Entity is a list of dictionaries.
        report_gen_object.log("Getting entity from web for date: " + date_item)
        try:
            web_entity = web_scrapper_object.get_entity(date_item)
        except:
            report_gen_object.log("Could not get entity. Web format seems to have changed. Aborting")
            report_gen_object.store_report()
            exit()


        # -- Getting entity from Doc
        report_gen_object.log("Getting entity from doc for day: " + str(get_day_index(date_item)))
        report_gen_object.log("Remember: Monday is day 0")
        try:
            doc_entity = doc_reader_object.get_entity(date_item)
        except:
            report_gen_object.log("Could not get entity. The schedule is not formatted as expected. Aborting")
            report_gen_object.store_report()
            exit()

        # -- comparing the entites and logging
        compare_entity_object = CompareEntity(doc_entity, web_entity, report_gen_object)
        if compare_entity_object.comapre():
            report_gen_object.log("No mismatch found for: " + date_item)
        
        report_gen_object.log("*" * 10)

    report_gen_object.store_report()
        

