# CRAWLER

```bash

 ▄████████    ▄████████    ▄████████  ▄█     █▄   ▄█          ▄████████    ▄████████ 
███    ███   ███    ███   ███    ███ ███     ███ ███         ███    ███   ███    ███ 
███    █▀    ███    ███   ███    ███ ███     ███ ███         ███    █▀    ███    ███ 
███         ▄███▄▄▄▄██▀   ███    ███ ███     ███ ███        ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███        ▀▀███▀▀▀▀▀   ▀███████████ ███     ███ ███       ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    █▄  ▀███████████   ███    ███ ███     ███ ███         ███    █▄  ▀███████████ 
███    ███   ███    ███   ███    ███ ███ ▄█▄ ███ ███▌    ▄   ███    ███   ███    ███ 
████████▀    ███    ███   ███    █▀   ▀███▀███▀  █████▄▄██   ██████████   ███    ███ 
             ███    ███                          ▀                        ███    ███ 

```

A powerful and flexible web crawler that recursively explores a website, extracts useful data (URLs, images, scripts, forms, etc.), and displays the structure of the pages. It allows you to perform content searches, download website resources, and export crawled URLs.


## Features

- **Recursive Crawling**: Explore all links on the website recursively to fully analyze its structure.
- **Custom Headers**: Add custom headers to all requests to handle specific functionality (e.g., authentication).
- **Random User-Agent**: Optionally use a random User-Agent to mimic requests from different browsers and avoid detection.
- **Search Content**: Search the crawled pages' content using regular expressions.
- **Export URLs**: Export all crawled URLs into a text file for further analysis or record-keeping.
- **Download Resources**: Download website resources (HTML, CSS, JavaScript, images, etc.) to a specified directory for offline use.
- **Redirection Handling**: Automatically handle and follow HTTP redirections during crawling.
- **Error Handling**: Provides clear feedback on the status of each page (e.g., success, redirects, errors).

## Installation

1. Clone the repository:
```bash
$ git clone https://github.com/matth200/CRAWLER
$ cd CRAWLER
$ python3 -m pip install -r requirements.txt
```

## Usage

### Command-Line Arguments:

- `--url <url>`: The URL of the website you want to crawl (required).
- `--headers <headers>`: A JSON string containing custom headers to include in each request (optional).
- `--random-agent`: Randomizes the user-agent for each request (optional).
- `--search <regex>`: A regular expression to search for specific content within the website (optional).
- `--download <directory>`: The directory where all website resources should be downloaded (optional).
- `-f`: Skip the user prompt for warnings and automatically proceed with the crawl (optional).
- `--export-urls <file>`: Export all crawled URLs to the specified file (optional).

### Example Commands:

#### Basic Crawl:
```bash
$ python crawler.py --url https://example.com
```

#### Crawl with Random User-Agent:
```bash
$ python crawler.py --url https://example.com --random-agent
```

#### Crawl with Custom Headers:
```bash
$ python crawler.py --url https://example.com --headers '{"Authorization": "Bearer token"}'
```

#### Crawl with Search (Regex):
```bash
$ python crawler.py --url https://example.com --search ".{0,20}api.{0,20}"
```

#### Crawl and Download Resources:
```bash
$ python crawler.py --url https://example.com --download /tmp/example
```

#### Export URLs:
```bash
$ python crawler.py --url https://example.com --export-urls /tmp/exported_urls.txt
```

### Output:
- The crawler will display the website structure in a tree format, showing each page and its status (e.g., `200 OK`, `404 Not Found`).
- If the `--search` option is used, the pages where the search pattern was found will be displayed.
- If `--export-urls` is specified, all crawled URLs will be saved to the specified file.
- Warnings will be shown for custom headers or authentication tokens that might trigger unintended actions on the website.

### Example Output:
```bash
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

Unsupported Data:
 - javascript:void(0)
```

## TO DO

- **Option to Download Content**: Allow downloading full website content and resources for offline use.
- **JS Mapping**: If a `.js` file is found, check for its `.js.map` source map file to gather more debugging data.
- **Highlight Specific Data**: Mark data such as localhost URLs, `127.0.0.1`, subdomains, and more.
- **Extract Comments**: Collect HTML and React comments, or any other client-side comments found.
- **Detect PHP Code**: Identify and log PHP code within the crawled pages, with details on where it was found.
- **API Detection in JavaScript**: Search for possible API endpoints inside compiled JavaScript files.
- **Extract Meta-Data**: Collect metadata such as alt text on images and other relevant file information.
- **Multithreading Support**: Implement multithreading to improve crawl performance.
- **Advanced Error Handling**: Enhance error handling and retries for failed requests.

## Notes

This crawler is designed for educational purposes and should be used responsibly. Always respect a website's `robots.txt` file and terms of service.

Be cautious when crawling sites with custom headers or authentication tokens to avoid unintentionally triggering actions that could negatively affect the website.

By using this tool, you acknowledge your responsibility to ensure that your crawling activities are ethical and legal.