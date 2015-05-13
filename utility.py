__author__ = 'bzhang'

import requests
import random


class Utility:
    cookies = None
    token = ""
    login_id = None
    learn_base_url = 'http://localhost:8000/learn/api/v1/'

    def __init__(self):
        pass

    def login(self):
        url = 'http://localhost:8000/webapps/login/'
        params = {
            'user_id': 'administrator',
            'password': 'changeme'
        }
        response = requests.post(url, params)
        self.cookies = response.cookies

    def token(self):
        url = self.learn_base_url + 'utilities/xsrfToken'
        response = requests.get(url, cookies=self.cookies)
        self.token = response.json()['xsrfToken']
        return self.token

    def get_login_user_info(self):
        url = self.learn_base_url + '/users/me'
        response = requests.get(url, cookies=self.cookies)
        self.login_id = response.json()['id']
        return response.json()

    def create_course_conversation(self, course_id, json_body):
        url = self.learn_base_url + 'courses/' + course_id + '/conversations'
        headers = {'X-Blackboard-XSRF': self.token, 'Content-Type': 'application/json'}
        response = requests.post(url, json=json_body, headers=headers, cookies=self.cookies)
        return response.json()

    def add_participants_to_course_conversation(self, course_id, conversation_id, new_participant_ids):
        url = self.learn_base_url + 'courses/' + course_id + '/conversations/' + conversation_id
        headers = {'X-Blackboard-XSRF': self.token, 'Content-Type': 'application/json'}
        json_body = dict()
        json_body['newParticipantIds'] = new_participant_ids
        response = requests.patch(url, json=json_body, headers=headers, cookies=self.cookies)
        return response.json()

    def get_course_memberships(self, course_id):
        url = self.learn_base_url + 'courses/' + course_id + '/memberships'
        response = requests.get(url, cookies=self.cookies)
        return response.json()

    def send_message_in_conversation(self, course_id, conversation_id):
        url = self.learn_base_url + 'courses/' + course_id + '/conversations/' + conversation_id + '/messages'
        headers = {'X-Blackboard-XSRF': self.token, 'Content-Type': 'application/json'}
        json_body = {"body": {"rawText": "hello", "displayText": ""}}
        response = requests.post(url, cookies=self.cookies, headers=headers, json=json_body)
        return response.json()

    def create_one_course(self):
        url = self.learn_base_url + 'courses/'
        headers = {'X-Blackboard-XSRF': self.token, 'Content-Type': 'application/json'}
        json_body = {"name": 'test' + str(random.randint(1, 10000)), "courseId": 'test' + str(random.randint(1, 10000)),
                     "ultraStatus": "ULTRA"}
        response = requests.post(url, cookies=self.cookies, headers=headers, json=json_body)
        return response.json()

    def enroll(self, course_id, user_id, role):
        url = self.learn_base_url + 'courses/' + course_id + '/memberships'
        headers = {'X-Blackboard-XSRF': self.token, 'Content-Type': 'application/json'}
        json_body = {"isAvailable": True, "userId": user_id, "courseId": course_id, "role": role}
        response = requests.post(url, cookies=self.cookies, headers=headers, json=json_body)
        return response.json()


