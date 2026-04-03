from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from property_data import Property
from prediction_service import get_prediction
from stat_service import get_stats_data

app = FastAPI(
    title="BelgiImmo Prediction API",
    description="An API to predict Belgian real estate prices and provide market insights.",
    version="1.0.0",
)

# --- CORS Middleware ---
# Allow all origins for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"])
async def root():
    """
    Root endpoint to verify the API's operational status.

    Returns:
        dict: A simple confirmation message.
    """
    return {"message": "BelgiImmo Real Estate Prediction API is running"}


@app.get("/stats", tags=["Market Data"])
async def get_stats():
    """
    Retrieve comprehensive market statistics for the dashboard.

    This endpoint aggregates data across regions (Brussels, Flanders, Wallonia)
    to provide median prices and property distributions.

    Returns:
        dict: A nested dictionary containing regional comparisons and global stats.
    """
    return get_stats_data()


@app.post("/predict", tags=["Machine Learning"])
async def predict(data: Property):
    """
    Predict the price of a property based on its features.

    Takes property details (size, rooms, location, etc.) and processes them
    through a pre-trained machine learning model.

    Args:
        data (Property): A Pydantic model representing the property features.

    Returns:
        dict: A JSON response containing the status, the predicted value, and the currency.

    Raises:
        HTTPException: 500 error if the prediction logic fails or data is malformed.
    """

    print(f"Received data for prediction: {data}")
    try:
        prediction = get_prediction(data)
        return {
            "status": "success",
            "prediction": round(float(prediction), 2),
            "currency": "EUR",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    # Run the application using Uvicorn
    # host 0.0.0.0 makes the server accessible on the local network
    uvicorn.run(app, host="0.0.0.0", port=8000)
