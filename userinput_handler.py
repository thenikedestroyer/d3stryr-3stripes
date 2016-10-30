import re
from datetime import datetime, timedelta, date, time

ip_pattern = re.compile(r'\d{0,4}[.]\d{0,4}[.]\d{0,4}[.]\d{0,4}')
port_pattern = re.compile(r'\d{1,10}')
email_pattern = re.compile(r'(\w+[._-]*)+@(\w+[._-]*)+.(\w+[._-]*)')


class Account:
  def __init__(self, email, password, product_id, size, notification_email):
    self.email = email
    self.password = password
    self.product_id = product_id
    self.size = size
    self.notification_email = notification_email


def prompt(message, isvalid):
  '''Prompt for input given a message and return that value after verifying the input.

  Keyword arguments:
  message -- the message to display when asking the user for the value
  isvalid -- a function that returns (True, error_message) if the value given by the user is valid and (False, error_message) if not.
  '''
  res = None
  while res is None:
    res = input(str(message) + ': ').strip()
    status, error_message = isvalid(res)
    if not status:
      print(str(error_message))
      res = None
  return res


def validate_proxy(proxy_str):
  error_messages = []
  status, check_for_credentials, skip_checks = (False, False, False)
  proxy_components = proxy_str.split(':')
  ip, port, user, password = ('', '', '', '')

  if len(proxy_components) == 2:
    ip, port = proxy_components
  elif len(proxy_components) == 4:
    ip, port, user, password = proxy_components
    check_for_credentials = True
  else:
    error_messages.append('Invalid number of arguments')
    skip_checks = True

  if not (skip_checks or ip_pattern.match(ip)):
    error_messages.append('Error: Invalid Ip')
  if not (skip_checks or port_pattern.match(port)):
    error_messages.append('Error: Invalid Port')
  if check_for_credentials and not user:
    error_messages.append('Error: User should not to be empty if you use ip:port:user:pass format')
  if check_for_credentials and not password:
    error_messages.append('Error: password should not to be empty if you use ip:port:user:pass format')
  status = error_messages == []
  return status, '\n'.join(error_messages)


def validate_regex(regex_to_match, error_message):
  def temp(str_to_match):
    status = False if not regex_to_match.match(str_to_match) else True
    return status, error_message

  return temp


def validate_required(error_message):
  def temp(required_val):
    status = len(required_val) != 0
    return status, error_message

  return temp


def prompt_for_accounts_credentials(number_of_accounts):
  accounts = []
  for i in range(number_of_accounts):
    print('Enter Data for account number: %d' % (i + 1))
    email = prompt('==== Mail', validate_regex(email_pattern, 'Invalid Email'))
    password = prompt('==== Password', validate_required('Password is required'))
    product_id = prompt('=== Product Id', validate_required('Product Id Required'))
    size = prompt('=== Size', validate_required('Size is required'))
    notification_email = prompt('=== Product Id', validate_required('notification Email is required'))
    account = Account(email, password, product_id, size, notification_email)
    accounts.append(account)
  return accounts


def display_possible_datetime_formats():
  print('When should script run?')
  print('Possible formats: ')
  print('- dd-mm-yy hh:mm:ss')
  print('- hh:mm:ss\t to run at this time today')
  print('- dd-mm-yy\t to run it after n days at same time as now')


def parse_date(raw_datetime):
  day, month, year = 0, 0, 0
  date_object = None
  status = False
  if ' ' in raw_datetime:
    raw_datetime = raw_datetime.split(' ')[0]
  if '-' in raw_datetime:
    day, month, year = list(map(lambda x: int(x), raw_datetime.split('-')))
    date_object = date(year, month, day)
    status = True
  else:
    date_object = datetime.now().date()
  return date_object, status


def parse_time(raw_datetime):
  hours, minutes, seconds = 0, 0, 0
  time_object = None
  status = False
  if ' ' in raw_datetime:
    raw_datetime = raw_datetime.split(' ')[1]
  if ':' in raw_datetime:
    if raw_datetime.count(':') == 1:
      raw_datetime += ':00'
    hours, minutes, seconds = list(map(lambda x: int(x), raw_datetime.split(':')))
    time_object = time(hours, minutes, seconds)
    status = True
  else:
    time_object = datetime.now().time()
  return time_object, status


def parse_datetime_word(datetime_word):
  datetime_object = datetime.now()
  date_obj, time_obj = None, None
  date_status, time_status = True, True
  if datetime_word == 'now' or datetime_word == 'today':
    pass
  elif datetime_word == 'tomorrow':
    datetime_object += timedelta(days=1)
  else:
    date_status, time_status = False, False
  date_obj, time_obj = datetime_object.date(), datetime_object.time()
  return date_obj, date_status, time_obj, time_status



def parse_datetime(raw_datetime):
  date_obj, time_obj = None, None
  date_status, time_status = False, False
  if raw_datetime in ['now', 'tomorrow']:
    date_obj, date_status, time_obj, time_status = parse_datetime_word(raw_datetime)
  else:
    try:
      date_obj, date_status = parse_date(raw_datetime)
      time_obj, time_status = parse_time(raw_datetime)
    except Exception as e:
      print(e)
  return datetime.combine(date_obj, time_obj) if date_status or time_status else None


def validate_datetime(error_message):
  def temp(raw_datetime):
    status = False
    parsed_datetime = parse_datetime(raw_datetime)
    if parsed_datetime:
      status = True
    else:
      status = False
    return status, error_message

  return temp


def prompt_for_datetime():
  display_possible_datetime_formats()
  raw_datetime = prompt('Date Time', validate_datetime('Invalid date/time'))
  parsed_datetime = parse_datetime(raw_datetime)
  return parsed_datetime


def start():
  # raw_proxy = prompt('Enter Proxy Value in format ip:port or ip:port:user:pass', validate_proxy)
  # raw_number_of_accounts = prompt('Enter Number Of Accounts', lambda x: (x.isdigit(), 'Invalid number: ' + x))
  # accounts = prompt_for_accounts_credentials(int(raw_number_of_accounts))
  start_date = prompt_for_datetime()
