import unittest

from tahoma.protocol import Protocol

_USER = "somfy@ka.ro"
_PW   = "ojTvLGzDpHik82"

class TestProtocol(unittest.TestCase):

    def test_getUser(self):
        tahoma = Protocol(_USER, _PW)
        user = tahoma.getUser()
        self.assertTrue( user['firstName'] != "" )

    def test_getSetup(self):
        tahoma = Protocol(_USER, _PW)
        tahoma.getSetup()
        self.assertTrue( len(tahoma.getDevices()) > 0)

    def test_getActionGroups(self):
        tahoma = Protocol(_USER, _PW)
        groups = tahoma.getActionGroups()
        self.assertTrue( len(groups) > 0)

    def test_getStates(self):
        tahoma = Protocol(_USER, _PW)
        tahoma.getSetup()
        self.assertTrue( len(tahoma.getDevices()) > 0)
        tahoma.getStates(None)
