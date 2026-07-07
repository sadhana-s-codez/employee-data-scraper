import requests
import time

URL = "https://api.slingacademy.com/v1/sample-data/files/employees.json"


def get_designation(years):
    if years < 3:
        return "System Engineer"
    elif years <= 5:
        return "Data Engineer"
    elif years <= 10:
        return "Senior Data Engineer"
    else:
        return "Lead"


def fetch_employee_data(retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(URL, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Works whether API returns list or dictionary
                if isinstance(data, dict):
                    employees = data.get("employees", [])
                else:
                    employees = data

                return employees

            else:
                print("Failed to fetch data:", response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed:", e)

            if attempt < retries - 1:
                time.sleep(2)

    return []


def process_employee(employee):

    years = int(employee.get("years_of_experience", 0))

    employee["designation"] = get_designation(years)

    employee["full_name"] = (
        str(employee.get("first_name", "")) +
        " " +
        str(employee.get("last_name", ""))
    )

    phone = str(employee.get("phone", ""))

    if "x" in phone.lower():
        employee["phone"] = "Invalid Number"

    employee["full_name"] = str(employee.get("full_name", ""))
    employee["email"] = str(employee.get("email", ""))
    employee["phone"] = str(employee.get("phone", ""))
    employee["gender"] = str(employee.get("gender", ""))
    employee["age"] = int(employee.get("age", 0))
    employee["job_title"] = str(employee.get("job_title", ""))
    employee["years_of_experience"] = int(employee.get("years_of_experience", 0))
    employee["salary"] = int(employee.get("salary", 0))
    employee["department"] = str(employee.get("department", ""))

    return employee


def main():

    employees = fetch_employee_data()

    if not employees:
        print("No employee data found.")
        return

    for emp in employees:

        emp = process_employee(emp)

        print("Employee ID:", emp.get("id"))
        print("Full Name:", emp["full_name"])
        print("Designation:", emp["designation"])
        print("Email:", emp["email"])
        print("Phone:", emp["phone"])
        print("Gender:", emp["gender"])
        print("Age:", emp["age"])
        print("Job Title:", emp["job_title"])
        print("Years of Experience:", emp["years_of_experience"])
        print("Salary:", emp["salary"])
        print("Department:", emp["department"])
        print("-" * 40)


if __name__ == "__main__":
    main()