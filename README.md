# srsinst.dc205

`srsinst.dc205` is a Python package to control the
[DC205 Voltage source](https://thinksrs.com/products/dc205.html)
from [Stanford Research Systems (SRS)](https://thinksrs.com/).

`srsinst.dc205` is based on [srsgui](https://pypi.org/project/srsgui/),
which you do not need to install separately,
but is included with this install.

## Installation
You need a working Python 3.7 or later with `pip` (Python package installer) installed.
If you don't, [install Python](https://www.python.org/) to your system.

To install `srsinst.dc2052` as an instrument driver , use Python package installer `pip` from the command line.

    python -m pip install srsinst.dc205

To use it as a GUI application, create a virtual environment,
if necessary, and install:

    python -m pip install srsinst.dc205[full]


## Run `srsinst.dc205` as GUI application
If the Python Scripts directory is in your PATH environment variable,
start the application by typing from the command line:

    dc205

If not,

    python -m srsinst.dc205

will start the GUI application.

Once running the GUI, you can:
- Connect to an DC205 from the Instruments menu.
- Select a task from the Task menu.
- Press the green arrow to run the selected task.

You can write your own task(s) or modify an existing one and run it from the GUI application, too.

## Use `srsinst.dc205` as instrument driver
* Start a Python interpreter, a Jupyter notebook, or an editor of your choice
to write a Python script.
* Import the **DC205** class from `srsinst.dc205` package.
* Create an instance of the **DC205** and establish a remote connection.

    C:\>python
    Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.

    >>> from srsinst.dc205 import DC205
    >>> vs = DC205('serial','COM7',115200)
    >>> vs.check_id()
    ('DC205', 's/n20500476', 'ver1.80')
    >>>

**DC205** is comprised of multiple **Component**s,
which provides groupings of related commands and class methods.
 The **Component** class has a convenience attribute `dir` to show  available attributes and methods in the Python dictionary format.

    >>> vs.dir.keys()
    dict_keys(['components', 'commands', 'methods'])

**DC205** has 5 components that contain remote commands and methods
as organized in the [Remote Operation chapter](https://www.thinksrs.com/downloads/pdfs/manuals/DC205m.pdf#page=47)
of the *DC205 Operating and Service Manual*.

    >>> vs.dir['components'].keys()
    dict_keys(['config', 'setting', 'scan', 'setup', 'interface', 'status'])

## Configure DC205 components
Let's set the DC205 Configuration.

    >>> vs.config.dir
    {'components': {},
     'commands': {'voltage_range': ('DictCommand', 'RNGE'),
                  'isolation': ('DictCommand', 'ISOL'),
                  'remote_sensing': ('DictCommand', 'SENS'),
                  'output': ('DictCommand', 'SOUT')},
                  'methods': ['set_range', 'enable_output', 'disable_output']}
>>>

If a command is a `DictCommand` instance, it uses mapped keys and values.
Use `get_command_info()` to find out the mapping dictionary information.

    >>> vs.config.get_command_info('voltage_range')
    {'command class': 'DictCommand',
     'raw remote command': 'RNGE',
     'set_dict': {'range1': 0, 'range10': 1},
     'get_dict': {'range1': 0, 'range10': 1, 'range100': 2},
     'index_dict': None
    }

The command `vs.config.voltage_range` encapsulates the raw command 'RNGE'
explained in the [Setion 4.4.4 of the manual](https://www.thinksrs.com/downloads/pdfs/manuals/DC205m.pdf#page=55).
The token integers (0, 1, and 2) are mapped to the strings (`'range1'`, `'range10'`, and `'range100'`)

    >>> vs.config.voltage_range
    'range1'
    >>> vs.config.voltage_range='range10'
    >>> print(vs.config.voltage_range)
    range10

You can configure other parameters in the similar way.

    >>> vs.setting.voltage
    0.0
    >>> vs.setting.voltage = 0.5
    >>> vs.setting.voltage
    0.5
    >>> vs.config.get_command_info('output')
    {'command class': 'DictCommand',
     'raw remote command': 'SOUT',
     'set_dict': {'off': 0, 'on': 1},
     'get_dict': {'off': 0, 'on': 1},
     'index_dict': None
    }
    >>> vs.config.output
    'off'
    >>> vs.config.output = 'on'
    >>> vs.config.output
    'on'



