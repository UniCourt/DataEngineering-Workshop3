import unittest
import requests


def print_log( *texts ):
    with open("event_logs.txt", "a") as file_object:
        for text in texts:
            file_object.write(str(text) + " ")
        file_object.write("\n")


class Test(unittest.TestCase):

    def test_get_student_branch(self):
      try:
        result = requests.get("http://0.0.0.0:8000/members/students/B.COM")
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result, None)
      except requests.exceptions.ConnectionError:
        print('connection error occurred')

    def test_get_all_students_for_branch(self):
       try:
         required = {'status': 'success',
                     'students': [{'address': 'derla',
                                   'branch': 'B.COM',
                                   'first_name': 'rathan',
                                   'last_name': 'derla',
                                   'mobile': '	987456165',
                                   'roll_number': 2}]}

         result = requests.get("http://0.0.0.0:8000/members/students/2")
         self.assertEqual(result.status_code, 200)
         result = result.json()
         self.assertEqual(result, required)
       except requests.exceptions.ConnectionError:
            print('connection error occurred')
         
