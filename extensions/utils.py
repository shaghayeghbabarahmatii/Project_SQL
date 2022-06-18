from . import jalali
from django.utils import timezone

def persian_numbers_converter(string):
	numbers = {"0": "۰","1": "۱","2": "۲","3": "۳","4": "۴","5": "۵","6": "۶","7": "۷","8": "۸","9": "۹"}
	for e, p in numbers.items():
		output = string.replace(e, p)
	return output

def jalali_converter(time):
	jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",]
	time = timezone.localtime(time)
	time_to_str = "{},{},{}".format(time.year, time.month,time.day)
	time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
	time_to_list = list(time_to_tuple)
	for index, month in enumerate(jmonths):
		if time_to_list[1] == index + 1:
			time_to_list[1] = month
			break
	output = "{} {} {}، ساعت {}:{}".format(time_to_list[2],time_to_list[1],time_to_list[0],time.hour,time.minute)
	return output
def jalali_full_converter(time):
	jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",]
	time = timezone.localtime(time)
	time_to_str = "{},{},{}".format(time.year, time.month,time.day)
	time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
	time_to_list = list(time_to_tuple)
	for index, month in enumerate(jmonths):
		if time_to_list[1] == index + 1:
			time_to_list[1] = month
			break
	output =[time_to_list[2],time_to_list[1],time_to_list[0],time.hour,time.minute]
	return output

def jalali_tuple_converter(time):
	time = timezone.localtime(time)
	time_to_str = "{},{},{}".format(time.year, time.month,time.day)
	time_to_jalali_tuple = jalali.Gregorian(time_to_str).persian_tuple()
	return time_to_jalali_tuple
def jalali_string_converter(time):
	time = timezone.localtime(time)
	time_to_str = "{}-{}-{}".format(time.year, time.month,time.day)
	time_to_jalali_string = jalali.Gregorian(time_to_str).persian_tuple()
	return time_to_jalali_string
	

#>>> jalali.Persian('1393-1-11').gregorian_string()
#'2014-3-31'
#>>> jalali.Persian(1393, 1, 11).gregorian_datetime()
#datetime.date(2014, 3, 31)
#>>> jalali.Persian('1393/1/11').gregorian_string("{}/{}/{}")
#'2014/3/31'
#>>> jalali.Persian((1393, 1, 11)).gregorian_tuple()
#(2014, 3, 31)
#
#>>> jalali.Gregorian('2014-3-31').persian_string()
#'1393-1-11'
#>>> jalali.Gregorian('2014,03,31').persian_tuple()
#(1393, 1, 11)
#>>> jalali.Gregorian(2014, 3, 31).persian_string("{0}")
#'1393'

