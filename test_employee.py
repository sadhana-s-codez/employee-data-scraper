import unittest
import requests
from employee import fetch_employee_data, process_employee, get_designation

URL = "https://api.slingacademy.com/v1/sample-data/files/employees.json"


class TestEmployee(unittest.TestCase):

    def test_json_download(self):
        response = requests.get(URL, timeout=10)
        self.assertEqual(response.status_code, 200)

    
    def test_json_extraction(self):
        employees = fetch_employee_data()

        self.assertIsInstance(employees, list)
        self.assertGreater(len(employees), 0)

    
    def test_file_type_and_format(self):
        response = requests.get(URL, timeout=10)

        self.assertIn(
            "application/json",
            response.headers["Content-Type"]
        )

    
    def test_data_structure(self):
        employees = fetch_employee_data()

        employee = process_employee(employees[0])

        required_fields = [
            "id",
            "full_name",
            "designation",
            "email",
            "phone",
            "gender",
            "age",
            "job_title",
            "years_of_experience",
            "salary",
            "department"
        ]

        for field in required_fields:
            self.assertIn(field, employee)

    
    def test_invalid_phone(self):
        sample = {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "123456x",
            "years_of_experience": 2,
            "email": "",
            "gender": "",
            "age": 25,
            "job_title": "",
            "salary": 10000,
            "department": ""
        }

        result = process_employee(sample)

        self.assertEqual(result["phone"], "Invalid Number")

    
    def test_designation(self):
        self.assertEqual(get_designation(2), "System Engineer")
        self.assertEqual(get_designation(4), "Data Engineer")
        self.assertEqual(get_designation(8), "Senior Data Engineer")
        self.assertEqual(get_designation(12), "Lead")


if __name__ == "__main__":
    unittest.main()