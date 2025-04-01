# NCFBLA Programs
CTSO IT tech support is here!!!!

The following files are in the `.gitignore` file and should NOT be checked into the repo:
* `input/` directory
    * Contains files like `members.csv`, `scores.csv`, `body.txt`
* `rubrics/` directory
* `sender_info.txt` file

They are not checked into the repo for privacy reasons.

## Setup

If you want to send emails yourself, clone the repo locally and add the file `sender_info.txt`. make it so the first line is the email, and the second line is the app password (you generate this through google account, it's 16 characters; look it up)

so sender_info.txt could look like:
```
mahiremran7@gmail.com
abcd efgh ijkl mnop
```

Note you probably have to set up python environment + run `pip install` for certain libraries

Sending emails WILL take a while to run; this is because there's a 5s wait in between each API request

You will likely want to make test files that are YOUR rubric PDFs/emails/test scores, as well as a few friends to test team events. Formats for files like the rubrics change over time and the code may need to be adjusted accordingly.

So when you run it, update the methods to use those test files (ex: `input/scores_test.csv`). 
* You can always use `input/members.csv` since it's just all the NCFBLA members and doesn't have any stakes of sending emails. But you will have to update this CSV for the new year's members.

## File Descriptions

* `deca_pdfs.py` isn't important and code is deprecated
* `fbla_rubrics.py` is for sending out emails of fbla rubrics (put rubric pdfs in `rubrics/` directory, delete all old rubrics).
    * `send_objtest_emails` is used for sending out objective test emails. Assumes:
        * `input/members.csv` exists and contains info on names + emails
        * `input/scores.csv` exists and contains info on people's objective test scores
        * see the method docstrings for more info on formatting.
    * `send_rubrics` is used for sending our rubric emails, takes in directory with rubrics PDFS. Assumes:
        * `rubrics/` exists and contains all the FBLA rubrics
        * `rubrics_txt/` exists (you may have to add this folder manually)
        * `input/members.csv` exists and contains info on names + emails
        * See the method docstrings for more info on formatting.
* `prof_emails.py` was old code used to send out emails to UWB professors, could be used in future (can repurpose to send emails to ppl in general if needed)
    * Assumes `input/body.txt` exists and contains the body of the email to send out to people (right now professors)
