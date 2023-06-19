import asyncio
import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from analysis import analysis

async def test(politician):
    cookies = json.loads(open("bing_cookies_lol.json", encoding="utf-8").read())
    bot = await Chatbot.create(cookies=cookies)

    prompt = ("Your task is to provide detailed information about a politician named ["+ politician + "] . Please conduct three searches using the following queries: 'Twitter,' 'Campaign Website,' and 'Public Statements.' Make sure to retrieve as much information as possible from the search results and include it in your report. Please provide specific details and avoid just linking to the websites. Remember to exclude any quotes while conducting the searches. Your aim is to create a comprehensive and detailed report on the politician based on the information found."


    )

    try:
        response = await asyncio.wait_for(
            bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=False),
            timeout=60
        )

        adaptive_text = response["adaptive_text"]
        response_json = json.dumps({"adaptive_text": adaptive_text}, indent=2)
        analysis(response_json)
    except asyncio.TimeoutError:
        print("Request timed out. Your IP might be blocked or the process took longer than expected.")

    await bot.close()
