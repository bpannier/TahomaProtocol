import unittest

from tahoma.device import Device


class TestDevice(unittest.TestCase):
    def test_nolabel(self):
        deviceDefinition = {}
        self.assertRaises(ValueError, Device, None, deviceDefinition)

    def test_noDefinition(self):
        deviceDefinition = {'label': 'testDevice'}
        self.assertRaises(ValueError, Device, None, deviceDefinition)

    def test_labelEmptyDefinition(self):
        deviceDefinition = {
            'label': 'testDevice',
            "deviceURL": "io://0203-1234-1234/11111122",
            "controllableName": "io:RollerShutterVeluxIOComponent",
            'definition': {}
        }

        device = Device(None, deviceDefinition)

        self.assertEqual('testDevice', device.label)
        self.assertEqual('io://0203-1234-1234/11111122', device.url)
        self.assertEqual('io:RollerShutterVeluxIOComponent', device.type)
        self.assertEqual(len(device.commandDefinitions), 0)
        self.assertEqual(len(device.stateDefinitions), 0)

    def test_commandDefinition(self):
        deviceDefinition = {
            'label': 'testDevice',
            "deviceURL": "io://0203-1234-1234/11111122",
            "controllableName": "io:RollerShutterVeluxIOComponent",
            'definition': {
                "commands": [{
                                 "commandName": "identify",
                                 "nparams": 0,
                                 "qualifiedName": "core:IdentificationCommand"
                             }]
            }
        }

        device = Device(None, deviceDefinition)

        self.assertEqual('testDevice', device.label)
        self.assertEqual('io://0203-1234-1234/11111122', device.url)
        self.assertEqual('io:RollerShutterVeluxIOComponent', device.type)
        self.assertEqual(len(device.commandDefinitions), 1)
        self.assertEqual(len(device.stateDefinitions), 0)
        self.assertEqual(device.commandDefinitions[0], 'identify')

    def test_stateDefinition(self):
        deviceDefinition = {
            'label': 'testDevice',
            "deviceURL": "io://0203-1234-1234/11111122",
            "controllableName": "io:RollerShutterVeluxIOComponent",
            'definition': {
                "states": [{
                               "eventBased": False,
                               "values": ["off", "on"],
                               "type": "DiscreteState",
                               "qualifiedName": "core:OnOffState"
                           }]
            },
            'states': [{
                       "name": "core:OnOffState",
                       "type": 1,
                       "value": 23
                       }]
        }

        device = Device(None, deviceDefinition)

        self.assertEqual('testDevice', device.label)
        self.assertEqual('io://0203-1234-1234/11111122', device.url)
        self.assertEqual('io:RollerShutterVeluxIOComponent', device.type)
        self.assertEqual(len(device.commandDefinitions), 0)
        self.assertEqual(len(device.stateDefinitions), 1)
        self.assertEqual(device.stateDefinitions[0], 'core:OnOffState')
        self.assertEqual(device.activeStates['core:OnOffState'], 23)

    def test_missingActiveState(self):
        deviceDefinition = {
            'label': 'testDevice',
            "deviceURL": "io://0203-1234-1234/11111122",
            "controllableName": "io:RollerShutterVeluxIOComponent",
            'definition': {
                "states": [{
                               "eventBased": False,
                               "values": ["off", "on"],
                               "type": "DiscreteState",
                               "qualifiedName": "core:OnOffState"
                           }]
            }
        }

        self.assertRaises(ValueError, Device, None, deviceDefinition)

    def test_notDefinedActiveState(self):
        deviceDefinition = {
            'label': 'testDevice',
            "deviceURL": "io://0203-1234-1234/11111122",
            "controllableName": "io:RollerShutterVeluxIOComponent",
            'definition': {
                "states": [{
                               "eventBased": False,
                               "values": ["off", "on"],
                               "type": "DiscreteState",
                               "qualifiedName": "core:OnOffState"
                           }]
            },
            'states': [{
                           "name": "core:OnOffState",
                           "type": 1,
                           "value": 0
                       }, {
                           "name": "core:ClosureState",
                           "type": 1,
                           "value": 0
                       }]
        }

        self.assertRaises(ValueError, Device, None, deviceDefinition)

    def test_doubleDefinedActiveState(self):
        deviceDefinition = {
            'label': 'testDevice',
            "deviceURL": "io://0203-1234-1234/11111122",
            "controllableName": "io:RollerShutterVeluxIOComponent",
            'definition': {
                "states": [{
                               "eventBased": False,
                               "values": ["off", "on"],
                               "type": "DiscreteState",
                               "qualifiedName": "core:OnOffState"
                           },
                           {
                               "eventBased": False,
                               "values": ["open", "closed"],
                               "type": "DiscreteState",
                               "qualifiedName": "core:ClosureState"
                           }]
            },
            'states': [{
                           "name": "core:OnOffState",
                           "type": 1,
                           "value": 0
                       }, {
                           "name": "core:OnOffState",
                           "type": 1,
                           "value": 0
                       }]
        }

        self.assertRaises(ValueError, Device, None, deviceDefinition)

    def test_activeStateWithoutDefinition(self):
        deviceDefinition = {
            'label': 'testDevice',
            "deviceURL": "io://0203-1234-1234/11111122",
            "controllableName": "io:RollerShutterVeluxIOComponent",
            'definition': {

            },
            'states': [{
                           "name": "core:OnOffState",
                           "type": 1,
                           "value": 0
                       }]
        }

        self.assertRaises(ValueError, Device, None, deviceDefinition)

    def test_fullParsingSetState(self):
        deviceDefinition = {
            "creationTime": 1455691457020,
            "lastUpdateTime": 1455691457020,
            "label": "led",
            "deviceURL": "hue://1234-1234-1234/1234567890/lights/1",
            "shortcut": False,
            "controllableName": "hue:BloomHUEComponent",
            "definition": {
                "commands": [{
                    "commandName": "identify",
                    "nparams": 0,
                    "qualifiedName": "core:IdentificationCommand"
                }, {
                    "commandName": "off",
                    "nparams": 0,
                    "qualifiedName": "core:OffCommand"
                }, {
                    "commandName": "on",
                    "nparams": 0,
                    "qualifiedName": "core:OnCommand"
                }, {
                    "commandName": "onWithTimer",
                    "nparams": 1,
                    "qualifiedName": "core:OnWithTimerCommand"
                }, {
                    "commandName": "refreshState",
                    "nparams": 0,
                    "qualifiedName": "core:RefreshStateCommand"
                }, {
                    "commandName": "setCieColorSpaceXY",
                    "nparams": 2,
                    "qualifiedName": "core:SetCieColorSpaceXYCommand"
                }, {
                    "commandName": "setHSB",
                    "nparams": 3,
                    "qualifiedName": "core:SetHSBColorCommand"
                }, {
                    "commandName": "setHueAndSaturation",
                    "nparams": 2,
                    "qualifiedName": "core:SetHueAndSaturationCommand"
                }, {
                    "commandName": "setIntensity",
                    "nparams": 1,
                    "qualifiedName": "core:SetIntensityCommand"
                }, {
                    "commandName": "setIntensityWithTimer",
                    "nparams": 3,
                    "qualifiedName": "core:SetIntensityWithTimerCommand"
                }, {
                    "commandName": "setName",
                    "nparams": 1,
                    "qualifiedName": "core:SetNameCommand"
                }, {
                    "commandName": "setOnOff",
                    "nparams": 1,
                    "qualifiedName": "core:SetOnOffCommand"
                }, {
                    "commandName": "setRGB",
                    "nparams": 3,
                    "qualifiedName": "core:SetRGBColorCommand"
                }, {
                    "commandName": "setXYB",
                    "nparams": 3,
                    "qualifiedName": "core:SetXYBColorCommand"
                }],
                "states": [{
                    "eventBased": False,
                    "type": "ContinuousState",
                    "qualifiedName": "core:CieColorSpaceXState"
                }, {
                    "eventBased": False,
                    "type": "ContinuousState",
                    "qualifiedName": "core:CieColorSpaceYState"
                }, {
                    "eventBased": False,
                    "type": "ContinuousState",
                    "qualifiedName": "core:ColorHueState"
                }, {
                    "eventBased": False,
                    "type": "ContinuousState",
                    "qualifiedName": "core:ColorSaturationState"
                }, {
                    "eventBased": False,
                    "type": "ContinuousState",
                    "qualifiedName": "core:LightIntensityState"
                }, {
                    "eventBased": False,
                    "type": "DataState",
                    "qualifiedName": "core:NameState"
                }, {
                    "eventBased": False,
                    "values": ["off", "on"],
                    "type": "DiscreteState",
                    "qualifiedName": "core:OnOffState"
                }, {
                    "eventBased": False,
                    "values": ["ct", "hs", "xy"],
                    "type": "DiscreteState",
                    "qualifiedName": "hue:HueColorModeState"
                }],
                "dataProperties": [{
                    "value": "3000",
                    "qualifiedName": "core:identifyInterval"
                }],
                "widgetName": "DimmerHueSaturationLight",
                "uiClass": "Light",
                "qualifiedName": "hue:BloomHUEComponent",
                "type": "ACTUATOR"
            },
            "states": [{
                "name": "core:ColorHueState",
                "type": 1,
                "value": 242
            }, {
                "name": "core:ColorSaturationState",
                "type": 1,
                "value": 9
            }, {
                "name": "core:CieColorSpaceXState",
                "type": 2,
                "value": 0.409
            }, {
                "name": "core:CieColorSpaceYState",
                "type": 2,
                "value": 0.379
            }, {
                "name": "hue:HueColorModeState",
                "type": 3,
                "value": "hs"
            }, {
                "name": "core:NameState",
                "type": 3,
                "value": "led"
            }, {
                "name": "core:OnOffState",
                "type": 3,
                "value": "off"
            }, {
                "name": "core:LightIntensityState",
                "type": 1,
                "value": 0
            }],
            "attributes": [{
                "name": "core:LampType",
                "type": 3,
                "value": "bloom"
            }],
            "available": True,
            "enabled": True,
            "placeOID": "12345678-1234-1234-1234-12345678",
            "widget": "DimmerHueSaturationLight",
            "type": 1,
            "oid": "12345678-1234-1234-1234-1234567890",
            "uiClass": "Light"
        }

        device = Device(None, deviceDefinition)
        self.assertEqual(device.label, "led")
        self.assertEqual(device.type, "hue:BloomHUEComponent")
        self.assertEqual(device.url, "hue://1234-1234-1234/1234567890/lights/1")
        self.assertEqual(len(device.commandDefinitions), 14)
        self.assertEqual(len(device.stateDefinitions), 8)
        self.assertEqual(len(device.activeStates), 8)
        self.assertEqual(device.activeStates["core:ColorHueState"], 242)
        self.assertEqual(device.activeStates["core:ColorSaturationState"], 9)
        self.assertEqual(device.activeStates["core:CieColorSpaceXState"], 0.409)
        self.assertEqual(device.activeStates["core:CieColorSpaceYState"], 0.379)
        self.assertEqual(device.activeStates["hue:HueColorModeState"], "hs")
        self.assertEqual(device.activeStates["core:NameState"], "led")
        self.assertEqual(device.activeStates["core:OnOffState"], "off")
        self.assertEqual(device.activeStates["core:LightIntensityState"], 0)

        updateData = [{
            "name": "core:ColorHueState",
            "type": 1,
            "value": 123
        }, {
            "name": "core:ColorSaturationState",
            "type": 1,
            "value": 456
        }, {
            "name": "core:CieColorSpaceXState",
            "type": 2,
            "value": 0.123
        }, {
            "name": "core:CieColorSpaceYState",
            "type": 2,
            "value": 0.456
        }, {
            "name": "hue:HueColorModeState",
            "type": 3,
            "value": "hsa"
        }, {
            "name": "core:NameState",
            "type": 3,
            "value": "led2"
        }, {
            "name": "core:OnOffState",
            "type": 3,
            "value": "off2"
        }, {
            "name": "core:LightIntensityState",
            "type": 1,
            "value": 222
        }]

        device.setActiveStates(updateData)
        self.assertEqual(device.activeStates["core:ColorHueState"], 123)
        self.assertEqual(device.activeStates["core:ColorSaturationState"], 456)
        self.assertEqual(device.activeStates["core:CieColorSpaceXState"], 0.123)
        self.assertEqual(device.activeStates["core:CieColorSpaceYState"], 0.456)
        self.assertEqual(device.activeStates["hue:HueColorModeState"], "hsa")
        self.assertEqual(device.activeStates["core:NameState"], "led2")
        self.assertEqual(device.activeStates["core:OnOffState"], "off2")
        self.assertEqual(device.activeStates["core:LightIntensityState"], 222)

