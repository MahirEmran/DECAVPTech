import pandas as pd 
import smtplib
from email.mime.text import MIMEText

def get_dict():
    df = pd.read_csv('fbla_input/members.csv')
    return {a+' '+b: c for a, b, c in zip(df['First Name'], df['Last Name'], df['Email'])}


def get_new_df(d):
    df = pd.read_csv('fbla_input/scores2.csv')
    df['Emails'] = df['Attendees'].apply(lambda x: get_emails(x, d))
    return df

def get_emails(s, d):
    emails = [d[x] for x in s.split("; ")]
    return ';'.join(emails)

def send_emails(df):
    for row in df:
        sender = 'fblanchs.exec@gmail.com'
        password = 'fblaexec!'
        subject = f'NCCC {row['Name']} Objective Test Scores'
        msg = MIMEText(get_body(row['Attendees'], row['objective Score 1']))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(row['Emails'].split(';'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

def get_body(names, num):
    names = names.replace("; ", " & ")
    print(names)
    s = f'Hello {names},\n\n'
    s += f'Your score for this objective test was: {num}.\n'
    s += "If this was a team event, this number is your team's average score.\n\n"
    s += "Thank you for competing!\nNorth Creek FBLA"
    return s

def main():
    d = get_dict()
    df = get_new_df(d)
    send_emails(df)

if __name__ == "__main__":
    main()