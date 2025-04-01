import pandas as pd 
import smtplib
from email.mime.text import MIMEText
import time

def send_prof_emails(df, subject):
    """
    Sends emails to people in df, where df is assumed to have the following format:
    Name,Email
    Mahir Emran,1099249@apps.nsd.org
    Essentially has a Name and Email column
    """
    for idx, row in df.iterrows():
        # Ignore this totally nothing is happening here :D
        if row['Name'] == 'Jeff Stride':
            continue
        sender = ''
        password = ''
        # Pulls sender info from the txt file
        with open('sender_info.txt') as f:
            lines = f.readlines()
            sender = lines[0]
            password = lines[1]
      
        # Gets the body of the email with the name of the person being emailed
        msg = MIMEText(get_body(row['Name']))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = row['Email']
        print(row['Email'])
        # Sends the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, [row['Email']], msg.as_string())
        # Pauses program for 5s to not get timed out on requests
        time.sleep(5)

def get_body(name):
    """
    Given the name of the person being emailed, return a String
    of the body of the email. It reads input/body.txt to get the body of the email.
    
    input/body.txt should contain everything that is in the body of the email, EXCEPT
    for the greeting, which is added in this function.
    
    You could update this to change the details for the conference. In addition, right now
    it just uses the last name for the professor. Maybe this should be changed.
    """
    # Gets the last name of the person being emailed
    lastname = name.split(' ')[-1]
    print(lastname)

    # Creates the body to be sent in the email
    s = f'Dear Professor {lastname},\n\n'
    
    with open('input/body.txt') as f:
        lines = f.readlines()
        # Reads the body of the email
        for line in lines:
            s += line
    print(s)
    return s

def main():
    # Reads the CSV of professors to send emails to
    send_prof_emails(pd.read_csv('input/uwb_profs_test.csv'), "North Creek FBLA Judging Request")

    print('Done')

if __name__ == "__main__":
    main()