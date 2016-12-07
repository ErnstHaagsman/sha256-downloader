import asyncio
import hashlib
import aiohttp

chunk_size = 1_024  # Set to 1 KB chunks


async def download_url(url, destination):
    file_hash = hashlib.sha256()
    with open(destination, 'wb') as file:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    file_hash.update(chunk)
                    file.write(chunk)

    print(f'Downloaded {destination}, sha256: {file_hash.hexdigest()}')


def main():
    # Let's download the newest version of PyCharm (community for mac because it's smallest...
    # SHA256: 51f8d3e3f28c8d72c2eb33b28652b641e7f7a50ef3e054341dac5c64d4d7f792

    loop = asyncio.get_event_loop()
    print('Starting loop')
    loop.run_until_complete(download_url('https://download.jetbrains.com/python/pycharm-community-2016.3.dmg',
                                         'python-ce.dmg'))


if __name__ == '__main__':
    main()
