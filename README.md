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
  * `alt_ids` -- other unique identifiers (alternative DOIs, etc.)
  * `description` -- a brief (tweet sized) text description of the dataset
  * `date` -- date of publication, which may help resolve conflicting identifiers
