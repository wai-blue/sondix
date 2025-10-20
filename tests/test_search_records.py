
import os
import sys
import json
from clients.python.dtxs_client.main import DtxsClient
from use_cases.common import prBlue, prRed, prGreen, prYellow, prLightBlue

if (len(sys.argv) <= 2):
  prYellow("Usage: python -m tests.test_record <configFile> <dbName>")
  prYellow("")
  prYellow("  configFile     Configuration of OAuth and DTXS endpoints")
  prYellow("  dbName         Name of the database where records will be manipulated with")
  sys.exit()

configFile = sys.argv[1]
dbName = sys.argv[2]

with open(configFile) as f: config = json.load(f)

prBlue("[1] Checking the environment")

client = DtxsClient(config['dtxsClient'])
client.getAccessToken()

prLightBlue("Authenticating")

if (len(client.accessToken) == 0):
  prRed("!! Did not receive access token. Exitting.")
  sys.exit()

prGreen("-> Received access token, length: " + str(len(client.accessToken)) + " bytes")

prLightBlue("Configuring DTXS client")

client.database = dbName
prGreen("DTXS client configured")

# -------- RECORD CREATION TEST --------
prYellow("Testing search query")

records = json.loads( # parse result to JSON
  client.searchRecords( # search records
    [ # a list of 'search queries'
      {
        "property": "class", # a property that should be checked, can be "class" or "owner".
        "equals": "ndo:Actors.Persons" # type of comparison, can be "equals" (uses '=' operator) or "match" (uses SQL-based 'like' operator). 
      }
    ]
  )
)

for i, record in enumerate(records):
  print(
    " UID = " + record['uid']
    + " | Version = " + str(record['version'])
    + " | Owner = " + record['owner']
    + " | Class = " + record['class']
  )
