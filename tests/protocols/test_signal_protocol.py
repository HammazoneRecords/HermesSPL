import unittest

from protocols.signal_protocol import (
    AmbiguousStateError,
    InvalidTransitionError,
    OutputPermissionError,
    SignalProtocol,
    SignalState,
)


class SignalProtocolTests(unittest.TestCase):
    def test_valid_transitions_follow_explicit_ladder(self):
        protocol = SignalProtocol()
        self.assertEqual(protocol.state, SignalState("000"))
        receipts = [protocol.transition(state) for state in ("001", "010", "100", "111")]
        self.assertEqual([receipt["event"] for receipt in receipts], ["transition"] * 4)
        self.assertEqual(protocol.state.code, "111")
        self.assertTrue(all(receipt["accepted"] for receipt in receipts))
        self.assertEqual(receipts[-1]["from_state"], "100")
        self.assertEqual(receipts[-1]["to_state"], "111")

    def test_invalid_transition_is_rejected_without_mutation(self):
        protocol = SignalProtocol("001")
        with self.assertRaises(InvalidTransitionError):
            protocol.transition("100")
        self.assertEqual(protocol.state.code, "001")
        receipt = protocol.last_receipt
        self.assertEqual(receipt["event"], "transition_rejected")
        self.assertFalse(receipt["accepted"])

    def test_ambiguous_state_is_rejected(self):
        with self.assertRaises(AmbiguousStateError):
            SignalProtocol("01")
        with self.assertRaises(AmbiguousStateError):
            SignalProtocol("010/100")

    def test_output_permissions_are_gated_by_state(self):
        protocol = SignalProtocol("001")
        self.assertTrue(protocol.can_output("status"))
        self.assertFalse(protocol.can_output("response"))
        with self.assertRaises(OutputPermissionError):
            protocol.gate_output("response", {"text": "blocked"})
        rejected = protocol.last_receipt
        self.assertEqual(rejected["event"], "output_rejected")

        protocol.transition("010")
        self.assertTrue(protocol.can_output("diagnostic"))
        protocol.transition("100")
        self.assertTrue(protocol.can_output("response"))
        receipt = protocol.gate_output("response", {"text": "allowed"})
        self.assertEqual(receipt["event"], "output_allowed")
        self.assertEqual(receipt["payload"], {"text": "allowed"})


if __name__ == "__main__":
    unittest.main()
