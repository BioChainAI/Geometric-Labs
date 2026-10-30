"""Validate scaffold structure and preserved source hashes, not mathematics."""
import ast
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "scaffold_manifest.json").read_text())
    for name in manifest["modules"]:
        path = root / name
        if not path.is_file():
            raise ValueError(f"Missing module: {name}")
        if path.suffix == ".py":
            ast.parse(path.read_text(), filename=name)
    for record in manifest["sources"]:
        digest = hashlib.sha256((root / record["path"]).read_bytes()).hexdigest()
        if digest != record["sha256"]:
            raise ValueError(f"Source changed: {record['path']}")
    if manifest["status"] != "scaffold_only":
        raise ValueError("This validator cannot certify implementation status")
    print(f"Scaffold valid: {len(manifest['modules'])} planned files; 3 source hashes verified.")
    print("Algorithms, experiments, proofs and seven theorem guardrails remain OPEN.")


if __name__ == "__main__":
    main()
