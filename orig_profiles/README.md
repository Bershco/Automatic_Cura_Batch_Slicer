# 🗂️ `orig_profiles/` Folder

This folder should contain your original Cura-generated **extruder** profiles with the `.inst.cfg` extension.

### 📌 Requirements:
- Only files with `_ext` in their name will be used (i.e., extruder-specific profiles)
- The script reads the internal profile name from the `name = ...` field inside the `[general]` section of each file
- Output `.cfg` files will be placed in the sibling `profiles/` folder

### 🛠 How to Use

1. Place your `.inst.cfg` files inside this `orig_profiles/` directory.
2. Run: (exists in the parent directory)

```bash
convert_profiles.bat
```

3. The converted profiles will appear inside the `profiles/` directory with names based on the `name` key in each `.inst.cfg` file.

✅ That’s it! These are now ready to be used by the batch slicing CLI.
