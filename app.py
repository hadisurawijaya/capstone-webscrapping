from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'table-responsive'})
row = table.find_all('td', attrs={'class':'text-narrow-screen-hidden'})

row_length = len(row)

temp = [] #initiating a list 

for i in range(0, row_length):
    
    #get date
    period = table.find_all('td')[i*4].text
    
    #get rate
    rate = table.find_all('a')[i*2].text
    rate = rate.strip() #to remove excess white space
    
    temp.append((period, rate)) 

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('period','rate'))

#insert data wrangling here
data['period'] = data['period'].astype('datetime64')
data['rate'] = data['rate'].str.replace(",", "")
data['rate'] = data['rate'].astype('float64')
data = data.set_index('period')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)