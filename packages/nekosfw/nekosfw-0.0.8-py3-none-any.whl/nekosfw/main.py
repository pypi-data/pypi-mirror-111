import enum
import aiohttp
import asyncio


class ImageType(enum.Enum):
    """Enums To Get The Type Of Image
    """
    Waifu = 'waifu'
    Kitsune = 'kitsune'
    Neko = 'neko'
    Kemonomimi = "kemonomimi"
    Foxgirl = "foxgirl"


async def getImage(imageType: ImageType) -> str:
    """[summary]

    Args:
        imageType (ImageType): Image Type You Want To Get 

    Raises:
        Exception: Bad request 400
        Exception: Request failed with some other reason

    Returns:
        str: link for the image
    """
    baseUrl = f"https://crza.dev/api/neko-sfw?image={imageType.value}"
    async with aiohttp.ClientSession() as client:
        async with client.get(baseUrl) as response:
            statusCode = response.status
            if statusCode == 200:
                r: dict = await response.json()
                imageLink = r.get('url')
                if not (imageLink is None or imageLink == "None" or imageLink == ""):
                    return(imageLink)

            elif statusCode == 429:
                headers = response.headers
                limitTimeReset = int(headers.get('Retry-After'))
                await asyncio.sleep(limitTimeReset)
                return await getImage(imageType)

            elif statusCode == 400:
                r: dict = await response.json()
                errMessage = r.get('message')
                raise Exception(
                    f"Couldn't fetch the image,\nResponse code : {statusCode}\nresponse: {errMessage}")

            else:
                raise Exception(
                    f"Request failed with status code : {statusCode}")

# Example To Get A Random SFW Foxgirl Image
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(getImage(ImageType.Foxgirl))
