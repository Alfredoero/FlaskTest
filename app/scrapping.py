from bs4 import BeautifulSoup
import requests
import urllib.request
import vobject
import ssl
from urllib.parse import urlparse

ssl._create_default_https_context = ssl._create_unverified_context


class Scrapping:
	
	url = ""
	members_info = []

	def start(self, url):
		request = urllib.request.urlopen(url)
		soup = BeautifulSoup(request, "html.parser")
		members_list = soup.findAll('div', {'class': 'member'})

		for memb in members_list:
			self.members_info.append(self.get_info(memb, url))


	def get_info(self, member, url):
	
		full_name = member.h2.text
		division = member.findAll('div', {'class': 'position'})
		spans = member.findAll('span')
		dns = self.get_dns(url)
		vcf_c = "%s/%s" % (dns, spans[2].a['href'])

		file_vcf = urllib.request.urlretrieve(vcf_c.replace(' ', '%20'), "vcards/%s.vcf" % full_name)		
		downloaded_file = open("vcards/%s.vcf" % full_name, 'r', encoding="utf-8")
		vcard = vobject.readOne(downloaded_file, allowQP=True)
		try:
			org = vcard.contents['org'][0].value
		except KeyError:
			location = "Not Found"
		try:
			tel = vcard.contents['tel'][0].value
		except KeyError:
			location = "Not Found"
		try:
			email = vcard.contents['email'][0].value			
		except KeyError:
			location = "Not Found"
		try:
			role = vcard.contents['title'][0].value
		except KeyError:
			location = "Not Found"
		try:
			streets = " ".join([ street for street in vcard.contents['adr'][0].value.street if street!=""])
			location = "%s %s %s" % (streets, vcard.contents['adr'][0].value.city, vcard.contents['adr'][0].value.country)
		except KeyError:
			location = "Not Found"

		return {'full_name': full_name, 'role': role, 'company': org[0], 'division': division[0].text, 'location': location, 'phone_number': tel, 'email': email, 'link_vcf': vcf_c}


	def get_dns(self, url):
		return "https://%s" % urlparse(url).hostname


