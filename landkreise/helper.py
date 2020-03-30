import re
import datetime
import locale
import logging
from email.utils import parsedate

logger = logging.getLogger(__name__)

# NOTE: these have to be sorted, with the most general regex at the bottom!
date_regexes = {
	"Stand:\d+\.\w+,\d+Uhr" : "Stand:%d.%B,%HUhr",
        "Stand:\d+\.\w+\d+,\d+Uhr" : "Stand:%d.%B%Y,%HUhr",


	"Stand:\d+\.\d+.\d+,\d+\.\d+Uhr" : "Stand:%d.%m.%Y,%H.%MUhr",
	"Stand\d+\.\d+.\d+,\d+\.\d+Uhr" : "Stand%d.%m.%Y,%H.%MUhr",
        "Stand\d+\.\d+.\d+,\d+:\d+Uhr" : "Stand%d.%m.%Y,%H:%MUhr",
    
    
    "Stand\d+\.\w+,\d+Uhr" : "Stand%d.%B,%HUhr",

	"Stand:\d+\.\w+\d+;\d+\.\d+Uhr" : "Stand:%d.%B%Y;%H.%MUhr",


	"mitStandvon\w+,\d+\.\w+,\d+\.\d+Uhr":"mitStandvon%A,%d.%B,%H.%MUhr",

	"Stand\d+\.\d+\.\d+-\d+:\d+Uhr":"Stand%d.%m.%Y-%H:%MUhr",
        "Stand\d+.\d+.\d+" : "Stand%d.%m.%Y",
        "Stand:\w+,\d+\.\w+\d+": "Stand:%A,%d.%B%Y",
	"\d+\.\d+\.\d+":"%d.%m.%Y",
	"\d+\.\w+\d+":"%d.%B%Y",
	"\d+\.\w+":"%d.%B"

    }

def parse_dateheader(datestring):
    return datetime.datetime(*parsedate(datestring)[:6])


def check_and_replace_year(date_string):
    # TODO this is not particular safe, for example if we switched the dateformat to military style.
    if re.match("1900", date_string):
        return date_string.replace("1900", datetime.date.today().strftime("%Y"))
    else:
        return date_string

def extract_case_num(text, prefix, source=None):
    try:
        cases_raw = text.split(prefix)[1]
        return get_number_only(cases_raw)
    except (IndexError, ValueError) as e:
        raise ParsingError((prefix, source), 'Failed to split by %r in %s : %s', e)

def extract_case_num_directregex(text, regex, match, source=None):
    try:
        cases_raw = re.findall(regex,text)[match]
        return get_number_only(cases_raw)
    except (IndexError, ValueError) as e:
        raise ParsingError((regex, source), 'Failed to match %r in %s : %s', e)

def genfunc_dateformats_parser(gen_default=datetime.datetime.now(), *date_formats, locales=["de_DE.utf-8"]):
    def parse_date(date_value,default=gen_default):
        errors = []
        for date_format in date_formats:
            for oneLocale in locales:
                try:
                    locale.setlocale(locale.LC_ALL, oneLocale)
                    result = datetime.datetime.strptime(date_value, date_format)
                    if result.date().year == 1900 and type(default) == datetime.datetime:
                        result = result.replace(year=default.date().year)
                    return result
                except Exception as e:
                    errors.append("%s value=%r format=%r (locale=%s)" % (e,date_value,date_format,oneLocale))
                    continue
        logger.warn("All date conversions failed: %s" % '\n                  '.join(errors))
        return default
    # set name of conversion function to something more useful
    namext = ("_%s_" % gen_default) + "_".join(str(df) for df in date_formats)
    if hasattr(parse_date, "__qualname__"):
        parse_date.__qualname__ += namext
    parse_date.__name__ += namext
    return parse_date

def extract_status_date(bs, regex, input_date_format, output_date_format="%Y-%m-%d %H:%M:%S", source=None):
    status_raw = bs.findAll(text=re.compile(regex))
    return extract_status_date(status_raw, input_date_format, output_date_format, (regex,source))

def extract_status_date_directregex(text, regexmatch, input_date_format, match, output_date_format="%Y-%m-%d %H:%M:%S", source=None):
    status_raw = re.findall(regexmatch,text)
    return extract_status_date(status_raw, input_date_format, match, output_date_format, (regexmatch, source))

def extract_status_date(matches_array, input_date_format, match, output_date_format="%Y-%m-%d %H:%M:%S", source=("regex","url/file")):
    if matches_array == None or len(matches_array)<=match:
        raise ParsingError(source, 'Failed to match %r in %s')
    status_raw = matches_array[match]
    if callable(input_date_format):
        date_string = input_date_format(status_raw).strftime(output_date_format)
    else:
        locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
        date_string = datetime.datetime.strptime(status_raw, input_date_format).strftime(output_date_format)
    return check_and_replace_year(date_string)

def clear_text_of_ambigous_chars(text):
    return text.replace("\xa0", " ").replace("\r","\n")

def get_status(text,occurrence=0,default_time=datetime.datetime.now()):
    text = clear_text_of_ambigous_chars(text)
    text = remove_chars_from_text(text,["\n"," "])
    
    #print(text)

    has_hour=False
    current_find=""
    current_date=None
    date=None
    date_format=None
    for regex in date_regexes:
        # try to match against the current regex
        try:
            current_find = re.findall(regex, text,re.UNICODE)[occurrence]
            if "%H" in date_regexes.get(regex): has_hour=True
            if(current_find): 
                #if not current_find:
                #    # try dateparser
                #    # NOTE: dateparser is still not very good and requires to remove brackets etc!
                #    from dateparser.search import search_dates
                #    text = remove_chars_from_text(text,["(",")"])
                #    result = search_dates(text, languages=["de"])


                if has_hour:
                    date_format = "%Y-%m-%d %H:%M:%S"
                else:
                    date_format = "%Y-%m-%d"
                # check if there is an hour (if not, do not output any)
                current_date = datetime.datetime.strptime(current_find,date_regexes.get(regex))
                date = current_date.strftime(date_format)
                break;
        except (IndexError,ValueError) as e:
            pass

    if not date:
        raise InvalidDateException(text)
    # TODO parameterize datetime.date.today()
    if current_date.date().year == 1900:
      current_date = current_date.replace(year=default_time.date().year)
      date = current_date.strftime(date_format)
    
    return date
       
def remove_chars_from_text(text,what_to_remove):
    for entry in what_to_remove:
        text=text.replace(entry,"")
    return text

def get_number_only(text):
    return int(re.findall("[0-9]+", text)[0])

def get_table(table):
    data = []
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data


class InvalidDateException(Exception):
    def __init__(self, message, text=None):
        super().__init__(message)
        print(text)

class ParsingError(Exception):
    """Raised when a URL cannot be parsed."""

    def __init__(self, source, message='Failed to parse source: %r %r', cause=None):
        if not source:
            raise ValueError("Required argument `source' not given.")
        if (cause is None):
            param = source
        else:
            param = () + source + (cause,)
        Exception.__init__(self, str(message) % param)
        self.source = source
        self.cause = cause
