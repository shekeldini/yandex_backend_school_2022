import urllib.error
import urllib.parse
import urllib.request
from utils import request


class TestUserNotFound:
    def __init__(self):
        self.user_id = "23124151"

    def buy_common(self):
        params = urllib.parse.urlencode({
            "user_id": self.user_id,
            "item_id": "common_1"
        })
        status, response = request(f"/check?{params}", json_response=True)
        assert response[0]["problem"] == "NO_USER"

    def test_wrong_category(self):
        params = urllib.parse.urlencode({
            "user_id": self.user_id,
            "item_id": "test_123"
        })
        status, response = request(f"/check?{params}", json_response=True)
        assert response[0]["problem"] == "WRONG_CATEGORY"

    def test_incorrect_item_id(self):
        params = urllib.parse.urlencode({
            "user_id": self.user_id,
            "item_id": "common_test"
        })
        status, response = request(f"/check?{params}", json_response=True)
        assert response[0]["problem"] == "INCORRECT_ITEM_ID"

    def test_item_not_found(self):
        params = urllib.parse.urlencode({
            "user_id": self.user_id,
            "item_id": "common_100000"
        })
        status, response = request(f"/check?{params}", json_response=True)
        assert response[0]["problem"] == "ITEM_NOT_FOUND"

    def test_receipt(self):
        params = urllib.parse.urlencode({
            "user_id": self.user_id,
            "item_id": "receipt_1"
        })
        status, response = request(f"/check?{params}", json_response=True)
        assert response[0]["problem"] == "NO_USER_NO_RECEIPT"

    def test_special(self):
        params = urllib.parse.urlencode({
            "user_id": self.user_id,
            "item_id": "special_16"
        })
        status, response = request(f"/check?{params}", json_response=True)
        assert response[0]["problem"] == "NO_USER_SPECIAL_ITEM"

    def test_all(self):
        self.buy_common()
        self.test_wrong_category()
        self.test_incorrect_item_id()
        self.test_item_not_found()
        self.test_receipt()
        self.test_special()

