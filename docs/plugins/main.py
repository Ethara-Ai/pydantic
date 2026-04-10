from __future__ import annotations as _annotations

import json
import logging
import os
import re
import textwrap
from pathlib import Path
from textwrap import indent

import autoflake
import pyupgrade._main as pyupgrade_main  # type: ignore
import requests
import tomli
import yaml
from build.__main__ import (
    build_package,
)  # Might be private, but there's currently no public API to programmatically build wheels..
from jinja2 import Template  # type: ignore
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from packaging.version import Version

logger = logging.getLogger('mkdocs.plugin')
THIS_DIR = Path(__file__).parent
DOCS_DIR = THIS_DIR.parent
PROJECT_ROOT = DOCS_DIR.parent


try:
    from .conversion_table import conversion_table
except ImportError:
    # Due to how MkDocs requires this file to be specified (as a path and not a
    # dot-separated module name), relative imports don't work:
    # MkDocs is adding the dir. of this file to `sys.path` and uses
    # `importlib.spec_from_file_location` and `module_from_spec`, which isn't ideal.
    from conversion_table import conversion_table

# Start definition of MkDocs hooks


def on_pre_build(config: MkDocsConfig) -> None:
    """
    Before the build starts.
    """
    pass


def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files) -> str:
    """
    Called on each file after it is read and before it is converted to HTML.
    """
    pass


# End definition of MkDocs hooks


def add_changelog() -> None:
    pass


def add_mkdocs_run_deps(site_url: str) -> None:
    # set the pydantic, pydantic-core, pydantic-extra-types versions to configure for running examples in the browser
    pass


MIN_MINOR_VERSION = 9
MAX_MINOR_VERSION = 13


def upgrade_python(markdown: str) -> str:
    """
    Apply pyupgrade to all Python code blocks, unless explicitly skipped, create a tab for each version.
    """
    pass


def _upgrade_code(code: str, min_version: int) -> str:
    pass


def insert_json_output(markdown: str) -> str:
    """
    Find `output="json"` code fence tags and replace with a separate JSON section
    """
    pass


def get_orgs_data() -> list[dict[str, str]]:
    pass


tile_template = """
<div class="tile">
  <a href="why/#org-{key}" title="{name}">
    <img src="logos/{key}_logo.png" alt="{name}" />
  </a>
</div>"""


def render_index(markdown: str, page: Page) -> str | None:
    pass


def render_why(markdown: str, page: Page) -> str | None:
    pass


def render_pydantic_settings(markdown: str, page: Page) -> str | None:
    pass


def _generate_table_row(col_values: list[str]) -> str:
    pass


def _generate_table_heading(col_names: list[str]) -> str:
    pass


def build_schema_mappings(markdown: str, page: Page) -> str | None:
    pass


def build_conversion_table(markdown: str, page: Page) -> str | None:
    pass


def devtools_example(markdown: str, page: Page) -> str | None:
    pass


experts_template = Template(
    """
<div class="user-list user-list-center">
    {% for user in people.experts %}
    <div class="user">
        <a href="{{ user.url }}" target="_blank">
            <div class="avatar-wrapper">
                <img src="{{ user.avatarUrl }}"/>
            </div>
            <div class="title">@{{ user.login }}</div>
        </a>
        <div class="count">Questions replied: {{ user.count }}</div>
    </div>
    {% endfor %}
</div>
"""
)

most_active_users_template = Template(
    """

<div class="user-list user-list-center">
    {% for user in people.last_month_active %}
    <div class="user">
        <a href="{{ user.url }}" target="_blank">
            <div class="avatar-wrapper">
                <img src="{{ user.avatarUrl }}"/>
            </div>
            <div class="title">@{{ user.login }}</div>
        </a>
        <div class="count">Questions replied: {{ user.count }}</div>
    </div>
    {% endfor %}
</div>
"""
)

top_contributors_template = Template(
    """
<div class="user-list user-list-center">
    {% for user in people.top_contributors %}
    <div class="user">
        <a href="{{ user.url }}" target="_blank">
            <div class="avatar-wrapper">
                <img src="{{ user.avatarUrl }}"/>
            </div>
            <div class="title">@{{ user.login }}</div>
        </a>
        <div class="count">Contributions: {{ user.count }}</div>
    </div>
    {% endfor %}
</div>
"""
)

top_reviewers_template = Template(
    """
<div class="user-list user-list-center">
    {% for user in people.top_reviewers %}
    <div class="user">
        <a href="{{ user.url }}" target="_blank">
            <div class="avatar-wrapper">
                <img src="{{ user.avatarUrl }}"/>
            </div>
            <div class="title">@{{ user.login }}</div>
        </a>
        <div class="count">Reviews: {{ user.count }}</div>
    </div>
    {% endfor %}
</div>
"""
)

maintainers_template = Template(
    """
<div class="user-list user-list-center">
    {% for user in people.maintainers %}
    <div class="user">
        <a href="{{ user.url }}" target="_blank">
            <div class="avatar-wrapper">
                <img src="{{ user.avatarUrl }}"/>
            </div>
            <div class="title">@{{ user.login }}</div>
        </a>
    </div>
    {% endfor %}
</div>
"""
)


def populate_pydantic_people(markdown: str, page: Page) -> str | None:
    pass
