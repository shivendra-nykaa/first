from flask import render_template,jsonify,request,make_response
from mine import app
import csv
import logging
from datetime import datetime as dt
from pythonjsonlogger import jsonlogger
from jsonformatter import JsonFormatter

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Shivendra'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user,posts=posts)

@app.before_request
def beforerequest():
	file_handler = logging.FileHandler('request.log')
	file_handler.setLevel(logging.DEBUG)
	headers_ = request.headers
	jsonformatter = jsonlogger.JsonFormatter(
		'%(levelname) %(headers_) %(name) %(filename) %(module) %(funcName) %(lineno) '
		'%(message) %(asctime)', datefmt='%m/%d/%Y %I:%M:%S %p')
	file_handler.setFormatter(jsonformatter)
	loggers = [
		#application.logger,
		logging.getLogger()
	]

	for logger in loggers:
		try:
			logger.addHandler(file_handler)
			logger.info('testing',extra={"headers": headers_})
		except Exception as e:
			print(e)

	print(str(request.headers))

def movies_list():
	with open('/home/shivendra.singh/shivam/app/mine/movies.csv') as csv_file:
		data=csv.reader(csv_file, delimiter=',')
		places = []
		first_line=True
		for row in data:
			if not first_line:
				places.append({"Film": row[0],"genre":row[1], "studio":row[2], "audience_score": row[3], "profitability": row[4], "rotten": row[5], "gross":row[6], "year":row[7]})
			else:
				first_line = False

	return places

def get_paginate(result, url, start, limit):
	count=len(result)
	if (count<start):
		abort(404)

	mp={}
	mp['start'] = start
	mp['limit'] = limit
	mp['count'] = count
	if start==1:
		mp['previous'] =''
	else:
		start_copy=max(1,start-limit)
		limit_copy=start-1
		mp['previous'] = url +'?start=%d&limit=%d'%(start_copy,limit_copy)

	if (start+limit)>count:
		mp['next'] = ''
	else:
		start_copy = start+limit
		mp['next'] = url + '?start=%d&limit=%d'%(start_copy,limit)

	mp['result']=result[(start-1):(start-1+limit)]
	return mp

@app.route('/movies', methods=['GET'])
def movies_s():
    movies=movies_list()
    start=int(request.args.get('start',1))
    limit=int(request.args.get('limit',3))
    headers = request.headers
    #head = Response.headers
    #return jsonify({'headers': str(dict(headers))})
    #print(ax)
    #return ax
    return jsonify(get_paginate(movies, '/movies', start, limit))

@app.route('/movies/<int:yr>', methods=['GET'])
def movie_year(yr):
	movies=movies_list()
	result=[]
	for mov in movies:
		if int(mov["year"])==yr:
			result.append(mov)

	start=int(request.args.get('start',1))
	limit=int(request.args.get('limit',3))
	#return jsonify({'Movies': result})
	#return jsonify(get_paginate(result, '/movies/yr',start,limit))
	return str(yr)

#@app.route('/movies/<string:mn>', methods=['GET'])
def movies_n():
	movies=movies_list()
	result=[]
	for mov in movies:
		if mov["Film"]==mn:
			result.append(mov)

	return jsonify({'Movies': result})

@app.route('/movies/<string:genre>',methods=['GET'])
def genre(genre):
	movies=movies_list()
	start=request.args.get('start',1)
	limit=request.args.get('limit',3)
	result=[]
	for mov in movies:
		if mov["genre"]==genre:
			result.append(mov)

	return jsonify({'Movies': result})
	#return jsonify(get_paginate(result, '/movies/genre',start,limit))
	#return genre
