# 🔄 Automatic Batch Slicing with CuraEngine (CLI)

This tool automates the process of slicing `.stl` files using **CuraEngine** with multiple print profiles, generating `.gcode` files organized by folder and profile.

## 🚀 Project Goals

- ⚡ Speed up slicing workflows by batch-processing entire directories
- 📁 Preserve original folder structures in output
- 🔧 Automatically apply multiple print profiles per file
- 🧼 Logs only actual slicing errors, not verbose spam
- 🧩 Works standalone via command line (GUI may come later)

---

## 🛠 Prerequisites

- `Python 3.11+`
- A functional CuraEngine setup (DLLs and `.def.json` files included in `cura_engine_runtime`)
- STL files you wish to slice
- Cura `.inst.cfg` quality profiles (we'll convert these!) (usually found in %appdata%\cura\<version_number>\quality_changes for Windows users)

---

## 📦 First-Time Setup

1. Clone the repo:

```bash
git clone https://github.com/yourusername/auto-cura-slicer.git
cd auto-cura-slicer
```

2. Install dependencies:

```bash
pip install tqdm
```

3. Convert your Cura `.inst.cfg` profiles (see below)

---

## 🖨️ Converting Cura Profiles

Run the following to convert original Cura GUI `.inst.cfg` profiles to CLI-friendly `.cfg` format:

```bash
convert_profiles.bat
```

It pulls from the `orig_profiles/` folder and outputs standard `.cfg` files into `profiles/`.

---

## ▶️ Running the Slicer

Use the provided batch file:

```bash
run_slicer.bat
```

You will be prompted to select:

- STL input folder or file
- Output folder

---

## 📂 Output Structure

```
output/
└── some_model/
    ├── some_model__some_profile1.gcode
    ├── some_model__some_profile2.gcode
    ...
```

Each `.stl` gets its own subfolder, and each profile gets its own `.gcode`.

---

## 📋 Logs

- All slicing errors go into `logs/slicer_log_YYYY-MM-DD_HH-MM-SS.txt`
- If the file is empty after the run, everything went smoothly 🚀

---

## 🧪 Notes

- The `cura_engine_runtime/` folder includes everything needed to run CuraEngine CLI slicing
- Only tested with Cura 5.6 and Ender 3 V3 SE setup (but you can adapt)

---

## 📄 License

This project is licensed under the MIT License.
