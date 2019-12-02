#!/usr/bin/env python
# encoding: utf-8

from urllib.parse import urlparse
import json
import re
import sys
import unittest


def url_validator (url):
    """validate the format of a URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


class TestVerifyDatasets (unittest.TestCase):
    ALLOWED_FIELDS = set([
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

    PAT_ID_FORMAT = re.compile(r"^dataset\-(\d+)$")

    PAT_LEADING_SPACE = re.compile(r"^\s.*")
    PAT_TRAILING_SPACE = re.compile(r".*\s$")


    def setUp (self):
        """load the dataset list"""
        self.datasets = []
        filename = "datasets.json"
        #filename = "test.json"

        with open(filename, "r") as f:
            self.datasets = json.load(f)


    def test_file_loaded (self):
        print("\n{} datasets loaded".format(len(self.datasets)))
        self.assertTrue(len(self.datasets) > 0)


    def test_has_required_fields (self):
        for dataset in self.datasets:
            if not set(["id", "title", "provider"]).issubset(dataset.keys()):
                raise Exception("{}: missing required fields".format(dataset["id"]))


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
                if key not in self.ALLOWED_FIELDS:
                    raise Exception("{}: unknown field name {}".format(dataset["id"], key))


    def test_unique_titles (self):
        title_set = set([])

        for dataset in self.datasets:
            title = dataset["title"]

            if title in title_set:
                raise Exception("{}: duplicate title {}".format(dataset["id"], title))
            else:
                title_set.add(title)


    def test_id_sequence (self):
        id_list = []

        for dataset in self.datasets:
            m = self.PAT_ID_FORMAT.match(dataset["id"])

            if not m:
                raise Exception("badly formed ID |{}|".format(dataset["id"]))
            else:
                id = int(m.group(1))

                if id in id_list:
                    raise Exception("duplicate ID |{}|".format(dataset["id"]))
                else:
                    id_list.append(id)


    def test_enum_providers (self):
        provider_set = set([])

        for dataset in self.datasets:
            provider_set.add(dataset["provider"])

        self.assertTrue(len(provider_set) > 0)
        print("\n providers:")

        for provider in sorted(list(provider_set)):
            print(provider)


    def has_clean_name (self, dataset, field):
        val = dataset[field]

        if self.PAT_LEADING_SPACE.match(val):
            raise Exception("{}: leading space in {} |{}|".format(dataset["id"], field, val))
        elif self.PAT_TRAILING_SPACE.match(val):
            raise Exception("{}: trailing space in {} |{}|".format(dataset["id"], field, val))


    def test_clean_names (self):
        for dataset in self.datasets:
            self.has_clean_name(dataset, "title")
            self.has_clean_name(dataset, "provider")
    
    def test_related_datasets (self):
        # if a dataset has an 'original' subdict that includes a `joins_to` field, check that the
        # dataset exists in datasets.json
        for dataset in self.datasets:
            if 'original' in dataset.keys():
                if 'joins_to' in dataset['original'].keys():
                    for ds in dataset['original']['joins_to']:
                        if ds not in list(set([f['id'] for f in self.datasets])):
                            raise Exception("Metadata for {} indicates that the dataset can be joined to {}, but {} is not in datasets.json. Please update datasets.json or fix the metadata field joins_to".format(dataset['id'], ds,ds))
                


if __name__ == "__main__":
    unittest.main()
