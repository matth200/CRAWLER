#!/bin/python3
from colorama import Back, Style, Fore
import requests
import re
import argparse
import os
from urllib.parse import urlsplit
import urllib3
urllib3.disable_warnings()
from live import LoadingBar
from colorama import Fore
import json
import random
import sys

def log(texte):
    with open("log.txt", "a+") as file:
        file.write(texte+"\n")


def display_warning(force):
    print("""
########################################################################
#                           ⚠ WARNING ⚠                               #
########################################################################
# The use of the argument '--headers' or certain authentication tokens #
# in your crawler could trigger unintended actions on the target site. #
#                                                                      #
# Double-check your headers and payloads to avoid harmful requests.    #
#                                                                      #
# Always test responsibly and avoid sending sensitive data.            #
########################################################################
    """)

    if not force:
        while True:
            response = input("Do you want to continue even if this can cause harm to the system ? (Y/n)\n")
            if response.lower() == "y" or response.lower() == "n":
                break
        if response == "n":
            print("Okay byebye...")
            sys.exit()
        print("You accepted the risk, let's continue!")

def display_head():
    print("""
 ▄████████    ▄████████    ▄████████  ▄█     █▄   ▄█          ▄████████    ▄████████ 
███    ███   ███    ███   ███    ███ ███     ███ ███         ███    ███   ███    ███ 
███    █▀    ███    ███   ███    ███ ███     ███ ███         ███    █▀    ███    ███ 
███         ▄███▄▄▄▄██▀   ███    ███ ███     ███ ███        ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███        ▀▀███▀▀▀▀▀   ▀███████████ ███     ███ ███       ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    █▄  ▀███████████   ███    ███ ███     ███ ███         ███    █▄  ▀███████████ 
███    ███   ███    ███   ███    ███ ███ ▄█▄ ███ ███▌    ▄   ███    ███   ███    ███ 
████████▀    ███    ███   ███    █▀   ▀███▀███▀  █████▄▄██   ██████████   ███    ███ 
             ███    ███                          ▀                        ███    ███ 

          """)

parser = argparse.ArgumentParser(prog="CRAWLER", description="Create a Tree of the webpage with all the information you got from one page")
parser.add_argument("--url", required=True, help="The url of the page you wanna analyse")
parser.add_argument("--headers", help="Add headers into all the request")
parser.add_argument("--random-agent", help="Makes the user agent random", action='store_true')
parser.add_argument("--search", help="Regex to search in all the website") # to do
parser.add_argument("--download", help="Specify a directory to download all the website content") # to do
parser.add_argument("-f", help="No need for input by the user, it will be okay for everything", action='store_true')
parser.add_argument("--export-urls", help="Export all the url that you have crawled")

display_head()

args = parser.parse_args()

headers = {}
user_agent = "crawler"
if args.headers:
    display_warning(args.f)
    headers = json.loads(args.headers)
if args.random_agent:
    with open("misc/user_agents.txt", "r") as file:
        user_agents = file.read().split("\n")
        if user_agents[-1] == "":
            user_agents = user_agents[:-1]
        choice = random.randint(0, len(user_agents)-1)
        user_agent = user_agents[choice]
        print("User-Agent ->", user_agent)


#get random user agent if needed
headers["user-agent"] = user_agent

trees = {}
information_tree = {}
searchs = [] # variable to store search parameter
queues = []
trash_links = []
trash_datas = []
current_index = 0
page_to_see = 1

# def split_url(url):
#     rep = re.findall("(https?://[^/]+)(/.*)?", url)
#     if len(rep) == 1:
#         return rep[0]
#     return None
# def split_url(url):
#     """
#     Splits a URL into its base (scheme + domain) and relative path.

#     :param url: The full URL to split.
#     :return: A tuple (base_url, relative_path) or None if the input is invalid.
#     """
#     try:
#         parsed = urlsplit(url)  # Parse the URL into components
#         base_url = f"{parsed.scheme}://{parsed.netloc}"  # Construct the base URL
#         relative_path = parsed.path if parsed.path else "/"
#         #log("split_url: {} -> {} {}".format(url, base_url, relative_path))
#         return base_url, relative_path
#     except Exception as e:
#         print(f"Error parsing URL: {e}")
#         return None
    

def search_on_data(search, data, page):
    global searchs
    regex = f'{search}'
    elts = re.findall(search, data, re.DOTALL | re.IGNORECASE)

    if len(elts) > 0:
        searchs.append({
            "data": elts,
            "page": page
        })

