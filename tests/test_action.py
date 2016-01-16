import unittest

from tahoma.action import Action

class TestAction(unittest.TestCase):

    def test_empty(self):
        act = Action(None)
        self.assertEqual("", act.deviceURL)
        self.assertEqual(0, len(act.commands))

    def test_deviceURL(self):
        act = Action("tst")
        self.assertEqual('tst', act.deviceURL)
        self.assertEqual(0, len(act.commands))

    def test_buildOneCommand(self):
        act = Action("dev")
        act.addCommand("cmd1")
        self.assertEqual(1, len(act.commands))
        self.assertEqual('cmd1', act.commands[0].name)

    def test_buildOneCommandWithArgument(self):
        act = Action("dev")
        act.addCommand("cmd2", "arg1", 2, "arg3")

        self.assertEqual(1, len(act.commands))
        self.assertEqual('cmd2', act.commands[0].name)

        args = act.commands[0].parameter
        self.assertEqual(3, len(args))
        self.assertEqual("arg1", args[0])
        self.assertEqual(2, args[1])
        self.assertEqual("arg3", args[2])

        actStr = str(act)
        self.assertEqual( actStr, '''{
    "commands": [
        {
            "name": "cmd2",
            "parameters": [
                "arg1",
                2,
                "arg3"
            ]
        }
    ],
    "deviceURL": "dev"
}''')

    def test_parseCommand(self):
        actionData = {
            "commands": [
                {
                    "name": "setClosure",
                    "parameters": [
                        26
                    ]
                },
                {
                    "name": "open",
                    "parameters": []
                }
            ],
            "deviceURL": "io://1234-1234-1234/12345678"
        }


        act = Action(actionData)

        self.assertEqual(act.deviceURL, "io://1234-1234-1234/12345678")
        self.assertEqual(len(act.commands), 2)

        self.assertEqual("setClosure", act.commands[0].name)
        args = act.commands[0].parameter
        self.assertEqual(1, len(args))
        self.assertEqual(26, args[0])

        self.assertEqual("open", act.commands[1].name)
        args = act.commands[1].parameter
        self.assertEqual(0, len(args))

    def test_parseNoParameter(self):

        actionData = {
            "deviceURL": "io://1234-1234-1234/12345678",
            "commands": [{
                "type": 1,
                "name": "open"
            }]
        }

        act = Action(actionData)

        self.assertEqual(act.deviceURL, "io://1234-1234-1234/12345678")
        self.assertEqual(len(act.commands), 1)

        self.assertEqual("open", act.commands[0].name)
        self.assertEqual(0, len(act.commands[0].parameter))
