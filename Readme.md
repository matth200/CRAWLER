# CRAWLER

Program designed to get all the natural resources of a website, download them, analyse them...

## TO DO

- Add the possibility to search inside the website a regex
- Adding the possibility to specify custom headers for every request
- Random agent possibility
- Option to download content
- If a file end with .js test the .js.map to see if this exists
- Option to output a file with the trees of the website
- Make "?" option being something we can highlight
- specify which data where belonging to
- Highlight particular data like localhost, 127.0.0.1, subdomains...
- Get all the comment (html comment, react comment...)
- Get all php code found and indicate in which file you got it
- Looking for api inside compiled javascript for client side javascript based (maybe just the same as research regex)
- Looking for meta-data on every files (on images for example)
- Make a pourcentage of each files in a website
- Option de limiter le nombre de page à aller voir
- Filter specific data in src, href like 'data:base64...', 'javascript:...', 'mailto: ...'
- Option of multithreading
- live updating trees
- put the absolute link in parenthesis and status code
- order keys inside the dictionnary
- filter directory and file with end files and depth inside the dictionnaray
- limit of the page seen 
- make possible to only accept the content of some kind of file 
- put a warning when using headers (because if the server is authenticated, it can cause problem)
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
