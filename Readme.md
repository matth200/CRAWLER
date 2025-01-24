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
$ python3 crawler.py --url https://localhost/

 ▄████████    ▄████████    ▄████████  ▄█     █▄   ▄█          ▄████████    ▄████████ 
███    ███   ███    ███   ███    ███ ███     ███ ███         ███    ███   ███    ███ 
███    █▀    ███    ███   ███    ███ ███     ███ ███         ███    █▀    ███    ███ 
███         ▄███▄▄▄▄██▀   ███    ███ ███     ███ ███        ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███        ▀▀███▀▀▀▀▀   ▀███████████ ███     ███ ███       ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    █▄  ▀███████████   ███    ███ ███     ███ ███         ███    █▄  ▀███████████ 
███    ███   ███    ███   ███    ███ ███ ▄█▄ ███ ███▌    ▄   ███    ███   ███    ███ 
████████▀    ███    ███   ███    █▀   ▀███▀███▀  █████▄▄██   ██████████   ███    ███ 
             ███    ███                          ▀                        ███    ███ 

          
Looking for all the pages of the website...
Processing [████████████████████████████████████████] 100.00% | - (267/267)
Completed!
The trees of the website:
├── 📂 public
│   ├── 📂 api
....
```
