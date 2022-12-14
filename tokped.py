# Tokopedia Product Scrap v1.0
# https://github.com/heryandp 
# heryandp

import requests,glob, json, os,csv
from bs4 import BeautifulSoup as bs

class tokopedia():

	def __init__(self, namatoko):
		self.tokourl = 'https://tokopedia.com/'+namatoko
		self.namatoko = namatoko
		self.headerbrowser = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
		print(self.tokourl)
		self.getid()
	
	def getid(self):
		try:
			req = requests.post(self.tokourl, headers=self.headerbrowser, timeout=300)
			# print(req.status_code)
			if req.status_code == 200:
				sup = bs(req.text, 'html.parser')
				for i in sup.find_all('meta', attrs={'name':'branch:deeplink:$android_deeplink_path'}):
					self.idToko = i.get('content')[5:]
					# print('id Toko : '+self.idToko)
				self.getData()
			else:
				print('Toko Tidak ditemukan')
		except Exception as e:
			# print(e)
			print("Timeout/Toko tidak valid!")
	
	def getData(self):
		print("====== GRABBING PRODUK ======")
		print("[+] Mulai download produk ...")
		urlJson = 'https://ace.tokopedia.com/search/product/v3?shop_id={}&rows=15000&start=0&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=shop_product'.format(self.idToko)
		req = requests.get(urlJson, headers=self.headerbrowser,timeout=300).json()
		# hapus file lama
		print("[+] Hapus file lama ...")
		if not os.path.exists("data"):
			os.makedirs("data")
		for filename in glob.glob("data/"+self.idToko+"_tokped.json"):
			os.remove(filename)
		for filename in glob.glob(self.idToko+'_tokped.csv'):
			os.remove(filename)
		# dump json
		print("[+] Membuat csv data produk ...")
		with open("data/"+self.idToko+"_tokped.json", 'w') as json_file:
			json.dump(req['data']['products'],json_file)
		# load json
		f = open("data/"+self.idToko+"_tokped.json")
		f_read = json.load(f)
		csv_data = []
		for i in f_read:
			try:
				ori_p = i['original_price'].replace("Rp","")
				csv_data.append([
					self.idToko,
					self.namatoko,
					i['id'],
					i['url'],
					i['name'],
					i['category_name'],
					i['stock'],
					i['rating_average'],
					i['count_review'],
					i['price_int'],
					ori_p.replace(".",""),
					i['discount_percentage'],
					i['count_sold'].replace("Terjual ","")
				])
			except KeyError:
				csv_data.append([
					self.idToko,
					self.namatoko,
					i['id'],
					i['url'],
					i['name'],
					i['category_name'],
					i['stock'],
					i['rating_average'],
					i['count_review'],
					i['price_int'],
					ori_p.replace(".",""),
					i['discount_percentage'],
					0
				])
		csv_header = ['id_toko','toko','id_produk','url_produk','produk','kategori','stok','rating','review','harga','harga_asli','diskon','terjual']
		with open(self.idToko+'_tokped.csv', 'w',newline='', encoding='utf-8') as file:
			writer = csv.writer(file)
			writer.writerow(csv_header)
			writer.writerows(csv_data)
		print('done! '+ self.idToko+'_tokped.csv')
		f.close()

print("[ TOKOPEDIA-PRODUCT-GRABBER v1.0 by heryan ]")
print(" _____     _                        _ _       ")
print("|_   _|   | |                      | (_)      ")
print("  | | ___ | | _____  _ __   ___  __| |_  __ _ ")
print("  | |/ _ \| |/ / _ \| '_ \ / _ \/ _` | |/ _` |")
print("  | | (_) |   < (_) | |_) |  __/ (_| | | (_| |")
print("  \_/\___/|_|\_\___/| .__/ \___|\__,_|_|\__,_|")
print("                    | |                       ")
print("                    |_|                       ")
print("[+] https://github.com/heryandp/tokopedia-product-scrap")
inputLink = input('[+] Masukkan username toko : https://www.tokopedia.com/')
actionToko = tokopedia(inputLink)