
from srsgui import Task
from .dc205 import DC205


def get_dc205(task: Task, name=None) -> DC205:
    inst = task.get_instrument(name)
    
    if not issubclass(inst.__class__, DC205):
        raise TypeError('{} is not a DC205 instance'.format(name))
    return inst
