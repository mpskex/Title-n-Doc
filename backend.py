#coding: utf-8
import model
from keywords import ParsingException
from flask import Flask, request, url_for, render_template, make_response
from flask import abort, redirect

""" 
Title-n-Doc
    mpskex @ github
"""

app = Flask("Title_n_Doc")
m = model.w2v_model(pretrained='1000v500')

@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def index():
	"""
	Index
	"""
	if request.method == 'GET':
		return render_template('index.html')
	else:
		return make_response('Error')

@app.route('/submit', methods = ['POST', 'GET'])
def submit():
	"""
	Submit page
	"""
	if request.method == 'POST':
		content = request.form.get('input_content')
		title = request.form.get('input_title')
		print('content: ', content, '\ntitle: ', title, "\n")
		if content is None or title is None:
			abort(501)
		#	TODO:	Funtion code here
		try:
			dist = m.dist_docs(title, content, method='mean_euclid')
		except ParsingException as e:
			abort(502)
		html_str = ""
		return render_template('submit.html', result=dist)
	else:
		abort(404)

@app.errorhandler(400)
def page_not_found(error):
	return render_template('error.html', resp)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('error.html', resp_code='404', error_message=u'没能找到您请求的网页>_<', \
	reason=u'请检查您的网址是否输入正确'), 404

@app.errorhandler(501)
def internal_error(error):
	return render_template('error.html', resp_code='501', error_message=u'输入数据有空>_<', \
	reason=u'可能是您输入有空～请您检查输入后再试'), 501

@app.errorhandler(502)
def internal_error(error):
	return render_template('error.html', resp_code='502', error_message=u'中文解析出现问题>_<', \
	reason=u'可能是您输入的词汇我全都不知道呢'), 502
@app.errorhandler(503)
def internal_error(error):
	return render_template('error.html', resp_code='503', error_message=u'无法删除您请求的路径点>_<'), 503

@app.errorhandler(505)
def internal_error(error):
	return render_template('error.html', resp_code='505', error_message=u'未知内部错误!>_<'), 505

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)