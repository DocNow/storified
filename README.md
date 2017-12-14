On December 12, 2017 [Storify] [announced] that they were going to shut down
completely on May 16, 2018. Users have until then to download their stories at
which point they will disappear from the web.

*storified* is a little utility for downloading your stories as HTML, XML and
JSON--which can be handy if you have a bunch of stories. You can take these
files and mount them on your own website and point your links to them instead of
Storify.

The immediate goal is to also add functionality to download referenced images,
CSS and JavaScript and then rewriting the HTML to point to them, since these
links will break when Storify goes offline.

## Install

1. Install [Python]
2. pip install storified

## Run

    % storified.py <account name>

This will create a directory named after your account under the downloads directory, which contains a
sub-directory for each story, which in turn contains the HTML, JSON and XML
export files for the story. For example, here is a partial directory structure
created for the [digdialog] Storify account:

```
downloads/
└── digdialog/
    ├── a-woman-s-touch-manual-labor-pink-collar-workers-a
    │   ├── index.html
    │   ├── index.json
    │   └── index.xml
    ├── alberto-campagnolo-digital-dialogue-november-1-201
    │   ├── index.html
    │   ├── index.json
    │   └── index.xml
    └── alexandrina-agloro-digital-dialogue-october-31-201
        ├── index.html
        ├── index.json
        └── index.xml
```

[Storify]: https://en.wikipedia.org/wiki/Storify
[announced]: https://web.archive.org/web/20171212163903/https://storify.com/faq-eol
[Python]: https://python.org
[digdialog]: https://storify.com/digdialog/
