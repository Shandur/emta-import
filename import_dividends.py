import csv
import requests
from http import HTTPStatus

# Personal unique declaration ID.
declaration_id = 0

# Request headers.
request_headers = {
    "Cookie": "TODO",
    "x-principal-person-id": "TODO",
    "x-xsrf-token": "TODO",
}

# Global static declaration request data.
# Do not edit!
income_type = "4"
declaration_part = "FOREIGN_OTHER_INCOME"
base_url = "https://maasikas.emta.ee"

csv_file_path = "dividends.csv"


def create_records(records: csv.DictReader):
    session = requests.Session()
    session.headers.update(request_headers)

    records_count = 0
    row_number = 1
    for record in records:
        name = record.get("name")
        code = record.get("code")
        country = record.get("country")
        currency = record.get("currency")
        income = record.get("income")
        payout_date = record.get("payout_date")
        income_tax = record.get("income_tax")
        tax_date = record.get("tax_date")
        declaration_id = record.get("declaration_id")

        # Fetching the next record version.
        version = next_version(session)

        request_body = {
            "part": declaration_part,
            "name": name,
            "code": code,
            "country": country,
            "incomeType": income_type,
            "currency": currency,
            "income": income,
            "payoutDate": payout_date,
            "incomeTax": income_tax,
            "taxDate": tax_date,
            "foreignSalaryTableVersion": None,
            "declarationId": declaration_id,
            "version": version,
        }

        print(f"Entry for row #{row_number}: {request_body} \n\n")
        resp = session.post(
            f"{base_url}/fidek23-api/client/foreign/other-income", json=request_body
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(
                f"got {resp.status_code} for row {row_number}: {resp.json()}"
            )

        records_count += 1
        row_number += 1
    print(f"Created {records_count} records.")
    return


# Fetching the version for the next record in the declaration.
def next_version(session: requests.Session):
    resp = session.get(
        f"{base_url}/fidek23-api/client/foreign/other-income?declarationId={declaration_id}&idPrint=false&jointApplicationId=&prefilled=false"
    )
    if resp.status_code != HTTPStatus.OK:
        raise Exception(
            f"failed to fetch next version - got {resp.status_code} code: {resp.json()}"
        )

    version = resp.json()["data"]["version"]
    if not version:
        raise Exception(
            f"failed to find next version from 'data' - check the response: {resp.json()}"
        )

    return version


def main():
    with open(csv_file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        create_records(reader)


if __name__ == "__main__":
    main()
