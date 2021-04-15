#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

# import re
import glob
import shutil
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_ROOT = os.path.join(ROOT, "src")
BUILD_ROOT = os.path.join(ROOT, "build")


def render(file, env, context):
    basename = os.path.basename(file)
    print(f"---- {basename}")
    with open(file) as fd:
        content = fd.read()

    template = env.from_string(content)
    output = template.render(context)

    with open(os.path.join(BUILD_ROOT, basename), "w") as fd:
        fd.write(output)


def build():
    print(f"building {ROOT} ...")
    shutil.rmtree(BUILD_ROOT, ignore_errors=True)
    shutil.copytree(src=os.path.join(SRC_ROOT, "root"), dst=os.path.join(BUILD_ROOT))

    env = Environment(
        loader=FileSystemLoader(os.path.join(ROOT, "templates")),
        undefined=StrictUndefined,
    )
    context = {}
    context["current_date"] = datetime.now().replace(microsecond=0).isoformat()

    all_pages = []
    for file in glob.glob(os.path.join(SRC_ROOT, "pages/*.html")):
        context["current_page"] = os.path.basename(file)
        all_pages.append(context["current_page"])

        render(file, env, context)

    context["all_pages"] = all_pages
    render(os.path.join(SRC_ROOT, "pages", "sitemap.xml"), env, context)

    print()


if __name__ == "__main__":
    build()
