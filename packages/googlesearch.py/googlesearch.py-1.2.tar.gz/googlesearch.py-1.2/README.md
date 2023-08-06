<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1200px-Google_%22G%22_Logo.svg.png" width="80px">

# Google Search Scrapper

## How To Use
- Create the code like this to get **results based on your query**.

```python
import google_search_py

# Use .search() to send query and get results from Google, Write The query inside the brackets

search = google_search_py.search("apple inc")
print(search)

# Output

{
    'title': 'Apple (India)', 
    'description': 'Discover the innovative world of Apple and shop everything iPhone, iPad, Apple Watch, Mac, and Apple TV, plus explore accessories, entertainment and expert device support.',
    'url': 'https://www.apple.com/in/', 
    'favicon': 'https://www.google.com/s2/favicons?domain=https://www.apple.com/in/'
}

```

<hr>

**MIT License | Copyright (c) 2021 Sijey**
