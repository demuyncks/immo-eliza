# Restructuring Plan — MachineLearning_RealEstate

---

## 1. Current File Structure

```text
MachineLearning_RealEstate/
├── main.py                                        ← CLI orchestrator (scraping pipeline)
├── README.md                                      ← almost empty (70 bytes)
├── requirements.txt                               ← global Python dependencies
├── RESTRUCTURING_PLAN.md                          ← this file
│
├── scraper/                                       ← web scraping modules
│   ├── __init__.py
│   ├── crawler.py                                 ← URL discovery (threaded)
│   ├── parser.py                                  ← HTML data extraction
│   └── cleaning.py                                ← raw CSV sanitization
│
├── utils/                                         ← shared utilities
│   ├── interface_utils.py                         ← CLI menus
│   ├── file_utils.py                              ← CSV I/O
│   └── helpers.py                                 ← text/regex helpers
│
├── data/                                          ← all data files, mixed levels
│   ├── cleaned_properties_dataset_2026-03-11-11h58.csv   ← 13,300 rows
│   ├── cleaned_properties_dataset_2026-03-12-13h12.csv   ← 13,099 rows (CANONICAL)
│   ├── final_properties_dataset.csv                      ← 13,250 rows
│   ├── immo_eliza_final_dataset_cleaned.csv               ← 13,211 rows
│   ├── properties_dataset_2026-03-11-11h27.csv            ← raw (13,300 rows)
│   ├── properties_dataset_2026-03-11-11h31.csv            ← raw (13,302 rows)
│   ├── properties_urls_2026-03-04_10h12.csv
│   ├── properties_urls_2026-03-11-11h23.csv
│   ├── lots_urls.csv
│   ├── lots_urls_full_list.csv
│   └── simon-data/                                ← personal subfolder
│       ├── properties-1-cleaned.csv
│       ├── properties-2-extrapolated.csv
│       ├── properties-2b-located.csv
│       └── provinces-zip.csv
│
├── Notebook/                                      ← orphan folder (1 file)
│   └── scraping.ipynb
│
├── notebooks/                                     ← main notebooks
│   ├── data-cleaning.ipynb
│   ├── html_scraper.ipynb
│   ├── immo-liza.ipynb
│   ├── url-scraper.ipynb
│   └── simon-notebooks/                           ← personal subfolder
│       ├── 0-final-main.ipynb                     ← CANONICAL: full pipeline (cleaning→ML)
│       ├── data-analysis-1-cleaning.ipynb         ← Phase 2a: step-by-step analysis
│       ├── data-analysis-2-extrapolation.ipynb    ← Phase 2b: step-by-step analysis
│       ├── data-analysis-2b-locations.ipynb       ← Phase 2c: step-by-step analysis
│       ├── data-analysis-3-visu-and-corr.ipynb    ← Phase 2d: step-by-step analysis
│       ├── data-cleaning-final.ipynb              ← archive (test for 0-final-main)
│       ├── input-cleaning.ipynb                   ← archive (prototype for API preprocessing)
│       ├── cleaning-final.py                      ← archive (misplaced script)
│       ├── machine-learning-cleaning.ipynb        ← archive (merged into 0-final-main)
│       ├── machine-learning-main.ipynb            ← archive (merged into 0-final-main)
│       ├── machine-learning-models.ipynb          ← archive (merged into 0-final-main)
│       ├── machine-learning-outliers.ipynb        ← archive (merged into 0-final-main)
│       ├── best_model_apartments.pkl              ← duplicate (already in deployment/)
│       ├── best_model_houses.pkl                  ← duplicate (already in deployment/)
│       ├── scaler_apartments.pkl                  ← duplicate (already in deployment/)
│       └── scaler_house.pkl                       ← duplicate (inconsistent name)
│
└── Deployment/                                    ← fullstack deployment
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── metadata.json
    ├── README.md
    ├── .env.example
    ├── .gitignore
    ├── .vscode/
    ├── .idea/
    ├── src/                                       ← React/TypeScript frontend
    │   ├── main.tsx
    │   ├── App.tsx
    │   ├── index.css
    │   └── lib/utils.ts
    └── belgi-immo-backend-master/                 ← real FastAPI backend
        ├── main.py                                ← API endpoints (/, /predict, /stats)
        ├── predictionService.py                   ← ML inference logic
        ├── PropertyData.py                        ← Pydantic models
        ├── statService.py                         ← market analytics from CSV
        ├── requirements.txt
        ├── Dockerfile
        ├── test_main.http
        ├── final_properties_dataset_*.csv         ← dataset embedded in backend (to remove)
        ├── data/
        │   └── visuals_2026-03-25-12h46.csv       ← required by /stats endpoint (keep versioned)
        ├── models/
        │   ├── best_model_apartments.pkl
        │   ├── best_model_houses.pkl
        │   ├── scaler_apartments.pkl
        │   └── scaler_houses.pkl
        ├── __pycache__/
        └── .idea/
```

