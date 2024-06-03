import time
from datetime import datetime, timedelta
from dateutil.parser import parse
import re
import json
import os

import requests
import bs4

import WebAutomation.RequestHelper as RequestHelper


class Post:
    def __init__(self, post_soup):
        self.id = post_soup.find("a", attrs={"title": "Reply to this post"}).text.strip()
        self.is_op = "opContainer" in post_soup["class"]
        self.username = post_soup.find("span", attrs={"class": "name"}).text.strip()
        self.timestamp = post_soup.find("span", attrs={"class": "dateTime"}).text.replace(f"No.{self.id}", "").strip()

        # backlink_container = post_soup.find("div", attrs={"class": "backlink"})
        # if backlink_container is not None:
        #     self.backlinks = [link["href"] for link in backlink_container.find_all("a")]
        # else:
        #     self.backlinks = []

        image_info = post_soup.find("div", attrs={"class": "fileText"})
        if image_info is not None:
            self.image_name = image_info.find("a").text
            self.image = image_info.find("a")["href"]
            self.image = self.image if not self.image.startswith("//") else f"http:{self.image}"
        else:
            self.image = None
            self.image_name = None

        self.content = [
            str(
                (element.text.strip() if element.name.lower().strip() != "br" else "\n")
                if type(element) is bs4.element.Tag
                else element.strip()
            )
            for element
            in post_soup.find("blockquote", attrs={"class": "postMessage"}).contents
            # if str(element.text if type(element) is bs4.element.Tag else element) != ""
        ]

    def __str__(self) -> str:
        username_text = f"{self.username}{' (OP)' if self.is_op else ''}"
        header_text = f"{username_text} {self.timestamp} No.{self.id}"

        post_components = [header_text]
        # if len(self.backlinks) > 0:
        #     post_components.append("Backlinks: " + ", ".join(self.backlinks))
        if self.image is not None:
            post_components.append(f"File: {self.image}")
        if len(self.content) > 0:
            post_components.append("".join(self.content))

        return "\n".join(post_components)

    def __iter__(self) -> dict:
        yield "id",  self.id
        yield "username",  self.username
        yield "timestamp",  self.timestamp
        # yield "backlinks",  self.backlinks
        yield "content",  self.content
        yield "image_name", self.image_name
        yield "image",  self.image


class Thread:
    def __init__(self, thread_soup, board_title=None):
        self.thread_soup = thread_soup
        self.id = thread_soup["id"]
        self.subject = thread_soup.find("span", attrs={"class": "subject"}).text
        self.board_title = board_title
        self.posts = [Post(post) for post in thread_soup.children if "adg-rects" not in post["class"]]

    def last_post_timestamp(self) -> datetime:
        str_update_dt = self.posts[-1].timestamp
        str_update_dt = str_update_dt[:str_update_dt.index("(")] + " " + str_update_dt[str_update_dt.index(")")+1:]
        return parse(str_update_dt)

    def calc_estimated_timeout(self) -> datetime:  # TODO: find relevant info to estimate timeout
        return self[-1].timestamp

    def save(self, local_path: str = os.getcwd()) -> None:
        thread_path = "".join([
            f"{local_path}/",
            f"{'' if self.board_title is None else (self.board_title.replace('/', '').strip() + '/')}",
            f"thread/",
            f"{self.id}"
        ])
        print(f"Saving thread to {thread_path}")
        if not os.path.exists(thread_path):
            os.makedirs(thread_path)

        thread_dict = {
            "id": self.id,
            "board": self.board_title,
            "subject": self.subject,
            "posts": [dict(post) for post in self]
        }

        json.dump(thread_dict, open(f"{thread_path}/thread.json", "w+"))

        if not os.path.exists(f"{thread_path}/images"):
            os.makedirs(f"{thread_path}/images")

        for image in self.get_images():
            image_name = image.split("/")[-1]
            full_image_path = f"{thread_path}/images/{image_name}"

            if not os.path.exists(full_image_path):
                with open(full_image_path, "wb+") as f:
                    f.write(requests.get(image).content)
                time.sleep(.5)

        print(f"Thread {self.id} saved")

    def get_images(self) -> list[str]:
        return [post.image for post in self.posts if post.image is not None]

    def get_thread_info(self) -> dict:
        return {
            "id": self.id,
            "board": self.board_title,
            "subject": self.subject,
            "post_count": len(self.posts),
            "image_count": len(self.get_images()),
            "last_post": self.last_post_timestamp(),
            "posts": [dict(post) for post in self]
        }

    def __str__(self) -> str:
        return "\n\n".join([str(post) for post in self.posts])

    def __repr__(self) -> str:
        return "\n".join([
            f"Subject: {self.subject}",
            f"Posts found: {len(self.posts)}",
            f"Images found: {len(self.get_images())}",
            f"Update time: {self.last_post_timestamp()}",
            f"Time since last post: {datetime.now() - self.last_post_timestamp()}"
        ])

    def __len__(self) -> int:
        return len(self.posts)

    def __getitem__(self, idx: int) -> Post:
        return self.posts[idx]

    # def __iter__(self) -> dict:
    #     yield "id", self.id
    #     yield "board", self.board_title
    #     yield "subject", self.subject
    #     yield "post_count", len(self.posts)
    #     yield "image_count", len(self.get_images())
    #     yield "last_post", self.last_post_timestamp()
    #     yield "posts", [dict(post) for post in self]


