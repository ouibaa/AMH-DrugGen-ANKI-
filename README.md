# AMH-DrugGen-ANKI-

A python 3.0 script which accesses the AMH database and generates ANKI scripts.
Once AMH database access is established (Mechanism is not provided - has been deleted from available scripts),
a python script running Selenium (w/ Python bindings) and chromedriver will scrape the relevant panel for all links to drugs

A key file not included is 'details.py' - this carries environment variables including:

- details.scrape_link: a string containing the link to our proxy which accesses AMH
- details.email: An email address to access proxy
- details.password: the password to access proxy

Initiate script with:

```
python drug-scrape.py
```

The script will scrape for:

- drug name
- MOA
- indications
- Adverse effects
- dosage
- practical points

No additional scrapings will be completed
Once scraped, the genanki library is used to rapidly generate a cloze deck for each of these sections (except drug name and link).

Further additions to consider:

- scraping and determining main indication
- maintaining innerHTML to allow for proper formatting in anki deck (as anki deck uses HTML formatting)
