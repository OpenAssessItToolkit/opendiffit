# OpenDiffIt - (Work in Progress)

This project will help monitor when documents (like PDFs) have been added or modified on your server and flags them for review.


## Example usage:


### Prerequisite assets:

__Step 1. Use server logs or google analytics to create a .csv (spreadsheet) file. It should contain a column with a `url` header with the location of those files.__

_We also add a `count` column for number of downloads. The count can be used as a contributing factor for prioritizing certain files)._

file-list.csv

|url                        |count |
|---------------------------|------|
|https://cats.com/foo.pdf   |988   |
|https://dogs.com/bar.pdf   |786   |
|https://fish.com/baz.pdf   |235   |

-

__Step 2. Create that .csv report on regular intervals. It could be each month (or every day).__

OpenDiffIt will compare those files.


## Using OpenDiffIt:

__Step 3. Run `add_hash` on those two .csv files. It will analyze that remote file and create a unique fingerprint.__

```
python opendiffit/add_hash.py --input-file="file-list-january.csv" --output-file="file-list-january-hashed.csv"
```
`file-list.csv_hashed.csv`

|url                        |count | hash                                    |
|---------------------------|------|-----------------------------------------|
|https://cats.com/foo.pdf   |988   |822f21dca1925576c8a2c1d5eea470690356f800 |
|https://dogs.com/bar.pdf   |786   |c5c4459dcfa0fa37a8e77697fba5edc2c56zzzzz |
|https://fish.com/baz.pdf   |235   |dc44e6a2f1252b3d307cec61d142e3d77e5f53fx |

`file-list.csv_hashed-new.csv`

|url                        |count | hash                                    |
|---------------------------|------|-----------------------------------------|
|https://cats.com/foo.pdf   |903   |822f21dca1925576c8a2c1d5eea470690356f800 |
|https://dogs.com/bar.pdf   |702   |c5c4459dcfa0fa37a8e77697fba5edc2c5qqqqqq |
|https://fish.com/baz.pdf   |201   |dc44e6a2f1252b3d307cec61d142e3d77e5f53fx |
|https://birds.com/baz.pdf  |101   |3836ef7f58f69ad35223f0b3af21f5f154c2dab9 |

-

__Step 4. Run `idenfity_diffs` on those two files. It will add a column that indicates which files are the same, new, or updated since.__

```
python opendiffit/identify_diffs.py --old="old-file-list.csv" --new="new-file-list.csv" --diff="diff-report.csv"
```

`file-list.csv_hashed-diff.csv`

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