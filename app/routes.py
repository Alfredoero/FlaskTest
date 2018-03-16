from flask import render_template
from app import app, db
from bs4 import BeautifulSoup
from app.models import Member
from sqlalchemy.exc import IntegrityError
import requests
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


@app.route('/')
@app.route('/index')
def index():

	return render_template('app/index.html')

@app.route('/scrap')
def scrap():
	url = "https://www.garrisoninv.com/senior-investment-professionals.php"
	request = urllib.request.urlopen(url)

	soup = BeautifulSoup(request, "html.parser")

	members_list = soup.findAll('div', {'class': 'member'})

	for memb in members_list:
		full_name = memb.h2.text
		role = memb.findAll('div', {'class': 'position'})


		u = Member(full_name=full_name, role=role[0].text, company="", division="", location="", phone_number="", email="", link_vcf="")
		try:
			db.session.add(u)
			db.session.commit()
		except IntegrityError:
			db.session.rollback()



	db_members = Member.query.all()

	return render_template('app/scraped.html', members=db_members)
