import unittest

from tahoma.event import Event, EventState, DeviceStateChangedEvent, CommandExecutionStateChangedEvent, ExecutionStateChangedEvent

class TestEvent(unittest.TestCase):

    def test_DeviceEvent(self):

        eventData = {
            "name": "DeviceStateChangedEvent",
            "setupOID": "12345678-1234-1234-1234-1234567890",
            "deviceURL": "io://1234-1234-1234/123456",
            "deviceStates": [{
                "name": "core:ClosureState",
                "value": "100"
            }, {
                "name": "core:OpenClosedState",
                "value": "closed"
            }]
        }

        event = Event.factory(eventData)
        self.assertTrue( isinstance(event, DeviceStateChangedEvent))
        self.assertEqual(event.deviceURL, "io://1234-1234-1234/123456")
        self.assertEqual(len(event.states), 2 )
        self.assertEqual(event.states[0]['name'], 'core:ClosureState')
        self.assertEqual(event.states[0]['value'], '100')
        self.assertEqual(event.states[1]['name'], 'core:OpenClosedState')
        self.assertEqual(event.states[1]['value'], 'closed')

    def test_CommandEvent(self):

        eventData = {
            "name": "CommandExecutionStateChangedEvent",
            "setupOID": "12345678-1234-1234-1234-1234567890",
            "execId": "12345678-1234-1234-1234-1234567800",
            "newState": "1",
            "deviceURL": "io://1234-1234-1234/123456",
            "rank": "0"
        }

        event = Event.factory(eventData)
        self.assertTrue(isinstance(event, CommandExecutionStateChangedEvent))
        self.assertEqual(event.deviceURL, "io://1234-1234-1234/123456")
        self.assertEqual(event.execId, "12345678-1234-1234-1234-1234567800")
        self.assertEqual(event.state, EventState.NotTransmitted)
        self.assertEqual(event.failureType, None)

    def test_CommandEventFailure(self):

        eventData = {
            "name": "CommandExecutionStateChangedEvent",
            "setupOID": "12345678-1234-1234-1234-1234567890",
            "execId": "12345678-1234-1234-1234-1234567800",
            "newState": "5",
            "failureType": "106",
            "deviceURL": "io://1234-1234-1234/123456",
            "rank": "0"
        }

        event = Event.factory(eventData)
        self.assertTrue(isinstance(event, CommandExecutionStateChangedEvent))
        self.assertEqual(event.deviceURL, "io://1234-1234-1234/123456")
        self.assertEqual(event.execId, "12345678-1234-1234-1234-1234567800")
        self.assertEqual(event.state, EventState.Failed)
        self.assertEqual(event.failureType, "106")

    def test_ExecutionEvent(self):

        eventData = {
            "name": "ExecutionStateChangedEvent",
            "setupOID": "12345678-1234-1234-1234-1234567890",
            "execId": "12345678-1234-1234-1234-1234567800",
            "newState": "4",
            "ownerKey": "12345678-1234-1234-1234-1234567811",
            "type": "1",
            "subType": "1",
            "oldState": "3"
        }

        event = Event.factory(eventData)
        self.assertTrue(isinstance(event, ExecutionStateChangedEvent))
        self.assertEqual(event.execId, "12345678-1234-1234-1234-1234567800")
        self.assertEqual(event.state, EventState.Completed)
        self.assertEqual(event.failureType, None)
        self.assertEqual(event.failureDeviceURL, None)

    def test_ExecutionEventFailed(self):

        eventData = {
            "name": "ExecutionStateChangedEvent",
            "setupOID": "12345678-1234-1234-1234-1234567890",
            "execId": "12345678-1234-1234-1234-1234567800",
            "newState": "5",
            "failureType": "106",
            "ownerKey": "12345678-1234-1234-1234-1234567811",
            "type": "1",
            "subType": "1",
            "oldState": "3",
            "failedCommands": {
                "command": {
                    "deviceURL": "io://1234-1234-1234/123456",
                    "failureType": "106", # Canceled
                    "rank": "0"
                }
            }
        }

        event = Event.factory(eventData)
        self.assertTrue(isinstance(event, ExecutionStateChangedEvent))
        self.assertEqual(event.execId, "12345678-1234-1234-1234-1234567800")
        self.assertEqual(event.state, EventState.Failed)
        self.assertEqual(event.failureType, "106")
        self.assertEqual(event.failureDeviceURL, "io://1234-1234-1234/123456")