---

## 2. Issues Identified

### Structural issues

| # | Issue | Impact |
| --- | ------- | -------- |
| 1 | **Two notebook folders**: `Notebook/` and `notebooks/` (different case) | Confusing, one file is isolated |
| 2 | **`simon-notebooks/`**: personal name, not suitable for a public GitHub repo | Unprofessional |
| 3 | **Duplicate `.pkl` files**: models exist in `notebooks/simon-notebooks/` AND `Deployment/belgi-immo-backend-master/models/` | Unnecessary duplication |
| 4 | **`belgi-immo-backend-master/`**: verbose nested folder name with `-master` suffix | Should be `api/` |
| 5 | **`data/` contains all levels mixed**: raw, interim, processed, reference all in one folder | Impossible to know which file to use |
| 6 | **4 nearly identical cleaned CSVs** with no indication of which is canonical | Permanent ambiguity |
| 7 | **`simon-data/`**: personal subfolder name | Not suitable for public repo |
| 8 | **`immo-eliza-env/`**: Python virtual environment tracked in the repo | Must never be versioned |
| 9 | **`README.md` at root is empty** | Project is unreadable on GitHub |
| 10 | **Dataset embedded in backend**: `final_properties_dataset_*.csv` inside `belgi-immo-backend-master/` | Data must not live inside the API folder |
| 11 | **`.idea/` folders** (JetBrains IDE) in multiple places | Should be in `.gitignore`, not committed |
| 12 | **`cleaning-final.py`** in `simon-notebooks/` | Misplaced Python script inside a notebooks folder |

### Naming inconsistencies

- `scaler_house.pkl` (in `simon-notebooks/`) vs `scaler_houses.pkl` (in backend `models/`) — inconsistent naming
- Timestamp formats vary: `2026-03-11-11h27` vs `2026-03-04_10h12` (mixed separators)

---

## 3. Proposed Structure

### Guiding principles

1. **One folder per project phase** — `scraping/`, `data/`, `notebooks/`, `deployment/`
2. **Data separated by processing level** — raw → interim → processed
3. **Models stay inside `deployment/api/models/`** — loaded by the API at runtime
4. **No spaces or personal names** in folder or file names
5. **One root README** + local READMEs where needed
6. **`.gitignore`** excludes large data files, virtualenvs, IDE folders, and secrets

---

### Target structure

