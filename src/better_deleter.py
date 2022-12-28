import requests
import json
import asyncio


async def perform_request(method, endpoint, **args):
    if method == "GET":
        r = requests.get(
            f"https://discord.com/api/v9/{endpoint}", headers=headers, **args
        )
    elif method == "DELETE":
        r = requests.delete(
            f"https://discord.com/api/v9/{endpoint}", headers=headers, **args
        )

    try:
        response_json = r.json()
        response_json["status_code"] = r.status_code
    except json.decoder.JSONDecodeError:
        return

    if r.status_code == 429:  # ratelimit
        retry_after = response_json.get("retry_after")
        await asyncio.sleep(retry_after)
        return await perform_request(method, endpoint, **args)

    return response_json


async def clear_guild_messages(token, guild_id, user_id):
    global headers
    headers = {"Authorization": token}
    messages = []

    search = await perform_request(
        "GET", f"guilds/{guild_id}/messages/search", params={"author_id": user_id}
    )
    messages += search["messages"]

    total_results = search["total_results"]
    for offset in range(25, total_results, 25):
        search = await perform_request(
            "GET",
            f"guilds/{guild_id}/messages/search",
            params={"author_id": user_id, "offset": offset},
        )
        messages += search["messages"]

    for message in messages:
        await perform_request(
            "DELETE", f"channels/{message[0]['channel_id']}/messages/{message[0]['id']}"
        )


async def clear_channel_messages(token, channel_id, user_id):
    global headers
    headers = {"Authorization": token}
    messages = []

    search = await perform_request(
        "GET", f"channels/{channel_id}/messages/search", params={"author_id": user_id}
    )
    messages += search["messages"]

    total_results = search["total_results"]
    for offset in range(25, total_results, 25):
        search = await perform_request(
            "GET",
            f"channels/{channel_id}/messages/search",
            params={"author_id": user_id, "offset": offset},
        )
        messages += search["messages"]

    for message in messages:
        await perform_request(
            "DELETE", f"channels/{message[0]['channel_id']}/messages/{message[0]['id']}"
        )
