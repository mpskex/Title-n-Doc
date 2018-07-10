#coding: utf-8
from flask import Flask, request, url_for, render_template, make_response
from flask import abort, redirect

app = Flask("Title_n_Doc")

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

@app.errorhandler(400)
def page_not_found(error):
	return render_template('error.html', resp)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('error.html', resp_code='404', error_message=u'没能找到您请求的网页>_<', \
	reason=u'请检查您的网址是否输入正确'), 404

@app.errorhandler(501)
def internal_error(error):
	return render_template('error.html', resp_code='501', error_message=u'创建路径点失败>_<', \
	reason=u'可能是您输入重复～请您检查输入后再试'), 501

@app.errorhandler(502)
def internal_error(error):
	return render_template('error.html', resp_code='502', error_message=u'输入不完整>_<'), 502

@app.errorhandler(503)
def internal_error(error):
	return render_template('error.html', resp_code='503', error_message=u'无法删除您请求的路径点>_<'), 503

@app.errorhandler(505)
def internal_error(error):
	return render_template('error.html', resp_code='505', error_message=u'未知内部错误!>_<'), 505

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)