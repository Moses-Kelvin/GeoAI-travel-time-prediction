import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("trip_data.csv").dropna()
print(f"Loaded {len(df)} trips with valid ORS data")

# Feature engineering
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
features = ['dist_km', 'hour_sin', 'hour_cos', 'day_of_week']
X = df[features]
y = df['actual_duration_min']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f} minutes")
print(f"Baseline (always predict mean): {np.mean(np.abs(y_test - y_test.mean())):.2f} minutes")