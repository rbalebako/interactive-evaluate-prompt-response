# Interactive Evaluate Prompt Response

A small Flask app for comparing a chatbot response with a stronger reference answer. It runs a set of evaluation metrics and displays their scores, helping
you inspect whether automated judges agree with your expectations.

This was used for a Innosuisse funded workshop on the quality of AI metrics.

I think if I was starting over with this in 2026 or later, it could be vibe coded pretty easily, but at the time we were trying to measure the measurements in a group format.

## What it evaluates

- **Lakera Guard** checks the submitted response with its configured detectors.
- **DeepEval correctness** judges the response against the reference answer.
- **DeepEval answer relevancy** measures how relevant the response is to the
  reference answer.

The app also includes a small example set that can be run from the command line.

## Requirements

- Python 3.10 or newer
- An OpenAI API key for DeepEval
- A Lakera Guard API key for the Lakera checks

## Run locally

1. Clone the repository and enter its directory.
2. Create and activate a virtual environment:

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with `.venv\Scripts\activate`.

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set the API keys in your shell:

   ```sh
   export OPENAI_API_KEY="your-openai-api-key"
   export LAKERA_GUARD_API_KEY="your-lakera-api-key"
   ```

   Do not commit API keys or put real credentials in source files.

5. Start the web app:

   ```sh
   python main.py
   ```

   Open [http://localhost:8080](http://localhost:8080). Enter the response to
   evaluate and the reference answer, then submit the form. Evaluations call
   external services and may take some time.

For a production-like local run, start it with Gunicorn instead:

```sh
gunicorn --bind "0.0.0.0:${PORT:-8080}" main:app
```

To run the example evaluation set instead:

```sh
python golden_test.py
```

## Tests

Install the test dependencies and run the suite:

```sh
pip install -r requirements-dev.txt
python -m pytest
```

The suite stubs DeepEval and mocks the Lakera HTTP request, so tests run without
API keys or external network access.

## Privacy

Submitted response text is sent to Lakera Guard, and DeepEval may send inputs
and outputs to its configured model provider. Do not submit confidential,
personal, or otherwise sensitive content unless you have approval to share it
with those services.

## Development status

This is an experimental project, not a production-ready evaluation service.
The pytest suite covers the Flask form flow and evaluation helpers; external
services are mocked. There is no platform-specific deployment guide.
Contributions that expand test coverage, improve error handling, and document
supported evaluation behavior are welcome.

## License

No project license is currently included. The website template and bundled
third-party assets have their own licensing and attribution requirements; see
the notices in the relevant files before redistributing them.
