import re
import os
import requests
import xml.etree.ElementTree as ET
from tqdm import trange, tqdm
from functools import partial
from argparse import ArgumentParser
import urllib.request as libreq
import time, datetime

from exts import db


def check_entry(entry):
    for child in entry:
        if child.tag.endswith("title"):
            return True
    return False


def update(theday, start_id, max_result):
    raw = db.raw_arxiv_data
    processed = db.processed_arxiv_data

    start_id_number = int(start_id.split(".")[1])
    id_list = ",".join(
        [
            "{:02}{:02}.{:05}".format(theday.year % 100, theday.month, number)
            for number in range(start_id_number + 1, start_id_number + max_result + 1)
        ]
    )
    url = "http://export.arxiv.org/api/query?id_list={}&max_results={}".format(
        id_list, max_result
    )

    with libreq.urlopen(url) as connection:
        r = connection.read().decode("utf-8")
        r = re.sub(r"ns\d:", "", r)
        r = re.sub(r' xmlns=".*"', "", r)
        root = ET.fromstring(r)
        delete_list = []
        raw_articles = []
        articles = []
        for child in root:
            if not child.tag.endswith("entry"):
                delete_list.append(child)
            elif not check_entry(child):
                delete_list.append(child)
                end = True

        for child in delete_list:
            root.remove(child)

        for child in root:
            if child.tag == "entry":
                id = child.find("id").text.split("/")[-1].split("v")[0]
                raw_articles.append(
                    {"arxiv_id": id, "text": ET.tostring(child).decode("utf-8")}
                )

                title = child.find("title").text
                submitted_date = child.find("published").text
                submitted_date = datetime.datetime.strptime(
                    submitted_date, "%Y-%m-%dT%H:%M:%SZ"
                )
                abstract = child.find("summary").text
                authors = [au.find("name").text for au in child.findall("author")]
                category = child.find("category")
                category = child.find("category").attrib["term"]

                if category.startswith("cs"):
                    articles.append(
                        {
                            "arxiv_id": id,
                            "added_date": datetime.datetime(
                                theday.year, theday.month, theday.day, 0, 0, 0
                            ),
                            "submitted_date": submitted_date,
                            "title": title,
                            "abstract": abstract,
                            "authors": authors,
                            "category": category,
                        }
                    )

        if len(raw_articles) > 0:
            raw.insert_many(raw_articles)
        if len(articles) > 0:
            processed.insert_many(articles)
    return len(articles)
