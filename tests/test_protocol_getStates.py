import unittest

from tahoma.protocol import Protocol
from test_protocol_getSetup import SetupInput

class TestProtocolGetStates(unittest.TestCase):

    def test_requestBuilding(self):
        tahoma = Protocol("", "", unittest=1 )
        tahoma._getSetup(SetupInput) # only for unit tests

        light = tahoma.getDevice("hue://1234-1234-1234/123456789012/lights/1")
        window = tahoma.getDevice("io://1234-1234-1234/12345644")

        request = tahoma._createGetStateRequest( [ light, window ] )

        shouldBe = '''[{"deviceURL": "hue://1234-1234-1234/123456789012/lights/1","states": [{"name": "core:CieColorSpaceXState"},{"name": "core:CieColorSpaceYState"},{"name": "core:ColorHueState"},{"name": "core:ColorSaturationState"},{"name": "core:LightIntensityState"},{"name": "core:NameState"},{"name": "core:OnOffState"},{"name": "hue:HueColorModeState"}]},{"deviceURL": "io://1234-1234-1234/12345644","states": [{"name": "core:ClosureState"},{"name": "core:NameState"},{"name": "core:OpenClosedState"},{"name": "core:PriorityLockTimerState"}]}]'''

        self.assertEqual(request, shouldBe)

    def test_applyChanges(self):
        tahoma = Protocol("", "", unittest=1 )
        tahoma._getSetup(SetupInput) # only for unit tests

        changeData = {
	"devices": [{
		"label": "Light name",
		"deviceURL": "hue://1234-1234-1234/123456789012/lights/1",
		"shortcut": False,
		"states": [{
			"name": "core:ColorHueState",
			"type": 1,
			"value": 265
		}, {
			"name": "core:ColorSaturationState",
			"type": 1,
			"value": 44
		}, {
			"name": "core:CieColorSpaceXState",
			"type": 2,
			"value": 0.432
		}, {
			"name": "core:CieColorSpaceYState",
			"type": 2,
			"value": 0.2792
		}, {
			"name": "hue:HueColorModeState",
			"type": 3,
			"value": "hs"
		}, {
			"name": "core:NameState",
			"type": 3,
			"value": "Light name"
		}, {
			"name": "core:OnOffState",
			"type": 3,
			"value": "on"
		}, {
			"name": "core:LightIntensityState",
			"type": 1,
			"value": 20
		}],
		"available": False,
		"enabled": False,
		"type": 1
	}, {
		"label": "window2",
		"deviceURL": "io://1234-1234-1234/12345644",
		"shortcut": False,
		"states": [{
			"name": "core:NameState",
			"type": 3,
			"value": "window2"
		}, {
			"name": "core:PriorityLockTimerState",
			"type": 1,
			"value": 0
		}, {
			"name": "core:ClosureState",
			"type": 1,
			"value": 22
		}, {
			"name": "core:OpenClosedState",
			"type": 3,
			"value": "open"
		}],
		"available": False,
		"enabled": False,
		"type": 1
	}]
}

        light = tahoma.getDevice("hue://1234-1234-1234/123456789012/lights/1")
        window = tahoma.getDevice("io://1234-1234-1234/12345644")

        self.assertEqual( light.activeStates["core:CieColorSpaceXState"], 0.3505 )
        self.assertEqual( light.activeStates["core:LightIntensityState"], 0 )
        self.assertEqual( light.activeStates["core:OnOffState"], "off" )

        self.assertEqual( window.activeStates["core:ClosureState"], 100 )
        self.assertEqual( window.activeStates["core:OpenClosedState"], "closed" )

        tahoma._getStates(changeData) # only for unit tests

        self.assertEqual( light.activeStates["core:CieColorSpaceXState"], 0.432 )
        self.assertEqual( light.activeStates["core:LightIntensityState"], 20 )
        self.assertEqual( light.activeStates["core:OnOffState"], "on" )

        self.assertEqual( window.activeStates["core:ClosureState"], 22 )
        self.assertEqual( window.activeStates["core:OpenClosedState"], "open" )
