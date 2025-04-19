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
            if line and "=" in line and not line.startswith(";"):
                key, val = line.split("=", 1)
                args += ["-s", f"{key.strip()}={val.strip()}"]
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

        rel_path = stl.relative_to(input_dir).with_suffix("")
        output_subdir = output_dir / rel_path.parent
        output_subdir.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    main()
