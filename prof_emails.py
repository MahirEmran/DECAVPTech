import pandas as pd 
import smtplib
from email.mime.text import MIMEText
import time

def send_prof_emails(df):
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
        subject = "North Creek FBLA Judging Request"
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
    of the body of the email
    """
    # Gets the last name of the person being emailed
    lastname = name.split(' ')[-1]
    print(lastname)
    # Creates the body to be sent in the email
    s = f'Dear Professor {lastname},\n\n'
    s += "I hope this message finds you well. My name is Mahir Emran, and I’m part of our Future Business Leaders of America (FBLA) club at North Creek High School.\n\n" 
    s += "We are organizing our annual Winter Leadership Conference on February 1st, 2025 where 900+ students from 12 high schools compete in various subjects such as marketing, computer science, business, and public speaking. We would love to have you as a judge to score and give feedback on student presentations!\n\n"
    s += "If you want to see the available events, they are listed at https://www.fbla.org/high-school/competitive-events/.\n\n"
    s += "We offer two shifts from 7:30AM - 12:30PM and 11:00AM-4:00PM. The event will be hosted at North Creek High School (3613 191st Pl SE, Bothell, WA 98012). Availability for either shift would be amazing!\n\n"
    s += "If you're interested or would like more details, I’d be happy to provide further information. The form to sign up as a judge is this link: https://docs.google.com/forms/d/e/1FAIpQLSfj1gbcBChgCmuTsclTvKaWo613D-75BIHKlMHLWfZw_Ybm1Q/viewform\n\n"
    s += "Thank you for considering this opportunity!\n"
    s += "Best regards,\n"
    s += "Mahir Emran\n"
    s += "FBLA VP of Technology Development\n"
    s += "North Creek High School\n"
    return s

def main():
    # Reads the CSV of professors to send emails to
    send_emails(pd.read_csv('fbla_input/uwb_profs_test.csv'))

    print('Done')

if __name__ == "__main__":
    main()