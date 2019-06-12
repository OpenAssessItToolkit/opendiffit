# OpenDiffIt - (Work in Progress)

This project will help monitor when documents (like PDFs) have been added or modified on your server and flags them for review.


## Example usage:


### Prerequisite assets:

__Step 1. Get some data to create a .csv (spreadsheet) file. It should contain a column with a `url` header with the location of those files.__

You can get this data from:

a. Google analytics to create a CSV.

b. Parse Server logs and create a CSV.

c. Crawl the website with [OpenFindIt](https://github.com/OpenAssessItToolkit/openfindit) via Scrapy. This will also generate a CSV for you.

The only requirement is that there is a column with a `url` header to indicate the location of those files.

_In the example below we add a `count` column for number of downloads. The count can be used as a contributing factor for prioritizing certain files)._

`file-list-january.csv`

|url                        |count |
|---------------------------|------|
|https://cats.com/foo.pdf   |988   |
|https://dogs.com/bar.pdf   |786   |
|https://fish.com/baz.pdf   |235   |

`file-list-february.csv`

|url                        |count |
|---------------------------|------|
|https://cats.com/foo.pdf   |903   |
|https://dogs.com/bar.pdf   |702   |
|https://fish.com/baz.pdf   |201   |
|https://birds.com/baz.pdf  |101   |

-

__Step 2. Create that .csv report on regular intervals. It could be each month (or every day).__

OpenDiffIt will compare those files.


## Using OpenDiffIt:

__Step 3. Run `add_hash` on those two .csv files. It will analyze that remote file and create a unique fingerprint.__

```
python3 opendiffit/add_hash.py --input-file="file-list-january.csv" --output-file="file-list-january_hashed.csv"
```

Result: `file-list-january_hashed.csv`

|url                        |count | hash                                    |
|---------------------------|------|-----------------------------------------|
|https://cats.com/foo.pdf   |988   |822f21dca1925576c8a2c1d5eea470690356f800 |
|https://dogs.com/bar.pdf   |786   |c5c4459dcfa0fa37a8e77697fba5edc2c56zzzzz |
|https://fish.com/baz.pdf   |235   |dc44e6a2f1252b3d307cec61d142e3d77e5f53fx |


```
python3 opendiffit/add_hash.py --input-file="file-list-february.csv" --output-file="file-list-february_hashed.csv"
```

Result: `file-list-february_hashed.csv`

|url                        |count | hash                                    |
|---------------------------|------|-----------------------------------------|
|https://cats.com/foo.pdf   |903   |822f21dca1925576c8a2c1d5eea470690356f800 |
|https://dogs.com/bar.pdf   |702   |c5c4459dcfa0fa37a8e77697fba5edc2c5qqqqqq |
|https://fish.com/baz.pdf   |201   |dc44e6a2f1252b3d307cec61d142e3d77e5f53fx |
|https://birds.com/baz.pdf  |101   |3836ef7f58f69ad35223f0b3af21f5f154c2dab9 |

-

__Step 4. Run `idenfity_diffs` on those two files. It will add a column that indicates which files are the same, new, or updated since.__

```
python3 opendiffit/identify_diffs.py --old="file-list-january_hashed.csv" --new="file-list-january_hashed.csv" --diff="file-list_january-february_diffed.csv"
```

Result: `file-list_january-february_diffed.csv`

|url                        |count | hash                                    |diff    |
|---------------------------|------|-----------------------------------------|--------|
|https://cats.com/foo.pdf   |903   |822f21dca1925576c8a2c1d5eea470690356f800 |SAME    |
|https://dogs.com/bar.pdf   |702   |c5c4459dcfa0fa37a8e77697fba5edc2c5qqqqqq |UPDATED |
|https://birds.com/baz.pdf  |101   |3836ef7f58f69ad35223f0b3af21f5f154c2dab9 |NEW     |
|https://fish.com/baz.pdf   |201   |dc44e6a2f1252b3d307cec61d142e3d77e5f53fx |SAME    |

_Notice that `https://birds.com/baz.pdf` is a new file.  Notice that `https://dogs.com/bar.pdf` has a new hash. This indicates that the file has been modified since the last time the report ran._

-

__5. Then a human can use that `diff` column to review new and updated documents for accessibility.__

Testing a PDF for accessibility requires a real human to test for accessibility.

### Assumptions:

- The existing files are accessible.
- You want to ensure new and modified files are accessible.
- You only want to check files that have been downloaded.


# Other utilities

If the csv includes multiple domains there is an optional `split.py` script to divide the csv files into multiple files based on domain.

```
python3 opendiffit/split.py --old="file-list-january.csv" --new="file-list-january_hashed.csv" --diff="file-list_january-february_diffed.csv"
```