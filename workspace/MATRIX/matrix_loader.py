"""
MATRIX LOADER — Single import for all scripts.
Usage:
    from matrix_loader import resolve_name, get_path, get_schema
    
    # Resolve any name variant to canonical
    canonical = resolve_name("jhanosbara")  # → "JHANOS_BARA"
    
    # Get exact path for any layer
    profile_path = get_path("JHANOS_BARA", "profile")  # → Path("~/.hermes/profiles/jhanosbara")
    agent_space_path = get_path("JHANOS_BARA", "agent_space")  # → Path("ANDROMALIUS/AGENT_ARENA/ACTIVE/AGENT_JHANOS_BARA_TRIS")
    tri_path = get_path("JHANOS_BARA", "tri")  # → Path("ANDROMALIUS/TRISMIGISTUS/COMPONENTS/agents/JHANOS_BARA")
    
    # Get schema for a file category
    schema = get_schema("agent_soul")  # → {...}
    
    # Get all schemas an agent category needs
    schemas = get_agent_schemas("jhanos_gate") → ["agent_soul", "agent_scope", ...]
"""

import json
from pathlib import Path

MATRIX = Path("/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/MATRIX")
BASE = Path("/root/MW_CENTRAL")

# Load once
with open(MATRIX / "naming-authority.json") as f:
    _authority = json.load(f)
    _agents = _authority["agents"]

with open(MATRIX / "schema-registry.json") as f:
    _schemas = json.load(f)


def resolve_name(name_variant: str) -> str:
    """Resolve any name variant to canonical UPPER_SNAKE_CASE."""
    # Already canonical
    if name_variant in _agents:
        return name_variant
    
    # Strip agent-space prefix/suffix
    cleaned = name_variant.replace("AGENT_", "").replace("_TRIS", "")
    if cleaned in _agents:
        return cleaned
    
    # Normalize: remove underscores/dashes, lowercase
    norm = cleaned.replace("_", "").replace("-", "").lower()
    
    for canonical, entry in _agents.items():
        if canonical.replace("_", "").lower() == norm:
            return canonical
    
    raise ValueError(f"Cannot resolve agent name: {name_variant!r}")


def get_path(name_variant: str, layer: str) -> Path:
    """Get exact filesystem path for an agent's layer.
    
    layer: 'agent_space' | 'tri' | 'profile'
    """
    canonical = resolve_name(name_variant)
    entry = _agents[canonical]
    path_str = entry["paths"][layer]
    
    if path_str is None:
        raise ValueError(f"{canonical} has no {layer} path defined")
    
    if path_str.startswith("~/"):
        return Path.home() / path_str[2:]
    elif path_str.startswith("ANDROMALIUS/"):
        return BASE / path_str
    else:
        return Path(path_str)


def get_all_paths(name_variant: str) -> dict:
    """Get all 3 layer paths for an agent."""
    return {
        layer: get_path(name_variant, layer)
        for layer in ["agent_space", "tri", "profile"]
    }


def get_schema(schema_name: str) -> dict:
    """Get schema definition by name."""
    return _schemas["schemas"].get(schema_name)


def get_agent_schemas(category: str) -> list:
    """Get all schemas needed for an agent category."""
    return _schemas["enforcement_matrix"]["by_category"].get(category, [])


def get_category(name_variant: str) -> str:
    """Get category (jhanos_gate, core, scout) for an agent."""
    canonical = resolve_name(name_variant)
    return _agents[canonical].get("category", "uncategorized")


def list_agents(category: str = None) -> list:
    """List all agents, optionally filtered by category."""
    results = []
    for canonical, entry in _agents.items():
        if category is None or entry.get("category") == category:
            results.append(canonical)
    return sorted(results)


def validate_agent(name_variant: str) -> dict:
    """Check if an agent's files conform to their schemas."""
    canonical = resolve_name(name_variant)
    category = get_category(canonical)
    schemas = get_agent_schemas(category)
    paths = get_all_paths(canonical)
    
    report = {
        "canonical": canonical,
        "category": category,
        "layers": {},
        "issues": [],
    }
    
    for layer, path in paths.items():
        if path.exists():
            report["layers"][layer] = {"path": str(path), "exists": True}
        else:
            report["layers"][layer] = {"path": str(path), "exists": False}
            report["issues"].append(f"Missing {layer}: {path}")
    
    return report


if __name__ == "__main__":
    # Demo
    print("=== MATRIX LOADER DEMO ===")
    print(f"resolve_name('jhanosbara') = {resolve_name('jhanosbara')}")
    print(f"resolve_name('AGENT_JHANOS_BARA_TRIS') = {resolve_name('AGENT_JHANOS_BARA_TRIS')}")
    print(f"resolve_name('JHANOS_BARA') = {resolve_name('JHANOS_BARA')}")
    print(f"get_category('jhanosbara') = {get_category('jhanosbara')}")
    print(f"get_path('JHANOS_BARA', 'profile') = {get_path('JHANOS_BARA', 'profile')}")
    print(f"Agents: {list_agents()}")
    print(f"Gate agents: {list_agents('jhanos_gate')}")
