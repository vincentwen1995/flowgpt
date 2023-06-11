from datetime import datetime, timedelta
import pytz


def convert_to_utc(source_tz: str, datetime_str: str, datetime_format: str) -> datetime:
    """
    Convert a datetime string from the source timezone to UTC.

    Args:
        source_tz (str): The source timezone as a string.
        datetime_str (str): The datetime string to convert.
        datetime_format (str): The format of the datetime string.

    Returns:
        datetime: The converted datetime in UTC.

    Raises:
        pytz.UnknownTimeZoneError: If the source timezone is unknown or invalid.
        ValueError: If the datetime string is in an incorrect format.

    Example:
        source_tz = "US/Eastern"
        datetime_str = "2023-06-10 12:00:00"
        datetime_format = "%Y-%m-%d %H:%M:%S"
        utc_datetime = convert_to_utc(source_tz, datetime_str, datetime_format)
    """
    # Define the source timezone
    source_timezone = pytz.timezone(source_tz)

    # Parse the datetime string using the specified format
    source_datetime = datetime.strptime(datetime_str, datetime_format)

    # Set the source timezone to the datetime object
    source_datetime = source_timezone.localize(source_datetime)

    # Convert to UTC
    utc_datetime = source_datetime.astimezone(pytz.UTC)

    return utc_datetime


def datetime_range(start_dt: datetime, end_dt: datetime, delta: timedelta) -> datetime:
    current_dt = start_dt
    while current_dt <= end_dt:
        yield current_dt
        current_dt += delta
