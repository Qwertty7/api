import json

import requests


class Authenticate(object):
    def __init__ (self):
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.session = requests.Session()
        # every time you create instance of authenticate init will be triggered
        # need to add self in passing-> def authenticate (self, base_url, email, password)->
        # to be able to have access to Session -> self.requests.Session(), now instead
        # request.get -> Session.get => instead create request every time, will have session
        # and executing all request on top this session
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})

    # created Chrome session

    def authenticate (self, email, password):
        resp = self.session.post(self.base_url + '/login', json={"email": email, "password": password})
        json_parsed = json.loads(resp.text)
        token = json_parsed.get('token', None)
        if token:
            self.session.headers.update({'Authorization': 'Bearer ' + token})
        return resp

    def post_new_candidate (self, first_name, last_name, email, password):
        json_data = {"firstName": first_name, "lastName": last_name, "email": email, "password": password}
        return self.session.post(self.base_url + '/candidates', json=json_data)

    def delete_candidate_by_id (self, new_candidate_id):
        return self.session.delete(self.base_url + '/candidates/' + str(new_candidate_id))

    def get_all_candidates (self):
        return requests.get(self.base_url + '/candidates')

    def get_all_positions (self):
        return requests.get(self.base_url + '/positions')

    def perform_user_verification (self):
        return self.session.post(self.base_url + '/verify')

    # убедиться, что у кандидата 2 позиции
    def get_candidate_positions(self, user_id):
        return self.session.get(self.base_url + '/candidates/' + str(user_id) + '/positions')

    # создаем кандидату 2 позиции
    def assign_positions_for_candidate(self, user_id, position_id):
        return self.session.post(self.base_url + '/candidates/' + str(user_id) + '/positions' + str(position_id))
    # ?
    def get_candidate_by_id(self, new_candidate_id):
        pass

    # во второй позиции изменить информацию (PUT)
    def update_positions_data(self, positions_id, company_name):
        json_data = {"company": company_name}
        return self.session.put(self.base_url + '/positions/' + str(positions_id), json=json_data)




