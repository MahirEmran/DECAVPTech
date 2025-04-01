# you guys suck
ctso it tech support is here

sender_info.txt is ignored in the `.gitignore` file, as well as the directories input/, rubrics/, and rubrics_txt/. do NOT check these into the repo, because of privacy stuff

if you want to send emails yourself, clone the repo locally and add the file. make it so the first line is the email, and the second line is the app password (you generate this through google account, its 16 characters look it up)

so sender_info.txt could look like:
```
mahiremran7@gmail.com
abcd efgh ijkl mnop
```

then you can run whichever file you want to. note you probably have to set up python environment + run `pip install` for certain libraries

this will take a while to run; this is because there's a 5s wait in between each API request

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
        * see the method docstrings for more info on formatting.
* `prof_emails.py` was old code used to send out emails to professors, could be used in future (can repurpose to send emails to ppl in general if needed)
