# Email_sender
Sends emails to specified recipients using a Gmail account using SMTP.

## Usage
```bash
./send_email.py "date|title|emails|filepath"           # for .txt files
./send_email.py "date|title|emails|filepath|row"       # for .csv files
```

## Arguments

* **date**
    * Date to display in the email body
    * Format: `dd/mm/yyyy` (e.g. `05/11/2026`)
* **title**
    * Title of the email
* **emails**
    * Recipient email address(es)
    * Separate multiple emails with a comma (e.g. `a@gmail.com,b@gmail.com`)
* **filepath**
    * Path to the file containing the email body content
    * Accepts `.txt` or `.csv` files
* **row** *(csv only)*
    * Row number to pull content from under the `content` column
    * Zero-indexed (e.g. `0` = first data row, `1` = second data row)

## Credentials
You will be prompted for credentials each time the script runs:
* **Email** — the Gmail account used to send emails
* **App Password** — your 16-character Gmail App Password

## Notes
* Replies are redirected away from the sender via the `Reply-To` header
* The `From` field must match the authenticated Gmail account
* Gmail App Password requires 2-Step Verification to be enabled