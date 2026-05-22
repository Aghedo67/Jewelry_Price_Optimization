# 💎 Gem · Price Intelligence
### Jewelry Market Optimization Engine — Streamlit App

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## Usage

1. **Upload** your `jewelry_orders.csv` using the sidebar uploader
2. **Overview tab** — instant EDA: price distributions, category breakdowns, time series, null map
3. **Analysis tab** — deep-dive charts: metal × gem heatmap, color/gender breakdowns, correlation matrix
4. **Model Training tab** — click ▶ TRAIN MODELS to run the full pipeline:
   - Feature engineering → mutual-info selection → preprocessing
   - Ridge · RandomForest · XGBoost · LightGBM benchmarked
   - SHAP global importance + business analyst summary table
5. **Price Predictor tab** — select product attributes and get an optimal price with market comparables

---

## Expected CSV Columns

| Column | Type | Notes |
|--------|------|-------|
| Order_Datetime | string/datetime | Parsed automatically |
| Order_ID | int | |
| Product_ID | int | |
| SKU_Quality | int | |
| Category_ID | float | nullable |
| Category | string | nullable |
| Brand_ID | float | nullable |
| Price_USD | float | **Target variable** |
| User_ID | float | nullable |
| Target_Gender | string | ~50% nullable — OK |
| Main_Color | string | nullable |
| Main_Metal | string | nullable |
| Main_Gem | string | nullable |

---

## Project Structure

```
jewelry_app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Design

Dark luxury aesthetic with Cormorant Garamond serif + DM Mono typefaces.
Gold accent (#c9a96e) throughout for a premium jewelry brand feel.
