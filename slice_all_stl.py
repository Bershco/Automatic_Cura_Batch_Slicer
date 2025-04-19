import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import sys

def load_cfg_as_s_args(cfg_path):
    args = []
    with open(cfg_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" not in line or line.startswith(";"):
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            if val == "":
                continue
            args += ["-s", f"{key}={val}"]

    # Add safe fallback defaults if missing
    keys = {arg[3:].split("=")[0] for arg in args if arg.startswith("-s")}
    fallback_settings = {
        "mesh_rotation_matrix": "1,0,0,0,1,0,0,0,1",
        "roofing_layer_count": "1",
        "roofing_monotonic": "false",
        "acceleration_enabled": "false",
        "jerk_enabled": "false",
        "min_wall_line_width": "0.3",
    }
    for key, val in fallback_settings.items():
        if key not in keys:
            args += ["-s", f"{key}={val}"]

    return args

def find_stl_files(base_path):
    base = Path(base_path)
    return sorted(base.rglob("*.stl"))

def load_profiles(profile_folder="profiles"):
    return {
        cfg.stem: str(cfg)
        for cfg in Path(profile_folder).glob("*.cfg")
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input STL folder or file")
    parser.add_argument("-o", "--output", required=True, help="Destination folder for G-code")
    parser.add_argument("--engine", default="cura_engine_runtime/CuraEngine.exe", help="Path to CuraEngine.exe")
    parser.add_argument("--log", default="logs/slicer_log.txt", help="Log file for errors")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    log_path = Path(args.log).resolve()
    cura_engine = Path(args.engine).resolve()

    output_path.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("")  # 🔧 Always pre-create empty log

    profiles = load_profiles()
    stl_files = [input_path] if input_path.is_file() else find_stl_files(input_path)

    for stl in tqdm(stl_files, desc="Slicing STL Files", file=sys.stdout):
        relative = stl.relative_to(input_path)
        out_dir = output_path / relative.parent / stl.stem
        out_dir.mkdir(parents=True, exist_ok=True)

        for profile_name, profile_path in profiles.items():
            output_file = out_dir / f"{stl.stem}__{profile_name}.gcode"
            settings = load_cfg_as_s_args(profile_path)

            cmd = [
                str(cura_engine),
                "slice",
                "-j", "cura_engine_runtime/resources/definitions/creality_ender3v3se.def.json",
                "-o", str(output_file),
                "-l", str(stl)
            ] + settings

            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0 or not output_file.exists() or output_file.stat().st_size == 0:
                if result.stderr.strip():
                    with open(log_path, "a", encoding="utf-8") as log:
                        log.write(f"[ERROR] Failed slicing {stl.name} with profile {profile_name}\n")
                        log.write(f"Command: {' '.join(cmd)}\n")
                        log.write(result.stderr + "\n")

if __name__ == "__main__":
    main()
