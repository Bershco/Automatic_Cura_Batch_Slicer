from pathlib import Path

orig_dir = Path(__file__).parent / "orig_profiles"
output_dir = Path(__file__).parent / "profiles"
output_dir.mkdir(exist_ok=True)

def extract_name_and_lines(path):
    name = path.stem
    lines = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("["):
                continue  # Skip section headers and blank lines
            if "=" in stripped:
                key, val = map(str.strip, stripped.split("=", 1))
                if key == "name":
                    name = val.lower().replace(" ", "_")
                lines.append(f"{key} = {val}")
    return name, lines

count = 0
for path in orig_dir.glob("*.inst.cfg"):
    if "_ext" not in path.stem:
        continue  # only extruder profiles
    profile_name, settings_lines = extract_name_and_lines(path)
    new_path = output_dir / f"{profile_name}.cfg"
    with new_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(settings_lines) + "\n")
    print(f"✅ Converted: {path.name} → {new_path.name}")
    count += 1

if count == 0:
    print("⚠️ No extruder profiles found in orig_profiles/")
else:
    print(f"🎉 {count} profiles converted into 'profiles/'")
