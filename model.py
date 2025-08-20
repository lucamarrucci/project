# model.py
import pandas as pd
import numpy as np

def _clip01(x): return np.clip(x,0,1)
def normalize(x,a,b): return _clip01((x-a)/(b-a+1e-6))

def training_value(session: dict) -> float:
    dur = float(session.get("duration_min") or 0)
    rpe = float(session.get("rpe") or 0)
    trimp = dur*rpe
    swim = float(session.get("swim_meters") or 0)
    hi = float(session.get("high_intensity_meters") or 0)
    gym = float(session.get("gym_volume_kg") or 0)
    q = float(session.get("quality_note") or 0.5)
    s_int = normalize(trimp,0,720)
    s_swim = 0.7*normalize(swim,0,6000)+0.3*normalize(hi,0,1500)
    s_gym = normalize(gym,0,20000)
    s_ext = _clip01(0.85*s_swim+0.15*s_gym)
    score = 0.55*s_int+0.30*s_ext+0.15*_clip01(q)
    return float(np.clip(score*100,0,100))
