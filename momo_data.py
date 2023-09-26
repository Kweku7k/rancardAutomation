import requests
import csv

def checkMomoData(msisdn):
    try:
        url = "https://payapp.rancard.com/api/v2/topup/emergent/checkMomo?account=8d6b3cb93ec61ff92ef7fd7d2fef3564&msisdn="+msisdn
        print(url)
        response = requests.get(url)
        print(response.status_code)
        print(type(response.text))
        print(type(response.content))
        print(response.json())

        if response.status_code == 200:
            if response.json().get("response") == "success":
                return [response.json().get("lastName"), response.json().get("firstName"), response.json().get("details")]
            else:
                return ["-", "-", response.json().get("details")]
        else:
            return "Request Failed!"
    
    except Exception as e:
        print(e)
        return "Completed With An Exception."

def modify_last_value(input_file, output_file, modification_function):
    try:
        with open(input_file, 'r', newline='') as csv_infile, \
             open(output_file, 'w', newline='') as csv_outfile:

            reader = csv.reader(csv_infile)
            writer = csv.writer(csv_outfile)

            print(reader)

            # header = next(reader)
            # header.append(["surName", "firstName", "details"])

            count = 0
            for row in reader:
                count += 1
                if len(row) > 0:
                    # Modify the last value using the provided modification_function
                    for i in checkMomoData(row[0]):
                        row.append(i)
                else:
                    row.append("FLOP.")
                print("------------",count)
                writer.writerow(row)

        print("CSV file modification complete.")
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:
def modify_function(value):
    # Modify the last value as needed (e.g., converting to uppercase)
    return value.upper()

# input_file = "input.csv"
# output_file = "output.csv"

modify_last_value('rewardSheet.csv', 'momodata.csv', checkMomoData)
# print(checkMomoData('233545977791'))
