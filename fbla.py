import pandas as pd 
import smtplib
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import PyPDF2

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

# def send_emails(df):
#     for row in df:
#         sender = 'fblanchs.exec@gmail.com'
#         password = 'fblaexec!'
#         subject = f'NCCC {row['Name']} Objective Test Scores'
#         msg = MIMEText(get_body(row['Attendees'], row['objective Score 1']))
#         msg['Subject'] = subject
#         msg['From'] = sender
#         msg['To'] = ', '.join(row['Emails'].split(';'))
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
#             smtp_server.login(sender, password)
#             smtp_server.sendmail(sender, recipients, msg.as_string())

def get_body(names, num):
    names = names.replace("; ", " & ")
    print(names)
    s = f'Hello {names},\n\n'
    s += f'Your score for this objective test was: {num}.\n'
    s += "If this was a team event, this number is your team's average score.\n\n"
    s += "Thank you for competing!\nNorth Creek FBLA"
    return s

def convert_pdf_to_text(dir, out_dir):
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
                errs.append("Name " + name + " not found in member email spreadsheet")
        
    send_rubric_emails(emails)
    
    for err in errs:
        print(err)


def send_rubric_emails(emails):
    for key in emails:
        sender = 'fblanchs.exec@gmail.com'
        password = 'fblaexec!'
        subject = f'NCCC Results'
        msg = MIMEText(get_rubric_email_body(key[1], emails[key]))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = emails[key][0]
        for f in emails[key]:
            with open('rubrics/' + f[0:f.index('.txt')] + ".pdf", "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, [emails[key][0]], msg.as_string())

def get_rubric_email_body(name, events):
    msg = ""
    msg += f'Hello {name},\n\n'
    msg += "attached are results for these events:\n\n"
    for event in events:
        event_name = " ".join(event[:event.index("-")].split("_"))
        msg += f'{event}\n'
    msg += f'\nthx!\n\n'
    msg += f'bye - NCFBLA aka mahir testing rn'
    


def get_names_from_rubric(path):
    names = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith("Revision:"):
                s = line[8:]
                words = s.split(", ")
                for name in words:
                    chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")  # Allowed characters
                    clean_name = ''.join(filter(lambda c: c in chars, name))
                    names.append(clean_name)
                break

    return names if len(names) != 0 else None


def main():
    members = get_dict()
    path = "rubrics_txt/"
    # df = get_new_df(d)
    # send_emails(df)
    convert_pdf_to_text('rubrics/', path)
    send_rubrics(members, path)


if __name__ == "__main__":
    main()