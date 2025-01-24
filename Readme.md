# CRAWLER

Program designed to get all the natural resources of a website, download them, analyse them...

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
