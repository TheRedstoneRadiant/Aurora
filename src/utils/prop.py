"""
! PROPRIETARY CODE WARNING !

This file contains entirely proprietary code.

Unauthorized access, deobfuscation, reverse engineering, or any attempt to reuse, reproduce, or distribute the code in any form is strictly prohibited.
"""

import json, base64
from tls_client import Session
from uuid import uuid4

x = chr(21635614 // 214214)
OBFS = "HR0cHM6Ly95b3UuY29tL2FwaS9zdHJlYW1pbmdTZWFyY2g"
TOK = base64.b64decode(x + "W91Q2hhdFRva2Vu").decode()
HED = base64.b64decode(
    x
    + f"yJhdXRob3JpdHkiOiJ5b3UuY29tIiwiYWNjZXB0IjoidGV4dC9ldmVudC1zdHJlYW0iLCJhY2NlcHQtbGFuZ3VhZ2UiOiJlbixmci1GUjtxPTAuOSxmcjtxPTAuOCxlcy1FUztxPTAuNyxlcztxPTAuNixlbi1VUztxPTAuNSxhbTtxPTAuNCxkZTtxPTAuMyIsImNhY2hlLWNvbnRyb2wiOiJuby1jYWNoZSIsInJlZmVyZXIiOiJodHRwczovL3lvdS5jb20vc2VhcmNoP3E9d2hvK2FyZSt5b3UmdGJtPXlvdWNoYXQiLCJzZWMtY2gtdWEiOiJcIk5vdF9BIEJyYW5kXCI7dj1cIjk5XCIsXCJHb29nbGUgQ2hyb21lXCI7dj1cIjEwOVwiLFwiQ2hyb21pdW1cIjt2PVwiMTA5XCIiLCJzZWMtY2gtdWEtbW9iaWxlIjoiPzAiLCJzZWMtY2gtdWEtcGxhdGZvcm0iOiJcIldpbmRvd3NcIiIsInNlYy1mZXRjaC1kZXN0IjoiZW1wdHkiLCJzZWMtZmV0Y2gtbW9kZSI6ImNvcnMiLCJzZWMtZmV0Y2gtc2l0ZSI6InNhbWUtb3JpZ2luIiwiY29va2llIjoic2FmZXNlYXJjaF9ndWVzdD1PZmY7IHV1aWRfZ3Vlc3Q9VVVJRCIsInVzZXItYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsg{x}DY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLGxpa2UgR2Vja28pIENocm9tZS8xMDguMC4wLjAgU2FmYXJpLzUzNy4zNiJ9"
).decode()


class Client:
    def q(self, query, **kwargs):
        self.reply = ""

        response = self.get_response(query, **kwargs)
        self.parse_response(response)

        return {"response": self.reply}

    def get_response(
        self,
        q: str,
    ) -> dict:
        client = Session(client_identifier="chrome_108")
        client.headers = json.loads(HED.replace("UUID", str(uuid4())))

        response = client.get(
            base64.b64decode(chr(97) + OBFS + "=").decode(),
            params={
                "q": q,
                "page": 1,
                "count": 10,
                "safeSearch": "Off",
                "onShoppingPage": False,
                "mkt": "",
                "responseFilter": "Computation",
                "domain": base64.b64decode(chr(101) + "W91Y2hhdA=="),
                "queryTraceId": str(uuid4()),
                "chat": "[]",
            },
        )

        return response

    def parse_response(self, response):
        split = response.text.splitlines()
        for index, line in enumerate(split):
            if line.startswith("event:"):
                event = line[7:]
                if event == "done":
                    return

                data = json.loads(split[index + 1].strip("data: "))
                self.parse_event(event, data)

    def parse_event(self, event, data):
        if event == TOK:
            self.reply += data[TOK]
