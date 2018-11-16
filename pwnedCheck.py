#!/usr/bin/env python
'''
Author		:Gerry Grant
Date		:November 2018
Description	:Python script to utilise the haveibeenpwned.com api to check either individual email addresses
		 or a list of email addresses that can be read from a file.

Example usage	:To retrieve a single email address 'python3 pwnedCheck.py -a test@example.com
		 To retrieve the details for a number of emails, create a text file with each address on a single line.
		 'python3 pwnedCheck.py -f <filename>

		 The results are stored in a csv file called breached that is saved in the same directory as the script is 
		 run.

	
'''


import json
import requests
import time
import argparse
import csv

parser = argparse.ArgumentParser(description='Verify if emails appear on HaveIbeenPwned')
parser.add_argument("-a", dest="address",
                  help="Single email address to be checked")
parser.add_argument("-f", dest="filename",
                  help="File to be checked with one email addresses per line")
args = parser.parse_args()

address = str(args.address)
filename = args.filename

server = 'https://haveibeenpwned.com'
sslVerify = True
api = '/api/v2/breachedaccount/'
unverified = '?includeUnverified=true'
headers = {'User-Agent':'checkEmail'}
sleep = 1.3 #Avoid rate limit

def main():

	if address != 'None':
		checkAdd([address])

	elif filename != 'None':
		emailAdds = [line.rstrip('\n') for line in open(filename)]
		checkAdd(emailAdds)

	else: print('[!] Error')

def checkAdd(emails):

	breaches = []

	for add in emails:
		print('[+] Checking email %s' %add)
	
		check = requests.get(server+api+add+unverified, headers=headers,verify=sslVerify)
	
		if check.status_code == 404:
			print('[+]No breach on this account')

		if check.status_code == 429:
			print('[!]Rate limit exceeded. Retry in %s seconds' %check.headers['Retry-After'])
			time.sleep(float(check.headers['Retry-After']))

		if check.status_code == 400:
			print('[!] Error. Bad request')

		if check.status_code == 403:
			print('[!]Error Forbidden - is the user agent set?')

		if check.status_code == 200:
			print('[!] Email %s has been involved in a breach' %add)
			#breaches = []
			details = check.json()
			for breach in details:
				breaches.append([add, breach['Name'],breach['Title'],breach['Domain'],breach['BreachDate'],breach['Description']])
			
			
		time.sleep(sleep) #Sleep to avoid rate limit


	with open('breached.csv','a') as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerows(breaches)

		
	print('[+] All %s emails checked. Results are available in the file breached.csv' %len(emails))


if __name__ == '__main__':
	main()

			
			
			

	