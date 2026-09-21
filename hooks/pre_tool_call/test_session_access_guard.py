import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from session_access_guard import enforce


class SessionAccessGuardTests(unittest.TestCase):
    def test_own_session_read_allowed(self):
        with patch.dict(os.environ, {"HERMES_PROFILE": "agent-a"}, clear=False):
            self.assertEqual(enforce("read_session", {"session_id": "s1", "session_owner": "agent-a"})["action"], "allow")

    def test_unauthorized_cross_agent_read_blocked(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"HERMES_PROFILE": "agent-a", "SESSION_ACCESS_POLICY": str(Path(d) / "policy.json")}, clear=False):
            Path(d, "policy.json").write_text("{}", encoding="utf-8")
            self.assertEqual(enforce("read_session", {"session_id": "s2", "session_owner": "agent-b"})["action"], "block")

    def test_unauthorized_cross_agent_write_blocked(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"HERMES_PROFILE": "agent-a", "SESSION_ACCESS_POLICY": str(Path(d) / "policy.json")}, clear=False):
            Path(d, "policy.json").write_text("{}", encoding="utf-8")
            self.assertEqual(enforce("write_session", {"session_id": "s2", "session_owner": "agent-b"})["action"], "block")

    def test_curator_exception_requires_policy(self):
        with tempfile.TemporaryDirectory() as d:
            policy = Path(d, "policy.json")
            policy.write_text(json.dumps({"curator_profiles": ["curator"], "curator_permissions": ["read"]}), encoding="utf-8")
            with patch.dict(os.environ, {"HERMES_PROFILE": "curator", "SESSION_ACCESS_POLICY": str(policy)}, clear=False):
                self.assertEqual(enforce("read_session", {"session_id": "s2", "session_owner": "agent-b"})["action"], "allow")
                self.assertEqual(enforce("write_session", {"session_id": "s2", "session_owner": "agent-b"})["action"], "block")

    def test_public_metadata_is_readable_without_grant(self):
        with patch.dict(os.environ, {"HERMES_PROFILE": "agent-a"}, clear=False):
            self.assertEqual(enforce("read_session", {"session_id": "s2", "session_owner": "agent-b", "access_scope": "public_metadata"})["action"], "allow")


if __name__ == "__main__":
    unittest.main()
