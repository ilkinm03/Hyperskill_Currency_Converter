import json
import requests


def fetch_rates(currency_code):
    return requests.get(f"https://www.floatrates.com/daily/{currency_code}.json")


def ask_for_currency():
    try:
        return input().lower()
    except ValueError:
        print("Currency code must be a string")
        return ask_for_currency()


def ask_for_amount():
    try:
        return float(input())
    except ValueError:
        print("Amount must be a number")
        return ask_for_amount()


def converter():
    data = dict()
    while True:
        your_curr = ask_for_currency()
        if your_curr == "":
            break
        data = fetch_rates(your_curr)
        if data:
            break
        print("Currency code is invalid")
    data_json = json.loads(data.text)
    cache = dict()
    if your_curr == "usd":
        cache["eur"] = data_json["eur"]
    elif your_curr == "eur":
        cache["usd"] = data_json["usd"]
    else:
        cache = {"usd": data_json["usd"], "eur": data_json["eur"]}
    while cache != data_json:
        curr_to_convert = ask_for_currency()
        if curr_to_convert == "":
            break
        amount = ask_for_amount()
        print("Checking the cache...")
        if cache and curr_to_convert in cache:
            print("Oh! It is in the cache!")
            exchange = round(amount * cache[curr_to_convert]["rate"], 2)
        else:
            print("Sorry, but it is not in the cache!")
            cache[curr_to_convert] = data_json[curr_to_convert]
            exchange = round(amount * data_json[curr_to_convert]["rate"], 2)
        print(f"You received {exchange} {curr_to_convert.upper()}")


converter()
