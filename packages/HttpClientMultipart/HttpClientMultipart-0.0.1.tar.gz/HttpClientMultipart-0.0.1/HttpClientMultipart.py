#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implement client to upload file using HTTP multipart
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""This package implement client to upload file with HTTP"""

__version__ = "0.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """This package implement client to upload file using HTTP multipart"""
__license__ = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/HttpClientMultipart"

copyright = """
HttpClientMultipart  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
license = __license__
__copyright__ = copyright

print(copyright)

__all__ = ["Multipart"]

from argparse import ArgumentParser, Namespace
from urllib.request import urlopen, Request
from typing import Tuple, Sequence
from mimetypes import guess_type
from os.path import basename
import uuid

class Multipart:

    """This class build a multipart form-data from filename."""

    def __init__(self):
        self.boundary = uuid.uuid4().hex
        self.content_type = 'multipart/form-data; boundary=----{}'.format(self.boundary)

    def build_multipart(self, fields: Sequence[Tuple[str, str]], files: Sequence[Tuple[str, str, str]]) -> bytes:
        """ this function return the body from 
        fields (name, value) and files (name, filename, path)
        """

        body = b''
        for (name, value) in fields:
            body += (
                f'----{self.boundary}\r\n'
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f'{value}\r\n'
            ).encode()

        for (name, filename, path) in files:
            body += (
                f'----{self.boundary}\r\n'
                f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
                f'Content-Type: {guess_type(filename)[0] or "application/octet-stream"}\r\n\r\n'
            ).encode()
            with open(path, 'rb') as file:
                body += file.read() + b'\r\n'
        
        body += f'----{self.boundary}--\r\n'.encode()
        return body

def parser() -> Namespace:

    """This function parse command line arguments."""

    parser = ArgumentParser()
    parser.add_argument('--url', '-u', help="URL to send file.", required=True)
    parser.add_argument('--add-headers', '-H', nargs="+", default=[], help='Add headers, format: "Header-Name:Value".')
    parser.add_argument('--files-path', '-f', nargs="+", default=[], help='Files path, to add file in multipart "Field-Name:FilePath".')
    parser.add_argument('--add-parameters', '-p', nargs="+", default=[], help='Add parameters, format: "Parameter-Name:Value".')
    return parser.parse_args()

def main() -> None:

    """This function is used when this file is called from command line."""

    arguments = parser()

    headers = {}
    for header in arguments.add_headers:
        name, value = header.split(":", maxsplit=1)
        headers[name] = value

    fields = []
    for field in arguments.add_parameters:
        name, value = field.split(":", maxsplit=1)
        fields.append((name, value))

    files = []
    for file in arguments.files_path:
        name, path = file.split(":", maxsplit=1)
        files.append((name, basename(path), path))

    multipart = Multipart()
    headers['Content-Type'] = multipart.content_type

    response = urlopen(
        Request(arguments.url,
            headers=headers,
            data=multipart.build_multipart(fields, files),
        )
    )

    print(response.read())

if __name__ == "__main__":
    main()
