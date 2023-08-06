# HttpClientMultipart

## Description

This package implement client to upload file using HTTP multipart.

## Requirements
This package require :
 - python3
 - python3 Standard Library

## Installation
```bash
pip install HttpClientMultipart
```

## Usages

### Command line

```bash
HttpMultipart -h                                                                                             # Print help message
HttpMultipart --help                                                                                         # Print help message
HttpMultipart -u "http://example.com/post/file"
python3 -m HttpMultipart --url "http://example.com/post/file"                                                # Using module command line
python3 HttpMultipart.pyz -H "Referer:http://example.com/" "Cookie:S=123" -u "http://example.com/post/file"  # Using python executable file, add headers
HttpMultipart --add-headers "Referer:http://example.com/" "Cookie:S=123" -u "http://example.com/post/file"   # Add headers
HttpMultipart -p "submit:Upload" -u "http://example.com/post/file"                                           # Add simple field
HttpMultipart --add-parameters "submit:Upload" -u "http://example.com/post/file"                             # Add simple field
HttpMultipart -f "/home/user/test.csv" -u "http://example.com/post/file"                                     # Add file
HttpMultipart --files-path "/home/user/test.csv" -u "http://example.com/post/file"                           # Add file
```

### Python script

```python
from HttpClientMultipart import Multipart
from urllib.request import Request, urlopen

multipart = Multipart()

response = urlopen(
    Request("http://example.com/post/file",
        headers={'Content-Type': multipart.content_type},
        data=multipart.build_multipart([("SubmitButton", "Upload file")], [("file", "test.csv", "/home/user/test.csv")]),
    )
)

print(response.read())
```

## Links
 - [Pypi](https://pypi.org/project/HttpClientMultipart)
 - [Github](https://github.com/mauricelambert/HttpClientMultipart)
 - [Documentation](https://mauricelambert.github.io/info/python/code/HttpClientMultipart.html)
 - [Python executable](https://mauricelambert.github.io/python/code/HttpClientMultipart.pyz)

## License
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).