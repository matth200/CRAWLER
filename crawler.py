#!/bin/python3
import requests
import re
from bs4 import BeautifulSoup
import argparse
import os
from urllib.parse import urlsplit
from live import LoadingBar
from colorama import Fore
import json


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

Made by Mattheo. D 
          """)

parser = argparse.ArgumentParser(prog="CRAWLER", description="Create a Tree of the webpage with all the information you got from one page")
parser.add_argument("--url", required=True, help="The url of the page you wanna analyse")
parser.add_argument("--headers")

display_head()

args = parser.parse_args()

#headers = json.parse(args.headers)


trees = {}
queues = []
trash_links = []

# def split_url(url):
#     rep = re.findall("(https?://[^/]+)(/.*)?", url)
#     if len(rep) == 1:
#         return rep[0]
#     return None
def split_url(url):
    """
    Splits a URL into its base (scheme + domain) and relative path.

    :param url: The full URL to split.
    :return: A tuple (base_url, relative_path) or None if the input is invalid.
    """
    try:
        parsed = urlsplit(url)  # Parse the URL into components
        base_url = f"{parsed.scheme}://{parsed.netloc}"  # Construct the base URL
        relative_path = parsed.path if parsed.path else "/"
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
    
    return result


def rel2url(original_url, original_relative):
    absolute, relativeWithOption = split_url(original_url)
    relative, option = splitOptionOnUrl(relativeWithOption)
    rel = rel2rel(os.path.dirname(os.path.normpath(relative)), original_relative)
    return absolute+rel+option

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
    return isItNew

absolute, relative = split_url(args.url)
addTree(relative)
queues = [relative]
original = absolute


#get all the link a (relative/absolute)
def get_all_link(html, original_absolute, original_relative):
    global trash_links, queues
    links_result = []
    relatives_result = []


    links_abs = re.findall(r"https?://(?:[a-zA-Z0-9-_]+\.?)+[a-zA-Z0-9-_]+(?::[0-9]{1,5})?(?:/[^\"' ]*)?", html)
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
                    queues.append(relative)
                relatives_result.append(relative)
            

    # print(relatives_result)
    # print(links_result)
    return (relatives_result, links_result)



#get all the image (relative/absolute)
#get all the script (relative/absolute)
#get all the comment (relative/absolute)
#get all the form
#get by redirection

def get_page(url):
    absolute, relativeWithOption = split_url(url)
    relative, option = splitOptionOnUrl(relativeWithOption)
    addTree(relative)

    rep = requests.get(url,verify=False, allow_redirects=False)
    if rep.status_code in [301, 302, 303, 307, 308]:
        #analyse even if it's a redirection
        absolute,relative = split_url(url)
        redirection_relative = rel2rel(os.path.dirname(os.path.normpath(relative)), rep.headers['Location'])
        addTree(redirection_relative)
        redirection = absolute+redirection_relative
    #test if everything is alright
    html = rep.text
    get_all_link(html, absolute, os.path.dirname(os.path.normpath(relative)))

def display_tree(d, prefix=""):
    """
    Recursively display a dictionary as a tree structure.

    :param d: The dictionary representing the tree structure.
    :param prefix: The string prefix for the current level of the tree.
    """
    for key, value in d.items():
        if isinstance(value, dict):  # If it's a folder
            print(f"{prefix}📂 {key}")
            display_tree(value, prefix + "   ")  # Recurse with increased indentation
        else:  # If it's a file
            print(f"{prefix}📄 {key}")

def display_liste(liste):
    for elt in liste:
        print(" - "+elt)


#get_page(args.url)
bar = LoadingBar(100, prefix="Processing", length=40, color=Fore.MAGENTA)

max_steps = 0
# main loop with queues
while True:
    if len(queues) >= 1:
        current = queues[0]
        url = original+current
        get_page(url)
        max_steps = max(len(queues), max_steps)
        bar.setTotal(max_steps)
        #print(max_steps - len(queues))
        bar.update(max_steps - len(queues))
        del queues[0]
        continue
    break

bar.finish()

print("The trees of the website:")
display_tree(trees)
print("Links not belonging to the page: ")
display_liste(trash_links)
print("Queues:")
display_liste(queues)


# url = absolute+queues[0]
# print(url)
# rep = requests.get(url, allow_redirects=False)

# if rep.status_code in [301, 302, 303, 307, 308]:
#     #analyse even if it's a redirection
#     print(rep.text)
#     absolute,relative = split_url(url)
#     redirection_relative = rel2rel(os.path.dirname(relative), rep.headers['Location'])
#     addTree(redirection_relative)
#     redirection = absolute+redirection_relative
#     print(f"Redirected to: {redirection}")
# else:
#     print("No redirection occurred.")