```text
MachineLearning_RealEstate/
│
├── README.md                              ← full project description (to rewrite)
├── .gitignore                             ← excludes data/, real-estate-env/, .idea/, etc.
│
│ ──────────────────────────────────────────────────────────────────
│  PHASE 1 — SCRAPING
│  Entry point: python scraping/main.py
│ ──────────────────────────────────────────────────────────────────
├── scraping/
│   ├── main.py                            ← CLI orchestrator (outputs to data/raw/ and data/processed/)
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── crawler.py                     ← URL discovery (unchanged)
│   │   ├── parser.py                      ← HTML data extraction (unchanged)
│   │   └── cleaning.py                    ← raw CSV sanitization (1 path update needed)
│   └── utils/
│       ├── __init__.py
│       ├── interface_utils.py             ← CLI menus (unchanged)
│       ├── file_utils.py                  ← CSV I/O (unchanged)
│       └── helpers.py                     ← text/regex helpers (unchanged)
│
│ ──────────────────────────────────────────────────────────────────
│  PHASE 2 — DATA
│  All data/ subfolders except reference/ are gitignored
│ ──────────────────────────────────────────────────────────────────
├── data/
│   ├── raw/                               ← scraper output, never modified (gitignored)
│   │   ├── properties_dataset_*.csv       ← timestamped raw scraping output
│   │   └── properties_urls_*.csv          ← timestamped URL lists
│   │
│   ├── interim/                           ← intermediate steps (gitignored)
│   │   ├── properties-1-cleaned.csv
│   │   ├── properties-2-extrapolated.csv
│   │   └── properties-2b-located.csv
│   │
│   ├── processed/                         ← final data, ready for ML (gitignored)
│   │   └── cleaned_properties_dataset_2026-03-12-13h12.csv  ← CANONICAL DATASET
│   │
│   └── reference/                         ← static lookup tables (versioned in Git)
│       └── provinces_zip.csv              ← postal codes → provinces
│
│ ──────────────────────────────────────────────────────────────────
│  PHASE 2-3 — NOTEBOOKS
│ ──────────────────────────────────────────────────────────────────
├── notebooks/
│   ├── 01_data_analysis_cleaning.ipynb    ← step-by-step cleaning (from data-analysis-1)
│   ├── 02_data_analysis_extrapolation.ipynb← missing value imputation (from data-analysis-2)
│   ├── 03_data_analysis_locations.ipynb   ← geographic enrichment (from data-analysis-2b)
│   ├── 04_data_analysis_visualization.ipynb← EDA and correlations (from data-analysis-3)
│   ├── final_main.ipynb                   ← CANONICAL: full pipeline cleaning→ML (✅ already created)
│   └── archive/                           ← exploratory/prototype notebooks
│       ├── scraping_exploration.ipynb     ← (from Notebook/scraping.ipynb)
│       ├── html_scraper.ipynb
│       ├── url_scraper.ipynb
│       ├── immo_liza.ipynb
│       ├── data_cleaning_final.ipynb      ← test that led to 05_final_main
│       ├── input_cleaning.ipynb           ← prototype for API preprocessing logic
│       ├── machine_learning_cleaning.ipynb
│       ├── machine_learning_main.ipynb
│       ├── machine_learning_models.ipynb
│       └── machine_learning_outliers.ipynb
│
│ ──────────────────────────────────────────────────────────────────
│  PHASE 4 — DEPLOYMENT
│ ──────────────────────────────────────────────────────────────────
└── deployment/
    │
    ├── api/                               ← FastAPI backend (ex belgi-immo-backend-master)
    │   ├── main.py                        ← endpoints: /, /predict, /stats
    │   ├── prediction_service.py          ← ML inference logic (renamed from predictionService.py)
    │   ├── property_data.py               ← Pydantic input models (renamed from PropertyData.py)
    │   ├── stat_service.py                ← market analytics (renamed from statService.py)
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   ├── README.md
    │   ├── data/
    │   │   └── visuals_2026-03-25-12h46.csv  ← required for /stats — versioned in Git
    │   └── models/                        ← trained ML models (loaded at runtime)
    │       ├── best_model_apartments.pkl
    │       ├── best_model_houses.pkl
    │       ├── scaler_apartments.pkl
    │       └── scaler_houses.pkl
    │
    └── frontend/                          ← React/TypeScript app
        ├── index.html
        ├── package.json
        ├── package-lock.json
        ├── tsconfig.json
        ├── vite.config.ts
        ├── .env.example
        ├── .gitignore
        └── src/
            ├── main.tsx
            ├── App.tsx
            ├── index.css
            └── lib/
                └── utils.ts
```

---

## 4. Data versioning rules

