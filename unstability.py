import codecs
import csv
import getpass
import readability
import sys


class InstapaperCSV:

    csv_file = None

    def __init__(self, csv_filename):

        self.csv_file = codecs.open(csv_filename, 'r', 'UTF-8')
        print self.csv_file.read()



def count_links(csv_file):

    pass
if __name__ == "__main__":

    if len(sys.argv) > 1:
        instapaper_csv = sys.argv[1]
    else:
        exit("Please specify location of Instapaper CSV file.")

    print "Welcome to unstability by @richbs"
    k = raw_input("What is your Readability API key?")
    s = raw_input("What is your Readability API secret")
    u = raw_input("What is your Readability account username? ")
    p = getpass.getpass("What is your Readability password? (Not stored here)")

    icsv = InstapaperCSV(instapaper_csv)

    print "Thank you", u
