import inspect

func = inspect.currentframe().f_code
def my_function():
    print func.co_filename

if __name__ == '__main__':
    my_function()
