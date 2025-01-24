# CRAWLER

A powerful and flexible web crawler that recursively explores a website, extracts useful data (URLs, images, scripts, forms, etc.), and displays the structure of the pages. It allows you to perform searches on the content, download website resources, and export crawled URLs.

## Features

- **Recursive Crawling**: Explore all links on the website recursively.
- **Custom Headers**: Add custom headers to all requests for additional functionality.
- **Random User-Agent**: Optionally use a random User-Agent to mimic various browsers.
- **Search Content**: Search through the content of the crawled pages using regular expressions.
- **Export URLs**: Export all the URLs crawled during the process.
- **Download Resources**: Download website resources (HTML, CSS, JavaScript, images, etc.) to a specified directory.
- **Redirection Handling**: The crawler can handle and follow redirections.
- **Error Handling**: It provides feedback on the status of each page (success, redirects, errors, etc.).

## Installation

1. Clone the repository:
```bash
$ git clone https://github.com/matth200/CRAWLER
$ cd CRAWLER
$ python3 -m pip install -r requirements.txt
```


## Usage

Command-Line Arguments:

    --url <url>: The URL of the website you want to crawl. Required
    --headers <headers>: JSON string containing custom headers to include in each request (optional).
    --random-agent: Randomizes the user-agent for each request (optional).
    --search <regex>: A regular expression to search for in the content of the website (optional).
    --download <directory>: Directory where all website resources should be downloaded (optional).
    -f: Skip the user prompt for warnings, run the crawler without confirmation (optional).
    --export-urls <file>: Export all crawled URLs to a file (optional).

Example Commands:

    Basic Crawl:

python crawler.py --url https://example.com

Crawl with Random User-Agent:

python crawler.py --url https://example.com --random-agent

Crawl with Custom Headers:

python crawler.py --url https://example.com --headers '{"Authorization": "Bearer token"}'

Crawl with Search (Regex):

python crawler.py --url https://example.com --search ".{0,20}api.{0,20}"

Crawl and Download Resources:

python crawler.py --url https://example.com --download /tmp/example

Export URLs:

    python crawler.py --url https://example.com --export-urls /tmp/exported_urls.txt

Output

    The crawler will display the structure of the website in a tree format.
    If the --search option is used, it will display the pages where the search pattern was found.
    If --export-urls is specified, all URLs crawled will be saved to the specified file.
    Warnings will be shown if you use custom headers or certain authentication tokens that could trigger unintended actions on the website.

## Example


```bash
$ python3 crawler.py --help

 ▄████████    ▄████████    ▄████████  ▄█     █▄   ▄█          ▄████████    ▄████████ 
███    ███   ███    ███   ███    ███ ███     ███ ███         ███    ███   ███    ███ 
███    █▀    ███    ███   ███    ███ ███     ███ ███         ███    █▀    ███    ███ 
███         ▄███▄▄▄▄██▀   ███    ███ ███     ███ ███        ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███        ▀▀███▀▀▀▀▀   ▀███████████ ███     ███ ███       ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    █▄  ▀███████████   ███    ███ ███     ███ ███         ███    █▄  ▀███████████ 
███    ███   ███    ███   ███    ███ ███ ▄█▄ ███ ███▌    ▄   ███    ███   ███    ███ 
████████▀    ███    ███   ███    █▀   ▀███▀███▀  █████▄▄██   ██████████   ███    ███ 
             ███    ███                          ▀                        ███    ███ 

          
usage: CRAWLER [-h] --url URL [--headers HEADERS] [--random-agent] [--search SEARCH] [--download DOWNLOAD] [-f] [--export-urls EXPORT_URLS]

Create a Tree of the webpage with all the information you got from one page

options:
  -h, --help            show this help message and exit
  --url URL             The url of the page you wanna analyse
  --headers HEADERS     Add headers into all the request
  --random-agent        Makes the user agent random
  --search SEARCH       Regex to search in all the website
  --download DOWNLOAD   Specify a directory to download all the website content
  -f                    No need for input by the user, it will be okay for everything
  --export-urls EXPORT_URLS
                        Export all the url that you have crawled
```


Example Output:

Looking for all the pages of the website...
Processing [====                        ] 30% (30/100)

The trees of the website:
├── 📂 home
│   ├── 📄 index.html --> {200 OK}
│   └── 📄 about.html --> {404 Not Found}
├── 📂 blog
│   ├── 📄 post1.html --> {200 OK}
│   └── 📄 post2.html --> {200 OK}

Links not belonging to the page:
 - http://external-link.com

Trash datas not supported:
 - javascript:void(0)



## TO DO

- Option to download content
- If a file end with .js test the .js.map to see if this exists
- Highlight particular data like localhost, 127.0.0.1, subdomains...
- Get all the comment (html comment, react comment...)
- Get all php code found and indicate in which file you got it
- Looking for api inside compiled javascript for client side javascript based (maybe just the same as research regex)
- Looking for meta-data on every files (on images for example)
- Option of multithreading
- handle error on the website


## Notes

This crawler is designed for educational purposes and should be used responsibly. Always respect a website’s robots.txt file and terms of service.
It is important to ensure that the URLs being crawled do not trigger unintended actions that could affect the website.