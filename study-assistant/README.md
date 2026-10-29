# AI Study Assistant (RAG)

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run
1. Put your PDFs / .txt / .md files in `data/`
2. Set your API key:
   - Windows (PowerShell): `$env:ANTHROPIC_API_KEY="your-key"`
   - Mac/Linux: `export ANTHROPIC_API_KEY="your-key"`
3. Index your files: `python ingest.py`
4. Launch the app: `streamlit run app.py`

Re-indexing changed files: delete the `db/` folder and rerun `ingest.py`.
