import codecs
import csv
import getpass
import readability
import os
import sys


class InstapaperCSV:

    csv_reader = None
    links_by_category = {}

    def __init__(self, csv_filename):

        csv_file = open(csv_filename, 'r')
        self.csv_reader = csv.reader(csv_file)
        for l in self.csv_reader:
            category = l[3]
            link = l[0]
            title = l[1]
            # put links in tuple
            if category in self.links_by_category:
                self.links_by_category[category].append((link, title,))
            else:
                self.links_by_category[category] = [(link, title,)]

        self.count_links()

    def count_links(self):

        for cat in self.links_by_category:

            print 'Found', len(self.links_by_category[cat]), 'in', cat


if __name__ == "__main__":

    if len(sys.argv) > 1:
        instapaper_csv = sys.argv[1]
    else:
        exit("Please specify location of Instapaper CSV file.")

    print "Welcome to unstability by @richbs"
    if 'API_KEY' in os.environ:
        k = os.environ['API_KEY']
    else:
        k = raw_input("What is your Readability API key? ")

    if 'API_SECRET' in os.environ:
        s = os.environ['API_SECRET']
    else:
        s = raw_input("What is your Readability API secret? ")

    u = raw_input("What is your Readability account username? ")
    p = getpass.getpass("What is your Readability password? ")

    icsv = InstapaperCSV(instapaper_csv)

    print "Thank you", u
