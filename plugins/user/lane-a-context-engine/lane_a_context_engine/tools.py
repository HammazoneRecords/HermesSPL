"""Agent-callable tools for context pin/memory management."""

import json
import uuid
from typing import Any, Dict, List

from lane_a_context_engine.store import ContextMemoryStore
from lane_a_context_engine.pin_extraction import PinType


class ContextEngineTools:
    """Tools the agent can call to manage pins, memory, and data dump."""

    def __init__(self, store: ContextMemoryStore):
        self.store = store

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return tool schemas for the agent."""
        return [
            {
                "name": "context_pin",
                "description": "Pin important information so it survives compression. "
                               "Pin types: preserve_exact, preserve_meaning, preserve_relationship, "
                               "preserve_until_resolved, never_compress_away, archive_but_retrieve.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "The information to pin."},
                        "pin_type": {
                            "type": "string",
                            "enum": [t.value for t in PinType],
                            "description": "How the information must be preserved.",
                        },
                        "reason": {"type": "string", "description": "Why this information is important."},
                    },
                    "required": ["content", "pin_type"],
                },
            },
            {
                "name": "context_unpin",
                "description": "Deactivate a pin so it no longer survives compression.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pin_id": {"type": "string", "description": "The ID of the pin to deactivate."},
                    },
                    "required": ["pin_id"],
                },
            },
            {
                "name": "context_search_memory",
                "description": "Search the memory bank for relevant entries.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query."},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "context_search_dump",
                "description": "Search the data dump for relevant archived entries.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query."},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "context_promote",
                "description": "Promote a data dump entry to the memory bank.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dump_id": {"type": "string", "description": "The ID of the dump entry to promote."},
                        "importance": {"type": "number", "description": "Importance score (0.0-1.0)."},
                    },
                    "required": ["dump_id"],
                },
            },
        ]

    def handle_tool_call(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a tool call."""
        handlers = {
            "context_pin": self._handle_pin,
            "context_unpin": self._handle_unpin,
            "context_search_memory": self._handle_search_memory,
            "context_search_dump": self._handle_search_dump,
            "context_promote": self._handle_promote,
        }
        handler = handlers.get(name)
        if handler:
            return handler(args)
        return {"error": f"Unknown context engine tool: {name}"}

    def _handle_pin(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle context_pin tool call."""
        content = args.get("content", "")
        pin_type_str = args.get("pin_type", "preserve_meaning")
        reason = args.get("reason", "Agent-pinned via tool call")

        try:
            pin_type = PinType(pin_type_str)
        except ValueError:
            return {"error": f"Invalid pin type: {pin_type_str}"}

        pin_id = f"pin_{uuid.uuid4().hex[:8]}"
        self.store.add_pin(
            pin_id=pin_id,
            content=content,
            pin_type=pin_type.value,
            reason=reason,
        )
        return {"ok": True, "pin_id": pin_id, "pin_type": pin_type.value}

    def _handle_unpin(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle context_unpin tool call."""
        pin_id = args.get("pin_id", "")
        if not pin_id:
            return {"error": "Missing pin_id"}
        self.store.unpin(pin_id)
        return {"ok": True, "pin_id": pin_id}

    def _handle_search_memory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle context_search_memory tool call."""
        query = args.get("query", "")
        if not query:
            return {"error": "Missing query"}
        results = self.store.search_memory(query)
        return {"ok": True, "results": results, "count": len(results)}

    def _handle_search_dump(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle context_search_dump tool call."""
        query = args.get("query", "")
        if not query:
            return {"error": "Missing query"}
        results = self.store.search_dump(query)
        return {"ok": True, "results": results, "count": len(results)}

    def _handle_promote(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle context_promote tool call."""
        dump_id = args.get("dump_id", "")
        importance = args.get("importance", 0.5)
        if not dump_id:
            return {"error": "Missing dump_id"}
        try:
            memory_id = self.store.promote_dump_to_memory(dump_id, importance)
            return {"ok": True, "dump_id": dump_id, "memory_id": memory_id}
        except ValueError as e:
            return {"error": str(e)}
