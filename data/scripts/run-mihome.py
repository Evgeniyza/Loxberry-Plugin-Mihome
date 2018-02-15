import socket

from mihome.connector import XiaomiConnector

#Loxone address and port
UDP_IP = '192.168.178.32'
UDP_PORT = 5666

# Open socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# List of supported models
class MODEL:
  CUBE = 'cube'
  GATEWAY = 'gateway'
  MAGNET = 'magnet'
  MOTION = 'motion'
  SENSOR_HT = 'weather.v1'
  SMOKE = 'smoke'
  SWITCH = '86sw1'
  WATER_LEAK = 'sensor_wleak.aq1'
  
# Supported values
class VALUE:
  ALARM = 'alarm'
  DENSITY = 'density'
  HUMIDITY = 'humidity'
  ILLUMINATION = 'illumination'
  STATUS = 'status'
  TEMPERATURE = 'temperature'
  CHANNEL_0 = 'channel_0'
  ROTATE = 'rotate'
  VOLTAGE = 'voltage'

# Matrix that links values for models, conversion added
MODEL_VALUES_MATRIX = {
  MODEL.CUBE: {VALUE.STATUS: (dict, {'flip90': 'flip90',
                                     'flip180': 'flip180',
                                     'free_fall': 'free_fall',
                                     'move': 'move',
				     'rotate': 'rotate',
                                     'shake_air': 'shake_air',
                                     'tap_twice': 'tap_twice'},
                              ),
               VALUE.VOLTAGE: (int, 1000),
	      # VALUE.ROTATE: (int, replace(',','')),
               },
  MODEL.GATEWAY: {VALUE.ILLUMINATION: (int, 1),
                  },
  MODEL.MAGNET: {VALUE.STATUS: (dict, {'close': '0',
                                       'open': '1'}),
                 VALUE.VOLTAGE: (int, 1000),
                 },
  MODEL.MOTION: {VALUE.STATUS: (dict, {'motion': '1'}),
                 VALUE.VOLTAGE: (int, 1000),
                 },
  MODEL.SENSOR_HT: {VALUE.HUMIDITY: (int, 100),
                    VALUE.TEMPERATURE: (int, 100),
                    VALUE.VOLTAGE: (int, 1000),
                    },
  MODEL.SMOKE: {VALUE.ALARM: (int, 1),
                VALUE.DENSITY: (int, 1),
                VALUE.VOLTAGE: (int, 1000),
                },
  MODEL.SWITCH: {VALUE.STATUS: (dict, {'click': ('click', '1'),
                                       'long_click_press': ('press', '1'),
                                       'long_click_release': ('press', '0')}),
		 VALUE.CHANNEL_0: (dict, {'click': ('click', '1'),
                                       'long_click_press': ('press', '1'),
                                       'long_click_release': ('press', '0')}),
                 VALUE.VOLTAGE: (int, 1000),
                 },
  MODEL.WATER_LEAK: {VALUE.STATUS: (dict, {'no_leak': '0',
                                           'leak': '1'}),
                     VALUE.VOLTAGE: (int, 1000),
                     }
    
  }

def cb(model, sid, cmd, data):
  # Focus only on report event, ignore heartbeats
  #if cmd != 'report':
  #  return

  # Find device
  if model in MODEL_VALUES_MATRIX:
    # Read it's data values
    for k, v in (data or {}).items():
      # Check data values one by one and if known then prepare package
      if k in MODEL_VALUES_MATRIX.get(model):
        packet = None
        type, conv = MODEL_VALUES_MATRIX.get(model).get(k)

        # Integer value
        if type == int:
          packet = '%s %s %s %.2f' % (model, sid, k, type(v) / (conv or 1.0))

        # Dictionary
        if type == dict and v in conv:
          # Change key
          if isinstance(conv[v], tuple) and len(conv[v]) >= 2:
            packet = '%s %s %s %s' % (model, sid, conv[v][0], conv[v][1])
          # No conversion
          else:
            packet = '%s %s %s %s' % (model, sid, k, conv[v])

        # Send packet to Loxone
        if packet:
          sock.sendto(bytes(packet, 'utf-8'), (UDP_IP, UDP_PORT))

connector = XiaomiConnector(data_callback=cb)

while True:
    connector.check_incoming()