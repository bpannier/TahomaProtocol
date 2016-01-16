import unittest

from tahoma.event import ExecutionStateChangedEvent, DeviceStateChangedEvent
from tahoma.protocol import Protocol

from tahoma.eventState import EventState
from test_protocol_getSetup import SetupInput

class TestProtocolGetEvents(unittest.TestCase):

    def test_multiEventsWithImplicitUpdate(self):

        eventData = [{
            "name": "ExecutionStateChangedEvent",
            "setupOID": "123456-1234-1234-1234-1234567890",
            "execId": "12345678-1234-1234-1234-123456782012",
            "newState": "4",
            "ownerKey": "1234-1234-1234",
            "type": "5",
            "subType": "-1",
            "oldState": "2"
        }, {
            "name": "DeviceStateChangedEvent",
            "setupOID": "123456-1234-1234-1234-1234567890",
            "deviceURL": "io://1234-1234-1234/12345644",
            "deviceStates": [{
                "name": "core:ClosureState",
                "value": "12"
            }, {
                "name": "core:OpenClosedState",
                "value": "open"
            }]
        }]

        tahoma = Protocol("", "", unittest=1 )
        tahoma._getSetup(SetupInput) # only for unit tests

        device = tahoma.getDevice("io://1234-1234-1234/12345644")
        self.assertEqual(device.activeStates["core:ClosureState"], 100)
        self.assertEqual(device.activeStates["core:OpenClosedState"], "closed")

        events = tahoma._getEvents(eventData)
        self.assertEqual(len(events), 2)
        self.assertTrue(isinstance(events[0], ExecutionStateChangedEvent))
        self.assertEqual(events[0].execId, "12345678-1234-1234-1234-123456782012")
        self.assertEqual(events[0].state, EventState.Completed)

        self.assertTrue(isinstance(events[1], DeviceStateChangedEvent))
        self.assertEqual(events[1].deviceURL, "io://1234-1234-1234/12345644")

        self.assertEqual(device.activeStates["core:ClosureState"], 12)
        self.assertEqual(device.activeStates["core:OpenClosedState"], "open")



