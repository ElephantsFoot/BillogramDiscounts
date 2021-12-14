import json

import pytest

import main


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    return main.app.test_client()


class TestClass:
    def test_discount_code(self, client):
        """Testing discount code creation and usage."""

        response = client.post('/discount_code', json={
            "user_id": 1,
            "company_id": 1,
        })
        assert response.status_code == 200
        assert response.json["discount_code"]
        discount_code = response.json["discount_code"]

        # the discount can't be used by another user
        response = client.post('/use_discount_code', json={
            "discount_code": discount_code,
            "user_id": 2,
            "company_id": 1,
        })
        assert response.status_code == 400
        assert response.json["description"] == "The discount belongs to another user"

        # the discount can't be used for another company
        response = client.post('/use_discount_code', json={
            "discount_code": discount_code,
            "user_id": 1,
            "company_id": 2,
        })
        assert response.status_code == 400
        assert response.json["description"] == "The discount is for another company"

        response = client.post('/use_discount_code', json={
            "discount_code": discount_code,
            "user_id": 1,
            "company_id": 1,
        })
        assert response.status_code == 200

        # the same discount can't be used again
        response = client.post('/use_discount_code', json={
            "discount_code": discount_code,
            "user_id": 1,
            "company_id": 1,
        })
        assert response.status_code == 400
        assert response.json["description"] == "The discount has already been used"

    def test_users_shared_data(self, client):
        """Testing discount code creation and usage."""

        response = client.post('/discount_code', json={
            "user_id": 1,
            "company_id": 1,
        })
        assert response.status_code == 200

        response = client.post('/discount_code', json={
            "user_id": 2,
            "company_id": 2,
        })
        assert response.status_code == 200

        response = client.get('/users_shared_data', json={
            "company_id": 2,
        })
        assert response.status_code == 200
        assert response.json["user_ids"] == [2]
