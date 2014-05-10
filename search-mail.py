import sys
import argparse
import getpass
import imaplib
import json
import os.path

def main(argv):
    defaults = {}
    CONFIG_PATH = os.path.join(os.environ['HOME'], '.mailpy')
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            defaults = json.load(f)

    def add_arg(parser, name, default_default=None):
        d = defaults.get(name, default_default)
        if d is not None:
            parser.add_argument('--' + name, default=d)
        else:
            parser.add_argument('--' + name, required=True)


    parser = argparse.ArgumentParser()
    add_arg(parser, 'username')
    add_arg(parser, 'password', '-')
    add_arg(parser, 'host')
    add_arg(parser, 'port', 993)

    parser.add_argument('--delete-messages', default=False, action='store_true')
    parser.add_argument('--print-headers', default=False, action='store_true')

    parser.add_argument('--to', default=None)
    parser.add_argument('--from', dest='from_addr', default=None)
    parser.add_argument('--subject', default=None)

    args = parser.parse_args()

    search_criteria = []
    if args.to != None:
        search_criteria.extend(['TO', args.to])
    if args.from_addr != None:
        search_criteria.extend(['FROM', args.from_addr])
    if args.subject != None:
        search_criteria.extend(['SUBJECT', args.subject])

    if len(search_criteria) == 0:
        print >>sys.stderr, "No search criteria specified"
        sys.exit(1)

    if args.password == '-':
        args.password = getpass.getpass()

    imap = imaplib.IMAP4_SSL(args.host, args.port)
    imap.login(args.username, args.password)
    imap.select('INBOX')

    _, uids = imap.uid('SEARCH', *search_criteria)
    uids = uids[0].split()
    print >>sys.stderr, 'Matches %d messages' % len(uids)

    if not args.delete_messages and not args.print_headers:
        return

    for i, uid in enumerate(uids):
        if i % 10 == 0:
            print (i + 1), 'of', len(uids)
        if args.print_headers:
            print imap.uid('FETCH', uid, '(BODY.PEEK[HEADER])')[1][0][1].strip()
        if args.delete_messages:
            imap.uid('STORE', uid, '+FLAGS', '(\\Deleted)')

    if args.delete_messages and len(uids) > 0:
        imap.expunge()
            

if __name__ == '__main__':
    main(sys.argv)
