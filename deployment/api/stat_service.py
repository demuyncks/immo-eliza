import pandas as pd
import numpy as np

df = pd.read_csv('./data/visuals_2026-03-25-12h46.csv', sep = ',')
def get_stats_data():
    data = df.copy()
    
    # Groupping by cities
    stats = data.groupby('city').agg({
        'price': ['median', 'count'],
        'price_sqm': 'mean'
    })
    stats.columns = ['median_price', 'count', 'mean_price_sqm']
    
    # Small filter for relevance
    reliable = stats[stats['count'] >= 5]

    # Function to format TOP
    def format_top(source_df, col_name, is_ascending=False, suffix=""):
        top_5 = source_df.sort_values(by=col_name, ascending=is_ascending).head(5)
        result = []
        for city, row in top_5.iterrows():
            val = int(row[col_name])
            formatted_price = f"€{val:,}" + suffix
            result.append({"name": city, "price": formatted_price})
        return result

    # Market Distribution
    def get_market_dist(p_type):
        subset = data[data['type_of_property'] == p_type]['price'].dropna()
        total = len(subset)
        if total == 0: return []
        
        categories = [
            ("Budget (<300k)", subset < 300000, "#E5E7EB"),
            ("Mid-Range (300k-600k)", (subset >= 300000) & (subset < 600000), "#9CA3AF"),
            ("Premium (600k-1.2M)", (subset >= 600000) & (subset < 1200000), "#4B5563"),
            ("Luxury (>1.2M)", subset >= 1200000, "#1F2937")
        ]
        
        return [
            {"name": name, "value": round((mask.sum() / total) * 100, 1), "color": color}
            for name, mask, color in categories
        ]

    # Regional Comparison
    regional_data = []
    regions = [
        ("Brussels", "region_Brussels"),
        ("Flanders", "region_Flanders"),
        ("Wallonia", "region_Wallonia")
    ]
    
    for reg_name, reg_col in regions:
        reg_subset = data[data[reg_col] == True]
        if not reg_subset.empty:
            regional_data.append({
                "name": reg_name,
                "house": int(reg_subset[reg_subset['type_of_property'] == 'House']['price'].median() or 0),
                "apartment": int(reg_subset[reg_subset['type_of_property'] == 'Apartment']['price'].median() or 0),
                "avgM2": int(reg_subset['price_sqm'].mean() or 0)
            })

    # Final dict
    return {
        "summary": {
            "avg_price": int(data['price'].mean()),
            "transactions": len(data),
            "regions_tracked": 3
        },
        "top_expensive": {
            "total": format_top(reliable, 'median_price', is_ascending=False),
            "per_m2": format_top(reliable, 'mean_price_sqm', is_ascending=False, suffix="/m²")
        },
        "top_affordable": {
            "total": format_top(reliable, 'median_price', is_ascending=True),
            "per_m2": format_top(reliable, 'mean_price_sqm', is_ascending=True, suffix="/m²")
        },
        "regional_comparison": regional_data,
        "scatter_data": data[['living_area', 'price', 'region']].dropna().sample(min(500, len(data))).rename(
            columns={'living_area': 'area'}
        ).to_dict(orient='records'),
        "market_distribution": {
            "House": get_market_dist("House"),
            "Apartment": get_market_dist("Apartment")
        },
        "currency": "EUR"
    }
