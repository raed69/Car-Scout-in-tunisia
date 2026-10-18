from __future__ import annotations


def get_car_specs(model_name: str):
    """Return a minimal spec dictionary for a given model."""

    return {
        "model": model_name,
        "fuel_types": ["diesel", "petrol", "hybrid"],
        "transmissions": ["manual", "automatic"],
        "notes": "Spec lookup is intentionally mocked in this starter project.",
    }
