from python_linq import From
import unittest

class Nested(unittest.TestCase):
    
    def setUp(self):
        self.grades = [
            {
                "id": 1,
                "name": "Jakob",
                "grades": [
                    {
                        "courseId": 23,
                        "courseName": "Complex Analysis",
                        "credits": 6,
                        "grade": 5.0
                    },
                    {
                        "courseId": 36,
                        "courseName": "Calculus I",
                        "credits": 9,
                        "grade": 5.0
                    }
                ]
            },
            {
                "id": 2,
                "name": "Lpuise",
                "grades": [
                    {
                        "courseId": 23,
                        "courseName": "Complex Analysis",
                        "credits": 6,
                        "grade": 5.0
                    },
                    {
                        "courseId": 36,
                        "courseName": "Calculus I",
                        "credits": 9,
                        "grade": 4.5
                    }
                ]
            },
            {
                "id": 3,
                "name": "Daniel",
                "grades": [
                    {
                        "courseId": 23,
                        "courseName": "Complex Analysis",
                        "credits": 6,
                        "grade": 3.5
                    },
                    {
                        "courseId": 36,
                        "courseName": "Calculus I",
                        "credits": 9,
                        "grade": 3.0
                    }
                ]
            },
            {
                "id": 4,
                "name": "John",
                "grades": [
                    {
                        "courseId": 23,
                        "courseName": "Complex Analysis",
                        "credits": 6,
                        "grade": 4.0
                    },
                    {
                        "courseId": 36,
                        "courseName": "Calculus I",
                        "credits": 9,
                        "grade": 5.0
                    }
                ]
            },
            {
                "id": 5,
                "name": "Per",
                "grades": [
                    {
                        "courseId": 23,
                        "courseName": "Complex Analysis",
                        "credits": 6,
                        "grade": 3.0
                    },
                    {
                        "courseId": 36,
                        "courseName": "Calculus I",
                        "credits": 9,
                        "grade": 4.0
                    }
                ]
            },
            {
                "id": 6,
                "name": "Ann",
                "grades": [
                    {
                        "courseId": 23,
                        "courseName": "Complex Analysis",
                        "credits": 6,
                        "grade": 4.5
                    },
                    {
                        "courseId": 36,
                        "courseName": "Calculus I",
                        "credits": 9,
                        "grade": 1.0
                    }
                ]
            },   
        ]

    