# NEKOSFW

Developed by Crian69 (c) 2021

## Installing The Package

```python
pip install nekosfw
```

## Examples of How To Use

Initializing the image type to receive

```python
from nekosfw import ImageType

imagetype = ImageType.Foxgirl

# Other Code
```

All the currently available image types are:

<ol>
<li>Waifu</li>
<li>Kitsune</li>
<li>Neko</li>
<li>Kemonomimi</li>
<li>Foxgirl</li>
</ol>

Getting the image link

```python
from nekosfw import ImageType
from nekosfw import getImage
import asyncio

async def main():
    imagetype = ImageType.Foxgirl
    imageUrl = await getImage(imagetype)
    return imageUrl

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(main())

# Return the image url
```
