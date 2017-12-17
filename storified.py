#!/usr/bin/env python

import os
import logging
import argparse
import requests

def storified(account_name, archive_dir=None):
    try:
        if archive_dir:
            archive_dir = setup_dir(archive_dir)
        else:
            archive_dir = setup_dir(account_name)

        setup_logging(archive_dir)
        logging.info("starting to archive stories for %s to %s", account_name,
            archive_dir)

        for story in get_stories(account_name):
            archive_story(story, archive_dir)

        logging.info("finished archiving account %s", account_name)

    except StorifiedException as e:
        print(e)
        if len(logging.getLogger().handlers) != 0:
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
    slug = story["slug"]
    username = story["author"]["username"]
    logging.info("downloading story %s to %s", slug, story_dir)

    url = "https://api.storify.com/v1/stories/%s/%s" % (username, slug)
    download_file(url, os.path.join(story_dir, "index.json"))

    url = "https://storify.com/%s/%s.xml" % (username, slug)
    download_file(url, os.path.join(story_dir, "index.xml"))

    url = "https://storify.com/%s/%s.html" % (username, slug)
    download_file(url, os.path.join(story_dir, "index.html"))


def download_file(url, path):
    resp = requests.get(url)
    open(path, "w").write(resp.text)

def fetch_images(story_dir):
    logging.info("fetching images for %s", story_dir)

def rewrite_html(story_dir):
    logging.info("rewriting html %s", story_dir)

def setup_dir(path):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
    except Exception as e:
        raise StorifiedException("unable to create target directory: %s", path)
    return path

def setup_logging(archive_dir):
    logging.basicConfig(
        filename=os.path.join(archive_dir, 'storified.log'),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

class StorifiedException(Exception):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser("archive your Storify stories")
    parser.add_argument("account_name", help="Your Storify account name")
    parser.add_argument("--download-dir", "-d", default=None, 
                        help="a directory to download data to")
    args = parser.parse_args()
    storified(args.account_name, args.download_dir)
