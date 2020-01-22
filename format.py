#!/usr/bin/env python
#encoding: utf-8

from pathlib import Path
import codecs
import json
import re
import sys
import traceback


def reformat (path):
    with codecs.open(path, "r", encoding="utf8") as f:
        obj_list = json.load(f)

    obj_list = sorted(obj_list, key=lambda x: x["id"])

    with codecs.open(path, "wb", encoding="utf8") as f:
        json.dump(obj_list, f, indent=4, sort_keys=True, ensure_ascii=False)


def main ():
    reformat(Path("datasets.json"))
    reformat(Path("providers.json"))


if __name__ == "__main__":
    main()
