# emta-import

Helps to import dividends data and withholding taxes to "8.8 Income received in a foreign country and exempt from tax in Estonia" section in [EMTA](https://emta.ee) instead of manually entering them one-by-one.

Also provides a script to transform and import dividends summary from [InteractiveBrokers](https://www.interactivebrokers.co.uk/).

## Setup

Script requires [requests](https://pypi.org/project/requests/) library and was tested with Python 3.11.

```bash
git clone git@github.com:Shandur/emta-import.git
```

## Notes

- Right now, the script supports **only** US-based companies - support for other countries will come later.
- The script will match dividends and withholding taxes based on company symbol and date. If withholding tax doesn't match with any dividend records, the will be skipped.


## How to run

### (optional) Transforming data from IBKR
- In the (root) folder of this project, create an empty `ibkr_dividends.csv` file and leave it for now
- Log-in into IBKR and find a page with "Reports"
- Download "Activity" summary rport as SCV file for the year you're interested in
- Open the file in the text editor or Excel/Google Sheet
- You will need to find `Dividends,Header,Currency,Date,Description,Amount` row and copy **everything** till the row that contains `Withholding Tax,Data,Total in EUR,,,-1.131231,`. Check [ibkr_dividends_example.csv](./ibkr_dividends_example.csv) for an example
- Open the terminal and run `python ibkr_transform`. The script should create `dividends.csv` file that will be used in the following section

### Import dividends
- Open [import_dividends.py](./import_dividends.py) file. Find `declaration_id` and `request_headers` variables - you will update them later
- Log-in into [EMTA](https://emta.ee) and go to your personal profile
- Open "Taxes" section - it should open the latest relevant year
- Next, you need to open developer tools (devtools) in your browser:
  - in Google Chrome, go to "View" -> "Developer" -> "Developer Tools" (the doc will describe steps assuming this browser but other browsers should have similar functionality)
  - for other browser, check the relevant documentation of how to open "Developer Tools"
- In the devtools, open "Network" tab to see the list of all network connections on the website. You may need to resize the window to see more tabs
- Reload the page - you should see a list of different entries in the "Network" tab
- Click on the record that has `https://maasikas.emta.ee/fidek23-api/client/income` URL (you can use search bar to find the URL)
- Then go to "Headers" tab and find "Request headers" section. Click on it to unfold if it's folded. You will need to copy-paste **values** of request headers and add them to the **corresponding** **variables** in `import_dividends.py` file that you've opened recently. **Do not share these values with anyone!**
- Copy values of the following headers and add them to the corresponding keys to the `request_headers` variable:
  - `Cookie`
  - `X-Principal-Person-Id`
  - `X-Xsrf-Token`

So your updated `request_headers` variable may look like this:
```
request_headers = {
    "Cookie": "PAS-AUTHORIZATION=xxxxxxxxxxxxxxxxx; PAS-XSRF-TOKEN=xxxxxxxxxxx; MTASSO-TAG-gkju1j=6; .....",
    "x-principal-person-id": "123456789",
    "x-xsrf-token": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",
}
```
- Then, click on "General" section - it should be above the "Request Headers" section. Find "Request URL", copy the **numeric** value after `declarationId` parameter, and add the value into `declaration_id` variable in `import_dividends.py` file.

Example: `https://maasikas.emta.ee/fidek23-api/client/income?calculateSums=true&checkErrors=true&declarationId=123456789` -> copy only `123456789`

- Next, prepare `dividends.csv` file following the structure from the [example file](./dividends_example.csv). You can export CSV file from Excel or Google Sheet. But the first row must must have the same headers as in the example file.
- Check `companies.json` file. If some symbols are missing from `companies.json`, the script will use the symbol as the the name by default. You can either extend the list with the missing companies (and create a PR) or leave it as it is.
- Once everything is ready, open the terminal and run `python import_dividends.py` script. In case of success, it should show `Created {records_count} records.` message.
- **IMPORTANT!** In case of an error, the error message will show the actual row where the script failed. If you re-run the script, remove the data records that reside before the failing row (e.g., row #5 has failed, so you'd need to remove rows 2-4. Headers must stay). Otherwise, the script will create old records again starting from the beginning.

## TODO Improvements

- [ ] Support country codes for each symbol in `companies.json`
- [ ] Add more companies to `companies.json` or connect to 3rd-party API
- [ ] Add some simple UI to import dividends
- [ ] Add some visuals for the docs

## License

This package is under the [MIT License](LICENSE) license.
