from fastapi import APIRouter
from app.schemas.travel import FlightSearchRequest, FlightSearchResponse, FlightOffer, FlightSegment

router = APIRouter(prefix="/travel", tags=["Travel"])


@router.post("/search", response_model=FlightSearchResponse)
async def mock_flight_search(payload: FlightSearchRequest):
    # Mock data for demo purposes
    segment = FlightSegment(
        from_airport=payload.origin,
        to_airport=payload.destination,
        departure_time=f"{payload.departure_date}T07:00:00",
        arrival_time=f"{payload.departure_date}T10:30:00",
        airline="DemoAir",
        flight_number="DA101",
    )

    offer = FlightOffer(
        price=199.99,
        currency="USD",
        segments=[segment],
    )

    return FlightSearchResponse(offers=[offer])
