from datetime import datetime

import pytz as tz
from pyflow import Workflow

import formatters


def get_formatter(workflow: Workflow):
    timestamp_format = workflow.env.get("TIMESTAMP_FORMAT", "FORMAT_DEFAULT")
    return formatters.FORMATTERS[timestamp_format]


def get_icon(timezone: str, now: datetime, home_tz: str):
    if timezone == home_tz:
        return "img/icons/home.png"

    if timezone == "UTC":
        return "img/icons/utc.png"

    utc_offset = now.utcoffset()
    utc_offset_hours = round(utc_offset.days * 24 + utc_offset.seconds / 60 / 60)
    return f"img/icons/{utc_offset_hours}.png"


def get_home(workflow: Workflow):
    home_tz = workflow.env["HOME"][3:].replace("__", "/")

    home_now = (
        datetime.utcnow()
        .replace(tzinfo=tz.utc)
        .astimezone(
            tz=tz.timezone(home_tz),
        )
    )

    return home_tz, home_now


def get_name_replacements(workflow: Workflow):
    sep = "//"

    name_replacements = {}

    for line in workflow.env.get("NAME_REPLACEMENTS", "").split("\n"):
        if not line:
            continue

        if sep not in line:
            raise ValueError(
                f"name replacement '{line}' is missing the '{sep}' separator."
            )

        parts = line.split(sep)

        if len(parts) != 2:
            raise ValueError(
                f"name replacement '{line}' should have the format `old {sep} new`."
            )

        if "" in parts:
            raise ValueError(
                f"name replacement '{line}' should have the format `old {sep} new`."
            )

        old, new = parts
        name_replacements[old.strip()] = new.strip()

    return name_replacements
