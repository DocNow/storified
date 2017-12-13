#!/usr/bin/env python

import os
import logging
import argparse
import requests

def storified(account_name):
    try:
        archive_dir = setup_dir(account_name)
        logging.basicConfig(
            filename=os.path.join(archive_dir, "storified.log"),
            level=logging.INFO
        )
        for story in get_stories(account_name):
            archive_story(story, archive_dir)
        logging.info("finished archiving account %s", account_name)
    except StorifiedException as e:
        logging.error(e)

def get_stories(account_name):
    page = 0
    while True:
        page += 1
        resp = requests.get("https://private-api.storify.com/v1/stories/%s?page=%s&per_page=100&sort=date.created&filter=draft,published" % (account_name, page))
        results = resp.json()
        if len(results["content"]["stories"]) == 0:
            break
        for story in results["content"]["stories"]:
            yield story

def archive_story(story, archive_dir):
    story_dir = setup_dir(os.path.join(archive_dir, story["slug"]))
    download(story, story_dir)
    fetch_images(story_dir)
    rewrite_html(story_dir)
    logging.info("finished archiving %s", story["slug"])

def download(story, story_dir):
    # https://api.storify.com/v1/stories/docnow/docnowcommunity-chat-2" 
    # https://storify.com/docnow/docnowcommunity-chat-2.xml
    # https://storify.com/docnow/docnowcommunity-chat-2.html
    logging.info("downloading story %s to %s", story["slug"], story_dir)

def fetch_images(story_dir):
    logging.info("fetching images for %s", story_dir)

def rewrite_html(story_dir):
    logging.info("rewriting html %s", story_dir)

def setup_dir(path):
    if (os.path.exists(path)):
        raise StorifiedException("directory %s already exists", path)
    try:
        os.mkdir(path)
    except Exception as e:
        raise StorifiedException("unable to create target directory: %s", path)
    return path

class StorifiedException(Exception):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser("archive your Storify stories")
    parser.add_argument("account_name", help="Your Storify account name")
    args = parser.parse_args()
    storified(args.account_name)
