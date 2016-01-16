import unittest

from tahoma.actionGroup import ActionGroup

class TestActionGroup(unittest.TestCase):

    def test_parse(self):
        groupData = {
            "creationTime": 1435600451200,
            "lastUpdateTime": 1435600451201,
            "label": "open all",
            "shortcut": False,
            "actions": [{
                "deviceURL": "io://1234-1234-1234/12345678",
                "commands": [{
                    "type": 1,
                    "name": "open"
                }]
            }, {
                "deviceURL": "io://1234-1234-1234/12345679",
                "commands": [{
                    "type": 1,
                    "name": "open"
                }]
            }],
            "oid": "12345678-1234-1234-1234-1234567890"
        }

        group = ActionGroup(groupData)

        self.assertEqual(group.name, "open all")
        self.assertEqual(group.lastUpdate, 1435600451201)
        self.assertEqual(len(group.actions), 2)
        self.assertEqual(group.actions[0].deviceURL, "io://1234-1234-1234/12345678")
        self.assertEqual(len(group.actions[0].commands), 1)
