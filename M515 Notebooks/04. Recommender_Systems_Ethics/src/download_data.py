"""Download source data locally; do not redistribute MovieLens files in a public repository."""
from pathlib import Path
import hashlib,json,urllib.request
FILES=['u.data','u.item','u.genre','u.info','u.user','u.occupation','README']
PRIMARY='https://files.grouplens.org/datasets/movielens/ml-100k/'
MIRROR='https://raw.githubusercontent.com/chiang9/Medium_blog/main/data/ml-100k/'

def download(root):
    folder=Path(root)/'data/raw/movielens-100k';folder.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for name in FILES:
        path=folder/name;origin='existing local file'
        if not path.exists():
            errors=[]
            for base in [PRIMARY,MIRROR]:
                try:
                    with urllib.request.urlopen(base+name,timeout=15)as response:data=response.read()
                    path.write_bytes(data);origin=base+name;break
                except Exception as exc:errors.append(str(exc))
            else:raise RuntimeError(f'Cannot download {name}. Download from {PRIMARY} into {folder}. Errors: {errors}')
        manifest.append({'file':name,'origin':origin,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (folder/'local_manifest.json').write_text(json.dumps(manifest,indent=2))
    print('Source files available:',folder)
    return folder

if __name__=='__main__':download(Path(__file__).resolve().parents[1])
