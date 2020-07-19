import argparse, bs4, collections, os, requests, colorama

parser = argparse.ArgumentParser()
parser.add_argument("--dir_for_files")
args = parser.parse_args(["--dir_for_files", "tb_tabs"])
dir_name = args.dir_for_files

shortcut_list = []
command_list = ["back", "exit"]
visited_stack = collections.deque()
current_display = None

def create_shortcut(url_input):
    return url_input[8:].rsplit(".", 1)[0]

def create_tab(shortcut, url_variable):
    with open(f"{dir_name}/{shortcut}.txt", "w") as new_tab:
        new_tab.write(url_variable)

def update_display():
    current_display = url_input
    visited_stack.append(current_display)

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

while True:
    url_input = input()
    if url_input == "exit":
        break
    if url_input == "back":
        try:
            url_input = visited_stack.pop()
        except(IndexError):
            continue

    if url_input in shortcut_list:
        with open(f"{dir_name}/{shortcut}.txt", "r") as download_page:
            print(download_page.read())
        update_display()
        continue

    if url_input[0:8] != 'https://':
        url_input = 'https://' + url_input

    try:
        server_response = requests.get(url_input)
    except requests.exceptions.ConnectionError:
        print("Error: Incorrect URL")
        continue
    update_display()

    raw_html = bs4.BeautifulSoup(server_response.text, features="html.parser")
    for tag in raw_html.find_all('a'):
        tag.insert_before(colorama.Fore.BLUE)
        tag.insert_after(colorama.Fore.RESET)
    print(raw_html.get_text())

    shortcut = create_shortcut(url_input)
    if shortcut not in shortcut_list:
        shortcut_list.append(shortcut)
        create_tab(shortcut, raw_html.get_text())

