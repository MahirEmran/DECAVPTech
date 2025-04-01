import pandas as pd 
import smtplib
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import PyPDF2
import time


def send_rubrics(conf_name):
    """
    Sends rubric emails to members based on rubric PDFs and member information.

    Assumptions:
    - Member information is stored in 'input/members.csv'.
    - Rubric PDFs are stored in the 'rubrics/' directory.
    - Converted text files are stored in the 'rubrics_txt/' directory.
    - Email sender credentials are stored in 'sender_info.txt'.

    Parameters:
    - conf_name: Name of the conference (e.g., "NCCC 2025").
    """
    members = get_member_info('input/members.csv')
    print("Got members")
    # Deletes all old files in rubrics_txt/
    for file_name in os.listdir('rubrics_txt/'):
        file_path = os.path.join('rubrics_txt/', file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"Skipping non-file item: {file_path}")
    print("Making txt files")
    # Populates rubrics_txt directory with the PDF files
    convert_pdf_to_text('rubrics/', 'rubrics_txt/')
    print("Finished making txt files")
    # Uses the mapping of people and the new text files to send emails out
    print("Sending emails")

    errs = []
    # This dictionary maps the tuple of (email, name) to a list of files
    # Essentially, each file in that list is a rubric that the person has
    # The key is a tuple of the email and name
    emails = dict()
    for filename in os.listdir('rubrics_txt/'):
        names = get_names_from_rubric('rubrics_txt/' + filename)
        if names is None:
            errs.append("No names found in file: " + 'rubrics_txt/' + filename)
            continue
        for name in names:
            try:
                # For all the names found in the rubric, add the file to them
                t = (members[name], name)
                if t not in emails:
                    emails[t] = list()
                emails[t].append(filename)
            except:
                errs.append("Name " + name + " not found in member email spreadsheet from rubric " + filename)
    send_rubric_emails(emails, conf_name)
    for err in errs:
        print(err)


def send_objtest_emails(conf_name):
    """
    Sends emails to members with their objective test scores.

    Assumptions:
    - Member information is stored in 'input/members.csv'.
    - Objective test scores are stored in 'input/scores.csv'.
    - Email sender credentials are stored in 'sender_info.txt' (not committed to version control).

    Parameters:
    - conf_name: Name of the conference (e.g., "WLC 2025").
    """
    members = get_member_info('input/members.csv')
    emails = get_objtest_emails('input/scores.csv')
    for k, v in emails.items():
        print(k)
        sender = ''
        password = ''
        with open('sender_info.txt') as f:
            lines = f.readlines()
            sender = lines[0]
            password = lines[1]
        subject = f'{conf_name} Objective Test Scores'
        msg = MIMEText(get_objtest_email_body(k, v, conf_name))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = members[k]
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, [members[k]], msg.as_string())
        # Pauses program for 5s in between each email to not get timed out on requests
        time.sleep(5)


def get_member_info(path):
    """
    Given a filepath to a CSV file, returns a dictionary mapping
    the first and last name of a member to their email.
    
    CSV Format (members.csv):
    - Columns: 'First Name', 'Last Name', 'Email'
    - Example:
        First Name,Last Name,Email
        Mahir,Emran,1099249@apps.nsd.org
        John,Doe,john.doe@example.com
    
    Returns:
    - Dictionary where the key is the full name (e.g., "Mahir Emran") 
      and the value is the email address (e.g., "1099249@apps.nsd.org").
    """
    df = pd.read_csv(path)
    return {a+' '+b: c for a, b, c in zip(df['First Name'], df['Last Name'], df['Email'])}


def get_objtest_emails(filename):
    """
    Reads a CSV file containing objective test scores and generates a dictionary
    mapping attendees to their test results.

    CSV Format (scores.csv):
    - Columns: 'Name', 'Attendees', 'objective Score 1'
    - Example:
        Name,Attendees,objective Score 1
        Accounting I,Mahir Emran,45
        Business Management,Mahir Emran; Ritvik Bansal; Ibrahim Ansari,61.67

    Returns:
    - Dictionary where the key is an attendee's name (or team member's name) 
      and the value is a string containing their test results.
    """
    df = pd.read_csv(filename)
    results = {}
    for index, row in df.iterrows():
        test_name = row['Name']
        attendees = row['Attendees']
        score = row['objective Score 1']
        
        # Check if the attendees column contains multiple team members
        if isinstance(attendees, str) and "; " in attendees:
            team_members = attendees.split("; ")
            team_info = f"{test_name}\n"
            for member in team_members:
                # Fetch individual scores for team members
                member_score = df[(df['Name'] == test_name) & (df['Attendees'] == member)]['objective Score 1'].values
                if len(member_score) > 0:
                    team_info += f"{member}'s score: {member_score[0]}\n"
            team_info += f"Team Average: {score}\n"
            for member in team_members:
                if member not in results:
                    results[member] = ""
                results[member] += team_info + "\n"        
        else:
            # Handle individual attendees
            if attendees not in results:
                results[attendees] = ""
            alt_df = df[(df['Name'] == test_name) & (df['Attendees'].str.contains(attendees, na=False))]
            if len(alt_df) == 1:
                results[attendees] += f"{test_name}\n{attendees}'s score: {score}\n\n"
    return results


def get_objtest_email_body(name, scores, conf_name):
    """
    Generates the body of the email for objective test scores.

    Parameters:
    - name: Name of the recipient.
    - scores: String containing the recipient's scores.
    - conf_name: Name of the conference.

    Returns:
    - A formatted string containing the email body.
    """
    s = f'Hello {name},\n\n'
    s += f'This email contains your objective test and/or roleplay test score results for {conf_name}. If any of these were done with a team, you will see your team average and your other team members\' scores.\n\n'
    s += scores
    s += "Reply to this email if you have any questions or concerns. Thank you for competing at this conference!\n\n"
    s += "Sincerely,\nNorth Creek FBLA"
    return s


def convert_pdf_to_text(dir, out_dir):
    """
    Converts PDF files in a directory to text files.

    Parameters:
    - dir: Directory containing the PDF files.
    - out_dir: Directory to save the converted text files.

    Output:
    - For each PDF file, a corresponding .txt file is created in the output directory.
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


def get_names_from_rubric(path):
    """
    Given a .txt file of a rubric (called path), returns a list
    of names (as Strings)
    Ex: ['Mahir Emran', 'Ritvik Bansal', 'Ibrahim Ansari']
    Assumes format is like FBLA rubric
    
    Note that this method in particular may need to be updated if the rubric PDF format changes.
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


def send_rubric_emails(emails, conf_name):
    """
    Sends rubric emails with attachments to members.

    Parameters:
    - emails: Dictionary mapping (email, name) tuples to a list of rubric files.
    - conf_name: Name of the conference.
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
        subject = f'{conf_name} Results'
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
    Generates the body of the email for rubric results.

    Parameters:
    - name: Name of the recipient.
    - events: List of rubric file names.

    Returns:
    - A formatted string containing the email body.
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


def main():
    """
    Main method runs functions for sending out emails.
    Uncomment the desired function calls to execute.
    """
    # Code for sending rubrics
    # Assumes member info is in input/members.csv, rubric PDFs are in rubrics/
    # Input is a conference name
    # send_rubrics('NCCC 2025')

    # Code for sending objective test scores
    # Assumes member info is in input/members.csv, scores are in input/scores.csv
    # Input is a conference name
    # send_objtest_emails('WLC 2025')
    print("Done")


if __name__ == "__main__":
    main()