| Folder | Track in Git? | Reason |
| -------- | --------------- | -------- |
| `data/raw/` | No (`.gitignore`) | Regenerable by running the scraper |
| `data/interim/` | No (`.gitignore`) | Reproducible from notebooks 01–04 |
| `data/processed/` | No (`.gitignore`) | Reproducible from notebooks |
| `data/reference/` | Yes | Small static file — required by `scraping/scraper/cleaning.py` |
| `deployment/api/models/` | No (`.gitignore`) | Large binaries — use Git LFS or cloud storage if sharing |
| `deployment/api/data/` | Yes | `visuals_*.csv` is required for the `/stats` endpoint to run |

> **Note on `deployment/api/data/`**: this CSV is loaded at module level in `stat_service.py`
> (`pd.read_csv(...)` at the top of the file). If gitignored, the API crashes on startup for
> anyone who clones the repo. It is a deployment artifact, not a raw data file, so it stays versioned.

---

## 5. Files to delete / archive

### Delete (redundant or misplaced)

| File | Reason |
| ------ | -------- |
| `data/cleaned_properties_dataset_2026-03-11-11h58.csv` | Duplicate — canonical is the 2026-03-12 version |
| `data/final_properties_dataset.csv` | Duplicate |
| `data/immo_eliza_final_dataset_cleaned.csv` | Duplicate |
| `data/properties_dataset_2026-03-11-11h27.csv` | Duplicate raw file |
| `data/properties_dataset_2026-03-11-11h31.csv` | Duplicate raw file |
| `data/properties_urls_2026-03-04_10h12.csv` | Old URL list |
| `data/lots_urls.csv` | Subset of `lots_urls_full_list.csv` |
| `notebooks/simon-notebooks/best_model_*.pkl` | Duplicate — canonical copies are in `deployment/api/models/` |
| `notebooks/simon-notebooks/scaler_*.pkl` | Duplicate — same reason |
| `notebooks/simon-notebooks/cleaning-final.py` | Misplaced script — logic is in `scraping/scraper/cleaning.py` |
| `Notebook/` (folder) | Merged into `notebooks/archive/` |
| All `.idea/` folders | IDE config — add to `.gitignore` |
| `deployment/belgi-immo-backend-master/final_properties_dataset_*.csv` | Data must not live inside the API folder |

### Archive (move to `notebooks/archive/`)

| File | Reason |
| ------ | -------- |
| `Notebook/scraping.ipynb` | Exploratory scraping experiment |
| `notebooks/html_scraper.ipynb` | Replaced by `scraping/scraper/parser.py` |
| `notebooks/url-scraper.ipynb` | Replaced by `scraping/scraper/crawler.py` |
| `notebooks/immo-liza.ipynb` | Unstructured working notebook |
| `notebooks/data-cleaning.ipynb` | Superseded by `01_data_analysis_cleaning.ipynb` |
| `notebooks/simon-notebooks/data-cleaning-final.ipynb` | Test that led to `05_final_main.ipynb` |
| `notebooks/simon-notebooks/input-cleaning.ipynb` | Prototype for API preprocessing — reference only |
| `notebooks/simon-notebooks/machine-learning-cleaning.ipynb` | Merged into `05_final_main.ipynb` |
| `notebooks/simon-notebooks/machine-learning-main.ipynb` | Merged into `05_final_main.ipynb` |
| `notebooks/simon-notebooks/machine-learning-models.ipynb` | Merged into `05_final_main.ipynb` |
| `notebooks/simon-notebooks/machine-learning-outliers.ipynb` | Merged into `05_final_main.ipynb` |

---

## 6. Rename summary

