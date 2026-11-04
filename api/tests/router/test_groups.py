from tests.consts import TEST_BIRD_1


def test_group(client):
    response = client.get("/groups", params={"language": "en"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [TEST_BIRD_1["translations"][0]["group"]],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


def test_subgroup(client):
    translation = TEST_BIRD_1["translations"][1]
    response = client.get(f"/groups/{translation['group']}")
    assert response.status_code == 200
    assert response.json() == {
        "items": [translation["subgroup"]],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


def test_subgroup_ignores_missing_subgroup(client, bird_without_images):
    group = bird_without_images["translations"][0]["group"]
    response = client.get(f"/groups/{group}")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0, "page": 1, "per_page": 25}
