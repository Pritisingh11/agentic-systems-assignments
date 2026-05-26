from build_chain import build_chain


def is_response_valid(response: str) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not isinstance(response, str):
        errors.append("Response is not a string")
        return False, errors

    trimmed = response.strip()
    if not trimmed:
        errors.append("Response is empty after trimming whitespace")

    word_count = len(trimmed.split())
    if word_count > 100:
        errors.append(f"Response too long: {word_count} words (max 100)")

    return (len(errors) == 0), errors



chain = build_chain()

test_cases = [
        {"topic": "LangChain Expression Language", "analogy_domain": "school assembly line"},
        {"topic": "Prompt Templates", "analogy_domain": "wedding invitation cards"},
        {"topic": "Output Parsers", "analogy_domain": "food delivery packaging"},
]

for test_case in test_cases:  # Loop through every test case one by one.
    response = chain.invoke(test_case)  # Run the chain for the current test case.
    is_valid, errors = is_response_valid(response)  # Validate the generated response.
    print("Input:", test_case)  # Print the input that was tested.
    print("Response:", response)  # Print the generated response.
    print("Valid:", is_valid)  # Print whether the response passed validation.
    print("Errors:", errors)  # Print validation errors if any exist.
    print("-" * 40)  # Print a separator line between test cases.

   