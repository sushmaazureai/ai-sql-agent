import requests

while True:
    cmd = input("AI SQL > ")

    if cmd in ["exit", "quit"]:
        break

    res = requests.get("http://localhost:8000/ai", params={"q": cmd})
    print(res.json()["result"])