from tests.consts import TEST_BIRD_1


def test_species(client):
    response = client.get("/species", params={"language": "en"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [TEST_BIRD_1["translations"][0]["species"]],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


def test_sub_species(client):
    translation = TEST_BIRD_1["translations"][1]
    response = client.get(f"/species/{translation['species']}")
    assert response.status_code == 200
    assert response.json() == {
        "items": [translation["sub_species"]],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


def test_sub_species_ignores_missing_sub_species(client, bird_without_images):
    species = bird_without_images["translations"][0]["species"]
    response = client.get(f"/species/{species}")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0, "page": 1, "per_page": 25}
