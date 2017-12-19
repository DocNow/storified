On December 12, 2017 [Storify] [announced] that they were going to shut down
completely on May 16, 2018. Users have until then to download their stories at
which point they will disappear from the web.

*storified* is a little utility for downloading your stories as HTML, XML and
JSON--which can be handy if you have a bunch of stories. You can take these
files and mount them on your own website and point your links to them instead of
Storify.

storified will also rewrite the index.html to use local images, css and
javascript that are downloaded. The originally downloaded `index.html` is 
stored as `index-original.html`.

## Install

1. Install [Python]
2. pip install storified

## Run

    % storified.py <storify username>

This will create a directory named after your username, which contains a
sub-directory for each story, which in turn contains the HTML, JSON and XML
export files for the story. For example, here is a partial directory structure
created for the [digdialog] Storify user:

```
digdialog/
├── a-woman-s-touch-manual-labor-pink-collar-workers-a
│   ├── css
│   ├── images
│   ├── js
│   ├── index.html
│   ├── index-original.html
│   ├── index.json
│   └── index.xml
├── alberto-campagnolo-digital-dialogue-november-1-201
│   ├── css
│   ├── images
│   ├── js
│   ├── index.html
│   ├── index-original.html
│   ├── index.json
│   └── index.xml

...

```

If you want to control where the downloaded files go use the *--download-dir*
command line option:

    storified.py --download-dir /path/to/my/stories

## Docker

If you'd rather not install storified with pip you can also run it using 
[Docker]. 

```
% docker run -v <PATH>:/storified docnow/storified <STORIFY_USERNAME>
```

You will need to replace `<PATH>` with the full path to the directory you would
like the files to be downloaded to, and `<STORIFY_USERNAME>` to be the Storify
username who created the stories.

For example if you wanted to download `digdialog`'s stories to `/home/ed/storified`:

```
% docker run -v /home/ed/storified:/storified/downloads docnow/storified digdialog
```

[Storify]: https://en.wikipedia.org/wiki/Storify
[announced]: https://web.archive.org/web/20171212163903/https://storify.com/faq-eol
[Python]: https://python.org
[digdialog]: https://storify.com/digdialog/
[Docker]: https://docs.docker.com/engine/installation/
