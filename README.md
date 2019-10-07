# RCDatasets

This repo provides the `datasets.json` file, used as "ground truth"
for knowledge graph work in ADRF and Rich Context.

For a diagram of how this dataset list fits within the overall ETL
workflow used to update the knowledge graph, see the OmniGraffle
source at `docs/kg_etl_workflow.graffle` in this repo.


## Managing Updates

Having a separate repo helps us manage changes carefully.
This is _metadata_ not data and serves it as the basis for
linking.
That requires auditing of any changes, to avoid breaking links
in the graph downstream from any update.

Consequently, each update must be handled through a 
[pull request](https://help.github.com/en/articles/about-pull-requests) 
and audited in a code review.

  1. work in a separate branch and update from master
  1. look for other PRs (work in progress) and note the IDs used
  1. request a range of up to 5 IDs on the `rich_context` channel on Slack
  1. make edits in your branch
  1. confirm through unit tests: `python test.py`

At that point, create a PR and have someone else on the team review it.

Also, don't commit code here except for consistency checks used on the
dataset list itself.


## Required Fields

At a minimum, each record in the `datasets.json` file must have these
required fields:

  * `provider` -- name of the _data provider_
  * `title` -- name of the dataset
  * `id` -- a unique sequential identifier

For the names, use what the data provider shows on their web page and
try to be as consise as possible.

When adding records:

  - add to the bottom of the file
  - increment the `id` number manually
  - make sure not to introduce multiple names for the same provider

Other fields that may be included:

  * `alt_title` -- list of alternative titles or abbreviations, aka "mentions"
  * `url` -- URL for the main page describing the dataset
  * `doi` -- a unique persistent identifier assigned by the data provider
  * `alt_ids` -- stored as a list, other unique identifiers (alternative DOIs, etc). The value should be written as a `URN` e.g, a new DOI would be written as `'doi:<doi>'`
  * `description` -- a brief (tweet sized) text description of the dataset
  * `date` -- date of publication, which may help resolve conflicting identifiers


## To Do 
### quality checks on dataset entries
* spot checks on urls, titles, etc
* unify naming conventioins
* is 'program data' a dataset? revisit after november workshop

### additions to test.py
* add check for commas within entries


### enrich `datasets.json` with additional metadata. 

The datasets enumerated in `datasets.json` may have additional metadata, which would be given to us by the data provider or client using the dataset.

These fields might include (but not limited to):
* `keywords` and `categories` - list of terms associated with the dataset
* `geographical coverage` - geography that the dataset covers, e.g New York State, Germany
* `temporal coverage`  - time period of the dataset. If the dataset is regularly released, e.g. the U.S. Census, the value could be 'decennial'
* `data steward` - person responsible for protecting and sharing the dataset - id should come from `data_stewards.json`  (not yet in existence)
* `customer` - client or partner who requested that the dataset be entered into our knowledge graph - id should come from `customers.json` (not yet in existence)
* `long_description` - longer form description of dataset
* `in_adrf` - boolean value indicating whether or not the dataset is in the ADRF
* `funder` - organization (could be the agency) that funded creation or dissemination of the dataset
