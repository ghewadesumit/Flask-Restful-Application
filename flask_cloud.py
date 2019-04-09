from flask import Flask, render_template, flash, request, url_for, jsonify
import csv

app = Flask(__name__)

#*********************Converting CSV file to JSON file *****************************************
with open('dailyweather.csv') as csvfile:
    csv_rows = []
    onlyDates = []
    readcsv = csv.DictReader(csvfile)
    title = readcsv.fieldnames
    for row in readcsv:
        if row["DATE"] == "DATE":
            continue
        csv_rows.extend([{"DATES": row["DATE"] ,"TMAX": float(row["TMAX"]) ,"TMIN": float(row["TMIN"])}])
        onlyDates.extend([{"DATES":row['DATE']}])

#*******************When the localhost is started *******************************************
@app.route('/')
def index():
    return 'Weather API'

#******************************* historical ************************************************************
@app.route('/historical')
def historical():
	str1= ''
	str1 = ''.join(str(onlyDates))
	return str1

#****************************** historical/YYYYMMDD **************************************************
@app.route('/historical/<datestr>')
def historical_date(datestr):
	for i in range(len(csv_rows)):
	    str1 = ''
	    if datestr == csv_rows[i]["DATES"]:
	        str1 = ''.join(str(csv_rows[i]))
	        return str1

#***************************** forecast/YYYYMMDD ***************************************************
@app.route('/forecast/<datestr>')
def forecast_date(datestr):
	forecast = []
	for i in range(len(csv_rows)):
	    if datestr == csv_rows[i]["DATES"]:
	        for j in range(i,i+7):
	            forecast.extend([csv_rows[j]])
	        str1 = ''
	        str1 = ''.join(str(forecast))
	        return str1

#***************************HTML PAGE ************************************************************
@app.route('/weather/', methods=['GET','POST'])
def weather():
	forecast_date = ''
	forecast = []
	if request.method == 'POST':
		forecast_date = request.form['Dates']
		for i in range(len(csv_rows)):
			if forecast_date == csv_rows[i]["DATES"]:
				for j in range(i,i+7):
					forecast.extend([csv_rows[j]])

	return render_template("index.html", forecast = forecast)

#*************************** POST method Append record in JSON object *******************************************************
@app.route('/historical', methods = ['POST'])
def post_date():
	forecasting_date = {'DATES': request.json['DATES'], 'TMAX': request.json['TMAX'], 'TMIN': request.json['TMIN']}
	csv_rows.append(forecasting_date)
	return '', 201

#************************* POST method to delete the object ***************************************
@app.route('/historical/<datestr>', methods = ['DELETE'])
def delete_date(datestr):
	print('before',datestr)
	for i in range(len(csv_rows)):
		
		print(csv_rows[i]['DATES'])
		if datestr == csv_rows[i]["DATES"]:
			csv_rows.pop(i)
			return 'popped'
		else:
			return 'not found'



if __name__ == '__main__':
	app.run(debug=True)