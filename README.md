# migrationscript

Declare the following env vars:

```bash
export SRC_PATH="${REPOS}/devportal/docs"
export DEST_PATH="${REPOS}/aiven-docs/docs/docs"
export IMG_SRC_PATH="${REPOS}/devportal/images"
export IMG_DEST_PATH="${REPOS}/aiven-docs/docs/static/images"
```

```bash
pip install -r requirements.txt

python convert.py
```

