import requests
import os
import time
from urllib.parse import quote
import csv
import os
import xml.etree.ElementTree as ET

PREFECTURES = {'1':'北海道', '2':'青森県', '3':'岩手県', '4':'宮城県', '5':'秋田県', '6':'山形県', '7':'福島県', '8':'茨城県', '9':'栃木県', '10':'群馬県', '11':'埼玉県', '12':'千葉県', '13':'東京都', '14':'神奈川県', '15':'新潟県', '16':'富山県', '17':'石川県', '18':'福井県', '19':'山梨県', '20':'長野県', '21':'岐阜県', '22':'静岡県', '23':'愛知県', '24':'三重県', '25':'滋賀県', '26':'京都府', '27':'大阪府', '28':'兵庫県', '29':'奈良県', '30':'和歌山県', '31':'鳥取県', '32':'島根県', '33':'岡山県', '34':'広島県', '35':'山口県', '36':'徳島県', '37':'香川県', '38':'愛媛県', '39':'高知県', '40':'福岡県', '41':'佐賀県', '42':'長崎県', '43':'熊本県', '44':'大分県', '45':'宮崎県', '46':'鹿児島県', '47':'沖縄県'}
URL = "http://api.calil.jp/library?pref={}&appkey={}"

PATH = "./libraries/"
OUTPUT = "libraries.csv"
COLOMUS = ["systemid", "systemname", "libkey", "libid", "short", "formal", "url_pc", "address", "pref", "city", "post", "tel", "geocode", "category", "image"]
GEO = ["longtitude", "latitude"]

# crawler
for key, pref in PREFECTURES.items():
    print(pref)
    time.sleep(1)
    with open("./libraries/"+key+".xml", "w", encoding="utf-8") as f:
        xml = requests.get(URL.format(quote(pref), os.environ["CALIL_API_KEY"]))
        f.write(xml.text)


# parser
with open(OUTPUT, "a", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(COLOMUS + GEO)

for libxml in os.listdir(PATH):
    if libxml == OUTPUT:
        continue
    print(libxml)
    tree = ET.parse(PATH+libxml)
    root = tree.getroot()
    for child in root:
        row = []
        lnglat = []
        for col in COLOMUS:
            try:
                text = child.find(col).text
                if text:
                    row.append(text)
                else:
                    row.append("")

                if col == "geocode":
                    lnglat = text.split(",")
            except AttributeError as e:
                row.append("")
        else:
            row.extend(lnglat)

        with open(PATH+OUTPUT, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
