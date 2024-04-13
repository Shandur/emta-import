import csv
import re
import json


def compile_data(input_file, output_file):
    dividend_data = {}
    withholding_tax_data = {}

    # Company symbols to names.
    with open("companies.json") as json_data:
        company_symbol_names = json.load(json_data)

    with open(input_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (
                row["Header"] == "Data"
                and row["Description"]
                and row["Description"] != "Total"
            ):
                match = re.search(r"\((.*?)\)", row["Description"])
                if match:
                    company_code = match.group(1)
                    company_symbol = row["Description"][: match.start()].strip()
                    operation_date = row["Date"]
                    currency = row["Currency"]
                    amount = row["Amount"]
                    country = "USA" if currency == "USD" else ""

                    key = (company_symbol, company_code, operation_date)

                    company_name = company_symbol
                    if company_symbol in company_symbol_names:
                        company_name = company_symbol_names[company_symbol]

                    # Determine current section based on the "Dividends" header value.
                    if row["Dividends"] == "Dividends":
                        dividend_data[key] = {
                            "name": company_name,
                            "symbol": company_symbol,
                            "code": company_code,
                            "currency": currency,
                            "income": amount,
                            "payout_date": operation_date,
                            "country": country,
                        }
                    elif row["Dividends"] == "Withholding Tax":
                        withholding_tax_data[key] = {
                            "income_tax": abs(float(amount)),
                            "tax_date": operation_date,
                        }

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "symbol",
                "name",
                "code",
                "country",
                "currency",
                "income",
                "payout_date",
                "income_tax",
                "tax_date",
            ]
        )
        for key in dividend_data:
            if (
                key in withholding_tax_data
                and dividend_data[key]["payout_date"]
                == withholding_tax_data[key]["tax_date"]
            ):
                writer.writerow(
                    [
                        dividend_data[key]["symbol"],
                        dividend_data[key]["name"],
                        dividend_data[key]["code"],
                        dividend_data[key]["country"],
                        dividend_data[key]["currency"],
                        dividend_data[key]["income"],
                        dividend_data[key]["payout_date"],
                        withholding_tax_data[key]["income_tax"],
                        withholding_tax_data[key]["tax_date"],
                    ]
                )


def main():
    compile_data("ibkr_dividends.csv", "dividends.csv")


if __name__ == "__main__":
    main()
