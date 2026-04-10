# pyright: reportUnknownMemberType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
from __future__ import annotations as _annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, cast

from bs4 import Tag
from typing_extensions import TypedDict

from pydantic import TypeAdapter

if TYPE_CHECKING:
    from mkdocs.config import Config
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page


class AlgoliaRecord(TypedDict):
    content: str
    pageID: str
    abs_url: str
    title: str
    objectID: str
    rank: int


records: list[AlgoliaRecord] = []
records_ta = TypeAdapter(list[AlgoliaRecord])
# these values should match docs/javascripts/search-worker.js.
ALGOLIA_APP_ID = 'KPPUDTIAVX'
ALGOLIA_INDEX_NAME = 'pydantic-docs'

# Algolia has a limit of 100kb per record in the paid plan,
# leave some space for the other fields as well.
MAX_CONTENT_LENGTH = 90_000


def get_heading_text(heading: Tag):
    pass


def on_page_content(html: str, page: Page, config: Config, files: Files) -> str:
    pass


ALGOLIA_RECORDS_FILE = 'algolia_records.json'


def on_post_build(config: Config) -> None:
    pass


def algolia_upload() -> None:
    pass


if __name__ == '__main__':
    if sys.argv[-1] == 'upload':
        algolia_upload()
    else:
        print('Run with "upload" argument to upload records to Algolia.')
        sys.exit(1)
