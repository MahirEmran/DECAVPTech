import pandas as pd 
import smtplib
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import PyPDF2
import time


def get_member_info():
    df = pd.read_csv('fbla_input/members.csv')
    # members = {}
    # for a, b, c in zip(df['First Name'], df['Last Name'], df['Email']):
    #     if a + ' ' + b in members:
    #         raise Exception("Duplicate name " + a + ' ' + b + ' present in member list')
    #     members[a + ' ' + b] = c
    return {a+' '+b: c for a, b, c in zip(df['First Name'], df['Last Name'], df['Email'])}


def get_objtest_emails(filename):
    df = pd.read_csv(filename)
    results = {}
    for index, row in df.iterrows():
        group_name = row['Group Name']
        test_name = row['Name']
        attendees = row['Attendees']
        score = row['objective Score 1']
        if isinstance(attendees, str) and "; " in attendees:
            team_members = attendees.split("; ")
            team_info = f"{test_name}\n"
            for member in team_members:
                member_score = df[(df['Group Name'] == group_name) & (df['Name'] == test_name) & (df['Attendees'] == member)]['objective Score 1'].values
                if len(member_score) > 0:
                    team_info += f"{member}'s score: {member_score[0]}\n"
            team_info += f"Team Average: {score}\n"
            for member in team_members:
                if member not in results:
                    results[member] = ""
                results[member] += team_info + "\n"        
        else:
            if attendees not in results:
                results[attendees] = ""
            results[attendees] += f"{test_name}\n{attendees}'s score: {score}\n\n"
    return results


def send_objtest_emails(filename):
    members = get_member_info()
    emails = get_objtest_emails(filename)
    for k, v in emails.items():
        sender = ''
        password = ''
        with open('sender_info.txt') as f:
            lines = f.readlines()
            sender = lines[0]
            password = lines[1]
        subject = f'NCCC Objective Test Scores'
        msg = MIMEText(get_objtest_email_body(k, v))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = members[k]
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, [members[k]], msg.as_string())
        # Pauses program for 5s in between each email to not get timed out on requests
        time.sleep(5)

def get_objtest_email_body(name, scores):
    s = f'Hello {name},\n\n'
    s += f'This email contains your objective test score results for NCCC. If any of these were done with a team, you will see your team average and your other team members\' scores.\n\n'
    s += scores
    s += "Reply to this email if you have any questions or concerns. Thank you for competing at this conference!\n\n"
    s += "Sincerely,\nNorth Creek FBLA"
    return s

