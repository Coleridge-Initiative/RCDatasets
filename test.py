#!/usr/bin/env python
#encoding: utf-8

from git import Repo
from pathlib import Path
from urllib.parse import urlparse
import codecs
import json
import re
import sys
import traceback
import unittest


def url_validator (url):
    """validate the format of a URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


class TestVerifyDatasets (unittest.TestCase):
    PROVIDERS_ALLOWED_FIELDS = set([
            "id",
            "title",
            "ror",
            "url"
            ])

    DATASETS_ALLOWED_FIELDS = set([
            "alt_ids",
            "alt_title",
            "date",
            "description",
            "doi",
            "id",
            "provider",
            "title",
            "url",
            "original"
            ])

    PAT_DATASET_ID_FORMAT = re.compile(r"^dataset\-(\d+)$")
    PAT_PROVIDER_ID_FORMAT = re.compile(r"^provider\-(\d+)$")

    PAT_LEADING_SPACE = re.compile(r"^\s.*")
    PAT_TRAILING_SPACE = re.compile(r".*\s$")


    def setUp (self):
        """load the dataset list
        """
        self.datasets = []
        self.providers = []

        with codecs.open(Path("datasets.json"), "r", encoding="utf8") as f:
            try:
                self.datasets = json.load(f)
            except Exception:
                traceback.print_exc()
                self.fail("datasets.json could not be read")

        with codecs.open(Path("providers.json"), "r", encoding="utf8") as f:
            try:
                self.providers = json.load(f)
            except Exception:
                traceback.print_exc()
                self.fail("providers.json could not be read")

        ## trace the entities in this branch

        try:
            repo = Repo(".")
            active_branch = repo.active_branch.name
        except:
            active_branch = "DETACHED_" + repo.head.object.hexsha

        with open(Path("trace.json"), "w") as f:
            trace = {
                "branch": active_branch,
                "commit": repo.head.object.hexsha,
                "datasets": sorted([ d["id"] for d in self.datasets ]),
                "providers": sorted([ p["id"] for p in self.providers ])
                }
            json.dump(trace, f, indent=4, sort_keys=True)


    def test_file_loaded (self):
        print("\n{} datasets loaded".format(len(self.datasets)))
        self.assertTrue(len(self.datasets) > 0)

        print("\n{} providers loaded".format(len(self.providers)))
        self.assertTrue(len(self.providers) > 0)


    def test_has_required_fields (self):
        for dataset in self.datasets:
            if not set(["id", "title", "provider"]).issubset(dataset.keys()):
                raise Exception("{}: missing required fields".format(dataset["id"]))

        for provider in self.providers:
            if not set(["id", "title"]).issubset(provider.keys()):
                raise Exception("{}: missing required fields".format(provider["id"]))


    def test_has_valid_url (self):
        for dataset in self.datasets:
            if "url" in dataset:
                url = dataset["url"]

                if url == "" or not url:
                    pass
                elif not url_validator(url):
                    raise Exception("{}: badly formed URL {}".format(dataset["id"], url))


    def test_each_field (self):
        for dataset in self.datasets:
            for key in dataset.keys():
                if key not in self.DATASETS_ALLOWED_FIELDS:
                    raise Exception("{}: unknown field name {}".format(dataset["id"], key))

        for provider in self.providers:
            for key in provider.keys():
                if key not in self.PROVIDERS_ALLOWED_FIELDS:
                    raise Exception("{}: unknown field name {}".format(provider["id"], key))


    def test_dataset_unique_titles (self):
        title_set = set([])

        for dataset in self.datasets:
            title = dataset["title"]

            if title in title_set:
                raise Exception("{}: duplicate title {}".format(dataset["id"], title))
            else:
                title_set.add(title)


    def test_provider_unique_titles (self):
        title_set = set([])

        for provider in self.providers:
            title = provider["title"]

            if title in title_set:
                raise Exception("{}: duplicate title {}".format(provider["id"], title))
            else:
                title_set.add(title)


    def test_dataset_id_sequence (self):
        id_list = []

        for dataset in self.datasets:
            m = self.PAT_DATASET_ID_FORMAT.match(dataset["id"])

            if not m:
                raise Exception("badly formed ID |{}|".format(dataset["id"]))
            else:
                id = int(m.group(1))

                if id in id_list:
                    raise Exception("duplicate ID |{}|".format(dataset["id"]))
                else:
                    id_list.append(id)


    def test_provider_id_sequence (self):
        id_list = []

        for provider in self.providers:
            m = self.PAT_PROVIDER_ID_FORMAT.match(provider["id"])

            if not m:
                raise Exception("badly formed ID |{}|".format(provider["id"]))
            else:
                id = int(m.group(1))

                if id in id_list:
                    raise Exception("duplicate ID |{}|".format(provider["id"]))
                else:
                    id_list.append(id)


    def test_dataset_enum_providers (self):
        refenced_providers = set([])

        for dataset in self.datasets:
            refenced_providers.add(dataset["provider"])

        if (len(refenced_providers) < 1):
            print("no providers get referenced")

        self.assertTrue(len(refenced_providers) > 0)
        
        known_providers = set([ p["id"] for p in self.providers ])
        unknowns = refenced_providers - known_providers

        if (len(unknowns) > 0):
            print("unknown providers: {}".format(sorted(unknowns)))

        self.assertTrue(len(unknowns) < 1)


    def has_clean_name (self, dataset, field):
        val = dataset[field]

        if self.PAT_LEADING_SPACE.match(val):
            raise Exception("{}: leading space in {} |{}|".format(dataset["id"], field, val))
        elif self.PAT_TRAILING_SPACE.match(val):
            raise Exception("{}: trailing space in {} |{}|".format(dataset["id"], field, val))


    def test_dataset_clean_names (self):
        for dataset in self.datasets:
            self.has_clean_name(dataset, "title")


    def test_provider_clean_names (self):
        for provider in self.providers:
            self.has_clean_name(provider, "title")


    def has_clean_ror(self, provider, field):
        if field in provider:

            val = provider[field]

            if len(val) == 0:
                raise Exception("{}: empty value in {} |{}|".format(provider["id"], field, val))
            elif self.PAT_LEADING_SPACE.match(val):
                raise Exception("{}: leading space in {} |{}|".format(provider["id"], field, val))
            elif self.PAT_TRAILING_SPACE.match(val):
                raise Exception("{}: trailing space in {} |{}|".format(provider["id"], field, val))


    def test_provider_clean_ror (self):
        for provider in self.providers:
            self.has_clean_ror(provider, "ror")


if __name__ == "__main__":
    unittest.main()
