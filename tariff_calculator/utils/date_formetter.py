from datetime import datetime

def ru_to_ISO(_date:str):
    pattern = "%d.%m.%Y"
    iso_date = datetime.strptime(_date, pattern)
    return iso_date