print_condition = False

def set_print_condition(value):
  global print_condition
  print_condition = value

def con_print(*args, **kwargs):
  if print_condition:
    print(*args, **kwargs)

def if_print(local_condition, *args, **kwargs):
  if local_condition:
    print(*args, **kwargs)
