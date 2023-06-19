import time
from gpt4free import you


def analysis(paragraph):
    try:
        time.sleep(10)

        prompt = """
        Using an embedding/LDA type approach, analyze the following paragraph to identify the key ideological positions, political affiliations, or policy preferences conveyed. Consider both explicit and implicit statements and try to capture the overall tone and perspective of the author. Pay attention to any specific issues or values mentioned and how they align with common political ideologies. Provide an objective analysis by utilizing techniques such as word embeddings or topic modeling to uncover underlying themes and associations within the text:
        """

        response = you.Completion.create(
            prompt=prompt + paragraph,
            detailed=True,
            include_links=False
        )

        print(response.dict())

    except Exception as e:
        print(f"An error occurred: {e}")
