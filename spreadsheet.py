import httplib2
import numpy as np

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

class SpreadSheet(object):
  def __init__(self, keyfile, sheet_id):
    self.sheetId = sheet_id

    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scopes=SCOPES)
    http_auth = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    self.service = discovery.build('sheets', 'v4', http = http_auth, discoveryServiceUrl = discoveryUrl)

  def append(self, sheet_name, values):
    value_range_body = {'values':[values]}
    append_range = "!".join([x for x in [sheet_name, "A1"] if x])
    self.service.spreadsheets().values().append(
      spreadsheetId = self.sheetId,
      range = append_range,
      valueInputOption = 'USER_ENTERED',
      body = value_range_body
    ).execute()

if __name__ == '__main__':
  import sys, random
  from datetime import datetime, timedelta, timezone
  JST = timezone(timedelta(hours=+9), 'JST')

  keyfile = sys.argv[1]
  sheet_id = sys.argv[2]
  sheet_name = None
  if len(sys.argv) > 3:
    sheet_name = sys.argv[3]

  sheet = SpreadSheet(keyfile, sheet_id)
  timestamp = datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S.%f')
  value = 20 + random.random()
  sheet.append(sheet_name, [timestamp, 'test', value])
