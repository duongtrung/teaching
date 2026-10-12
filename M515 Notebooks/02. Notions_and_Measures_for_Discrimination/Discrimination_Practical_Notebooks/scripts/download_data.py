"""Verify supplied research snapshots, or download missing assets at recorded versions."""
from pathlib import Path
import json, hashlib, urllib.request, argparse
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--verify-only',action='store_true')
args=parser.parse_args()
manifest=json.loads((ROOT/'data/DATA_MANIFEST.json').read_text())
for item in manifest['raw_assets']:
    path=ROOT/item['path']
    if not path.exists():
        if args.verify_only: raise FileNotFoundError(path)
        path.parent.mkdir(parents=True,exist_ok=True)
        temp=path.with_suffix(path.suffix+'.part')
        request=urllib.request.Request(item['download_url'],headers={'User-Agent':'Educational fairness audit/1.0'})
        with urllib.request.urlopen(request,timeout=90) as response:
            temp.write_bytes(response.read())
        if hashlib.sha256(temp.read_bytes()).hexdigest()!=item['sha256']:
            temp.unlink(); raise ValueError('Unexpected source bytes; review the source version before proceeding.')
        temp.replace(path)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
        raise ValueError(f'Changed raw snapshot: {path.name}. Existing data were not overwritten.')
for item in manifest['generated_assets']:
    path=ROOT/item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'], f'Changed teaching input: {path}'
print('Research snapshots and labelled generated inputs verified.')
