import argparse
import os
import smtplib

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from prarxivate.utils import Config


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--sender', type=str, default='', help='sender email')
    parser.add_argument('-to', '--receiver', type=str, default='', help='receiver email')
    parser.add_argument('-pw', '--password', type=str, default='', help='password for email account')
    args = parser.parse_args()
    
    args.report_path = Config.report_path
    return args


def find_filepath(path, date):
    reports = os.listdir(path)
    try:
        result = [r for r in reports if date in r][0]
    except Exception as e:
        print('occurred error: {}'.format(e))
        exit(0)
    return result


def emails(args):
    now = datetime.now()
    target_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    target_filename = find_filepath(args.report_path, target_date)
    num_papers = target_filename.split('-')[4]

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'arXiv daily mailing'
    msg['From'] = args.sender
    msg['To'] = args.receiver

    html = """
    <p>Dear RCV Sejong,</p>
    <p>This is {n} papers at {d}.</p>
    <p>Best Regards,<br/>
    Jongmin Park</p>""".format(n=num_papers, d=target_date)
    html_contents = MIMEText(html, 'html')
    
    filepath = os.path.join(args.report_path, target_filename)
    with open(filepath,'rb') as f:
        attach = MIMEApplication(f.read(), _subtype="html")
    attach.add_header('Content-Disposition', 'attachment', filename=target_filename)
    msg.attach(attach)
    msg.attach(html_contents)

    # accept here: https://myaccount.google.com/lesssecureapps
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.login(args.sender, args.password)
            s.send_message(msg)
            print('Send complete to {}'.format(args.receiver))
    except Exception as e:
        lesssecureapps = 'https://myaccount.google.com/lesssecureapps'
        print('occurred error: {}'.format(e))
        raise ValueError('please check: {}'.format(lesssecureapps))


def main():
    args = get_args()
    emails(args)


if __name__ == '__main__':
    main()
