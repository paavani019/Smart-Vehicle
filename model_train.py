import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

data = pd.read_csv("vehicle_data.csv")

X = data[["battery_health", "engine_temp", "oil_pressure", "mileage_since_service"]]
y = data["health_score"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))
print("✅ Model trained and saved as model.pkl")
