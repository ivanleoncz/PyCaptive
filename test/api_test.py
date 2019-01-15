def test_index(client):
    res = client.get('/')

    assert res == 200
