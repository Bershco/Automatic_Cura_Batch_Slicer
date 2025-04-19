import subprocess
from pathlib import Path
from tqdm import tqdm

def load_cfg_as_s_args(cfg_path):
    args = []
    with open(cfg_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith(";"):
                key, val = line.split("=", 1)
                args += ["-s", f"{key.strip()}={val.strip()}"]
    return args

cura_engine = Path("cura_engine_runtime/CuraEngine.exe")
input_dir = Path("input_stl")
output_dir = Path("output_gcode")
profiles = {
    "PLA": "profiles/normal_pla_(no_supports)_printer.cfg",
    "PLA_supports": "profiles/normal_pla_(with_supports)_printer.cfg",
    "PETG": "profiles/normal_petg_(no_supports)_printer.cfg",
    "PETG_supports": "profiles/normal_petg_(with_supports)_printer.cfg"
}


output_dir.mkdir(exist_ok=True)
stl_files = list(input_dir.rglob("*.stl"))

for stl in tqdm(stl_files, desc="STL Files"):
    for label, profile in profiles.items():
        profile_path = Path(profile)
        settings = load_cfg_as_s_args(profile_path)

        rel_path = stl.relative_to(input_dir).with_suffix("")
        output_subdir = output_dir / rel_path.parent
        output_subdir.mkdir(parents=True, exist_ok=True)

        output_gcode = output_subdir / f"{rel_path.name}__{label}.gcode"
        cmd = [str(cura_engine), "slice", "-v", "-o", str(output_gcode), "-l", str(stl)] + settings
        subprocess.run(cmd)
