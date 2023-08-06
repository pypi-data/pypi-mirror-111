# youtea

## Install:
```
pip install youtea
```

Along the way depends on the requests library
```
pip install requests
```

## Example:
```py
gg = input("link: ")
print(f"\
like: {youtea.like(gg)}\n\
dislike: {dislike(gg)}\n\
views: {view(gg)}\n\
channel name: {channel_name(gg)}\n\
title video: {title(gg)}\n\
channel link: {channel_link(gg)}\n\
description: {description(gg)}\
")
```
