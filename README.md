# Migration script

Converts the devportal to a docusaurus-based setup.

Declare the following env vars:

```bash
export SRC_PATH="${REPOS}/devportal/docs"
export DEST_PATH="${REPOS}/aiven-docs/docs/docs"
export IMG_SRC_PATH="${REPOS}/devportal/images"
export IMG_DEST_PATH="${REPOS}/aiven-docs/docs/static/images"
export REPO_PATH="${REPOS}/devportal"
```

```bash
pip install -r requirements.txt

python convert/convert.py
```

Test:

```bash
python -m unittest
```