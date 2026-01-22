from datetime import datetime

def ru_to_ISO(_date:str):
    pattern = "%d.%m.%Y"
    try:
        iso_date = datetime.strptime(_date, pattern)
    except Exception as e:
        print(e)
        _date = _date.split('.')
        year = _date[-1]
        year = '20' + year
        _date = '.'.join(_date)
        iso_date = datetime.strptime(_date, pattern)
    return iso_date