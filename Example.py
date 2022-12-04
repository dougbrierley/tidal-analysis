import datetime

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

import utide

print(utide.__version__)

with open("data/can1998.dtf") as f:
    lines = f.readlines() # returns list 'lines' that contains each row as a list item
#print(lines[:5])
#print("".join(lines[:5])) #print 5 lines of the list, joined by nothing - they already have new line in them

names = ["seconds", "year", "month", "day", "hour", "elev", "flag"]

obs = pd.read_csv(
    "data/can1998.dtf",
    names=names,
    skipinitialspace=True,
    delim_whitespace=True,
    na_values="9.990", # Additional values to consider NA
)


date_cols = ["year", "month", "day", "hour"] # Identify column names for to_datetime
index = pd.to_datetime(obs[date_cols])
obs = obs.drop(date_cols, axis=1)
obs.index = index

print(obs.head(5))

bad = obs["flag"] == 2
corrected = obs["flag"] == 1

obs.loc[bad, "elev"] = np.nan # replaces flagged unreliable elevations with numpy NaN value
obs["anomaly"] = obs["elev"] - obs["elev"].mean() 
obs["anomaly"] = obs["anomaly"].interpolate()
print(f"{bad.sum()} points were flagged 'bad' and interpolated")
print(f"{corrected.sum()} points were flagged 'corrected' and left unchanged")

coef = utide.solve(
    obs.index,
    obs["anomaly"],
    lat=-25,
    method="ols",
    conf_int="MC",
    verbose=False,
)

print(coef)

tide = utide.reconstruct(obs.index, coef, verbose=False)

t = obs.index.to_pydatetime()

fig, (ax0, ax1, ax2) = plt.subplots(figsize=(17, 5), nrows=3, sharey=True, sharex=True)

ax0.plot(t, obs.anomaly, label="Observations", color="C0")
ax1.plot(t, tide.h, label="Prediction", color="C1")
ax2.plot(t, obs.anomaly - tide.h, label="Residual", color="C2")
fig.legend(ncol=3, loc="upper center")

plt.show