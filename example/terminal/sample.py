from terminal import Command, red

program = Command('foo', version='1.0.0')

@program.action
def show(color=True):
    """
    show something.

    :param color: disable or enable colors
    """
    if color:
        print(red('show'))
    else:
        print('show')
