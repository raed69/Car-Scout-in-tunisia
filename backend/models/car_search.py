from __future__ import annotations

from pydantic import BaseModel, Field


class CarSearch(BaseModel):
    """Structured request built from the user's natural language message."""

    brand: str | None = Field(default=None, description="Car brand such as Volkswagen, Renault, Peugeot")
    model: str | None = Field(default=None, description="Model such as Golf 7, Clio 4, 208")
    city: str | None = Field(default=None, description="City or region, for example Tunis or Sousse")
    max_price_tnd: int | None = Field(default=None, description="Maximum acceptable budget in TND")
    fuel: str | None = Field(default=None, description="Fuel type, such as diesel, petrol, hybrid")
    transmission: str | None = Field(default=None, description="Automatic or manual")
    year_min: int | None = Field(default=None, description="Minimum manufacturing year")
    year_max: int | None = Field(default=None, description="Maximum manufacturing year")
    mileage_max_km: int | None = Field(default=None, description="Maximum mileage in kilometers")
    notes: str | None = Field(default=None, description="Extra details from the user's message")
    assumed_from_preferences: list[str] = Field(
        default_factory=list,
        description="Names of the fields above that were filled from the saved preferences, not from the message",
    )
