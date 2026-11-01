import pytest
import requests

import singlepromptmetrics as metrics


def test_trim_score_formats_only_float_values():
    assert metrics.trim_score(0.876) == "0.88"
    assert metrics.trim_score(1) == 1
    assert metrics.trim_score("0.8") == "0.8"


def test_setup_lakera_guard_requires_api_key(monkeypatch):
    monkeypatch.delenv("LAKERA_GUARD_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="LAKERA_GUARD_API_KEY"):
        metrics.setup_lakera_guard()


def test_setup_lakera_guard_sets_bearer_authorization(monkeypatch):
    monkeypatch.setenv("LAKERA_GUARD_API_KEY", "test-token")

    client = metrics.setup_lakera_guard()

    assert client.headers["Authorization"] == "Bearer test-token"


def test_lakera_evaluation_posts_response_and_filters_moderated_content(
    monkeypatch,
):
    monkeypatch.setenv("LAKERA_GUARD_API_KEY", "test-token")
    posted = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "results": [
                    {"detector_type": "prompt_injection", "result": True},
                    {"detector_type": "moderated_content", "result": False},
                ]
            }

    class FakeSession:
        def __init__(self):
            self.headers = {}

        def post(self, url, json, timeout):
            posted.update(url=url, payload=json, timeout=timeout)
            return FakeResponse()

    monkeypatch.setattr(metrics.requests, "Session", FakeSession)

    results = metrics.evaluate_gpt_response_with_lakera_guard(
        "response to check",
        "reference response",
    )

    assert posted == {
        "url": "https://api.lakera.ai/v2/guard/results",
        "payload": {
            "messages": [
                {"role": "assistant", "content": "response to check"},
            ]
        },
        "timeout": 30,
    }
    assert results == [
        {
            "name": "prompt_injection",
            "library": "Lakera Guard",
            "score": True,
        }
    ]


def test_lakera_evaluation_propagates_http_errors(monkeypatch):
    monkeypatch.setenv("LAKERA_GUARD_API_KEY", "test-token")

    class FakeResponse:
        def raise_for_status(self):
            raise requests.HTTPError("service unavailable")

    class FakeSession:
        headers = {}

        def post(self, *args, **kwargs):
            return FakeResponse()

    monkeypatch.setattr(metrics.requests, "Session", FakeSession)

    with pytest.raises(requests.HTTPError, match="service unavailable"):
        metrics.evaluate_gpt_response_with_lakera_guard("response", "reference")


def test_deepeval_helpers_return_scores_and_use_expected_text():
    correctness = metrics.deepeval_test_correctness("actual", "expected")
    relevancy = metrics.deepeval_test_relevancy("actual", "reference")

    assert correctness == {
        "name": "correctness",
        "library": "DeepEval:Confident.AI",
        "score": "0.88",
    }
    assert relevancy == {
        "name": "relevancy",
        "library": "DeepEval:Confident.AI",
        "score": "0.88",
    }


def test_run_all_evaluations_combines_all_metric_groups(monkeypatch):
    calls = []

    def fake_lakera(bad_response, good_response):
        calls.append(("lakera", bad_response, good_response))
        return [{"name": "prompt_injection"}]

    def fake_correctness(bad_response, good_response):
        calls.append(("correctness", bad_response, good_response))
        return {"name": "correctness"}

    def fake_relevancy(bad_response, good_response):
        calls.append(("relevancy", bad_response, good_response))
        return {"name": "relevancy"}

    monkeypatch.setattr(metrics, "evaluate_gpt_response_with_lakera_guard", fake_lakera)
    monkeypatch.setattr(metrics, "deepeval_test_correctness", fake_correctness)
    monkeypatch.setattr(metrics, "deepeval_test_relevancy", fake_relevancy)

    results = metrics.run_all_evaluations("bad", "good")

    assert results == [
        {"name": "prompt_injection"},
        {"name": "correctness"},
        {"name": "relevancy"},
    ]
    assert calls == [
        ("lakera", "bad", "good"),
        ("correctness", "bad", "good"),
        ("relevancy", "bad", "good"),
    ]
