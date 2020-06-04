import unittest
from faker import Faker
from lib.recruit_career.authentication import Authenticate


fake = Faker()

class PositionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sess = Authenticate()
    # test, f-n for test
    def test_create_positions(self):
        # 1.Create new candidate
        new_candidate_data = {
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'email': fake.email(),
            'password': 'delete'
        }
        # f-n that send api request
        response = self.sess.post_new_candidate(new_candidate_data)
        self.assertTrue(response.ok)
        new_candidate = response.json()
        self.assertEqual(new_candidate['lastName'], new_candidate_data['lastName'])
        new_candidate_id = new_candidate['id']
        # login
        self.sess.authenticate("student@example.com", "welcome")

        # 2.assign existing first position for candidate
        response = self.sess.assign_positions_for_candidate(new_candidate_id, 4)
        print(response.content)
        self.assertTrue(response.ok)
        # new_candidate_position_id = response.json()
        # position_id = new_candidate_position_id['id']
        # self.assertEqual(str(position_id['positionId']), '4')

        # 2.assign another existing position for candidate
        response = self.sess.assign_positions_for_candidate(new_candidate_id, 23)
        print(response.content)
        self.assertTrue(response.ok)
        # new_candidate_position_id = response.json()
        # position_id = new_candidate_position_id['id']
        # self.assertEqual(str(position_id['positionId']), '4')


        # # assert that candidate has 2 new positions
        response = self.sess.get_candidate_positions(new_candidate_id)
        self.assertTrue(response.ok)
        candidate_positions = response.json()
        print(candidate_positions)
        # self.assertEqual()

#
#     #     во второй позиции изменить информацию (PUT)  и убедться что инф изменена
        positions_data = {
            "company": "ABC"
        }

        response = self.sess.update_positions_data('9', positions_data)
        self.assertTrue(response.ok)
        updated_data = response.json()
        print(updated_data)
#         self.assertEqual(positions_data['company'], updated_data['ABC'])
#

        response = self.sess.create_new_position('scrum master')
        self.assertTrue(response.ok)
        new_position = response.json()
        print(new_position)

        response = self.sess.create_new_position('engineer')
        self.assertTrue(response.ok)
        new_position = response.json()
        print(new_position)


        # delete position
        # response = self.sess.delete_position(new_position)
        # self.assertTrue(response.ok)


        # get all positions  and    verify that position was deleted
        response = self.sess.get_all_positions()
        self.assertTrue(response.ok)
        return response.json()
        #  verify that position was deleted


if __name__ == '__main__':
    unittest.main()
