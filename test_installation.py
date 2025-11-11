#!/usr/bin/env python3
"""
Quick test script to verify mcp-server-skill installation and setup.
"""

import sys
from pathlib import Path
import json


def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n🔍 Checking dependencies...")

    dependencies = {
        'mcp': 'MCP SDK',
        'yaml': 'PyYAML',
        'watchdog': 'Watchdog'
    }

    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed")
            all_installed = False

    return all_installed


def check_package():
    """Check if mcp_server_skill package is available."""
    print("\n🔍 Checking mcp-server-skill package...")
    try:
        import mcp_server_skill
        print(f"✅ mcp-server-skill package found (version {mcp_server_skill.__version__})")
        return True
    except ImportError:
        print("❌ mcp-server-skill package not found")
        print("   Install with: pip install -e . (from project root)")
        return False


def check_skills_directory():
    """Check if .skill directory exists."""
    print("\n🔍 Checking .skill directory...")
    skills_dir = Path.cwd() / ".skill"

    if skills_dir.exists():
        print(f"✅ .skill directory found at {skills_dir}")

        # Count skills
        skill_count = 0
        for folder in skills_dir.iterdir():
            if folder.is_dir() and (folder / "SKILL.md").exists():
                skill_count += 1
                print(f"   📁 {folder.name}")

        if skill_count > 0:
            print(f"✅ Found {skill_count} skill(s)")
        else:
            print("⚠️  No skills found in .skill directory")
            print("   Create a skill folder with SKILL.md to get started")

        return True
    else:
        print(f"⚠️  .skill directory not found")
        print(f"   Create with: mkdir {skills_dir}")
        return False


def check_server_executable():
    """Check if server script is executable."""
    print("\n🔍 Checking server executable...")
    try:
        from mcp_server_skill.server import main
        print("✅ Server script importable")
        return True
    except ImportError as e:
        print(f"❌ Cannot import server: {e}")
        return False


def test_skill_discovery():
    """Test skill discovery functionality."""
    print("\n🔍 Testing skill discovery...")
    try:
        from mcp_server_skill.skill_loader import SkillLoader

        loader = SkillLoader()
        skills = loader.discover_skills()

        print(f"✅ Skill discovery works ({len(skills)} skill(s) found)")

        if skills:
            print("\n📋 Available skills:")
            for name, skill in skills.items():
                print(f"   • {name}: {skill.description[:60]}...")

        return True
    except Exception as e:
        print(f"❌ Skill discovery failed: {e}")
        return False


def check_mcp_config():
    """Check for MCP configuration file."""
    print("\n🔍 Checking MCP configuration...")

    # Common MCP config locations
    configs = [
        Path.cwd() / "mcp_settings.json",
        Path.home() / ".config" / "Code" / "User" / "globalStorage" / "kilocode.kilo-code" / "settings" / "mcp_settings.json",
        Path.home() / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "kilocode.kilo-code" / "settings" / "mcp_settings.json",
        Path.home() / "AppData" / "Roaming" / "Code" / "User" / "globalStorage" / "kilocode.kilo-code" / "settings" / "mcp_settings.json",
    ]

    for config_path in configs:
        if config_path.exists():
            print(f"✅ Found MCP config at {config_path}")
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    if 'mcpServers' in config and 'skill' in config['mcpServers']:
                        print("✅ skill server configured in MCP")
                    else:
                        print("⚠️  skill server not configured in MCP")
                        print("   Add configuration from mcp_settings.example.json")
            except Exception as e:
                print(f"⚠️  Could not parse config: {e}")
            return True

    print("⚠️  No MCP config found")
    print("   See MCP_CONFIG.md for setup instructions")
    return False


def print_summary(results):
    """Print test summary."""
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)

    total = len(results)
    passed = sum(results.values())

    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All checks passed! You're ready to use mcp-server-skill")
    elif passed >= total - 2:
        print("\n⚠️  Most checks passed. Review warnings above.")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")


def main():
    """Run all tests."""
    print("="*60)
    print("🧪 mcp-server-skill Installation Test")
    print("="*60)

    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Package": check_package(),
        "Skills Directory": check_skills_directory(),
        "Server Executable": check_server_executable(),
        "Skill Discovery": test_skill_discovery(),
        "MCP Configuration": check_mcp_config(),
    }

    print_summary(results)

    # Exit with appropriate code
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
