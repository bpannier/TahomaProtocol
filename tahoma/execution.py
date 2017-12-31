from tahoma.action import Action
from tahoma.eventState import EventState

class Execution:

    def __init__(self, data):
        self.__id = data['id']
        self.__startTime = data['startTime']
        self.__state = EventState(data['state'])
        self.__name = data['actionGroup']['label']

        self.__actions = []

        for cmd in data['actionGroup']['actions']:
            self.__actions.append( Action(cmd) )

    @property
    def id(self):
        return self.__id

    @property
    def startTime(self):
        return self.__startTime

    @property
    def state(self):
        return self.__state

    @property
    def name(self):
        return self.__name

    @property
    def actions(self):
        return self.__actions