class Page:
    def __init__(self, url: str):
        print(f"Loading thread at url: {url}")
        self.url = url
        response = requests.get(url)
        if response.ok:
            self.page_soup = bs4.BeautifulSoup(response.content, "lxml")
        else:
            raise RequestHelper.NetworkError(response, f"Unable to load page: {response}")

        self.board_title = self.page_soup.find("div", attrs={"class": "boardTitle"}).text

        self.threads = [
            Thread(thread, self.board_title)
            for thread
            in self.page_soup.find_all("div", attrs={"class": "thread"})
        ]

    # def watch(self, save=True, local_path=None):
    #     if save:
    #         self.save(local_path)

    def __getitem__(self, idx: int) -> Thread:
        return self.threads[idx]


def search(board: str, query: str | None = None) -> dict:
    if query is not None:
        url = f"https://boards.4chan.org/{board}/catalog#s={query}"
    else:
        url = f"https://boards.4chan.org/{board}/catalog"

    response = requests.get(url)
    if response.ok:
        soup = bs4.BeautifulSoup(response.content, features="lxml")
        scripts = [
            script_element.text
            for script_element
            in soup.find("head").find_all("script")
            if "var catalog" in script_element.text
        ]
        if len(scripts) > 0:
            script = scripts[0]
        else:
            raise Exception("No scripts found.")
        match = re.findall(r"var catalog = ({.*[^{}]*})", script)[0].replace("var catalog = {", "{")
        return json.loads(match)
    else:
        raise RequestHelper.NetworkError(response)


def watch(url_list: list[str], save=True, local_path=None):
    response = requests.get("https://a.4cdn.org/boards.json")
    if not response.ok:
        RequestHelper.NetworkError(response)
    board_info = (json.loads(response.content))
    board_info["boards"] = {
        board["board"]: board
        for board
        in board_info["boards"]
    }

    while len(url_list) > 0:
        catalog = {}
        print(len(url_list), url_list)
        remove_list = []

        for idx, url in enumerate(url_list.copy()):
            thread_id = re.search(r"thread/[0-9]*", url)[0].replace("thread/", "")
            thread_board = re.search(r"[a-zA-Z]*/thread", url)[0].replace("/thread", "")
            if thread_board not in catalog:
                catalog.update({thread_board: search(thread_board)})
            if thread_id not in catalog[thread_board]['threads']:
                print(f"Thread {thread_id} not found")
                print()
                remove_list.append(idx)
                continue

            thread_pos = catalog[thread_board]['threads'][thread_id][thread_board]
            if thread_pos <= 130:
                print(f"Thread position: {thread_pos}")
            else:
                print(f"\033[91mThread position: {thread_pos}\033[00m")
            try:
                page = Page(url)
                print(f"Subject: {page[0].subject}")
                if len(page[0].posts) >= board_info["boards"][thread_board]["bump_limit"]:
                    print(f"\033[91mPosts found: {len(page[0].posts)}\033[00m")
                else:
                    print(f"Posts found: {len(page[0].posts)}")
                if len(page[0].get_images()) >= board_info["boards"][thread_board]["image_limit"]:
                    print(f"\033[91mImages found: {len(page[0].get_images())}\033[00m")
                else:
                    print(f"Images found: {len(page[0].get_images())}")
                print(f"Update time: {page[0].last_post_timestamp()}")
                print(f"Time since last post: {datetime.now() - page[0].last_post_timestamp()}")

                if save:
                    page[0].save(local_path)

            except Exception as e:
                print(e)
                remove_list.append(idx)

            print()
            time.sleep(1)

        for remove_idx in reversed(remove_list):
            del url_list[remove_idx]

        print("Round complete")
        if len(url_list) > 0:
            time.sleep(10)


def main():
    thread_urls = []
    watch(thread_urls)


if __name__ == "__main__":
    main()

