from src.quiz import QuizBird, _distractors

from tests.consts import TEST_BIRD_1

def _question(client, **params):
    response = client.get("/quiz/question", params={"language": "en", **params})
    assert response.status_code == 200, response.text
    return response.json()


def test_question(client, quiz_birds):
    question = _question(client)
    choices = question["choices"]
    assert len(choices) == 4
    ids = [choice["bird_id"] for choice in choices]
    assert len(set(ids)) == 4
    assert question["answer_id"] in ids
    assert 107 not in ids
    for choice in choices:
        # a photo of the bird, with its credits
        assert choice["image"]["id"] // 10 == choice["bird_id"] or choice["bird_id"] == TEST_BIRD_1["id"]
        assert choice["image"]["author"]["name"]
        assert choice["image"]["license"]["short_name"]
        assert choice["name"] and choice["latin_name"] and choice["group"]


def test_question_hard(client, quiz_birds):
    for _ in range(20):
        question = _question(client, difficulty="hard", exclude=[1, 104, 105, 106])
        choices = {choice["bird_id"]: choice for choice in question["choices"]}
        # one of the eagles is asked: the other ones are the closest choices
        assert question["answer_id"] in (101, 102, 103)
        assert {101, 102, 103} <= set(choices)
        # then a bird of the same group
        assert 104 in choices


def test_question_exclude(client, quiz_birds):
    for _ in range(10):
        question = _question(client, exclude=[1, 101, 102, 103, 104, 105])
        assert question["answer_id"] == 106
    # every bird has been asked: they can be asked again
    question = _question(client, exclude=[1, 101, 102, 103, 104, 105, 106])
    assert question["answer_id"] in (1, 101, 102, 103, 104, 105, 106)


def test_question_not_enough_birds(client):
    # only the test bird 1 has photos
    response = client.get("/quiz/question", params={"language": "en"})
    assert response.status_code == 404
    response = client.get("/quiz/question", params={"language": "de"})
    assert response.status_code == 404


def test_question_invalid_difficulty(client):
    response = client.get("/quiz/question", params={"difficulty": "expert"})
    assert response.status_code == 422


def _bird(bird_id, name, group, subgroup=None):
    return QuizBird(bird_id, name, f"latin {name}", group, subgroup)


def test_distractors_hard_falls_back_to_other_groups():
    answer = _bird(1, "golden eagle", "raptors", "eagles")
    birds = [answer, _bird(2, "bonelli's eagle", "raptors", "eagles"),
             _bird(3, "mallard", "ducks"), _bird(4, "robin", "passerines"), _bird(5, "teal", "ducks")]
    distractors = _distractors(answer, birds, "hard")
    assert distractors[0].id == 2
    assert {bird.id for bird in distractors[1:]} <= {3, 4, 5}
    assert len(distractors) == 3


def test_distractors_without_duplicate_names():
    answer = _bird(1, "robin", "passerines")
    birds = [answer, _bird(2, "Robin", "passerines"), _bird(3, "wren", "passerines")]
    assert [bird.id for bird in _distractors(answer, birds, "easy")] == [3]
