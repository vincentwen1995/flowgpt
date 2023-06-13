from datetime import datetime, timedelta
import pytz


def convert_to_utc(source_tz: str, dt: datetime) -> datetime:
    """
    Convert a datetime string from the source timezone to UTC.

    Args:
        source_tz (str): The source timezone as a string.
        dt (datetime): The datetime object to convert.

    Returns:
        datetime: The converted datetime in UTC.

    Raises:
        pytz.UnknownTimeZoneError: If the source timezone is unknown or invalid.
        ValueError: If the datetime string is in an incorrect format.

    Example:
        source_tz = "US/Eastern"
        dt = datetime(2023, 6, 10, 12, 0, 0)
        utc_datetime = convert_to_utc(source_tz, datetime_str, datetime_format)
    """
    if not dt.tzinfo:
        # Define the source timezone
        source_timezone = pytz.timezone(source_tz)

        # Set the source timezone to the datetime object
        dt = source_timezone.localize(dt)

    # Convert to UTC
    utc_datetime = dt.astimezone(pytz.UTC)

    return utc_datetime


def datetime_range(start_dt: datetime, end_dt: datetime, delta: timedelta) -> datetime:
    current_dt = start_dt
    while current_dt <= end_dt:
        yield current_dt
        current_dt += delta
