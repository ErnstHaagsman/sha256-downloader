import argparse
import asyncio
import hashlib
from urllib.parse import urlsplit

import aiohttp

chunk_size = 1024  # Set to 1 KB chunks


async def download_url(url, destination):
    print('Downloading {}'.format(url))
    file_hash = hashlib.sha256()
    with open(destination, 'wb') as file:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                received = 0
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    received += chunk_size
                    file_hash.update(chunk)
                    file.write(chunk)

    print('\r\nDownloaded {}, sha256: {}'.format(destination, file_hash.hexdigest()))


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
