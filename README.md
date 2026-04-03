# Belgian Real Estate — Price Prediction

End-to-end machine learning project: scraping Belgian property listings, training price prediction models, and serving predictions through a REST API with an interactive dashboard.

---

## Overview

| Phase | Description | Stack |
|-------|-------------|-------|
| Scraping | Collect property listings from real estate website | Python, BeautifulSoup, Requests, Selenium |
| Analysis | Clean, enrich, and explore the dataset | Pandas, Matplotlib, Seaborn |
| ML | Train separate models for houses and apartments | Scikit-learn, XGBoost |
| Deployment | REST API + interactive web dashboard | FastAPI, React, TypeScript |

---

## Results

13,099 properties scraped across Belgium (3 regions, 10 provinces).

| Model | CV R² | Test R² | MAE |
|-------|:-----:|:-------:|-----|
| Houses | 0.699 | 0.671 | €83,406 |
| Apartments | 0.686 | 0.687 | €60,533 |

Models: XGBoost with Lasso-based feature selection (23 features for houses, 22 for apartments).

---

## Project Structure

```
├── scraping/          # CLI pipeline: crawl URLs → scrape listings → clean data
│   ├── main.py        # Entry point: python scraping/main.py
│   ├── scraper/       # crawler.py, parser.py, cleaning.py
│   └── utils/         # CLI, file I/O, text helpers
│
├── data/
│   ├── raw/           # Scraped output (gitignored)
│   ├── interim/       # Intermediate cleaning steps (gitignored)
│   ├── processed/     # Final dataset (gitignored)
│   └── reference/     # Static lookup tables (provinces, zip codes)
│
├── notebooks/
│   ├── 01_data_analysis_cleaning.ipynb
│   ├── 02_data_analysis_extrapolation.ipynb
│   ├── 03_data_analysis_locations.ipynb
│   ├── 04_data_analysis_visualization.ipynb
│   ├── final_main.ipynb   # Full ML pipeline: cleaning → training → export
│   └── archive/           # Exploratory notebooks
│
└── deployment/
    ├── api/           # FastAPI backend (prediction + market stats endpoints)
    └── frontend/      # React/TypeScript dashboard
```

---

## Quickstart

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the scraping pipeline

```bash
python scraping/main.py
```

Launches a CLI menu with three steps: URL discovery, data extraction, and cleaning.
Output is saved to `data/raw/` and `data/processed/`.

The pipeline transforms raw scraped listings into a clean, enriched dataset ready for modelling. Below is a sample of the data before and after processing.

**Raw output** (`data/raw/`) — 12 sample rows as scraped:

| URL | Locality | Type of property | Price | Living Area | Fully equipped kitchen | Garden | Garden area | State of the building |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| .../fleurus/vbc89133 | 6220 Fleurus | Apartment | 140000.0 | 92.0 | Super equipped | 0.0 |  | Normal |
| .../liege/vbd95203 | 4000 Liege | House | 550000.0 | 285.0 |  | 1.0 |  | Normal |
| .../rebecq/rbv33426 | 1430 Rebecq | House | 299000.0 | 123.0 |  | 0.0 |  | Normal |
| .../ciney/vbd60649 | 5590 Ciney | House | 299000.0 | 140.0 | Fully equipped | 1.0 | 584.0 | Normal |
| .../gistel/rbv33447 | 8470 Gistel | House | 419879.0 | 180.0 | Fully equipped | 1.0 |  | Excellent |
| .../vorst/vbd33441 | 1190 Vorst | House | 900000.0 | 350.0 | Fully equipped | 0.0 |  | Normal |
| .../hastiere-lavaux/vbd96170 | 5540 Hastière-Lavaux | House | 35000.0 | 40.0 |  | 1.0 |  | To be renovated |
| .../elsene/vbd86190 | 1050 Elsene | Apartment | 525000.0 | 114.0 | Super equipped | 0.0 |  | Fully renovated |
| .../ronse/rbv05692 | 9600 Ronse | Apartment | 249500.0 | 87.0 | Super equipped | 1.0 |  | New |
| .../yvoir/vbd86400 | 5530 Yvoir | Apartment | 350000.0 | 100.0 |  | 0.0 |  | New |
| .../knokke-heist/rbi29435 | 8300 Knokke-Heist | Apartment | 1625000.0 | 125.0 | Fully equipped |  |  |  |
| .../merksem/rbv43152 | 2170 Merksem | Apartment | 139000.0 | 40.0 |  | 0.0 |  | Normal |

