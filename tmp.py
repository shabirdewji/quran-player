import requests

ITEM = "MishariRashidWithIbrahimWalk-SaheehIntl-English"

METADATA_URL = f"https://archive.org/metadata/{ITEM}"

print("Downloading metadata...")

data = requests.get(METADATA_URL).json()

BASE_URL = f"https://archive.org/download/{ITEM}"

surahs = []

for f in data["files"]:
    filename = f.get("name", "")

    # Keep only numbered MP3 files
    if not filename.endswith(".mp3"):
        continue

    if len(filename) < 3 or not filename[:3].isdigit():
        continue

    num = int(filename[:3])

    # Extract display name
    name = filename.replace(".mp3", "")

    if "+Surat+" in name:
        name = name.split("+Surat+", 1)[1]

    name = name.replace("+", " ")

    surahs.append({
        "id": num,
        "name": name,
        "filename": filename
    })

surahs.sort(key=lambda x: x["id"])

with open("surahs.py", "w", encoding="utf-8") as f:
    f.write('BASE_URL = "')
    f.write(BASE_URL)
    f.write('"\n\n')

    f.write("surahs = [\n")

    for s in surahs:
        f.write(
            f'    ({s["id"]}, "{s["name"]}", "{s["filename"]}"),\n'
        )

    f.write("]\n")

print(f"Created surahs.py with {len(surahs)} surahs")