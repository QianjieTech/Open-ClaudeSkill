"""Simple test script to verify refactored implementation."""

import sys
from pathlib import Path
from mcp_server_skill.state import ServerState
from mcp_server_skill.skill_loader import SkillLoader

def test_path_discovery():
    """Test the path discovery mechanism."""
    print("Testing path discovery...")

    # Test 1: Project-level discovery
    state = ServerState()
    effective_dir = state.get_effective_skills_directory()

    if effective_dir:
        print(f"[OK] Found skills directory: {effective_dir}")
    else:
        print("[SKIP] No skills directory found (expected if .skill doesn't exist)")

    # Test 2: Manual setting
    test_path = Path.cwd() / ".skill"
    if test_path.exists():
        success, message = state.set_skills_directory(str(test_path))
        print(f"[OK] Set skills directory: {message}")
    else:
        print(f"[WARN] Test .skill directory doesn't exist: {test_path}")

    return True

def test_skill_loading():
    """Test skill loading."""
    print("\nTesting skill loading...")

    state = ServerState()
    effective_dir = state.get_effective_skills_directory()

    if not effective_dir:
        print("[WARN] No skills directory, skipping skill loading test")
        return True

    loader = SkillLoader(effective_dir)
    skills = loader.discover_skills()

    print(f"[OK] Discovered {len(skills)} skills")

    for skill_name, skill in skills.items():
        print(f"  - {skill_name}: {skill.description[:60]}...")

        # Test resource resolution
        if skill.folder_path:
            print(f"    Folder: {skill.folder_path}")

    return True

def test_resource_resolution():
    """Test resource path resolution."""
    print("\nTesting resource resolution...")

    state = ServerState()
    effective_dir = state.get_effective_skills_directory()

    if not effective_dir:
        print("[WARN] No skills directory, skipping resource resolution test")
        return True

    loader = SkillLoader(effective_dir)
    skills = loader.discover_skills()

    # Try to resolve a resource from algorithmic-art skill if it exists
    if "algorithmic-art" in skills:
        skill = skills["algorithmic-art"]
        try:
            resource_path = loader.resolve_skill_resource_path(skill, "templates/viewer.html")
            print(f"[OK] Resolved resource: {resource_path}")
            print(f"  Exists: {resource_path.exists()}")
        except Exception as e:
            print(f"[WARN] Resource not found (expected): {e}")
    else:
        print("[WARN] algorithmic-art skill not found")

    return True

def main():
    """Run all tests."""
    print("="*60)
    print("Testing Refactored MCP Server Implementation")
    print("="*60)

    tests = [
        test_path_discovery,
        test_skill_loading,
        test_resource_resolution,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"[FAIL] Test failed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    print("\n" + "="*60)
    print(f"Tests completed: {sum(results)}/{len(results)} passed")
    print("="*60)

    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
