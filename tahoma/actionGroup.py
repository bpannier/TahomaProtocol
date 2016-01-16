from action import Action

class ActionGroup:

    def __init__(self, data):
        self.__lastUpdate = data['lastUpdateTime']
        self.__name = data['label']

        self.__actions = []

        for cmd in data['actions']:
            self.__actions.append( Action(cmd) )

    @property
    def lastUpdate(self):
        return self.__lastUpdate

    @property
    def name(self):
        return self.__name

    @property
    def actions(self):
        return self.__actions

