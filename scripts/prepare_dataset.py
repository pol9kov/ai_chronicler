import pathlib, os
root = pathlib.Path(__file__).resolve().parents[1]
os.chdir(root)
#!/usr/bin/env python3
import json, pathlib, re, os, yaml
cfg  = yaml.safe_load(root.joinpath("config.yaml").read_text())
vault = pathlib.Path(cfg["vault_path"])
tag = "#Для_ИИ_помощника"
out = root / "data" / "train.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", encoding="utf-8") as f:
    for md in vault.rglob("*.md"):
        txt = md.read_text(encoding="utf-8")
        if tag in txt:
            clean = re.sub(r"\n{2,}", "\n", txt).strip()
            json.dump({"text": clean}, f, ensure_ascii=False)
            f.write("\n")
print("✔ train.jsonl создан:", out)
