from ctypes import Union
import logging
import requests


log = logging.getLogger(__name__)


def get_paginated_data(uri: str, params: dict = None) -> list[dict]:
    if not params:
        params = {}

    # Default to the first page
    if not params.get("page"):
        params["page"] = 1

    data = []

    while True:
        log.debug(f"Requesting data with {params=}")

        res = requests.get(uri, params=params)
        res_data = res.json()

        data += res_data["data"]

        meta = res_data["meta"]
        current_page, total_pages, next_page = (
            meta["current_page"],
            meta["total_pages"],
            meta["next_page"],
        )

        if current_page >= total_pages:
            break

        params["page"] = next_page

    return data


def height_to_meters(feet: int, inches: int) -> float:
    return feet * 0.3048 + inches * 0.0254


def weight_to_kilograms(pounds: int) -> float:
    return pounds * 0.4535924
