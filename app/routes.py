from flask import render_template
from app import app, db
from app.models import Member
from sqlalchemy.exc import IntegrityError
from app.scrapping import Scrapping


@app.route('/')
@app.route('/index')
def index():

	return render_template('app/index.html')

@app.route('/scrap')
def scrap():
	url = "https://www.garrisoninv.com/senior-investment-professionals.php"
	
	scrap = Scrapping()
	scrap.start(url)

	for memb in scrap.members_info:
		 
		u = Member(full_name=memb["full_name"], role=memb["role"], company=memb["company"], division=memb["division"], location=memb["location"], phone_number=memb["phone_number"], email=memb["email"], link_vcf=memb["link_vcf"])
		try:
			db.session.add(u)
			db.session.commit()
		except IntegrityError:
			db.session.rollback()

	db_members = Member.query.all()

	return render_template('app/scraped.html', members=db_members)
