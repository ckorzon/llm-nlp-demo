class Natlang:
    _prompt_template_file = "prompt_template.txt"

    _categories_bank = ["food", "service", "atmosphere"]

    _positive_prefix = "We are thrilled that you enjoyed your visit to our Restaurant!"

    _negative_prefix = "On behalf of the White Fox Lounge, we are so sorry to hear that your visit to our establishment."

    _positive_response_suffixes = {
        "food": "Our chefs greatly appreciate your compliments, ",
        "service": "Our staff is happy to have provided a pleasant dining experience, ",
        "atmosphere": "Our management is delighted to know you've enjoyed our restaurant's setting, ",
        "other": "On behalf of our whole staff it was a pleasure to host you, "
    }

    _negative_response_suffixes = {
        "food": "Our kitchen staff apologizes for your unsatisfactory meal, ",
        "service": "Our waitstaff apologizes for your unsatisfactory experience, ",
        "atmosphere": "Our management apologizes for your dissatisfaction with our restaurant's atmosphere, ",
        "other": "Our staff apologizes for your unsatisfactory dining experience, "
    }

    _positive_conclusion = "and we would love to see you again soon."

    _negative_conclusion = "and we would appreciate if you could take a moment to complete the following survey so we can understand how we could do better next time: https://not-a-real-survey.com/a3csa93b4 ."

    def __init__(self):
        with open(Natlang._prompt_template_file) as file:
            self._prompt_template = " ".join(line.strip() for line in file)
    
    def _get_prompt(self, user_review: str):
        """For a given user_review, returns the prompt to be entered into an LLM for sentiment analysis and categorization.
        Precondition: user_review is a non-empty string
        Postcondition: Returned prompt is a non-empty string"""
        return f"{self._prompt_template}\n\n{user_review}"

    def _analyze_llm_response(self, response: str) -> dict:
        """For a given LLM response, capture the identified sentiment and category then return a dictionary with entries: positive (bool), and category (string).
        Precondition: Input response is a non-empty string which includes sentiment Happy or Sad, and a valid Category from the keywords bank
        Postcondition: Resulting dict contains entries 'positive': True/False, and 'category': string, such that category is a member of the _categories_bank."""
        # Note: This is a somewhat naive algorithm for extracting meaning from the LLM's response; it relies on excess wording of the category keywords not being included.
        result = {"positive": True, "category": None}
        response = response.lower()
        if ("unhappy" in response):
            result["positive"] = False
        for keyword in Natlang._categories_bank:
            if keyword in response:
                result["category"] = keyword
        return result

    def _craft_response(self, review_profile: dict) -> str:
        """Based on a sentiment analysis and categorization of a customer review, craft a directed response.
        Precondition: review_profile is a non-null dictionary with keys 'positive' and 'category'.
        Postcondition: Return value is a non-empty string with Natlang's response to the customer's review."""
        cat = review_profile.get("category", None)
        if cat is None:
            cat = "other"
        if review_profile["positive"]:
            return f"{Natlang._positive_prefix} {Natlang._positive_response_suffixes[cat]}{Natlang._positive_conclusion}"
        return f"{Natlang._negative_prefix} {Natlang._negative_response_suffixes[cat]}{Natlang._negative_conclusion}"

    def run(self):
        """Runs the Natlang program on a loop until user input requests a halt via entering a blank line.
        Precondition: _prompt_template_file exists in the current working directory
        Postcondition: None"""
        
        print("-- Enter customer reviews which need response, or enter a blank line to escape. --")
        while True:
            # Get the review as input
            review = input("Customer Review: ")
            if len(review) < 1:
                break
            # Prepare the prompt to send to Chat GPT
            prompt = self._get_prompt(review)
            # Send the prompt to Chat GPT
            print("")
            print("<Begin placeholder for LLM API Call>")
            print("#SYSTEM#: Enter the following prompt into Chat GPT:")
            print(prompt)
            print("")
            # Collect Chat GPT's response
            response = input("LLM Response: ")
            print("<End placeholder for LLM API Call>")
            print("")
            # Digest Chat GPT's response to our prompt
            review_profile = self._analyze_llm_response(response)
            # Craft & Print a response based on Chat GPT's analysis
            output = self._craft_response(review_profile)
            print(f"Natlang: {output}")
            print("")


if __name__ == "__main__":
    natlang = Natlang()
    natlang.run()