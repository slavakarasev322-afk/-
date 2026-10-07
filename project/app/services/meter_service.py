
"""Business services for meters and readings."""

from app.repositories.meter_repository import (
    add_meter,
    add_reading,
    delete_meter,
    get_meters,
    get_readings,
)


def create_meter(
    meter_type: str,
    serial_number: str,
    verification_date: str,
) -> int:
    """Validate and create a meter."""
    meter_type = meter_type.strip()
    serial_number = serial_number.strip()
    verification_date = verification_date.strip()

    if not meter_type:
        raise ValueError("Выберите тип ресурса.")

    if not serial_number:
        raise ValueError("Введите серийный номер.")

    return add_meter(
        meter_type=meter_type,
        serial_number=serial_number,
        verification_date=verification_date,
    )


def create_reading(
    meter_id: int,
    value_text: str,
) -> float:
    """Validate and save a meter reading."""
    try:
        value = float(
            value_text.replace(",", ".")
        )
    except ValueError as error:
        raise ValueError(
            "Показание должно быть числом."
        ) from error

    if value < 0:
        raise ValueError(
            "Показание не может быть отрицательным."
        )

    return add_reading(
        meter_id,
        value,
    )


def list_meters() -> list[dict]:
    """Return meters for the UI."""
    return get_meters()


def list_readings() -> list[dict]:
    """Return readings for the UI."""
    return get_readings()


def remove_meter(meter_id: int) -> None:
    """Remove a meter."""
    delete_meter(meter_id)
