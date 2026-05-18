#!/usr/bin/env python3

import datetime
import email
import smtplib
import sys
import csv
import getpass
import os

def usage():
    print("Usage: script.py \"date|title|emails|filepath|row|attachment\"")
    print("       row is only required for .csv files (0 = first data row)")
    print("       attachment is optional, must be a .pdf file path")
    return True

def dow(date):
    dateobj = datetime.datetime.strptime(date, r"%Y-%m-%d").date()
    return dateobj

def message_template(date, title, content):
    message = email.message.EmailMessage()
    weekday = dow(date)
    message['Subject'] = f"{title}"
    message['Reply-To'] = 'no-reply@noreply.com' 
    message.set_content(f'Today\'s date: {weekday}\n\n{content}')
    return message

def send_message(message, emails, attachment_pdf_path):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    sender = input('Insert your email: ')
    password = getpass.getpass('Insert your password: ')
    smtp.login(sender, password)
    message['From'] = sender

    if attachment_pdf_path:
        with open(attachment_pdf_path, 'rb') as f:
            message.add_attachment(
                f.read(),
                maintype='application',
                subtype='pdf',
                filename=os.path.basename(attachment_pdf_path)
            )
    for addr in emails.split(','):
        del message['To']
        message['To'] = addr
        smtp.send_message(message)
    smtp.quit()

def read_content(filepath, row_index=None):
    if filepath.endswith('.txt'):
        with open(filepath, 'r') as f:
            return f.read()
    elif filepath.endswith(".csv"):
        if row_index is None:
            raise ValueError("A row number is required for .csv files.")
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)          # reads csv with column headers
            rows = list(reader)
            if 'content' not in reader.fieldnames:
                raise ValueError("No 'content' column found in the CSV file.")
            if row_index >= len(rows):
                raise IndexError(f"Row {row_index} does not exist. CSV has {len(rows)} data rows.")
            return rows[row_index]['content']   # returns only the 'content' column value
    else:
        raise ValueError("Unsupported file type. Use a .txt or .csv file.")


def main():
    if len(sys.argv) < 2:
        return usage()
    try:
        parts = sys.argv[1].split('|')

        if len(parts) == 4:
            date, title, emails, filepath = parts
            row_index, attachment_pdf_path = None, None                        # no row needed for txt
        elif len(parts) == 5:
            date, title, emails, filepath, row = parts
            row_index = int(row)                    # convert row to integer
            attachment_pdf_path = None
        elif len(parts) == 6:
            date, title, emails, filepath, row, attachment_pdf_path = parts
            row_index = int(row)                    # convert row to integer
        else:
            print("Error: incorrect number of arguments", file=sys.stderr)
            return usage()

        content = read_content(filepath, row_index)
        message = message_template(date, title, content)
        send_message(message, emails, attachment_pdf_path)
        print('Successfully sent reminders to:', emails)

    except FileNotFoundError:
        print("Error: file not found", file=sys.stderr)
    except IndexError as e:
        print(f"Error: {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print("Failure to send email:", e, file=sys.stderr)

if __name__ == "__main__":
    sys.exit(main())