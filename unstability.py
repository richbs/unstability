import csv
import getpass
import readability
import os
import sys
import time


class Unstability:

    csv_reader = None
    links_by_category = {}
    username = ''
    password = ''
    token = ''
    rdc = None

    def __init__(self):
        """
        Checks the environment for the API_KEY and API_SECRET variables
        If no env variables available, ask the user for their API details
        Ask the user for their Readability username and password
        Exchange these credentials for user token and secret via xauth
        """
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

        self.username = u
        self.password = p

        user_token, user_secret = readability.xauth(k, s, u, p)
        self.rdc = readability.ReaderClient(k, s, user_token, user_secret)

    def process_csv(self, csv_filename):
        """
        Work through the Instapaper CSV and separate into lists per
        category, e.g. Unread, Archive
        """
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

    def process_links(self):
        """
        Chug through the assembled list of links and add them with the
        appropriate tag into Readibility.
        """
        for cat in self.links_by_category:

            link_list = self.links_by_category[cat]
            if cat == "Unread":
                q = raw_input(
                    "Add %d unread articles to your Readability list? " % (
                                                len(link_list)))
                if q == 'y':
                    self.add_list(link_list)
                else:
                    print 'Nope'
            elif cat == "Starred":
                q = raw_input(
                    "Add %d starred articles to your Readability archive? " % (
                                                len(link_list)))
                if q == 'y':
                    self.add_list(link_list, archive=True, starred=True)
                else:
                    print 'Nope'
            elif cat == "Archive":
                q = raw_input(
                    "Add %d articles to your Readability archive? " % (
                                                len(link_list)))
                if q == 'y':
                    self.add_list(link_list, archive=True, starred=False)
                else:
                    print 'Nope'
            else:
                q = raw_input(
                    "Add %d articles tagged with %s to your archive? " % (
                                                len(link_list), cat))
                if q == 'y':
                    self.add_list(link_list, archive=True, starred=False,
                                                                    tag=cat)
                else:
                    print 'Nope'

    def count_links(self):

        for cat in self.links_by_category:

            print 'Found', len(self.links_by_category[cat]), 'in', cat

    def add_list(self, link_list, archive=False, starred=False, tag=None):

        link_list.reverse()
        for url, title in link_list:
            print 'Adding', title
            response = self.rdc.add_bookmark(url, favorite=starred,
                                                        archive=archive)
            try:
                if tag:
                    print 'Adding tag', tag
                    bookmark_id = response['location'].split('/')[-1]
                    response = self.rdc.add_tags_to_bookmark(bookmark_id, tag)
            except KeyError:
                continue
            time.sleep(0.2)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        instapaper_csv = sys.argv[1]
    else:
        exit("Please specify location of Instapaper CSV file.")

    # get all the authentication stuff done
    unst = Unstability()
    # hack through the CSV
    unst.process_csv(instapaper_csv)
    # add those links to Readability, one by one
    unst.process_links()

    print "Thank you", unst.username
