import logging
import os
import json
import time
import uuid
from collections import defaultdict
from typing import List

import requests
import boto3
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from constants import (
    CLUB_NAME_INPUT,
    CLUB_CITY_INPUT,
    COUNTRY_INPUT,
    STATE_CODE_INPUT,
    STATE_CODES,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client("s3")

ENV_NAME = os.environ["ENV_NAME"]
FOOTWEDGE_GOLF_CLUB_SOURCE_BUCKET_NAME = os.environ[
    "FOOTWEDGE_GOLF_CLUB_SOURCE_BUCKET_NAME"
]

# ----------- Main handler -----------
def lambda_handler(event, context):
    logger.info(f"env: {ENV_NAME}")
    logger.info(f"Received event: {json.dumps(event, indent=4)}")
    state_code = event["stateCode"]
    validate_state_code(state_code)
    scrape_golf_courses(state_code)


def validate_state_code(state_code: str):
    if state_code not in STATE_CODES:
        raise Exception(
            f"{state_code} is not valid state code. Accepted values: \n{STATE_CODES}"
        )


def scrape_golf_courses(state_code: str):
    session = HTMLSession()
    url = "https://ncrdb.usga.org/"
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    form = soup.find(id="form1")
    form_details = get_form_details(form=form)

    start_time = time.time()
    form_data = prepare_form_data(form_details, state_code=state_code)
    golf_club_to_golf_courses = map_golf_clubs_to_golf_courses(
        url=url,
        form_data=form_data,
        session=session,
    )
    for golf_club_name, golf_courses in golf_club_to_golf_courses.items():
        logger.info(f"Uploading golf club: {golf_club_name} to S3...")
        upload_golf_club_to_s3(
            state_code=state_code,
            golf_club_name=golf_club_name,
            golf_courses=golf_courses,
        )
    logger.info(f"---- Processed {state_code} in {time.time()-start_time} seconds")


def get_form_details(form) -> dict:
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()

    inputs = []
    input_tags = form.find_all("input")
    select_tags = form.find_all("select")
    tags = input_tags + select_tags
    for tag in tags:
        input_type = tag.attrs.get("type", "text")
        input_name = tag.attrs.get("name")
        input_default_value = tag.attrs.get("value", "")
        inputs.append(
            {
                "type": input_type,
                "name": input_name,
                "default_value": input_default_value,
            }
        )

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def form_input_factory(input_name: str, state_code: str):
    if input_name == CLUB_NAME_INPUT:
        return ""
    elif input_name == CLUB_CITY_INPUT:
        return ""
    elif input_name == COUNTRY_INPUT:
        return "USA"
    elif input_name == STATE_CODE_INPUT:
        return state_code
    else:
        return ""


def prepare_form_data(form_details: dict, state_code: str):
    data = {}
    for input_tag in form_details["inputs"]:
        if input_tag["type"] == "hidden":
            # if it's hidden, use the default value
            data[input_tag["name"]] = input_tag["default_value"]
        elif input_tag["type"] != "submit":
            input_tag_name = input_tag["name"]
            value = form_input_factory(input_tag_name, state_code=state_code)
            data[input_tag_name] = value

    data["__EVENTTARGET"] = "myButton"
    return data


def scrape_golf_course_tee_boxes(url: str) -> List[dict]:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    tee_box_table = soup.find(id="gvTee")
    if not tee_box_table:
        logger.info(f"The url: {url} does not have tee box info to scrape")
        return []
    rows = tee_box_table.find_all(name="tr")
    headers = [col.get_text().strip().lower() for col in rows[0].find_all("th")]
    tee_box_dicts = []
    for row in rows:
        row_data = [col.get_text().lstrip() for col in row.find_all(name="td")]
        if not row_data:
            continue
        tee_box_data = dict(zip(headers, row_data))
        tee_box_dicts.append(
            {
                "tee_box_id": str(uuid.uuid4()),
                "tee_box_color": tee_box_data["tee name"],
                "gender": tee_box_data["gender"],
                "par": tee_box_data["par"],
                "distance": None,
                "units": "yards",
                "course_rating": tee_box_data["course rating  (18)"],
                "slope": tee_box_data["slope rating (18)"],
            }
        )

    return tee_box_dicts


def map_golf_clubs_to_golf_courses(
    url: str, form_data: dict, session: HTMLSession
) -> dict:
    res = session.post(url, data=form_data)
    soup = BeautifulSoup(res.content, "html.parser")
    golf_course_table = soup.find(id="gvCourses")
    golf_courses = golf_course_table.find_all(name="tr")

    golf_club_to_golf_courses = defaultdict(list)
    for golf_course in golf_courses:
        props = golf_course.find_all(name="td")
        if not props:
            continue
        golf_club, course, city, state_code = props
        golf_club_name = golf_club.get_text()
        golf_course_name = course.get_text()
        logger.info(f"Processing golf course: {golf_course_name}")
        course_tee_box_path = golf_course.find(name="a").attrs["href"]
        course_tee_box_url = f"{url}{course_tee_box_path}"
        tee_boxes = scrape_golf_course_tee_boxes(url=course_tee_box_url)
        golf_course_info = {
            "city": city.get_text(),
            "state_code": state_code.get_text(),
            "golf_course_name": golf_course_name,
            "golf_course_id": str(uuid.uuid4()),
            "num_holes": 18,
            "tee_boxes": tee_boxes,
        }
        golf_club_to_golf_courses[golf_club_name].append(golf_course_info)

    return golf_club_to_golf_courses


def upload_golf_club_to_s3(
    state_code: str, golf_club_name: str, golf_courses: List[dict]
):
    golf_club_data = {
        "golf_club_name": golf_club_name,
        "golf_club_id": str(uuid.uuid4()),
        "city": golf_courses[0]["city"],
        "state_code": state_code.split("-")[1],
        "courses": golf_courses,
    }
    formatted_golf_club_name = (
        golf_club_name.replace(" ", "-").replace("(", "").replace(")", "").lower()
    )
    file_key = f"{state_code}/{formatted_golf_club_name}.json"
    s3_client.put_object(
        Bucket=FOOTWEDGE_GOLF_CLUB_SOURCE_BUCKET_NAME,
        Key=file_key,
        Body=bytes(json.dumps(golf_club_data, indent=4).encode("UTF-8")),
    )
