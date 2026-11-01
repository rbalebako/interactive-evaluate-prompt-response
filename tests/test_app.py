import main


def test_home_page_renders_form():
    response = main.app.test_client().get("/")

    assert response.status_code == 200
    assert b'name="bad_response"' in response.data
    assert b'name="good_response"' in response.data


def test_post_evaluates_form_responses_and_renders_results(monkeypatch):
    submitted = {}

    def fake_run_all_evaluations(bad_response, good_response):
        submitted["responses"] = (bad_response, good_response)
        return [{"name": "correctness", "library": "test", "score": "0.90"}]

    monkeypatch.setattr(
        main.singlepromptmetrics,
        "run_all_evaluations",
        fake_run_all_evaluations,
    )

    response = main.app.test_client().post(
        "/",
        data={
            "bad_response": "<unsafe response>",
            "good_response": "reference response",
        },
    )

    assert response.status_code == 200
    assert submitted["responses"] == ("<unsafe response>", "reference response")
    assert b"&lt;unsafe response&gt;" in response.data
    assert b"correctness" in response.data
    assert b"0.90" in response.data
