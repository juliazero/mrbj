import requests
import yaml
import os

YAML_PATH = "modules/zygisk_rezygisk/track.yaml"
REPO = "PerformanC/ReZygisk"

# Pobranie aktualnej wersji z YAML
if os.path.exists(YAML_PATH):
    with open(YAML_PATH, "r") as f:
        data = yaml.safe_load(f)
else:
    data = {}

current_link = data.get("update_to", "")
current_filename = current_link.split("/")[-1] if current_link else ""

# Pobranie danych o najnowszym wydaniu z API GitHuba
api_url = f"https://api.github.com/repos/{REPO}/releases/latest"
res = requests.get(api_url)
res.raise_for_status()
release = res.json()

# Znalezienie pliku ZIP zawierającego "-release" w nazwie
latest_asset = next(
    (a for a in release["assets"] if a["name"].endswith("-release.zip")),
    None
)

if not latest_asset:
    print("❌ Nie znaleziono pliku release.zip w najnowszym wydaniu")
    exit(0)

latest_url = latest_asset["browser_download_url"]
latest_filename = latest_asset["name"]

# Porównanie z obecną wersją
if current_filename != latest_filename:
    print(f"🔄 Znaleziono nową wersję: {latest_filename}, aktualizacja YAML...")
    data["update_to"] = latest_url
    with open(YAML_PATH, "w") as f:
        yaml.dump(data, f)
else:
    print("✅ Brak aktualizacji.")
