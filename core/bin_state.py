from pydantic import BaseModel


class BinState(BaseModel):
    mass: float               # kg
    temperature: float        # °C
    moisture: float           # %
    pH: float
    oxygen: float             # 0–1
    microbial_activity: float # 0–1
    