def split_url(url):
    """
    Splits a URL into its base (scheme + domain) and relative path.

    :param url: The full URL to split.
    :return: A tuple (base_url, relative_path) or None if the input is invalid.
    """
    try:
        url = url.strip()
        parsed = urlsplit(url)  # Parse the URL into components
        base_url = f"{parsed.scheme}://{parsed.netloc}"  # Construct the base URL
        if base_url == "://":
            base_url = ""
            relative_path = url
        else:
            relative_path = url[len(base_url):]
        return base_url, relative_path
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None

def isAbsolute(url):
    return re.match("^ *https?://", url) != None

def splitOptionOnUrl(url):
    rep = re.findall("^([^#?]+)(.*)$", url)
    if len(rep) == 1:
        return rep[0]
    return None


def rel2rel(original, relative):
    """
    Resolve a relative path against an original path.

    Parameters:
    - original (str): The base path, e.g., '/test/public/'.
    - relative (str): The relative path to resolve, e.g., '../hello.php'.

    Returns:
    - str: The resolved absolute path.
    """
    # Ensure the original path ends with a slash for proper joining
    if not original.endswith("/"):
        original += "/"
    
    # Normalize and join the paths
    result = os.path.normpath(os.path.join(original, relative))

    #log("rel2rel: {} {} -> {}".format(original, relative, result))
    
    return result


def rel2url(original_url, original_relative):
    absolute, relativeWithOption = split_url(original_url)
    relative, option = splitOptionOnUrl(relativeWithOption)
    rel = rel2rel(os.path.dirname(os.path.normpath(relative)), original_relative)
    result = absolute+rel+option
    #log(f"rel2url: {original_url} {original_relative} -> {result}")
    return result

def addTree(relative):
    global trees
    if relative[0] == "/":
        relative = relative[1:]
    relative = relative.split("/")
    current_level = trees
    isItNew = False
    for depth, path in enumerate(relative):
        #final depth
        if depth == len(relative)-1:
            if not path in current_level.keys():
                isItNew = True
                current_level[path] = {}
        else:
            if not path in current_level.keys():
                current_level[path] = {}
                isItNew = True
            current_level = current_level[path]
    #log(f"addTree: {relative}")
    return isItNew

absolute, relative = split_url(args.url)
addTree(relative)
queues = [relative]
original = absolute

def isDataRelativeOk(relative):
    # if you got a link like data: base64... or mailto: mattheo@test.fr or javascript: ...
    # Define a regex pattern to capture scheme and data
    scheme_pattern = re.compile(r'^([a-zA-Z]+) ?:(.+)', re.IGNORECASE)
    # Allow only "http, https" scheme, block others
    whitelist = ["http", "https", "ws", "wss"]
    match = scheme_pattern.match(relative)
    if match:
        scheme = match.group(1).lower()
        if scheme in whitelist:
            return True
        return False
    return True

#get all the link a (relative/absolute)
def get_all_link(html, original_absolute, original_relative):
    global trash_links, queues, page_to_see
    links_result = []
    relatives_result = []


    links_abs = re.findall(r"https?://(?:[a-zA-Z0-9-_]+\.?)+[a-zA-Z0-9-_]+(?::[0-9]{1,5})?(?:/[^\"' \n]*)?", html)
    for link in links_abs:
        absolute, relativeWithOption = split_url(link)
        # ou alors on trie autrement mais la
        # on essaye de garder uniquement les éléments d'une même page
        if absolute == original_absolute:
            links_result.append(link)
        else:
            if link not in trash_links:
                trash_links.append(link)
    


    # all src
    src_relative = re.findall(r"src *= *'([^']*)'", html)
    src_relative.extend(re.findall(r"src *= *\"([^\"]*)\"", html))


    # all href
    href_relative = re.findall(r"href *= *'([^']*)'", html)
    href_relative.extend(re.findall(r"href *= *\"([^\"]*)\"", html))


    # all action
    action_relative = re.findall(r"action *= *'([^']*)'", html)
    action_relative.extend(re.findall(r"action *= *\"([^\"]*)\"", html))

    # all from javascript 


    #sort all together
    lists = [action_relative, href_relative, src_relative]
    for list_relative in lists:
        for relative in list_relative:
            if isDataRelativeOk(relative):
                if isAbsolute(relative):
                    absolute, relativeWithOption = split_url(relative)
                    # ou alors on trie autrement mais la
                    # on essaye de garder uniquement les éléments d'une même page
                    if absolute == original_absolute:
                        links_result.append(relative)
                    else:
                        if relative not in trash_links:
                            trash_links.append(relative)
                else:
                    #relative link
                    relative = rel2rel(original_relative, relative)
                    if addTree(relative):
                        page_to_see+=1
                        queues.append(relative)
                    relatives_result.append(relative)
            else:
                trash_datas.append(relative)
            

    # print(relatives_result)
    # print(links_result)
    return (relatives_result, links_result)



