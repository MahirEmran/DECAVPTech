# you guys suck
ctso it tech support is here

sender_info.txt is ignored in the `.gitignore` file. this is INTENTIONAL.

if you want to send emails yourself, clone the repo locally and add the file. make it so the first line is the email, and the second line is the app password (you generate this through google account, its 16 characters look it up)

so sender_info.txt could look like:
```
mahiremran7@gmail.com
abcd efgh ijkl mnop
```

then you can run whichever file you want to. note you probably have to set up python environment + run `pip install` for certain libraries

`deca_pdfs.py` isn't important that was for earlier in the year lmao
`fbla_rubrics.py` is for sending out emails of fbla rubrics (put rubric pdfs in `rubrics/` directory, delete all old rubrics)
`prof_emails.py` was old code used to send out emails to professors, could be used in future (can repurpose to send emails to ppl in general if needed)
