from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for

app = Flask(__name__)
@app.route('/')
def my_form():
	confvals=readConf()
	caname=confvals['CANAME']
	return render_template("main.html",caname=caname)

@app.route('/certlist')
def load_certlist():
	confvals=readConf()
	caname=confvals['CANAME']
	return render_template("listcerts.html",caname=caname)

@app.route('/', methods=['POST'])
def get_opt():
	option=request.form['ca_op']
	if option == 'listsignedcerts':
		return redirect(url_for('load_certlist'))
	if option == 'dispcacert':
		return redirect(url_for('load_cacert'))
	if option == 'dispcpcps':
		return redirect(url_for('load_cpcps'))
	if option == 'listrevoked':
		return redirect(url_for('load_revoked'))

@app.route('/revokelist')
def load_revoked():
	confvals=readConf()
	caname=confvals['CANAME']
	revokeddict=dict()
	revocationreason=dict()
	fp=open('revokelist.txt')
	lines=fp.readlines()
	fp.close()
	try:
		for line in lines:
			if line.find('#') != -1:
				continue
			serial=line.split(':')[0]
			dn=line.split(':')[1]
			reason=line.split('\n')[0].split(':')[2]
			revokeddict[serial]=dn
			revocationreason[serial]=reason
	except:
		error_text='File revokelist.txt has entries with incorrect syntax.'
		return render_template('cert-display.html',text=error_text,caname=caname)
		
	return render_template('revoked.html',revokeddict=revokeddict,revocationreason=revocationreason,caname=caname)

@app.route('/cpcps')
def load_cpcps():
	return render_template('cp-cps.html')

@app.route('/cacert')
def load_cacert():
	confvals=readConf()
	caname=confvals['CANAME']
	toopen='rootcert.pem'
	fp=open(toopen)
	lines=fp.readlines()
	fp.close()
	processed_text=''
	for line in lines:
		processed_text+=line
	processed_text=processed_text.replace('\n','<br>')
	return render_template('ca-cert-display.html',text=processed_text,caname=caname)

@app.route('/certlist', methods=['POST'])	
def list_certs():
	confvals=readConf()
	caname=confvals['CANAME']
	certs=dict()
	fp=open('certlist.txt')
	lines=fp.readlines()
	fp.close()
	try:
		for line in lines:
			key=line.split(':')[0]
			val=line.split('\n')[0].split(':')[1]
			certs[key]=val
	except:
		error_text='File certlist.txt has entries with incorrect syntax.'
		return render_template('cert-display.html',text=error_text,caname=caname)

	text = request.form['text']
	if not certs.__contains__(text):
		processed_text='Certificate with specified DN not found'
		return render_template('cert-display.html',text=processed_text,caname=caname)
	else:
		cert=certs[text]
	toopen=confvals['CERTDIR']
	toopen+='/'
	toopen+=cert
	try:
		fp=open(toopen)
		lines=fp.readlines()
		fp.close()
	except:
		error_text='Could not find certificate file specified.'
		return render_template('cert-display.html',text=error_text,caname=caname)
		
	processed_text=''
	for line in lines:
		processed_text+=line
	processed_text=processed_text.replace('\n','<br>')
	return render_template('cert-display.html',text=processed_text,caname=caname)

def readConf():
	confvals=dict()
	fp=open('caops.conf')
	lines=fp.readlines()
	fp.close()
	for line in lines:
		key=line.split('=')[0]
		val=line.split('=')[1].split('\n')[0]
		val=val.translate(None,'\'"')
		confvals[key]=val
	return confvals
if __name__ == '__main__':
	app.run()
