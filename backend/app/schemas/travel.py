from pydantic import BaseModel
from typing import Optional, List


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    adults: int = 1
    children: int = 0
    infants: int = 0


class FlightSegment(BaseModel):
    from_airport: str
    to_airport: str
    departure_time: str
    arrival_time: str
    airline: str
    flight_number: str


class FlightOffer(BaseModel):
    price: float
    currency: str = "USD"
    segments: List[FlightSegment]


class FlightSearchResponse(BaseModel):
    offers: List[FlightOffer]
