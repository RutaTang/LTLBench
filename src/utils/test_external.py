from unittest import TestCase

from src.utils.external import call_NuSMV


class Test(TestCase):
    def test_call_NuSMV_true(self):
        code = """
MODULE main
VAR
    state : {event1, event3, event2};
ASSIGN
    init(state) := event3;
    next(state) := case
        state = event1 : event3;
		state = event1 : event2;
		state = event2 : event1;
		state = event2 : event3;
		state = event3 : event3;
    esac;
LTLSPEC (G (G (state=event3 | state=event3)))
        """
        output = call_NuSMV(code)
        self.assertTrue(output)

    def test_call_NuSMV_false(self):
        code = """
MODULE main
VAR
    state : {event1, event3, event2};
ASSIGN
    init(state) := event2;
    next(state) := case
        state = event1 : event3;
                state = event1 : event2;
                state = event3 : event2;
                state = event2 : event1;
                state = event2 : event3;
    esac;
LTLSPEC state = event3
        """
        output = call_NuSMV(code)
        self.assertFalse(output)