| Before | After | Reason |
| -------- | ------- | -------- |
| `main.py` (root) | `scraping/main.py` | All scraping code under one folder |
| `scraper/` | `scraping/scraper/` | Under `scraping/` |
| `utils/` | `scraping/utils/` | Under `scraping/` |
| `immo-eliza-env/` | `real-estate-env/` | Rename + add to `.gitignore` |
| `Deployment/` | `deployment/` | Lowercase convention |
| `Deployment/belgi-immo-backend-master/` | `deployment/api/` | Clean name, no `-master` suffix |
| `Deployment/src/` + config files | `deployment/frontend/` | Clear separation from API |
| `notebooks/simon-notebooks/0-final-main.ipynb` | `notebooks/final_main.ipynb` | Remove personal path, rename (✅ already done) |
| `notebooks/simon-notebooks/data-analysis-1-cleaning.ipynb` | `notebooks/01_data_analysis_cleaning.ipynb` | Remove personal path |
| `notebooks/simon-notebooks/data-analysis-2-extrapolation.ipynb` | `notebooks/02_data_analysis_extrapolation.ipynb` | Remove personal path |
| `notebooks/simon-notebooks/data-analysis-2b-locations.ipynb` | `notebooks/03_data_analysis_locations.ipynb` | Remove personal path |
| `notebooks/simon-notebooks/data-analysis-3-visu-and-corr.ipynb` | `notebooks/04_data_analysis_visualization.ipynb` | Remove personal path |
| `data/cleaned_properties_dataset_2026-03-12-13h12.csv` | `data/processed/cleaned_properties_dataset_2026-03-12-13h12.csv` | Correct folder, keep name |
| `data/simon-data/provinces-zip.csv` | `data/reference/provinces_zip.csv` | Remove personal path, fix naming |
| `data/simon-data/properties-*.csv` | `data/interim/properties-*.csv` | Correct folder |
| `predictionService.py` | `prediction_service.py` | Python snake_case convention |
| `PropertyData.py` | `property_data.py` | Python snake_case convention |
| `statService.py` | `stat_service.py` | Python snake_case convention |

---

## 7. Code changes required after restructuring

These are the **only** source code edits needed. Everything else is structural (move/rename).

### `scraping/main.py`

Output paths and glob patterns must point to the new `data/` subfolders:

```python
# Before
urls_list_path = f"data/properties_urls_{timestamp}.csv"
dataset_path = f"data/properties_dataset_{timestamp}.csv"
cleand_dataset_path = f"data/cleaned_properties_dataset_{timestamp}.csv"
choose_csv_file("data/properties_urls_*.csv", ...)
choose_csv_file("data/properties_dataset_*.csv", ...)

# After
urls_list_path = f"data/raw/properties_urls_{timestamp}.csv"
dataset_path = f"data/raw/properties_dataset_{timestamp}.csv"
cleand_dataset_path = f"data/processed/cleaned_properties_dataset_{timestamp}.csv"
choose_csv_file("data/raw/properties_urls_*.csv", ...)
choose_csv_file("data/raw/properties_dataset_*.csv", ...)
```

### `scraping/scraper/cleaning.py` (line 444)

Reference to the renamed province lookup file:

```python
# Before
path_prov = "./data/simon-data/provinces-zip.csv"

# After
path_prov = "./data/reference/provinces_zip.csv"
```

### `deployment/api/main.py`

Imports must reflect the snake_case file renames:

```python
# Before
from PropertyData import Property
from predictionService import get_prediction
from statService import get_stats_data

# After
from property_data import Property
from prediction_service import get_prediction
from stat_service import get_stats_data
```

---

## 8. Execution steps (in order)

1. **Update `.gitignore`** — add `data/raw/`, `data/interim/`, `data/processed/`, `deployment/api/models/`, `real-estate-env/`, `**/.idea/`, `**/__pycache__/`
2. **Rename `immo-eliza-env/`** → `real-estate-env/`
3. **Clean up `data/`** — delete duplicates, move files into `raw/`, `interim/`, `processed/`, `reference/`
4. **Delete `.pkl` duplicates** from `notebooks/simon-notebooks/`
5. **Restructure `deployment/`** — rename `belgi-immo-backend-master/` → `api/`, move frontend files into `frontend/`
6. **Rename Python files** to snake_case in `deployment/api/`
7. **Reorganize notebooks** — move and rename per the table above, create `archive/`
8. **Move scraping code** — `main.py`, `scraper/`, `utils/` into `scraping/`
9. **Apply code changes** — update 3 files per section 7 above
10. **Verify the pipeline** — run `python scraping/main.py` and test the API
11. **Rewrite root `README.md`**

---

*Updated on 2026-04-01 — pending decision on data-analysis notebooks (question 3b).*
