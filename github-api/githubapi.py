#!/usr/bin/env python

from pygithub3 import Github

gh = Github(login='tworide', password='0oliwero')

print gh.users.emails.list().all()
print gh.repos.get(user='tworide').list().all()
