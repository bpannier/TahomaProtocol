
class EventState():
    # emulate Enum as we have to be compatible with Python 2.5 we can not use Class Enum from Python V3+

    def __init__(self, state):

        if isinstance(state, int):
            if state is EventState.Unknown0:
                self.__state = EventState.Unknown0
            elif state is EventState.NotTransmitted:
                self.__state = EventState.NotTransmitted
            elif state is EventState.Unknown2:
                self.__state = EventState.Unknown2
            elif state is EventState.Unknown3:
                self.__state = EventState.Unknown3
            elif state is EventState.Completed:
                self.__state = EventState.Completed
            elif state is EventState.Failed:
                self.__state = EventState.Failed
            elif state is EventState.Unknown:
                self.__state = EventState.Unknown
            else:
                raise ValueError("Unknown state init " + str(state))
        elif isinstance(state, str):
            # more states are missing
            if state is "NOT_TRANSMITTED":
                self.__state = EventState.NotTransmitted
            elif state is "COMPLETED":
                self.__state = EventState.Completed
            elif state is "FAILED":
                self.__state = EventState.Failed
            else:
                raise ValueError("Unknown state init '" + state + "'")
        else:
            raise ValueError("EventState init can only be called with int or str.")

    @property
    def state(self):
        return self.__state

    def __int__(self):
        return self.__state

    # python 2.5
    def __cmp__(self, other):
        if isinstance(other, int):
            return cmp(self.__state, other)
        if isinstance(other, EventState):
            return cmp(self.__state, other.__state)

        return -1

    # python > 3
    def __eq__(self, other):
        if isinstance(other, int):
            return self.__state == other
        if isinstance(other, EventState):
            return self.__state == other.__state

        return False

    # several names still missing
    Unknown0 = 0
    NotTransmitted = 1
    Unknown2 = 2
    Unknown3 = 3
    Completed = 4
    Failed = 5
    Unknown = 6

