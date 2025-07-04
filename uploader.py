import bme280
import mcp3208
import amq1602xa
import spreadsheet
import sys, random, os, subprocess, json
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9), 'JST')

keyfile = sys.argv[1]
sheet_id = sys.argv[2]
sheet = spreadsheet.SpreadSheet(keyfile, sheet_id)

def read_bme280():
  return bme280.BME280().readData()

def read_mh_z19():
  try:
    script = '%s/mh_z19.py' % os.path.dirname(os.path.abspath(__file__))
    cmd = "sudo python3 %s" % script
    j = subprocess.check_output(cmd, shell=True)
    if j == b'null\n':
      print("Warning: MH-Z19 returned null data")
      return {'co2': 0}
    return json.loads(j)
  except subprocess.CalledProcessError as e:
    print(f"Error running MH-Z19 script: {e}")
    return {'co2': 0}
  except json.JSONDecodeError as e:
    print(f"Error parsing MH-Z19 JSON: {e}")
    return {'co2': 0}
  except Exception as e:
    print(f"Unexpected error reading MH-Z19: {e}")
    return {'co2': 0}

def read_lls05():
  # value from MCP3208 CH0
  return mcp3208.MCP3208().read(0)

def upload_data(t, dat_bme280, dat_mh_z19, dat_lls05):
  record = [
    t.strftime('%Y-%m-%d %H:%M:%S.%f'),
    dat_bme280['temperature'],
    dat_bme280['humidity'],
    dat_bme280['pressure'],
    dat_mh_z19['co2'],
    dat_lls05
  ]
  sheet.append('Data', record)

def display_data(t, dat_bme280, dat_mh_z19, dat_lls05):
  amq = amq1602xa.AMQ1602XA()
  amq.write_string("%4dhPa  " % dat_bme280['pressure'])
  if dat_mh_z19['co2'] is not None:
    amq.write_string("%4dppm" % dat_mh_z19['co2'])
  amq.newline()
  amq.write_string("%.1f\xdfC " % dat_bme280['temperature'])
  amq.write_string("%d%% " % dat_bme280['humidity'])
  amq.write_string("%s" % t.strftime('%H:%M'))

dat1 = read_bme280()
dat2 = read_mh_z19()
dat3 = read_lls05()
t = datetime.now(JST)
upload_data(t, dat1, dat2, dat3)
display_data(t, dat1, dat2, dat3)
