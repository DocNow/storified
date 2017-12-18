#!/usr/bin/env python

import os
import re
import bs4
import sys
import logging
import argparse
import requests

from urllib.parse import urlparse

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
    rewrite_html(story, story_dir)
    logging.info("finished archiving %s", story["slug"])

def download(story, story_dir):
    slug = story["slug"]
    username = story["author"]["username"]
    logging.info("downloading story %s to %s", slug, story_dir)

    url = "https://api.storify.com/v1/stories/%s/%s" % (username, slug)
    download_file(url, story_dir + "/index.json")

    url = "https://storify.com/%s/%s.xml" % (username, slug)
    download_file(url, story_dir + "/index.xml")

    url = "https://storify.com/%s/%s.html" % (username, slug)
    download_file(url, story_dir + "/index.html")


def download_file(url, path):
    if url.startswith('//'):
        url = 'http:' + url
    resp = requests.get(url)
    if (resp.status_code != 200):
        logging.error("GET %s resulted in %s", url, resp.status_code)
        return None

    # create fs path baased on the url
    os_path = os.path.join(*path.split('/'))

    # add file extension if needed
    m = re.match(r'^(.+?)/(.+);?', resp.headers['content-type'])
    if m and m.group(1).lower() == 'image':
        filename, file_ext = os.path.splitext(os_path)
        if file_ext == '':
            path += '.' + m.group(2)
            os_path += '.' + m.group(2)
 
    # create the directory path if needed
    dir_name = os.path.dirname(os_path)
    if not os.path.isdir(dir_name):
        logging.info('making directory %s', dir_name) 
        os.makedirs(dir_name)

    logging.info('downloading %s to %s', url, os_path)
    open(os_path, "wb").write(resp.content)

    return path

def rewrite_html(story, story_dir):
    logging.info("rewriting html %s", story_dir)
    html_file = os.path.join(story_dir, 'index.html')
    html = open(html_file).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')

    for link in soup.select('link[rel="stylesheet"]'):
        href = link.get('href')
        if href.startswith('http'):
            path = localize(href, story_dir, 'css')
            if (path):
                link['href'] = path

    for img in soup.select('img'):
        src = img.get('src')
        path = localize(src, story_dir, 'images')
        if path:
            img['src'] = path

    new_html_file = html_file.replace('index.html', 'index-localized.html')
    open(new_html_file, 'w').write(soup.prettify())

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

def localize(url, story_dir, resource_type):
    uri = urlparse(url)
    path = story_dir + '/' + resource_type + '/' + uri.netloc + uri.path
    path = download_file(url, path)
    if path:
        return os.path.relpath(path, story_dir)
    else:
        return None

class StorifiedException(Exception):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser("archive your Storify stories")
    parser.add_argument("account_name", help="Your Storify account name")
    parser.add_argument("--download-dir", "-d", default=None, 
                        help="a directory to download data to")
    args = parser.parse_args()
    storified(args.account_name, args.download_dir)
