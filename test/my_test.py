"""
My Homework #2.
"""
from faker import Faker
import unittest

from lib.authentication import Authenticate


fake = Faker()


class CareerPortalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sess = Authenticate()

    def get_candidates(self):
        response = self.sess.get_all_candidates()  # `get_all_candidates` returns requests.Response object
        self.assertTrue(response.ok)
        return response.json()  # here we finally get list of candidates

    def test_login(self):
        candidates_count = len(self.get_candidates())  # Count how many candidates returned

        # Create new candidate
        new_candidate_data = {
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'email': fake.email(),
            'password': 'delete'
        }
        response = self.sess.post_new_candidate(new_candidate_data)
        self.assertTrue(response.ok)
        new_candidate = response.json()
        self.assertEqual(new_candidate['lastName'], new_candidate_data['lastName'])

        new_candidate_id = new_candidate['id']

        # login created candidate
        response = self.sess.authenticate(new_candidate_data['email'], new_candidate_data['password'])
        self.assertTrue(response.ok)

        # Retrieve the list of all candidates and check that one of the entries is the candidate you posted
        candidates = self.get_candidates()
        # Example of classic loop
        # candidate_ids = []
        # for candidate in candidates:
        #     candidate_ids.append(candidate['id'])
        # self.assertIn(new_candidate_id, candidate_ids)
        candidate_ids = [candidate['id'] for candidate in candidates]
        self.assertIn(new_candidate_id, candidate_ids)

        # GET the list of existing candidates AGAIN...
        candidates = self.get_candidates()
        # Ensure the count is now greater than before
        self.assertEqual(len(candidates), candidates_count + 1)

        # Login as student@example.com and
        # DELETE the candidate you created using the ID you stored
        self.sess.authenticate("student@example.com", "welcome")
        response = self.sess.delete_candidate_by_id(new_candidate_id)
        self.assertTrue(response.ok)  # keep in mind that we should get 204 status here
        # Optionally we can check exact status with
        # self.assertEqual(response.status_code, 204)

        # Ensure the candidate was deleted!
        # 1) request candidates list again and ensure users count equals candidates_count - 1
        # 2) request candidate by id, ensure that API replies with 404 status
        response = self.sess.get_candidate_by_id(new_candidate_id)
        self.assertEqual(response.status_code, 400)

        # Retrieve the list of all candidates and check that the deleted candidate is no longer included in the list
        candidates = self.get_candidates()
        candidate_ids = [candidate['id'] for candidate in candidates]
        self.assertNotIn(new_candidate_id, candidate_ids)

    def test_cannot_login(self):
        response = self.sess.authenticate('foo', 'barr')
        json_parsed = response.json()
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
