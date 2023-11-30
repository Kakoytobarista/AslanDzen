import datetime as dt


def year(request):
    """Add context with current year"""
    return {
        'year': dt.datetime.today().year,
    }
