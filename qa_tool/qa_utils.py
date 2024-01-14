# -- Utils
from datetime import date, timedelta
from typing import Union
import re

def date_splitter(my_date: str) -> Union[int, int, int]:
    """Takes a joined date in format yyyymmdd and returns three ints by splitting the date
        Args:
            my_date: str of date in joined format
        Returns:
            Splitted date: int, int, int representing year, month, day 
    """
    return int(str(my_date)[:4]), int(str(my_date)[4:6]), int(str(my_date)[6:])
def date_list_generator(start_date: str, end_date: str) -> list:
    """Takes a start and end date and returns a list of dates in between
    
        Args:
            start_date: date in format yyyymmdd
            end_date: date in format yyyymmdd
        Returns:
            A list of dates starting from start date and ending in end date
    """

    start_date = date(*date_splitter(start_date))
    end_date = date(*date_splitter(end_date))

    # difference between current and previous date
    delta = timedelta(days=1)

    # store the dates between two dates in a list
    dates = []

    while start_date <= end_date:
        # add current date to list by converting  it to iso format
        temp = start_date.isoformat()
        dates.append("".join(temp.split("-")))
        # increment start date by timedelta
        start_date += delta
    
    return dates

def get_day_index(date_item: str):
    """Gets the index of the day based on date_item in format yyyymmdd
       Args: 
            date_item: date in format yyyymmdd
       Returns:
            int corresponding to day index, e.g. Monday is 0, Tuesday is 1
    """
    date_item = date(*date_splitter(date_item))
    return date_item.weekday()

def getcolor(cell):
    pattern = re.compile('w:fill=\"(\S*)\"')
    match = pattern.search(cell._tc.xml)
    try:
        result = match.group(1) 
        return result   
    except:
        return None

def append_location(text: str, color: str) -> str:
    """Takes in a text and color (hex code). Calculates location using hex code
       and appends in text and returns it.  

       Args:
            text: input str
            color: hex code
        Returns:
            appended text 
    """

    location = get_location_using_color(color)
    if not (location == ""):
        return text + "\n" + location
    else:
        return text

def get_location_using_color(color: str) -> str:
    """Gets location using color
        Args:
            color: hex code
        Returns:
            location: string
    """
    if color == "auto" or color == "F2F2F2":
        return ""
    if color == "FDA500" or color == "FFA500":
        return "Track Turf"
    if color == "BAE0EB":
        return "Group X room"
    if color == "CADFB8" or color == "CADFB9" or color == "CADFB7":
        return "Upper Sports Zone"
    if color == "FFD579":
        return "Elite Studio"
    if color == "FFB4CF":
        return "Spin Studio"
    if color == "C5AAF9" or color == "C6AAFB" or color =="C6AAFA":
        return "Serenity Studio"
    
    return ""