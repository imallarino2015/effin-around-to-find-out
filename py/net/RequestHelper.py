import requests
import random as rand

import PIL.Image


class NetworkError(Exception):
    def __init__(self, response: requests.models.Response, message=None):
        self.args = (message, )
        self.response: requests.models.Response = response


# TODO: Find method of generating user agent (currently randomly selecting from list)
def generate_user_agent():
    user_agent_list = [
        # "Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>"
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'
    ]
    
    user_agent = rand.choice(user_agent_list)
    print(user_agent)
    return user_agent


def generate_headers(referer: str = None, **kwargs):
    headers = {
        'Accept': '*',
        'Accept-Encoding': '*',
        'Accept-Language': '*',
        'Connection': 'keep-alive',
        'Dnt': '1',
        'Host': '*',
        'TE': '*',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': generate_user_agent()
    }

    if referer is not None:
        headers.update({'Referer': referer})

    headers.update(kwargs)

    return headers


def fetch_image(
        img_url: str,
        headers: dict = None,
        cookies: dict = None,
        retry: int = 3
) -> PIL.Image:
    print("Collecting image from " + str(img_url))

    for i in range(retry):
        try:
            response = requests.get(img_url, headers=headers, cookies=cookies, stream=True)
            break
        except Exception as e:
            if i == 2:
                print("Max retries reached")
                raise e
            else:
                print("Retrying...")
                continue
    print(str(response))

    if response.status_code == 200:
        return PIL.Image.open(response.raw)
    elif response.status_code == 404:
        raise NetworkError(response, f"Failed to load image. Status code: {response.status_code}")
    else:
        raise NetworkError(response, response.content)


def download_file(
        file_path: str,
        file_url: str,
        headers: dict = None,
        cookies: dict = None,
        retry: int = 3,
        timeout: int = None
) -> PIL.Image:
    print("Collecting image from " + str(file_url))

    for i in range(retry):
        try:
            response = requests.get(file_url, headers=headers, cookies=cookies, stream=True, timeout=timeout)
            break
        except Exception as e:
            if i == 2:
                print("Max retries reached")
                raise e
            else:
                print("Retrying...")
                continue
    print(str(response))

    if response.ok:
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    elif 400 <= response.status_code <= 499:
        raise NetworkError(response, f"Failed to load image. Status code: {response.status_code}")
    else:
        raise NetworkError(response, response.status_code)


async def download_file_async(
        file_path: str,
        file_url: str,
        headers: dict = None,
        cookies: dict = None,
        retry: int = 3,
        timeout: int = None
) -> PIL.Image:
    print("Collecting image from " + str(file_url))

    for i in range(retry):
        try:
            response = requests.get(file_url, headers=headers, cookies=cookies, stream=True, timeout=timeout)
            break
        except Exception as e:
            if i == 2:
                print("Max retries reached")
                raise e
            else:
                print("Retrying...")
                continue
    print(str(response))

    if response.ok:
        with open(file_path, "wb") as f:
            f.write(response.content)
        return await file_path
    elif 400 <= response.status_code <= 499:
        raise NetworkError(response, f"Failed to load image. Status code: {response.status_code}")
    else:
        raise NetworkError(response, response.status_code)


if __name__ == "__main__":
    pass
