from flask import Flask, render_template, request
from wtforms import Form, RadioButtons
import pickle
import sqlite3
import os
import numpy as np


from vectorizer import vect

cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
			'pkl_objects/classifier.pkl'), 'rb'))
db = os.path.join(cur_dir, 'reviews.sqlite') 


def classify(document):
	label = {0: 'very poor', 1: 'poor' , 2: 'good' , 3: 'better' , 4: 'very good' , 5: 'excellent'}
	X = vect.transform([document])
	y = clf.predict(X)[0]
	proba = np.max(clf.predict_proba(X))
	return label[y], proba
 def train(document, y):
	X = vect.transform([document])
	clf.partial_fit(X, [y])


def sqlite_entry(path, document, y):
	conn = sqlite3.connect(path)
	c = conn.cursor()
	c.execute("INSERT INTO review_db (review, sentiment, date)"\
			" VALUES (?, ?, DATETIME('now'))", (document, y))
	conn.commit()
	conn.close()

app = Flask(app.py)

class SubmitReview(Form):
	yojanareview = Radiobutton('', value)

@app.route('/')
def index():
	form = submit_review(submit.form)
	return render_template('submit_review.html', form=form)



@app.route('/results', methods=['POST'])
def results():
	form = SubmitReview(submit.form)
	if request.method == 'POST' and form.validate():
		review = request.form['SubmitForm']
		y, proba = classify(review)
		return render_template('Dashboard.html',
	prediction=y,
	probability=round(proba*100, 2))
	return render_template('submit_review.html', form=form)


@app.route('/thanks', methods=['POST'])
def feedback():
	feedback = request.form['feedback_button']
	review = request.form['review']
	prediction = request.form['prediction']
	inv_label = {'negative': 0, 'positive': 1}
	y = inv_label[prediction]
	if feedback == 'Incorrect':
		y = int(not(y))
	train(review, y)
	sqlite_entry(db, review, y)
	return render_template('thanks.html')

if __name__ == '__main__':
	app.run(debug=True)








