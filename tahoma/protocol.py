"""dfsdf
"""
import json
import requests

from tahoma.event import Event, DeviceStateChangedEvent
from tahoma.execution import Execution
from tahoma.actionGroup import ActionGroup
from tahoma.device import Device

_CONNECT_HOST = "https://www.tahomalink.com/"
_BASE_URL  = _CONNECT_HOST + "enduser-mobile-web/externalAPI/json/"
_BASE_HEADERS = { 'User-Agent' : 'mine',  }

class Protocol :
    """dsdf
    """
    def __init__(self, userName, userPassword, **kwargs ):
        """Initalize the Tahoma protocol.
        :param userName: Tahoma username
        :param userPassword: Password
        :param kwargs: Ignore, only for unit test reasons

        raises IOError in case of connection issues
        raises ValueError in case of protocol issues
        """
        self.__devices = {}
        self.__gateway = {}
        self.__location = {}
        self.__cookie = ""

        # skip conntect/login if we do special unit testing
        if 'unittest' in kwargs:
            return

        login = { 'userId' : userName, 'userPassword' : userPassword }
        header = _BASE_HEADERS.copy()

        request = requests.post( _BASE_URL + "login", data=login, headers=header )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for login, protocol error: " + request.status_code + ' - ' + request.reason + "(" + e + ")")

        if 'error' in result.keys():
            raise ValueError('Could not login: ' + result['error'])

        if request.status_code != 200:
            raise ValueError('Could not login, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        if 'success' not in result.keys() or not result['success']:
            raise ValueError('Could not login, no success')

        cookie = request.headers.get("set-cookie")
        if cookie is None:
            raise ValueError('Could not login, no cookie set')

        self.__cookie = cookie

    def getUser(self):
        """ Get the user informations from the server.
        :return: a dict with all the informations
        :rtype: dict

        raises ValueError in case of protocol issues

        :Example:

        >>> "creationTime": <time>,
        >>> "lastUpdateTime": <time>,
        >>> "userId": "<email for login>",
        >>> "title": 0,
        >>> "firstName": "<First>",
        >>> "lastName": "<Last>",
        >>> "email": "<contact email>",
        >>> "phoneNumber": "<phone>",
        >>> "mobilePhone": "<mobile>",
        >>> "locale": "<two char country code>"

        :Warning:

        The type and amount of values in the dictionary can change any time.
        """

        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "getEndUser", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not get user info, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError:
            raise ValueError("Not a valid result for getEndUser, protocol error!")

        return result['endUser']

    def getSetup(self):
        """Load the setup from the server.

        Loads the configuration from the server, nothing will be returned. After loading the configuration the devices
        can be obtained through getDevice and getDevices. Also location and gateway will be set through this
        method.

        raises ValueError in case of protocol issues

        :Seealso:

        - getDevice
        - getDevices
        - location
        - gateway
        """

        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "getSetup", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not get setup, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for getSetup, protocol error: " + e)

        self._getSetup(result)

    def _getSetup(self, result):
        """ Internal method which process the results from the server."""
        self.__devices = {}

        if 'setup' not in result.keys() or  'devices' not in result['setup'].keys():
            raise ValueError("Did not find device definition.")

        for deviceData in result['setup']['devices']:
            device = Device( self, deviceData )
            self.__devices[device.url] = device

        self.__location = result['setup']['location']
        self.__gateway = result['setup']['gateways']

    @property
    def location(self):
        """Return the location information stored in your Tahoma box.

        When the configuration has been loaded via getSetup this method retrieves all the location details which have
        been saved for your Tahoma box.

        :return: a dict with all the informations
        :rtype: dict

        :Example:

        >>> "creationTime": <time>,
        >>> "lastUpdateTime": <time>,
        >>> "addressLine1": "<street>",
        >>> "postalCode": "<zip>",
        >>> "city": "<city>",
        >>> "country": "<country>",
        >>> "timezone": "Europe/<city>",
        >>> "longitude": 2.343,
        >>> "latitude": 48.857,
        >>> "twilightMode": 2,
        >>> "twilightCity": "<city>",
        >>> "summerSolsticeDuskMinutes": 1290,
        >>> "winterSolsticeDuskMinutes": 990,
        >>> "twilightOffsetEnabled": False,
        >>> "dawnOffset": 0,
        >>> "duskOffset": 0

        :Warning:

        The type and amount of values in the dictionary can change any time.

        :Seealso:

        - getSetup
        """
        return self.__location

    @property
    def gateway(self):
        """Return information about your Tahoma box.

        When the configuration has been loaded via getSetup this method retrieves all  details your Tahoma box.

        :return: a list of all gateways with a dict per gateway with all the informations
        :rtype: list

        :Example:

        >>> [{
        >>> 	"gatewayId": "1234-1234-1234",
        >>> 	"type": 15,
        >>> 	"placeOID": "12345678-1234-1234-1234-12345678",
        >>> 	"alive": True,
        >>> 	"timeReliable": True,
        >>> 	"connectivity": {
        >>> 		"status": "OK",
        >>> 		"protocolVersion": "8"
        >>> 	},
        >>> 	"upToDate": True,
        >>> 	"functions": "INTERNET_AUTHORIZATION,SCENARIO_DOWNLOAD,SCENARIO_AUTO_LAUNCHING,SCENARIO_TELECO_LAUNCHING,INTERNET_UPLOAD,INTERNET_UPDATE,TRIGGERS_SENSORS",
        >>> 	"mode": "ACTIVE"
        >>> }]

        :Warning:

        The type and amount of values in the dictionary can change any time.

        :Seealso:

        - getSetup
        """
        return self.__gateway

    def getDevices(self):
        """Return all devices which have been found with last getSetup request.

        With a previous getSetup call the devices which have been found will be returned.

        :return: Returns a dictionary { deviceURL -> Device }
        :rtype: dict

        :Seealso:

        - getSetup
        """
        return self.__devices

    def getDevice(self, url):
        """Return a particular device which have been found with the last getSetup request.

        :param url: The device URL of the device to be returned.
        :return: Return the device identified by url or None
        :rtype: Device

        :Seealso:

        - getSetup
        """
        return self.__devices[url]

    def applyActions(self, nameOfAction, actions):
        """Start to execute an action or a group of actions.

        This method takes a bunch of actions and runs them on your Tahoma box.

        :param nameOfAction: the label/name for the action
        :param actions: an array of Action objects
        :return: the execution identifier  ************** what if it fails
        :rtype: string

        raises ValueError in case of protocol issues

        :Seealso:

        - getEvents
        - getCurrentExecutions
        """

        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        actionsSerialized = []

        for action in actions:
            actionsSerialized.append( action.serialize() )

        data = { "label": nameOfAction, "actions": actionsSerialized }
        js = json.dumps( data, indent=None, sort_keys=True )

        request = requests.post( _BASE_URL + "apply", headers=header, data=js )

        if request.status_code != 200:
            raise ValueError('Could not apply action, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for applying an action, protocol error: " + request.status_code + ' - ' + request.reason + " (" + e + ")")

        if 'execId' not in result.keys():
            raise ValueError("Could not run actions, missing execId.")

        return result['execId']

    def getEvents(self):
        """Returns a set of events which have been occured since the last call of this method.

        This method should be called regulary to get all occuring Events. There are three different Event types/classes
        which can be returned:

        - DeviceStateChangedEvent, if any device changed it's state due to an applied action or just because of other reasons
        - CommandExecutionStateChangedEvent, a executed command goes through several phases which can be followed
        - ExecutionStateChangedEvent, ******** todo

        :return: an array of Events or empty array
        :rtype: list

        raises ValueError in case of protocol issues

        :Seealso:

        - applyActions
        - launchActionGroup
        - getHistory
        """

        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.post( _BASE_URL + "getEvents", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not get events, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for getEvent, protocol error: " + e)

        return self._getEvents(result)

    def _getEvents(self, result):
        """"Internal method for being able to run unit tests."""
        events = []

        for eventData in result:
            event = Event.factory(eventData)

            if event is not None: # otherwise it is an unknown event
                events.append(event)

                if isinstance(event, DeviceStateChangedEvent):
                    # change device state
                    if self.__devices[event.deviceURL] is None:
                        raise ValueError("Received device change state for unknown device '" + event.deviceURL + "'")

                    self.__devices[event.deviceURL].setActiveStates( event.states )

        return events

    def getCurrentExecutions(self):
        """Get all current running executions.

        :return: Returns a set of running Executions or empty list.
        :rtype: list

        raises ValueError in case of protocol issues

        :Seealso:

        - applyActions
        - launchActionGroup
        - getHistory
        """

        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "getCurrentExecutions", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not get current executions, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for getCurrentExecutions, protocol error: " + e)

        if 'executions' not in result.keys():
            return None

        executions = []

        for executionData in result['executions']:
            exe = Execution(executionData)
            executions.append(exe)

        return executions

    def getHistory(self):
        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "getHistory", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not get history, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for getHistory, protocol error: " + e)

        return result['history']


    def cancelAllExecutions(self):
        """Cancels all running executions.

        raises ValueError in case of any protocol issues.
        """
        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "cancelExecutions", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not cancel executions, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

    def getActionGroups(self):
        """

        :return:
        """

        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "getActionGroups", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not get actions groups, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for getActionGroups, protocol error: " + e)

        if 'actionGroups' not in result.keys():
            return None

        groups = []

        for groupData in result['actionGroups']:
            group = ActionGroup(groupData)
            groups.append(group)

        return groups

    def launchActionGroup(self, id):
        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "launchActionGroup?oid=" + id, headers=header )

        if request.status_code != 200:
            raise ValueError('Could not launch action group, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for launch action group, protocol error: " + request.status_code + ' - ' + request.reason + " (" + e + ")")

        if 'actionGroup' not in result.keys():
            raise ValueError("Could not launch action group, missing execId.")

        return result['actionGroup'][0]['execId']

    def getStates(self, devices):
        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        js = self._createGetStateRequest(devices)

        request = requests.post( _BASE_URL + "getStates", headers=header, data=js )

        if request.status_code != 200:
            raise ValueError('Could not update states, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )

        try:
            result = request.json()
        except ValueError as e:
            raise ValueError("Not a valid result for getStates, protocol error: " + e)

        self._getStates(result)

    def _createGetStateRequest(self, givenDevices):
        devList = []

        if isinstance(givenDevices, list):
            devices = givenDevices
        else:
            devices = []
            for devName  in self.__devices.keys():
                devices.append(self.__devices[devName])

        for device in devices:
            states = []

            # keys needs to be sorted to be compatible between Python V2.x and 3.x
            for stateName in sorted(device.activeStates.keys()):
                states.append( { 'name': stateName } )

            devList.append( { 'deviceURL': device.url, 'states': states } )

        return json.dumps( devList, indent=None, sort_keys=True, separators=(',', ': ') )

    def _getStates(self, result):

        if 'devices' not in result.keys():
            return

        for deviceStates in result['devices']:
            device = self.__devices[deviceStates['deviceURL']]

            device.setActiveStates(deviceStates['states'])

    def refreshAllStates(self):
        header = _BASE_HEADERS.copy()
        header['Cookie'] = self.__cookie

        request = requests.get( _BASE_URL + "refreshAllStates", headers=header )

        if request.status_code != 200:
            raise ValueError('Could not refresh all states, HTTP code: ' + str(request.status_code) + ' - ' + request.reason )








