import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load trip data
df = pd.read_csv("trip_data.csv").dropna()

# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Actual vs ORS duration (scatter)
ax1 = axes[0]
ax1.scatter(df['ors_duration_min'], df['actual_duration_min'], alpha=0.6, edgecolors='k')
ax1.plot([0, df['ors_duration_min'].max()], [0, df['ors_duration_min'].max()], 'r--', label='Perfect match')
ax1.set_xlabel('ORS estimated duration (minutes)')
ax1.set_ylabel('Actual duration (minutes)')
ax1.set_title('Actual vs ORS Travel Time')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Residuals (actual - ORS) vs distance
ax2 = axes[1]
residual = df['actual_duration_min'] - df['ors_duration_min']
ax2.scatter(df['dist_km'], residual, alpha=0.6, edgecolors='k')
ax2.axhline(y=0, color='r', linestyle='--')
ax2.set_xlabel('Straight-line distance (km)')
ax2.set_ylabel('Actual - ORS (minutes)')
ax2.set_title('Residuals vs Distance')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('screenshots/actual_vs_ors.png', dpi=150, bbox_inches='tight')
plt.show()