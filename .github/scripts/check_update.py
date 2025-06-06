import requests
import re
import yaml

YAML_PATH = "modules/zygisk_lsposed/track.yaml"
NIGHTLY_PAGE = "https://nightly.link/JingMatrix/LSPosed/workflows/core/master"

# Load current track.yaml data
with open(YAML_PATH, "r") as f:
    data = yaml.safe_load(f)

current_link = data.get("update_to", "")
current_filename = current_link.split("/")[-1]

# Download the nightly.link HTML page
res = requests.get(NIGHTLY_PAGE)
html = res.text

# Search for the latest ZIP file link with "zygisk-release" in the name
match = re.search(r'href="(https://nightly\.link/[^"]+LSPosed-v[\d.-]+-zygisk-release\.zip)"', html)

if not match:
    print("❌ Could not find ZIP link on nightly.link page")
    exit(0)

latest_url = match.group(1)
latest_filename = latest_url.split("/")[-1]

# Compare with the current filename from track.yaml
if current_filename != latest_filename:
    print(f"🔄 New version found: {latest_filename}, updating YAML...")
    data["update_to"] = latest_url
    with open(YAML_PATH, "w") as f:
        yaml.dump(data, f)
else:
    print("✅ No update needed.")
