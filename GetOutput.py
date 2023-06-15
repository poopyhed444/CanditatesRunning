import asyncio
import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

async def test(politician):
    cookies = json.loads(open("bing_cookies_lol.json", encoding="utf-8").read())
    bot = await Chatbot.create(cookies=cookies)
    prompt = "Your task is to tell me information about the following politician: [" + politician + "] as possible. Your search should include the query: \"Twitter\". Then you should make a second search that includes the query: \"Campaign Website\". Finally, a third search that includes the query: \"Public Statements\". Make sure you ignore all quotes! Then retrieve as much information as possible from those links to create the most detailed report possible. (Please do not be vague and be as specific as possible by including the information in your report rather than only linking information to those websites)"

    try:
        response = await asyncio.wait_for(
            bot.ask(prompt=prompt, conversation_style=ConversationStyle.balanced, simplify_response=True),
            timeout=60
        )

        adaptive_text = response["adaptive_text"]
        response_json = json.dumps({"adaptive_text": adaptive_text}, indent=2)
        print(response_json)
    except asyncio.TimeoutError:
        print("Request timed out. Your IP might be blocked or the process took longer than expected.")

    await bot.close()
