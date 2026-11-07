SQLALCHEMY_DATABASE_URL = "sqlite://"

TEST_BIRD_1 = {
    "id": 1,
    "latin_name": "test_latin_name1",
    "translations": [
        {
            "id": 1,
            "name": "test_name1",
            "group": "test_group1",
            "subgroup": "test_subgroup1",
            "details": "test_details1",
            "language_code": "en",
        },
        {
            "id": 2,
            "name": "test_name2",
            "group": "test_group2",
            "subgroup": "test_subgroup2",
            "details": "test_details2",
            "language_code": "fr",
        },
    ],
    "images": [
        {
            "id": 1,
            "image_name": "1.png",
            "original_url": "url1",
            "author": {
                "id": 1,
                "name": "author1",
                "link": "link1",
            },
            "license": {
                "id": 1,
                "short_name": "short_name1",
                "full_name": "full_name1",
                "link": "link1",
            },
        },
        {
            "id": 2,
            "image_name": "2.jpg",
            "original_url": "url2",
            "author": {
                "id": 2,
                "name": "author2",
                "link": "link2",
            },
            "license": {
                "id": 2,
                "short_name": "short_name2",
                "full_name": "full_name2",
                "link": "link2",
            },
        },
    ],
}

BIRD1_EN = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][0]["name"],
    "group": TEST_BIRD_1["translations"][0]["group"],
    "subgroup": TEST_BIRD_1["translations"][0]["subgroup"],
    "details": TEST_BIRD_1["translations"][0]["details"],
    "language_code": "en",
    "image_count": len(TEST_BIRD_1["images"]),
}

BIRD1_FR = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][1]["name"],
    "group": TEST_BIRD_1["translations"][1]["group"],
    "subgroup": TEST_BIRD_1["translations"][1]["subgroup"],
    "details": TEST_BIRD_1["translations"][1]["details"],
    "language_code": "fr",
    "image_count": len(TEST_BIRD_1["images"]),
}

BIRD1_EN_IMAGES = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][0]["name"],
    "group": TEST_BIRD_1["translations"][0]["group"],
    "subgroup": TEST_BIRD_1["translations"][0]["subgroup"],
    "details": TEST_BIRD_1["translations"][0]["details"],
    "language_code": "en",
    "image_ids": [img["id"] for img in TEST_BIRD_1["images"]],
    "image_count": len(TEST_BIRD_1["images"]),
}

BIRD1_FR_IMAGES = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][1]["name"],
    "group": TEST_BIRD_1["translations"][1]["group"],
    "subgroup": TEST_BIRD_1["translations"][1]["subgroup"],
    "details": TEST_BIRD_1["translations"][1]["details"],
    "language_code": "fr",
    "image_ids": [img["id"] for img in TEST_BIRD_1["images"]],
    "image_count": len(TEST_BIRD_1["images"]),
}

# bird without any image nor sub-group
TEST_BIRD_2 = {
    "id": 2,
    "latin_name": "test_latin_name2",
    "translations": [
        {
            "id": 3,
            "name": "test_name3",
            "group": "test_group3",
            "subgroup": None,
            "details": None,
            "language_code": "fr",
        },
    ],
}