**Processed output** (`data/processed/`) — same rows after cleaning, geocoding, and feature encoding:

| zip_code | city | province | region | type_of_property | price_sqm | price | living_area | fully_equipped_kitchen | garden | garden_area | state_of_the_building |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6220 | Fleurus | Hainaut | Wallonia | Apartment | 1522.0 | 140000 | 92.0 | 2 | False | 0.0 | 2 |
| 4000 | Liege | Liege | Wallonia | House | 1930.0 | 550000 | 285.0 | 1 | True | | 2 |
| 1430 | Rebecq | Walloon Brabant | Wallonia | House | 2431.0 | 299000 | 123.0 | 1 | False | 0.0 | 2 |
| 5590 | Ciney | Namur | Wallonia | House | 2136.0 | 299000 | 140.0 | 3 | True | 584.0 | 2 |
| 8470 | Gistel | West Flanders | Flanders | House | 2333.0 | 419879 | 180.0 | 3 | True | | 3 |
| 1190 | Vorst | Brussels | Brussels | House | 2571.0 | 900000 | 350.0 | 3 | False | 0.0 | 2 |
| 5540 | Hastière-Lavaux | Namur | Wallonia | House | 875.0 | 35000 | 40.0 | 1 | True | | 1 |
| 1050 | Elsene | Brussels | Brussels | Apartment | 4605.0 | 525000 | 114.0 | 2 | False | 0.0 | 3 |
| 9600 | Ronse | East Flanders | Flanders | Apartment | 2868.0 | 249500 | 87.0 | 2 | True | | 4 |
| 5530 | Yvoir | Namur | Wallonia | Apartment | 3500.0 | 350000 | 100.0 | 1 | False | 0.0 | 4 |
| 8300 | Knokke-Heist | West Flanders | Flanders | Apartment | 13000.0 | 1625000 | 125.0 | 3 | False | | 2 |
| 2170 | Merksem | Antwerp | Flanders | Apartment | 3475.0 | 139000 | 40.0 | 1 | False | 0.0 | 2 |

### 3. Train the models

Open and run `notebooks/final_main.ipynb`.
Uncomment the last cell to export `.pkl` files to `deployment/api/models/`.

### 4. Start the API

```bash
cd deployment/api
uvicorn main:app --reload
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/stats` | GET | Market statistics for the dashboard |
| `/predict` | POST | Price prediction from property features |

Full API doc : https://belgi-immo-backend.onrender.com/docs

### 5. Start the frontend

```bash
cd deployment/frontend
npm install
npm run dev
```

---

## Key Technical Choices

**Model selection** — We evaluated Linear Regression, Polynomial Features, Ridge, Random Forest, and XGBoost. Each candidate was tuned via GridSearchCV over a range of hyperparameters and validated with 5-fold cross-validation. XGBoost was retained as the best-performing model for both property types.

**Feature selection** — Three strategies were explored: SelectFromModel with Lasso, SelectFromModel with Random Forest, and SelectKBest (scikit-learn). The final pipeline applies a VarianceThreshold to remove near-constant features, followed by Lasso-based SelectFromModel to keep only the strongest predictors.

**Scaler fitted before selection** — The StandardScaler is applied on the full feature set before Lasso selection, then the model's subset is extracted. This matches the exact training pipeline and avoids data leakage.

**Separate models per property type** — Houses and apartments have fundamentally different feature distributions (land surface, number of facades, etc.). Training separate models improves accuracy significantly compared to a single combined model.

---

## Potential Improvements

- **Richer property data** — Integrating additional features such as proximity to public transport, schools, and local amenities, as well as neighbourhood income levels, would likely improve model accuracy meaningfully.
- **Temporal data collection** — Running the scraper on a regular schedule would grow the dataset over time and enable trend analysis (price evolution by region, seasonality effects).
- **Automated retraining** — Coupling the scheduled scraping with a retraining pipeline would keep the model up to date with market shifts.

---

## Contributors

| Name |
| ---- |
| BORISOV Andrey |
| DE MUYNCK Simon |
| HOANG Tien |
| ZGHAB Rihab |
