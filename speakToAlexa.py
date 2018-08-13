import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import sys
sys.path.insert(0, "..")

from opcua import Client
from opcua import ua

app = Flask(__name__)
ask = Ask(app, "/")

logging.basicConfig()
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

client = Client("opc.tcp://localhost:4840")

@ask.launch
def new_Produktion():
  logging.info("Read/Write variable with OPC-UA by Amazon Alexa voice command")
  welcome_msg = render_template('welcome')
  return question(welcome_msg)

@ask.intent("YesIntent")
def get_Job():
  client.connect()
  root = client.get_root_node()
  var = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL.bStartJob")
  var.set_value(True)
  whichnumber_msg = render_template('whichnumber')
  return question(whichnumber_msg)

@ask.intent("NoIntent")
def end_Job():
  end_msg = render_template('bye')
  return statement(end_msg)

@ask.intent("GetScrewIntent", convert={'count': int})
def answer(count):
  var = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL.uiNumberOfScrews")
  var.set_value(count, ua.VariantType.Int16)
  msg = render_template('deliverPart')
  return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)
