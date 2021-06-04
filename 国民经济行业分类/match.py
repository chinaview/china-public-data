import PyPDF2
pdf = './国民经济行业分类.pdf'
#
# f = open(pdf, 'rb')
# pdfReader = PyPDF2.PdfFileReader(f)
#
# pages = pdfReader.getNumPages()
#
# page = pdfReader.getPage(220).extractText()
import pandas as pd
gt = pd.read_csv('国民经济行业分类_2017.csv')

import tika
tika.initVM()
from tika import parser
parsed = parser.from_file(pdf)
content = parsed['content'].split('\n')
# for i, c in enumerate(content):
#     if '151' in c:
#         print(i)
#         pass

content = content[14198:]
lines = []
for c in content:
    try:
        int(c)
        continue
    except:
        pass
    if len(c.strip()) == 0:
        continue
    if len(c.replace('国民经济行业分类（GB/T 4754-2017） 所有经济活动的国际标准行业分类（ISIC Rev.4）', '').strip()) == 0:
        continue
    else:
        lines.append(c)
        print(c)

import pandas as pd

rev = pd.DataFrame(columns=['code', 'name'])

df = pd.DataFrame(columns=['GB/T 4754-2017 (code)', 'GB/T 4754-2017 (desc)', 'ISIC Rev.4 (code)', 'ISIC Rev.4 (desc)'])

lines = lines[5:]

import re
match = dict()

values = []
key = None
for i, line in enumerate(lines):
    digits = re.findall(r"\D(\d{4})\D", " "+line+" ")
    if len(digits) == 2:
        if key:
            match[key] = values
        key = digits[0]
        values = []
        values.append(digits[1])
    if len(digits) == 1:
        values.append(digits[0])

match[key] = values # for last val 9700
pass


values = []
key = None
for i, line in enumerate(lines):
    digits = re.findall(r"\D(\d{4})\D", " "+line+" ")
    if len(digits) == 2:
        code = digits[1]
        desc = line.split(code)[-1].strip()
        rev.loc[len(rev)] = [code, desc]

    if len(digits) == 1:
        code = digits[0]
        desc = line.split(code)[-1].strip()
        rev.loc[len(rev)] = [code, desc]

match[key] = values # for last val 9700
pass

rev.drop_duplicates(keep='first', inplace=True)

for key in match.keys():
    values = match[key]
    for value in values:
        revrow = rev.loc[rev['code'] == value]
        gtrow = gt.loc[gt['code'] == key]

        try:
            df.loc[len(df)] = [key, gtrow.iloc[0]['name'], value, revrow.iloc[0]['name']]
        except IndexError:
            continue

        pass

df.to_csv('附录 C.csv', index=False)
if __name__ == "__main__":
    pass
