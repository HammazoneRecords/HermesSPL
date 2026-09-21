"""HermesSPL Scope Guard — context_engine plugin.

Registers a pre_tool_call hook that enforces agent scope boundaries:
- Agents may only write to their own agent-space
- Identity files (SOUL, SCOPE, MEMORY, config, state) are read-only cross-agent
- Governance files (AGENTS.md, .hermes.md) are read-only for all agents
- MEMORY_CURATOR has special write access to MEMORY.md everywhere
"""

__version__ = "1.0.0"

from hermes_plugins.context_engine import ContextEnginePlugin, register_engine


class SplScopeGuardPlugin(ContextEnginePlugin):
    """HermesSPL scope enforcement engine."""

    name = "hermes-spl-scope"
    version = "1.0.0"
    description = "Agent scope boundary enforcement"

    def __init__(self, ctx=None):
        super().__init__(ctx)
        self._guardian = None

    def initialize(self):
        """Initialize the scope guardian."""
        from hermes_spl_scope.guardian import SplScopeGuardian
        self._guardian = SplScopeGuardian()
        return True

    def on_pre_tool_call(self, tool_name: str, tool_input: dict) -> tuple:
        """Intercept write operations and validate scope.
        
        Returns: (blocked: bool, block_message: str or None, modified_input: dict or None)
        """
        if self._guardian is None:
            return False, None, None
        
        if tool_name not in ("write_file", "patch"):
            return False, None, None
        
        target = tool_input.get("path", "")
        if not target:
            return False, None, None
        
        return self._guardian.check_write(target)


def register(ctx):
    """Register the plugin with Hermes."""
    plugin = SplScopeGuardPlugin(ctx)
    register_engine(plugin)
    return plugin
