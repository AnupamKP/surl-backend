from flask import url_for, json


class TestURLView:
    def test_create_url(self, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        payload = {
            "url": "https://www.google.com"
        }
        actual_response = client.post(url_for('url.create_url'), data=json.dumps(payload), headers=headers)
        actual_response_status_code = actual_response.status_code
        expected_response_status_code = 201

        assert actual_response_status_code == expected_response_status_code

    def test_get_url_all(self, client):
        actual_response = client.get(url_for('url.get_url_all'))
        actual_response_status_code = actual_response.status_code
        expected_response_status_code = 200

        assert actual_response_status_code == expected_response_status_code

    def test_get_url_from_id(self, client):
        actual_response = client.get(url_for('url.get_url_from_id', url_id='testid'), follow_redirects=True)
        actual_response_status_code = actual_response.status_code
        expected_response_status_code = 403

        assert actual_response_status_code == expected_response_status_code

    def test_delete_url_from_id(self, client):
        actual_response = client.delete(url_for('url.delete_url_from_id', url_id='testid'))
        actual_response_status_code = actual_response.status_code
        expected_response_status_code = 202

        assert actual_response_status_code == expected_response_status_code
