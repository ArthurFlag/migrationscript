# Migration script

Converts the devportal to a docusaurus-based setup.

Declare the following env vars:

```bash
export SRC_DOCS_PATH="${REPOS}/devportal/docs"
export SRC_REPO_PATH="${REPOS}/devportal"
export SRC_IMG_PATH="${REPOS}/devportal/images"
export DEST_REPO_PATH="${REPOS}/aiven-docs"
```

```bash
pip install -r requirements.txt

python convert/convert.py
```

Test:

```bash
python -m unittest
```