import PySimpleGUI as sg
import requests
import json
from requests.auth import HTTPBasicAuth
method = "get"

a_file = open("USstates_avg_latLong.json", "r")
data = json.load(a_file)

sg.theme('Default1')
layout = [
    [sg.Text('What state are you in?')],
    [sg.Text('State', size =(5, 1)), sg.InputText()],
    [sg.OK(), sg.Cancel()]
]

window = sg.Window('   Lighting Option Price Calculator', layout, size=(450, 100))
inputstate = ""

while True:
    event, values = window.read()
    if event == "OK":
        inputstate = values[0]
        window.close()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

for i in data:
  if i['state'].lower() == inputstate.lower():
    lat = str(i["latitude"])
    lon = str(i["longitude"])

url = 'https://developer.nrel.gov/api/utility_rates/v3.json?limit=1&api_key=5ip5lQx2Jc5nSHXO93Ric0s7pgD5xg1n06DIDcp1&lat=' + lat + "&lon=" + lon
auth = HTTPBasicAuth('apikey', '5ip5lQx2Jc5nSHXO93Ric0s7pgD5xg1n06DIDcp1')
rsp = requests.request(method, url)

data = rsp.text
parse_json = json.loads(data)
cprice = parse_json["outputs"]["commercial"]
iprice = parse_json["outputs"]["industrial"]
rprice = parse_json["outputs"]["residential"]
provider = parse_json["outputs"]["utility_name"]
# pretty_json = json.dumps(parse_json, indent=4)
#print(provider)
# print(pretty_json)
# print("Commercial price in $/kWh: " + str(cprice)+'\n'+"Industrial price in $/kWh: " + str(iprice)+'\n'+"Residential price in $/kWh: " + str(rprice))
#LED price average * https://www.buildwithrise.com/stories/guide-to-light-bulbs-infographic
  #1$ lifespan 25000 hr
#Incandescent prices
  #4.80 1000 hr
#Fluorescent prices
  #1.20 10000 hr

layout2 = [
    [sg.Text('Purpose (Commercial, Industrial, or Residential)', size =(40, 1)), sg.InputText()],
    [sg.Text('Number of Lightbulbs', size =(40, 1)), sg.InputText()],
    [sg.OK(), sg.Cancel()]
]

window2 = sg.Window('   Lighting Option Price Calculator', layout2, size=(700, 110))
while True:
    event, values = window2.read()
    if event == "OK":
        business = values[0].lower()
        amount = (float(values[1]))
        window2.close()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
#commercial
#source 
price = float(parse_json["outputs"][str(business)])
#price variables
length_cost_LED = round((price*amount*10),2) + amount * 4
length_cost_incan = round((price*amount*60),2) * 25 + amount * 25
length_cost_fluor = round((price*amount*20),2) * 2.5 + amount * 2 * 3

layout3 = [
    [sg.Text("Installing LED lightbulbs will have an initial cost of $" + str(round(4*amount)) + " and cost $" + str(round((price*amount*10),2)) + " per hour to keep on.")],
    [sg.Text("Installing incandescent lightbulbs will have an initial cost of $" + str(round(amount)) + " and cost $" + str(round((price*amount*60),2)) + " per hour to keep on.")],
    [sg.Text("Installing fluorescent lightbulbs will have an initial cost of $" + str(round(2*amount)) + " and cost $" + str(round((price*amount*20),2)) + " per hour to keep on.")],
    [sg.Text("\nPurchasing LED bulbs will save " + str(length_cost_incan - length_cost_LED) + "$ compared to buying incandescent bulbs\nPurchasing LED bulbs will save " + str(length_cost_fluor - length_cost_LED) + "$ compared to buying fluorescent bulbs.")],
    [sg.Button('Done')]
]

window3 = sg.Window('   Lighting Option Price Calculator', layout3, size=(800, 180))
while True:
    event, values = window3.read()
    if event == sg.WIN_CLOSED or event == 'Done':
        window3.close()
        break
    
import matplotlib.pyplot as plt
#led
x = [0,25000]
y = [4,0]
#incandescent
x1 = [0, 1000]
y1 = [1, 0]
#flurorescent
x2 = [0, 10000]
y2 = [2, 0]

plt.plot(x,y,color = "green", linewidth = 3)
plt.plot(x1, y1,color = "red", linewidth = 3)
plt.plot(x2, y2, color = "blue", linewidth = 3)
plt.xlabel("Time From Purchase")
plt.ylabel("Price (Estimated Cash Value)")
plt.ylim(-.01,5)
plt.xlim(-20,25000)

plt.title("Lightbulb Value over Time")

plt.show()