def convert_pdf_to_text(dir, out_dir):
    """
    Takes the PDF files from the path in dir and converts them to
    .txt files that are outputted in the path in out_dir
    """
    for filename in os.listdir(dir):
        pdf_path = dir + filename
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PdfReader object instead of PdfFileReader
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # Initialize an empty string to store the text
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        # Write the extracted text to a text file
        # filename[0:-4:1] removes the .pdf from name, adds .txt 
        with open(out_dir+filename[0:-4:1]+".txt", 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

def send_rubrics(members, path):
    errs = []
    emails = dict()
    for filename in os.listdir(path):
        
        names = get_names_from_rubric(path + filename)
        if names is None:
            errs.append("No names found in file: " + path + filename)
            continue
        for name in names:
            try:
                t = (members[name], name)
                if t not in emails:
                    emails[t] = list()
                emails[t].append(filename)
            except:
                errs.append("Name " + name + " not found in member email spreadsheet from rubric " + filename)
    send_rubric_emails(emails)
    for err in errs:
        print(err)


def send_rubric_emails(emails):
    """
    emails is a dictionary of tuple keys, where the tuple has the email and name. The value
    is a list of files (all rubrics) attached to that student.
    Ex: 
    {
    ('1099249@apps.nsd.org', 'Mahir Emran') : ['data-analysis_rubricjudge1.txt', 'data-analysis_rubricjudge2.txt']
    }
    """
    for key in emails:
        sender = ''
        password = ''
        # Gets the sender info from the file sender_info.txt
        # Remember this file should NOT be committed. It is in the .gitignore by default
        with open('sender_info.txt') as f:
            lines = f.readlines()
            sender = lines[0]
            password = lines[1]
        if not sender or not password:
            raise Exception("Sender or password do not exist")
        # Subject of the email
        subject = f'NCCC Results'
        print(key[1])
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = key[0]
        # Gets the body of the email to send to the person
        body = get_rubric_email_body(key[1], emails[key])
        msg.attach(MIMEText(body, 'plain'))
        # Attaches all the files on the email
        for f in emails[key]:
            # Replaces the .txt extension with the .pdf and gets the appropriate file
            # from the rubrics/ directory
            file_path = 'rubrics/' + f[0:f.index('.txt')] + ".pdf"
            with open(file_path, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=basename(file_path))
                part['Content-Disposition'] = f'attachment; filename="{basename(file_path)}"'
                msg.attach(part)
        # Sends the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, [key[0]], msg.as_string())
        # Pauses program for 5s in between each email to not get timed out on requests
        time.sleep(5)


def get_rubric_email_body(name, events):
    """
    Given an individual person and the events they've done (represented as file names),
    gets the content of the email to send them. Returns a String
    """
    msg = ""
    msg += f'Hello {name},\n\n'
    msg += "At this conference, you participated in the following events:\n\n"
    # Gets a set of unique event names (so no repeats) by using the file name
    # Ex: Data_Analysis-Final-Presentation_Entry1166654_Ansari,_Bansal,_Emran_Judge1.txt
    # turns into Data Analysis
    # Uses the dash and the underscore
    eventnames = {" ".join(event[:event.index("-")].split("_")) for event in events}
    for event in eventnames:
        msg += f'{event}\n'
    msg += f'\nAttached to this email are the rubric PDFs containing your scores and feedback from your judges. They are named accordingly with each event you participated in. If you competed in an event with a team, your teammates have also received the corresponding rubrics.\n\n'
    msg += f'Reply to this email with any questions you have. Do NOT attempt to contact your judges; there will be consequences for doing so.\n\n'
    msg += f'Thank you for competing at this conference!\n\n'
    msg += f'Sincerely,\n'
    msg += f'North Creek FBLA'
    return msg
    
def get_names_from_rubric(path):
    """
    Given a .txt file of a rubric (called path), returns a list
    of names (as Strings)
    Ex: ['Mahir Emran', 'Ritvik Bansal', 'Ibrahim Ansari']
    Assumes format is like FBLA rubric
    """
    names = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            # Revision: is reference for where the names are
            if line.startswith("Revision:"):
                s = line[8:]
                # Names are split like commas
                words = s.split(", ")
                for name in words:
                    # Uses set to filter to only alphabetic and space
                    # TODO: change to regex
                    chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")
                    clean_name = ''.join(filter(lambda c: c in chars, name))
                    names.append(clean_name)
                # Breaks since the first line with Revision: is the one that contains all the names
                break
    # Returns None if no names are found
    return names if len(names) != 0 else None


def main():
    """
    Main method runs functions for sending out emails
    """
    print("Starting")
    # Gets the dictionary mapping student name to email
    # Ex: { 'Mahir Emran': '1099249@apps.nsd.org', ...}
    members = get_member_info()
    print("Got members")
    # Deletes all old files in rubrics_txt/
    for file_name in os.listdir('rubrics_txt/'):
        file_path = os.path.join('rubrics_txt/', file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"Skipping non-file item: {file_path}")
    path = "rubrics_txt/"
    print("Making txt files")
    # Populates rubrics_txt directory with the PDF files
    convert_pdf_to_text('rubrics/', path)
    print("Finished making txt files")
    # Uses the mapping of people and the new text files to send emails out
    print("Sending emails")
    send_rubrics(members, path)
    print('Done')

    # Old code for sending objective test scores
    # TODO: Consolidate teams into one email. This involves recognizing individuals
    # in a team, so the email should contain the team average AND the individual scores
    # In other words, if a team takes an objective test, only one email should be sent; right now it is two
    # TODO: Consider grouping objective test scores into one email? So instead of above, I would get one
    # email with all my objective test scores (would contain team average and ONLY my individual)
    # send_objtest_emails('fbla_input/scores2.csv')


if __name__ == "__main__":
    main()
