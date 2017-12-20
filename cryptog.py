# Import libraries for CryptoG
import yaml
import time
from coinbase.wallet.client import Client as CoinbaseClient
from twilio.rest import Client as TwilioClient

# Load in config.yml
config = yaml.load(open('config.yml'))

# Get API keys from config.yml
coinbase_key = config['coinbase']['key']
coinbase_secret = config['coinbase']['secret']

twilio_sid = config['twilio']['sid']
twilio_token = config['twilio']['token']

# Configure the Coinbase and Twilio APIs
coinbase_client = CoinbaseClient(coinbase_key, coinbase_secret)
twilio_client = TwilioClient(twilio_sid, twilio_token)

# Get our change threshold and Twilio #s from config.yml
to_number = config['twilio']['to_number']
from_number = config['twilio']['from_number']

change_threshold = config['config']['change_threshold']
update_period = config['config']['update_period']

# Helper method for getting the price difference change ratio
def get_price_difference(prev, curr):
  return curr/prev - 1

if __name__ == "__main__":
  print "=*====================CryptoG====================*="
  print "CryptoG is up and running."
  print "You'll get an update every " + str(update_period) + " seconds if the price of BTC changes by " + str(change_threshold*100) + " percent."
  print "=*===============================================*="
  last_btc_price = float(coinbase_client.get_spot_price(currency_pair = 'BTC-USD').amount)

  # Update loop
  while True:
    curr_btc_price = float(coinbase_client.get_spot_price(currency_pair = 'BTC-USD').amount)

    diff = get_price_difference(last_btc_price, curr_btc_price)

    if diff > change_threshold:
      trend = 'DOWN'
      if curr_btc_price > last_btc_price:
        trend = 'UP'
        
      # Send a message if the difference is above our change threshold
      msg_body = 'BTC has gone ' + trend + ' by  ' + str(diff*100) + ' percent in the last ' + str(update_period) + ' seconds: ' + str(last_btc_price) + ' -> ' + str(curr_btc_price)

      msg = twilio_client.messages.create(
          to=to_number,
          from_=from_number,
          body=msg_body
        )

      print msg_body

    last_btc_price = curr_btc_price

    time.sleep(update_period);

  