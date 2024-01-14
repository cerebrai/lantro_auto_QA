# -- Class for generating report and logs

class ReportGen():
    """A class that has the functionality to gather logging/reports and 
       store them in a txt file at the end
    """
    def __init__(self, file_path: str) -> None:
        """
        Args:
            file_path: Path to the file where we store all the logs and 
                       reports
        
        Returns:
            None
        """
        self.file_path = file_path
        self.report = list()

    def log(self, log_line: str):
        """Logs the line given as input 
        
        Args:
            log_line: the string to log
        Returns: 
            None
        """
        self.report.append(log_line)
    
    def store_report(self):
        """Stores the report as txt file
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
        # Write each element of the list to the file
            for item in self.report:
                file.write(str(item) + '\n')

