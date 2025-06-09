from datetime import date

def ru_to_ISO(_date:str):
    _date = [int(x) for x in _date.split(".")]
    year = _date[2]
    month = _date[1]
    day = _date[0]
    iso_date = date(year=year, month=month,day=day)
    return iso_date