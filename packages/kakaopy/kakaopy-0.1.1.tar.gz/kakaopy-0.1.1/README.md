# kakaopy

## Usage

1. from kakaopy import kakaopy

```py
from kakaopy import kakaopy
```

2. set your REST_API_KEY

```py
setHeader('YOUR_REST_API_KEY')
```

3. make object (e.g. doc, vedio, image, book, blog, cafe, etc)

```
doc1 = kakaopy.doc()
```

4. (option) setting object option (e.g. size, page, sort, etc")

```py
doc1.setSort("racency")
```

5. search or save file.json in path : object.search(query) or object.save(query, path)

```py
doc1.search("python")
doc1.save(query = "web crawling", path = "web.json")
```
