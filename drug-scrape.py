from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import details #importing from details.py in same folder containing email/password

#genanki stuff
import sys
from genanki import Model
from genanki import Note
from genanki import Deck
from genanki import Package

CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
}
"""
MY_CLOZE_MODEL = Model(
  998877661,
  'My Cloze Model',
  fields=[
    {'name': 'Text'},
    {'name': 'Extra'},
  ],
  templates=[{
    'name': 'My Cloze Card',
    'qfmt': '{{cloze:Text}}',
    'afmt': '{{cloze:Text}}<br>{{Extra}}',
  },],
  css=CSS,
  model_type=Model.CLOZE)

notes = []

#begin webdriver
driver = webdriver.Chrome(executable_path="./chromedriver.exe") #??

driver.get(details.scrape_link)
time.sleep(1);
#click accept button on uniKey paywall page
driver.find_element_by_class_name('accept').click();
time.sleep(1);

#fill in login details and submit form for login
driver.find_element_by_id('userNameInput').send_keys(details.email)
driver.find_element_by_id('passwordInput').send_keys(details.password)
driver.find_element_by_id('submitButton').click();
time.sleep(1);

contentList = driver.find_elements_by_class_name('index')[6].find_elements_by_tag_name('a')

# Fetch and store the links in object links[]
links = []
for item in contentList:
    links.append(item.get_attribute('href'))

for link in links:
  driver.get(link)
  # time.sleep(1)
  # print(link)
  # title = driver.find_elements_by_tag_name('header')[1].find_elements_by_tag_name('h1')[0].text
  # MOA = driver.get_elements_by_class_name('mode-action')[1].text
  # indication = driver.get_elements_by_class_name('indication')[1].text
  # adv_eff = driver.get_elements_by_class_name('adv-eff')[1].text
  # dosage = driver.get_elements_by_class_name('dosage')[1].text
  # prac_pts = driver.get_elements_by_class_name('prac-pts')[1].text
  field = "'"
  try:
    title = driver.find_elements_by_tag_name('header')[1].find_elements_by_tag_name('h1')[0].text
    field += "<b>" + title + " </b>" + ": <br /> ";
  except:
    print("Title not found")

  field += "<b> Link: </b> " + link + " <br /> "
  try:
    MOA = driver.find_elements_by_class_name('mode-action')[1].text.replace('\n', ' <br/>').replace('Mode of action:', '')
    field += "<br /><b> Mechanism of action: </b> <br /> {{c1:: " + MOA + "}} <br /> "
  except:
    print("MOA not found")

  try:
    indication = driver.find_elements_by_class_name('indication')[1].text.replace('\n', ' <br/>').replace('Indications:', '')
    field += "<br /><b> Indication: </b> <br /> {{c2::" + indication + "}} <br /> "
  except:
    print("Indication not found")

  try:
    adv_eff = driver.find_elements_by_class_name('adv-eff')[1].text.replace('\n', ' <br/>').replace('Adverse effects:', '')
    field += "<br /><b> Adverse effects </b> <br /> {{c3::" + adv_eff + "}} <br /> "
  except:
    print("adverse effects not found")

  try:
    dosage = driver.find_elements_by_class_name('dosage')[1].text.replace('\n', ' <br/>').replace('Dosage –', '')
    field += "<br /><b> Dosage </b> <br /> {{c4::" + dosage + "}} <br /> "
  except:
    print("dosage not found")
    
  try:
    prac_pts = driver.find_elements_by_class_name('prac-pts')[1].text.replace('\n', ' <br/>').replace('Practice points:', ' ')
    field += "<br /><b> Practical points </b> <br /> {{c5::" + prac_pts + "}}"
  except:
    print("practical points not found")
  
  field += "'"
  fields = [field, ' ']
  # # Question: NOTE TWO: [...]              2nd deletion     3rd deletion
  # # Answer:   NOTE TWO: **1st deletion**   2nd deletion     3rd deletion
  # #
  # # Question: NOTE TWO: 1st deletion       [...]            3rd deletion
  # # Answer:   NOTE TWO: 1st deletion     **2nd deletion**   3rd deletion
  # #
  # # Question: NOTE TWO: 1st deletion       2nd deletion     [...]
  # # Answer:   NOTE TWO: 1st deletion       2nd deletion   **3rd deletion**
  # fields = ['NOTE TWO: {{c1::1st deletion}} {{c2::2nd deletion}} {{c3::3rd deletion}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  notes.append(my_cloze_note)

deckname = 'AMH_drugs'
deck = Deck(deck_id=0, name=deckname)
for note in notes:
  deck.add_note(note)
fout_anki = '{NAME}.apkg'.format(NAME=deckname)
Package(deck).write_to_file(fout_anki)
print('{N} Notes WROTE: {APKG}'.format(N=len(notes), APKG=fout_anki))





