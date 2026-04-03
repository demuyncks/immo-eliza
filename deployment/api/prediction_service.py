import os

import joblib
import pandas as pd


def get_prediction(data):
    property_type = data.type_of_property
    df = preprocess_data(data, property_type)

    model = load_model(property_type)

    if model:
        prediction = model.predict(df)[0]
    else:
        # Fallback if model file is missing
        prediction = 250000.0 + (data.living_area * 2500)

    return prediction


def preprocess_data(data, property_type):
    # 1. Convert Pydantic model to dictionary and apply ordinal mappings
    input_dict = data.dict()
    input_dict["fully_equipped_kitchen"] = kitchen_scale.get(
        input_dict["fully_equipped_kitchen"], 0
    )
    input_dict["state_of_the_building"] = building_scale.get(
        input_dict["state_of_the_building"], 2
    )

    # 2. Build raw DataFrame and one-hot encode province and region
    df_raw = pd.DataFrame([input_dict])
    df_raw["province_" + df_raw["province"].iloc[0]] = 1
    df_raw["region_" + df_raw["region"].iloc[0]] = 1

    # 3. Reindex to the scaler's feature set (fitted before Lasso selection)
    #    Missing columns are filled with 0 (province/region not present = 0)
    scaler_feat = scaler_features[property_type]
    df_for_scaler = df_raw.reindex(columns=scaler_feat).fillna(0).astype(float)

    # 4. Scale using the fitted StandardScaler
    scaler = joblib.load(
        "models/scaler_houses.pkl" if property_type == "House"
        else "models/scaler_apartments.pkl"
    )
    scaled_array = scaler.transform(df_for_scaler)

    # 5. Select only the features the model was trained on (post-Lasso selection)
    scaled_df = pd.DataFrame(scaled_array, columns=scaler_feat)
    final_df = scaled_df[model_features[property_type]]

    return final_df.values


# --- Model Loading ---
def load_model(property_type):
    # 1. Map types to their respective file paths
    model_paths = {
        "House": "models/best_model_houses.pkl",
        "Apartment": "models/best_model_apartments.pkl",
    }

    # 2. Get the path based on the input
    path = model_paths.get(property_type)

    # 3. Check if path exists and load; otherwise return None
    if path and os.path.exists(path):
        return joblib.load(path)

    return None


# --- Mappings ---

kitchen_scale = {
    "Not equipped": 0,
    "Partially equipped": 1,
    "Super equipped": 2,
    "Fully equipped": 3,
}

building_scale = {
    "New": 4,
    "Under construction": 4,
    "Fully renovated": 3,
    "Excellent": 3,
    "Normal": 2,
    "To be renovated": 1,
    "To renovate": 1,
    "To restore": 1,
    "To demolish": 0,
}

# Features the scaler was fitted on (before Lasso feature selection)
scaler_features = {
    "House": [
        "number_of_rooms", "living_area", "fully_equipped_kitchen", "furnished",
        "open_fire", "terrace", "terrace_area", "garden", "garden_area",
        "surface_of_the_land", "number_of_facades", "swimming_pool",
        "state_of_the_building", "province_Brussels", "province_East Flanders",
        "province_Flemish Brabant", "province_Hainaut", "province_Liege",
        "province_Limburg", "province_Luxembourg", "province_Namur",
        "province_Walloon Brabant", "province_West Flanders",
        "region_Flanders", "region_Wallonia",
    ],
    "Apartment": [
        "number_of_rooms", "living_area", "fully_equipped_kitchen", "furnished",
        "open_fire", "terrace", "terrace_area", "garden", "garden_area",
        "number_of_facades", "swimming_pool", "state_of_the_building",
        "province_Brussels", "province_East Flanders", "province_Flemish Brabant",
        "province_Hainaut", "province_Liege", "province_Limburg",
        "province_Luxembourg", "province_Namur", "province_Walloon Brabant",
        "province_West Flanders", "region_Flanders", "region_Wallonia",
    ],
}

# Features the model was trained on (after Lasso feature selection)
model_features = {
    "House": [
        "number_of_rooms", "living_area", "fully_equipped_kitchen", "furnished",
        "open_fire", "terrace", "terrace_area", "garden", "garden_area",
        "surface_of_the_land", "number_of_facades", "swimming_pool",
        "state_of_the_building", "province_Brussels", "province_East Flanders",
        "province_Flemish Brabant", "province_Hainaut", "province_Limburg",
        "province_Luxembourg", "province_Namur", "province_Walloon Brabant",
        "province_West Flanders", "region_Wallonia",
    ],
    "Apartment": [
        "number_of_rooms", "living_area", "fully_equipped_kitchen", "furnished",
        "open_fire", "terrace", "terrace_area", "garden", "garden_area",
        "number_of_facades", "swimming_pool", "state_of_the_building",
        "province_Brussels", "province_East Flanders", "province_Flemish Brabant",
        "province_Hainaut", "province_Liege", "province_Limburg",
        "province_Namur", "province_Walloon Brabant", "province_West Flanders",
        "region_Wallonia",
    ],
}
