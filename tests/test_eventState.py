import unittest

from tahoma.eventState import EventState

class TestEventState(unittest.TestCase):

    def test_IntStates(self):

        state = EventState(0)
        self.assertEqual(state.state, EventState.Unknown0)

        state = EventState(1)
        self.assertEqual(state.state, EventState.NotTransmitted)

        state = EventState(2)
        self.assertEqual(state.state, EventState.Unknown2)

        state = EventState(3)
        self.assertEqual(state.state, EventState.Unknown3)

        state = EventState(4)
        self.assertEqual(state.state, EventState.Completed)

        state = EventState(5)
        self.assertEqual(state.state, EventState.Failed)

        state = EventState(6)
        self.assertEqual(state.state, EventState.Unknown)

        self.assertRaises(ValueError, EventState, 7 )

    def test_StrState(self):

        state = EventState("NOT_TRANSMITTED")
        self.assertEqual(state.state, EventState.NotTransmitted)

        state = EventState("COMPLETED")
        self.assertEqual(state.state, EventState.Completed)

        state = EventState("FAILED")
        self.assertEqual(state.state, EventState.Failed)

        self.assertRaises(ValueError, EventState, "SOME" )

    def test_comparising(self):

        state = EventState(4)
        self.assertEqual(state.state, EventState("COMPLETED"))

        state = EventState(1)
        self.assertTrue( state == EventState("NOT_TRANSMITTED") )

        state = EventState(4)
        self.assertTrue( state != EventState("NOT_TRANSMITTED") )


