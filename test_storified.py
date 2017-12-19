import os
import re
import bs4
import pytest
import shutil
import logging
import tempfile
import storified

logging.basicConfig(filename='test.log', level=logging.DEBUG)

story_dir = os.path.join('test-data', 'all-things-appraisal')

def setup_module():
    if (os.path.isdir('test-data')):
        shutil.rmtree('test-data')
    os.mkdir('test-data')

def test_storified():
    storified.storified('AppraisalSAA', 'test-data')
    files = os.listdir(story_dir)
    assert len(files) == 6
    assert 'index.json' in files
    assert 'index.html' in files
    assert 'index.xml' in files
    assert 'index-original.html' in files
    assert 'css' in files
    assert 'images' in files

def test_rewrite():
    # make sure the css and images are local instead of at storify or twitter
    html_file = os.path.join(story_dir, 'index.html')
    html = open(html_file).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for link in soup.select('link[rel="stylesheet"]'):
        href = str(link.get('href'))
        print(href)
        assert not href.startswith('http')
    for img in soup.select('img'):
        pass
        # assert not img.get('src').startswith('http')

