import pandas as pd 
import smtplib
from email.mime.text import MIMEText
import time

def send_emails(df):
    for idx, row in df.iterrows():
        if row['Name'] == 'Jeff Stride':
            continue
        sender = 'mahiremran7@gmail.com'
        password = 'esuj nxoq wesk sfkh'
        subject = "North Creek FBLA Judging Request"
        msg = MIMEText(get_body(row['Name']))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = row['Email']
        print(row['Email'])
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, [row['Email']], msg.as_string())
        time.sleep(5)

def get_body(name):
    lastname = name.split(' ')[-1]
    print(lastname)

    
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
    send_emails(pd.read_csv('fbla_input/uwb_profs_test.csv'))
    print('Done')

if __name__ == "__main__":
    main()