#!/usr/bin/env python3

import redminelib
import optparse
import configparser
import getpass
import os


def get_options():
    "Return a tuple (options, arguments)"
    p = optparse.OptionParser()
    p.add_option("-u", "--user",
                 dest='username',
                 help='Username to connect as')
    p.add_option("-p", "--password",
                 dest='password',
                 help='Password to use for authentication')
    p.add_option("-U", "--url",
                 dest='url',
                 help='URL to connect to')
    p.add_option("--project",
                 dest='project',
                 help='Filter to issues for this project')

    return p.parse_args()


def get_credentials(options):
    "Return credentials for RedMine"

    cred = {'username': None,
            'password': None,
            'url': None
            }

    cfg = configparser.ConfigParser()

    if os.path.exists(os.path.join(os.getenv('HOME'),
                                   ".rmreporter")):
        cfg.read(os.path.join(os.getenv('HOME'),
                              ".rmreporter"))

    for p in ('url', 'username', 'password'):
        if 'credentials' in cfg:
            if p in cfg['credentials']:
                cred[p] = cfg['credentials'][p]
        if hasattr(options, p) and getattr(options, p):
            # Specified on command line
            cred[p] = getattr(options, p)

        if not cred[p]:
            print('%s not set in configuration or option, please enter' % p)

            if p == 'password':
                cred[p] = getpass.getpass()
            else:
                cred[p] = input('%s: ' % p)

    return cred


def rm_checker(issues, credentials, options):
    r = redminelib.Redmine(credentials['url'],
                           username=credentials['username'],
                           password=credentials['password'])

    if not issues:
        # No issue given, get all from
        if not options.project:
            issues = [p.id for p in r.issue.all()]
        else:
            issues = [p.id for p in r.issue.all()
                      if str(p.project) == str(options.project)]
            
    if issues:
        for p in issues:
            i = r.issue.get(int(p))

            print(dir(i))
            print("%s - %s - %s " % (i.id,
                                     i.project,
                                     i.subject))

            for t in i.time_entries:
                print("%g %s %s %s" % (t.hours,
                                       t.activity,
                                       t.created_on,
                                       t.user))

            print("--ENDTIMES--")


def main():
    opts, args = get_options()
    c = get_credentials(opts)
    rm_checker(args, c, opts)
    return None


if __name__ == "__main__":
    main()
