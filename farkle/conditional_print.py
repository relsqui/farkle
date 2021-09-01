print_condition = False

def set_print_condition(value):
  global print_condition
  print_condition = value

def con_print(*args, **kwargs):
  if print_condition:
    print(*args, **kwargs)