#get all the image (relative/absolute)
#get all the script (relative/absolute)
#get all the comment (relative/absolute)
#get all the form
#get by redirection

def get_page(url):
    global queues, page_to_see, information_tree
    absolute, relativeWithOption = split_url(url)
    relative, option = splitOptionOnUrl(relativeWithOption)
    addTree(relative)

    rep = requests.get(url,headers=headers, verify=False, allow_redirects=False)
    redirection = False
    if rep.status_code in [301, 302, 303, 307, 308]:
        #analyse even if it's a redirection
        absolute,relative = split_url(url)
        #if isAbsolute(rep.headers['Location']):
        absolute_redirect,relative_redirect = split_url(rep.headers['Location'])
        redirection_relative = rel2rel(os.path.dirname(os.path.normpath(relative)), relative_redirect)

        if addTree(redirection_relative):
            page_to_see+=1
            queues.append(redirection_relative)
        redirection = absolute+redirection_relative
    #test if everything is alright
    #log(f"get_page: {url} -> {relativeWithOption}")
    information_tree[relativeWithOption] = {
        "url": url,
        "code": rep.status_code
    }
    if redirection:
        information_tree[relativeWithOption]["redirection"] = redirection
    html = rep.text
    if args.search:
        search_on_data(args.search, html, url)
    get_all_link(html, absolute, os.path.dirname(os.path.normpath(relative)))

def display_tree_old(d, prefix=""):
    """
    Recursively display a dictionary as a tree structure.

    :param d: The dictionary representing the tree structure.
    :param prefix: The string prefix for the current level of the tree.
    """
    for key, value in d.items():
        if isinstance(value, dict):  # If it's a folder
            print(f"{prefix}📂 {key}")
            display_tree_old(value, prefix + "   ")  # Recurse with increased indentation
        else:  # If it's a file
            print(f"{prefix}📄 {key}")

def display_tree(d,prec="/", prefix=""):
    """
    Recursively display a dictionary as a tree structure with arrows,
    distinguishing between files and folders.

    :param d: The dictionary representing the tree structure.
    :param prefix: The string prefix for the current level of the tree.
    """
    last_key = list(d.keys())[-1]  # Identify the last key to determine the arrow type
    for key, value in d.items():
        # Choose the arrow style based on whether this is the last item
        connector = "└──" if key == last_key else "├──"
        
        # Determine if the current item is a file or a folder
        if isinstance(value, dict) and value:  # Non-empty dictionary (folder)
            print(f"{prefix}{connector} 📂 {key}")
            sub_prefix = prefix + ("    " if key == last_key else "│   ")
            display_tree(value, prec+key+"/", sub_prefix)
        else:  # Empty dictionary or non-dictionary item (file)
            elt = prec+key
            if elt in information_tree.keys():
                color = Back.BLACK
                if "code" in information_tree[elt].keys():
                    if 200 <= information_tree[elt]["code"] < 300:
                        color = Back.GREEN
                    elif 300 <= information_tree[elt]["code"] < 400:
                        color = Back.BLUE
                    elif 400 <= information_tree[elt]["code"] < 500:
                        color = Back.RED
                    elif 500 <= information_tree[elt]["code"] < 600:
                        color = Back.MAGENTA
                print(f"{prefix}{connector} 📄 {key} --> {color} {information_tree[elt]} {Style.RESET_ALL}")
            else:
                print(f"{prefix}{connector} 📄 {key} --> {elt}")

def display_liste(liste):
    for elt in liste:
        print(" - "+elt)


#get_page(args.url)
bar = LoadingBar(100, prefix="Processing", length=40, color=Fore.MAGENTA)

max_steps = 0

print("Looking for all the pages of the website...")
# main loop with queues
while True:
    if len(queues) >= 1:
        current = queues[0]
        url = original+current
        get_page(url)
        current_index +=1
        max_steps = max(len(queues), max_steps)
        bar.setTotal(page_to_see)
        bar.update(current_index)
        del queues[0]
        continue
    break

bar.finish()

print("The trees of the website:")
display_tree(trees)
print("Links not belonging to the page: ")
display_liste(trash_links)
print("Trash datas not supported:")
display_liste(trash_datas)


if args.export_urls:
    print(f"Saving all the urls inside {args.export_urls}...")
    with open(args.export_urls, "w") as file:
        for url in information_tree.keys():
            file.write(url+"\n")

# print("Queues:")
# display_liste(queues)

def display_search():
    print("Searchs:")
    for elt in searchs:
        print(f"{Fore.CYAN}{elt['page']}{Style.RESET_ALL}")
        for found in elt['data']:
            print(f"> {found}")

if args.search:
    display_search()

#to debug
# for key in information_tree.keys():
#     print(f"{key} - {information_tree[key]}")