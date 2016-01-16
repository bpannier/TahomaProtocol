
import json
from device import Device

class Action:

    def __init__(self, data):

        self.__commands = []

        if isinstance(data, dict):
            self.__deviceURL = data['deviceURL']

            for cmd in data['commands']:
                if 'parameters' in cmd.keys():
                    self.__commands.append( Command(cmd['name'], cmd['parameters']) )
                else:
                    self.__commands.append( Command(cmd['name'] ) )
        elif isinstance(data, str):
            self.__deviceURL = data
        else:
            self.__deviceURL = ""

    @property
    def deviceURL(self):
        return self.__deviceURL

    @deviceURL.setter
    def deviceURL(self, url):
        self.__deviceURL = url

    def addCommand(self, cmdName, *args):
        self.__commands.append(Command(cmdName,args))

    @property
    def commands(self):
        return self.__commands

    def serialize(self):
        commands = []

        for cmd in self.commands:
            commands.append( cmd.serialize() )

        out = { "commands": commands, "deviceURL": self.__deviceURL }

        return out

    def __str__(self):
        return json.dumps( self.serialize(), indent=4, sort_keys=True, separators=(',', ': ')  )

    def __repr__(self):
        return json.dumps( self.serialize(), indent=None, sort_keys=True, separators=(',', ': ')  )


class Command:

    def __init__(self, cmdName, *args):
        self.__name = cmdName

        if len(args):
            for arg in args[0]:
                if type(arg) is not str and type(arg) is not int and type(arg) is not float:
                    raise ValueError("Type '" + type(arg) + "' is not Integer, Boolean or .")

            self.__args = args[0]
        else:
            self.__args = []

    @property
    def name(self):
        return self.__name

    @property
    def parameter(self):
        return self.__args

    def serialize(self):
        return { "name": self.__name, "parameters": self.__args }

    def __str__(self):
        return json.dumps( self.serialize(), indent=4, sort_keys=True, separators=(',', ': ')  )

    def __repr__(self):
        return json.dumps( self.serialize(), indent=None, sort_keys=True, separators=(',', ': ')  )

