from pathlib import Path
import yaml
import sys

# Load defaults from a central config
DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
try:
    with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
        defaults = yaml.safe_load(f)
except FileNotFoundError:
    defaults = {}

# === Accept arguments ===
if len(sys.argv) != 3:
    print("Usage: python yaml_to_bat_converter.py <input_yaml_path> <output_bat_path>")
    sys.exit(1)

input_yaml = Path(sys.argv[1]).resolve()
print(f"🍠 Input YAML: {input_yaml}")
output_bat = Path(sys.argv[2]).resolve()
print(f"🦇 Output BAT: {output_bat}")

if not input_yaml.exists():
    print(f"❌ config.yaml not found at: {input_yaml}")
    sys.exit(1)

# === Load YAML content
with open(input_yaml, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# === Determine the tool to package
# Extract tool_to_ship from packaging section first, then fallback to root
packaging_config = config.get("packaging", {})
tool_to_ship = packaging_config.get("tool_to_ship")
if not tool_to_ship:
    # Fallback to root level for backwards compatibility
    tool_to_ship = config.get("tool_to_ship")

if not tool_to_ship:
    print("❌ No 'tool_to_ship' defined in config.yaml (neither in packaging section nor at root). Aborting.")
    sys.exit(1)

tool_config = config.get("tools", {}).get(tool_to_ship, {})
if not tool_config:
    print(f"❌ Tool config not found for '{tool_to_ship}' in config.yaml. Aborting.")
    sys.exit(1)

# === Extract tool-specific values
entry_command = tool_config.get("entry_command", "main.py")
packages = tool_config.get("packages", [])
tool_name = tool_config.get("tool_name", tool_to_ship)
# Extract packaging settings
embed_builder = config.get("paths", {}).get("embed_builder_path", defaults.get("embed_builder_path", ""))
open_log = str(packaging_config.get("open_log_after", defaults.get("open_log_after", True))).lower()
open_folder = str(packaging_config.get("open_folder_after", defaults.get("open_folder_after", False))).lower()

# === Extract common/shared paths
tools_dir = config.get("paths", {}).get("tools_dir", "")
common_dir = config.get("paths", {}).get("common_dir", "")

# === Extract need_urls (defaults to true)
need_urls = str(packaging_config.get("need_urls", True)).lower()

# === Create .bat lines
bat_lines = [
    ":: ================================",
    ":: 🔧 Configuration for this package",
    ":: ================================",
    "",
    ":: ================================",
    ":: 🐍 Python command to run (relative to scripts)",
    ":: ================================",
    f"set \"ENTRY_COMMAND={entry_command}\"",
    "",
    ":: ================================",
    ":: 📂 Behavior Toggles",
    ":: ================================",
    f"set \"OPEN_FOLDER_AFTER={open_folder}\"",
    f"set \"OPEN_LOG_AFTER={open_log}\"",
    f"set \"NEED_URLS={need_urls}\"",
    "",
    ":: ================================",
    ":: 📦 Tool Name",
    ":: ================================",
    f"set \"TOOL_NAME={tool_name}\"",
    f"set \"TOOLS_DIR={tools_dir}\"",
    f"set \"COMMON_DIR={common_dir}\"",
]

# === Extract tool-specific configuration and add environment variables
tool_env_vars = []
if tool_to_ship == "rhq_form_autofiller":
    # Map rhq_form_autofiller config to environment variables
    tool_env_vars.extend([
        "",
        ":: ================================",
        ":: 🔧 Tool-specific Configuration",
        ":: ================================",
    ])
    
    # Extract tool-specific settings
    url_template = tool_config.get("url_template", "")
    browser_timeout = tool_config.get("browser_timeout", 60)
    form_wait_time = tool_config.get("form_wait_time", 10)
    auto_login = str(tool_config.get("auto_login", True)).lower()
    
    tool_env_vars.extend([
        f"set \"RHQ_URL_TEMPLATE={url_template}\"",
        f"set \"RHQ_BROWSER_TIMEOUT={browser_timeout}\"",
        f"set \"RHQ_FORM_WAIT_TIME={form_wait_time}\"",
        f"set \"RHQ_AUTO_LOGIN={auto_login}\"",
    ])

# Add tool-specific environment variables to the bat lines
bat_lines.extend(tool_env_vars)

# === Write config.bat
with open(output_bat, "w", encoding="utf-8") as f:
    f.write("\n".join(bat_lines))

print(f"✅ config.bat created at: {output_bat}")
