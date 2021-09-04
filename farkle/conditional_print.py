import inspect

depth_tare = 0
print_condition = False
spacer = "  "

def stack_depth():
  return len(inspect.stack(0))

def tare_depth(offset=0):
  global depth_tare
  depth_tare = stack_depth() + offset

def set_print_condition(value):
  global print_condition
  print_condition = value

def con_print(*args, override=False, **kwargs):
  if print_condition or override:
    indent = stack_depth() - depth_tare
    print(spacer * indent, *args, **kwargs)

def if_print(local_condition, *args, **kwargs):
  if local_condition:
    print(*args, **kwargs)
