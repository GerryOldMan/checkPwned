Python script to utilise the haveibeenpwned.com api to check either individual email addresses or a list of email addresses that can be read from a file.

Example usage	:
To retrieve a single email address 'python3 pwnedCheck.py -a test@example.com
To retrieve the details for a number of emails, create a text file with each address on a single line. 'python3 pwnedCheck.py -f <filename>

The results are stored in a csv file called breached that is saved in the same directory as the script is run.
