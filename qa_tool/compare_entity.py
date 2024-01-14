# -- Class with the functionality to compare two entities
from thefuzz import fuzz
from qa_tool.report_gen import ReportGen

class CompareEntity():
    """Compares two entities to find mismatches
    """
    def __init__(self, doc_entity: list, 
                       web_entity: list, 
                       report_gen_object: ReportGen) -> None:
        
        """
        Args:
            doc_entity: List of dictionaries carrying information from docs
            web_entity: List of dictionaries carrying information from web
            report_gen_object: For logging and reporting
        """
        self.doc_entity = doc_entity
        self.web_entity = web_entity
        self.report_gen_object = report_gen_object
    
    def comapre(self) -> bool:
        """Compares the two entities, finds mismatches and logs results
        """

        # -- Looping through the entity_items 
        status = True
        for entity_item in self.doc_entity:
            
            # -- Find the best matching entry based on time and instructor name
            best_match_web_entity = self._get_best_match(entity_item)
            
            if best_match_web_entity == -1:

                # -- Two entries on web with same time and instructor
                print_entity = self._print_entity(entity_item)
                self.report_gen_object.log("ERROR two web entries with same time and instructor corresponding to doc entry: " + print_entity)
                status = False

            elif best_match_web_entity is None:
                # -- No best entry found
                print_entity = self._print_entity(entity_item)
                self.report_gen_object.log("MISMATCH: No entity on web found corresponding to: " + print_entity)
                status = False
            else:
                # -- Best entry found, comparing entry by entry
                if not self._compare_item_by_item(entity_item, best_match_web_entity):
                    # -- Mismatch between 2 entries
                    print_entity_doc = self._print_entity(entity_item)
                    print_entity_web = self._print_entity(best_match_web_entity)
                    self.report_gen_object.log("MISMATCH")
                    self.report_gen_object.log("Entry in Doc: " + print_entity_doc)
                    self.report_gen_object.log("Entry on Web: " + print_entity_web)
                    self.report_gen_object.log("\n")
                    status = False
                else:
                    pass

        return status
    
    def _print_entity(self, entity_item: dict):
        """Stacks all values in a dict as a list
        """
        output = list()
        for key in entity_item:
            output.append(entity_item[key])
        
        return "-".join(output)

    def _get_best_match(self, entity_item) -> dict:
        """Compares a given entity_item from doc with all the entity_items 
           from web and returns the best match based on same time and instructor
           name
        """
        doc_time = entity_item["time_slot"]
        doc_instructor = entity_item["instructor_name"]

        found_flag = False
        for web_entity_item in self.web_entity:
            web_time = web_entity_item["time_slot"]
            web_instructor = web_entity_item["instructor_name"]

            if self._compare_string(web_time, doc_time) and \
               self._compare_string(web_instructor, doc_instructor):
                if not found_flag:
                    best_match_entity = web_entity_item
                    found_flag = True
                else:
                    # found two web entries with same time and instructor (error)
                    return -1
        
        if found_flag:
            return best_match_entity
        else:
            return None
                

    def _compare_string(self, string1: str, string2: str) -> bool:
        """Given two strings returns true if they match
        """
        string1 =  ''.join(letter for letter in string1 if letter.isalnum()).lower()
        string2 =  ''.join(letter for letter in string2 if letter.isalnum()).lower()

        if string1 == string2:
            return True
        else:
            return False
        

    def _compare_item_by_item(self, entity_item1: dict, entity_item2: dict) -> bool:
        """Compares two dicts item by item and returns true if same else false
        """

        for key in entity_item1:
            if not self._compare_string(entity_item1[key], entity_item2[key]):
                return False

        return True
