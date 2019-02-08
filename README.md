#OpenDiffIt - (Work in Progress)

This project will help monitor when documents (like PDFs) have been modified or new files have been added and flags them for review.

Using server logs or google analytics create a spreadsheet that contains the `url` where the document resides and a `count` for number of downloads.

This project will analyze that spreadsheet and the files referenced in it by:

1. Creating a unique fingerprint for each document.
2. Flagging modified files when the fingerprint has changed.
3. Flagging new files added since the last report.

Then a human can use that data to review flagged documents for accessibility.

__Assumptions:__

- The existing files are accessible.
- You want to ensure new and modified files are accessible.
- You only want to check files that have been downloaded.