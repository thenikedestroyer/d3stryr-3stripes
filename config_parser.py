import re
from datetime import datetime


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
  """Prompt for input given a message and return that value after verifying the input.

  Keyword arguments:
  message -- the message to display when asking the user for the value
  isvalid -- a function that returns (True, error_message) if the value given by the user is valid and (False, error_message) if not.
  """
  res = None
  while res is None:
    res = input(str(message) + ': ')
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
    error_messages.append("Invalid number of arguments")
    skip_checks = True

  if not (skip_checks or ip_pattern.match(ip)):
    error_messages.append("Error: Invalid Ip")
  if not (skip_checks or port_pattern.match(port)):
    error_messages.append("Error: Invalid Port")
  if check_for_credentials and not user:
    error_messages.append("Error: User should not to be empty if you use ip:port:user:pass format")
  if check_for_credentials and not password:
    error_messages.append("Error: password should not to be empty if you use ip:port:user:pass format")
  status = error_messages == []
  return status, '\n'.join(error_messages)


def validate_regex(regex_to_match, error_message):
  def temp(str_to_match):
    status = False if not regex_to_match.match(str_to_match) else True
    return status, error_message
  return temp


def validate_required(error_mesage):
  def temp(required_val):
    status = len(required_val) != 0
    return status, error_mesage
  return temp


def prompt_for_accounts_credentials(number_of_accounts):
  accounts = []
  for i in range(number_of_accounts):
    account = Account()
    print("Enter Data for account number: %d" % (i + 1))
    account.email = prompt("==== Mail", validate_regex(email_pattern, 'Invalid Email'))
    account.password = prompt("==== Password", validate_required("Password is required"))
    account.product_id = prompt("=== Product Id", validate_required("Product Id Required"))
    account.size = prompt("=== Size", validate_required("Size is required"))
    account.notification_email = prompt("=== Product Id", validate_required("notification Email is required"))
    accounts.append(account)
  return accounts


def display_possible_datetime_formats():
  print("When should script run?")
  print("Possible formats: ")
  print("- [dd/mm/yyy hh:mm:ss]")
  print("- [hh:mm:ss]\t to run at same day")
  print("- [n hh:mm:ss]\t to run it after n days at certain time")
  print("- [n]\t to run it after n days at same time as now")


def prompt_for_datetime():
  display_possible_datetime_formats()

  return datetime


def start():
  # raw_proxy = prompt("Enter Proxy Value in format ip:port or ip:port:user:pass", validate_proxy)
  raw_number_of_accounts = prompt("Enter Number Of Accounts", lambda x: (x.isdigit(), 'Invalid number: ' + x))
  accounts = prompt_for_accounts_credentials(int(raw_number_of_accounts))
  start_date = prompt_for_datetime()

