import argparse
import asyncio
import hashlib
from urllib.parse import urlsplit

import aiohttp

chunk_size = 1_024  # Set to 1 KB chunks


async def download_url(url, destination):
    print(f'Downloading {url}')
    file_hash = hashlib.sha256()
    with open(destination, 'wb') as file:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                total_bytes = int(response.headers['content-length'])
                received = 0
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    received += chunk_size
                    progress(received, total_bytes)
                    file_hash.update(chunk)
                    file.write(chunk)

    print(f'\r\nDownloaded {destination}, sha256: {file_hash.hexdigest()}')


def progress(downloaded, total):
    work_done = downloaded / total
    # inspired by: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(work_done * 50), work_done * 100), end="", flush=True)


def main():
    # get the URL from the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help='The URL to download')
    arguments = parser.parse_args()

    # get the filename from the URL
    url_parts = urlsplit(arguments.url)
    file_name = url_parts.path[url_parts.path.rfind('/') + 1:]

    # start the download async
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_url(arguments.url, file_name))


if __name__ == '__main__':
    main()
