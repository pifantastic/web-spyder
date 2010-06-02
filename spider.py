#!/usr/bin/python

"""
Web Spider v%(VERSION)s
 
Synopsis: spider.py [options] url
	
	-u  HTTP Authentication username
	-p  HTTP Authentication password
	-n  number of spiders to spawn
	-s  PHPSESSID for authenticated requests
	-h  This help message
"""

import os, sys, getpass, time, getopt

VERSION = '0.1'

# Defaults
URL = ''
N = 5
USERNAME = ''
PASSWORD = ''
PHPSESSID = ''

# Print script usage and exit
def usage(exit_code=0): 
  print __doc__ % globals()
  sys.exit(exit_code)

if __name__ == "__main__":
  # Parse command line
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:p:n:s:")
    if len(sys.argv) < 2:
      usage(1)
  except getopt.GetoptError, err:
    print str(err)
    usage(1)
    
  for o, a in opts:
    if o == "-h":
      usage()
    elif o == "-u": 
      USERNAME = a
    elif o == "-p": 
      PASSWORD = a
    elif o == "-s":
      PHPSESSID = a
    elif o == "-n": 
      try:
        N = int(a)
      except Exception, err:
        print str("-n accepts an integer")
        usage(1)
    else: 
      assert False, "unhandled option"
  
  if len(args) > 0:
    URL = args[0]
  else:
    print("No url supplied")
    usage(1)
    
  auth = ''
  if USERNAME:
    if PASSWORD == '':
      PASSWORD = getpass.getpass("HTTP Authentication password: ")
    auth = "%s:%s@" % (USERNAME, PASSWORD)
  
  header = ''
  if PHPSESSID != '':
    header = '--header="Cookie: PHPSESSID=%s"' % PHPSESSID
    
  command = 'wget --mirror --quiet %s http://%s%s/ 2>1 > /dev/null &' % (header, auth, URL)
  
  print("Spawning %d spiders" % N)
  for x in range(N):
    print("Spawning spider %d" % (x + 1))
    os.system(command)
    time.sleep(1)

