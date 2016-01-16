

import json

class Device:

    def __init__( self, protocol, dataInput ):

        self.__protocol = protocol
        self.__rawData = dataInput

        debugOutput = json.dumps( dataInput )

        if not 'label' in dataInput.keys():
            raise ValueError('No device name found: ' + debugOutput )

        self.__label = dataInput['label']

        if not 'controllableName' in dataInput.keys():
            raise ValueError('No control label name found: ' + debugOutput )

        self.__type = dataInput['controllableName']

        if not 'deviceURL' in dataInput.keys():
            raise ValueError('No control URL: ' + debugOutput )

        self.__url = dataInput['deviceURL']

        ### Parse definitions

        if not 'definition' in dataInput.keys():
            raise ValueError('No device definition found: ' + debugOutput )

        self.__definitions = {
            'commands' : [],
            'states' : []
        }

        definition = dataInput['definition']

        if 'commands' in definition.keys():
            for command in definition['commands']:
                if command['commandName'] in self.__definitions['commands']:
                    raise ValueError("Command '" + command['commandName'] + "' double defined - " + debugOutput)

                self.__definitions['commands'].append(command['commandName'])

        if 'states' in definition.keys():
            for state in definition['states']:
                if state['qualifiedName'] in self.__definitions['states']:
                    raise ValueError("State '" + state['qualifiedName'] + "' double defined - " + debugOutput)

                self.__definitions['states'].append(state['qualifiedName'])

        ### Parse active states

        # calculate the amount of known active states
        activeStatesAmount = 0
        if 'states' in dataInput.keys():
            for state in dataInput['states']:
                activeStatesAmount += 1

        # make sure there are not more active states than definitions
        if activeStatesAmount > len(self.stateDefinitions):
            raise ValueError(
                'Missmatch of state definition and active states (' + str(len(self.stateDefinitions)) + '/' + str(
                    activeStatesAmount) + '): ' + debugOutput)

        if len(self.stateDefinitions) > 0:

            if not 'states' in dataInput.keys():
                raise ValueError("No active states given.")

            self.__activeStates = {}

            for state in dataInput['states']:

                if not state['name'] in self.stateDefinitions:
                    raise ValueError("Active state '" + state['name'] + "' has not been defined: " + debugOutput)

                if state['name'] in self.__activeStates.keys():
                    raise ValueError("Active state '" + state['name'] + "' has been double defined: " + debugOutput)

                self.__activeStates[state['name']] = state['value']

    @property
    def label(self):
        return self.__label

    @property
    def commandDefinitions(self):
        return self.__definitions['commands']

    @property
    def stateDefinitions(self):
        return self.__definitions['states']

    @property
    def activeStates(self):
        return self.__activeStates

    def setActiveState(self, name, value):
        if name not in self.__activeStates.keys():
            raise ValueError("Can not set unknown state '" + name + "'")

        if isinstance(self.__activeStates[name], int) and isinstance(value, str):
            # we get an update as str but current value is an int, try to convert
            self.__activeStates[name] = int(value)
        elif isinstance(self.__activeStates[name], float) and isinstance(value, str):
            # we get an update as str but current value is a float, try to convert
            self.__activeStates[name] = float(value)
        else:
            self.__activeStates[name] = value

    def setActiveStates(self, states):
        for state in states:
            self.setActiveState(state['name'], state['value'])

    @property
    def type(self):
        return self.__type

    @property
    def url(self):
        return self.__url

    def executeAction(self, action):
        self.__protocol




