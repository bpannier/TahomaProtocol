import unittest

from tahoma.execution import Execution
from tahoma.eventState import EventState

class TestExecution(unittest.TestCase):

    def test_parse(self):
        data = {
            "startTime": 1448329821365,
            "owner": "me@some.com",
            "actionGroup": {
                "label": "DeviceName - Action - AppDevice",
                "shortcut": False,
                "actions": [{
                    "deviceURL": "io://1234-1234-1234/12345678",
                    "commands": [{
                        "type": 1,
                        "name": "setClosure",
                        "parameters": [21]
                    }]
                }]
            },
            "id": "12345678-1234-1234-1234-1234567890",
            "executionType": "Immediate execution",
            "executionSubType": "MANUAL_CONTROL",
            "state": "NOT_TRANSMITTED"
        }

        exe = Execution(data)

        self.assertEqual(exe.startTime, 1448329821365)
        self.assertEqual(exe.id, "12345678-1234-1234-1234-1234567890")
        self.assertEqual(exe.state, EventState.NotTransmitted)
        self.assertEqual(exe.name, "DeviceName - Action - AppDevice")

        self.assertEqual(len(exe.actions), 1 )
        self.assertEqual(exe.actions[0].deviceURL, "io://1234-1234-1234/12345678")
        self.assertEqual(len(exe.actions[0].commands), 1)
        self.assertEqual(exe.actions[0].commands[0].name, "setClosure")
        self.assertEqual(len(exe.actions[0].commands[0].parameter), 1)
        self.assertEqual(exe.actions[0].commands[0].parameter[0], 21)

