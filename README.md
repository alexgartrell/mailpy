mailpy
======

imap utility scripts for outlook sufferers

== About ==

I created this repo when I found myself deleting a million generic task email updates from our internal tasks tool.
Now, I can accomplish the same with:

  python search-mail.py --subject '[tasks]' --delete-messages
  
And because you are a coward, I've added the ability to preview messages or view them while you do the delete with the following:

  python search-mail.py --subject '[tasks]' --print-headers | grep '^Subject'

For the sanity of everyone, I'm holding the hard requirement that only standard python libraries 2.7+ will be used, so install should never
be more work than a git-clone.

== Pull Requests ==

I'm thrilled to accept pull requests.  Just please don't add any external dependencies and please make it generally useful stuff.
