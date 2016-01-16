

from eventState import EventState

class Event:

    @staticmethod
    def factory(data):
        if data['name'] is "DeviceStateChangedEvent":
            return DeviceStateChangedEvent(data)
        elif data['name'] is "ExecutionStateChangedEvent":
            return ExecutionStateChangedEvent(data)
        elif data['name'] is "CommandExecutionStateChangedEvent":
            return CommandExecutionStateChangedEvent(data)
        else:
            raise ValueError("Unknown event '" + data['name'] + "' occurred.")


class DeviceStateChangedEvent(Event):

    def __init__(self, data):

        self.__deviceURL = data['deviceURL']
        self.__states = data['deviceStates']

    @property
    def deviceURL(self):
        return self.__deviceURL

    @property
    def states(self):
        return self.__states

class CommandExecutionStateChangedEvent(Event):
    def __init__(self, data):

        self.__execId = data['execId']
        self.__deviceURL = data['deviceURL']

        try:
            self.__state = EventState(int(data['newState']))
        except ValueError:
            self.__state = EventState.Unknown

        if self.__state == EventState.Failed:
            self.__failureType = data['failureType']
        else:
            self.__failureType = None

    @property
    def execId(self):
        return self.__execId

    @property
    def deviceURL(self):
        return self.__deviceURL

    @property
    def state(self):
        return self.__state

    @property
    def failureType(self):
        return self.__failureType

class ExecutionStateChangedEvent(Event):

    def __init__(self, data):

        self.__execId = data['execId']

        try:
            self.__state = EventState(int(data['newState']))
        except ValueError:
            self.__state = EventState.Unknown

        if self.__state == EventState.Failed:
            self.__failureType = data['failureType']
            self.__failedDeviceURL = data['failedCommands']['command']['deviceURL']
        else:
            self.__failureType = None
            self.__failedDeviceURL = None

    @property
    def execId(self):
        return self.__execId

    @property
    def state(self):
        return self.__state

    @property
    def failureType(self):
        return self.__failureType

    @property
    def failureDeviceURL(self):
        return self.__failedDeviceURL



