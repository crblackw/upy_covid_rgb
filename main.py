import machine
import neopixel
import utime as time
import urequests as requests
import ujson as json
import os
import secrets
import network

ssid = secrets.ssid
pwd = secrets.pwd

START_FRESH = False
RECORD_COUNT = 9


def main():
    """ Main entry point of the app """
    if START_FRESH:
        os.remove("data.txt")

    try:
        while True:
            np = neopixel.NeoPixel(machine.Pin(2), 7)
            np.fill((0, 0, 0))
            np.write()

            do_connect()

            latest = pull_daily_covid()
            print("latest: ", latest)

            data = load_data()
            print("loaded data: ", data)

            data = append_data(data, latest)
            print("updated data: ", data)

            write_data(data)

            update_pixels(data, np)

            time.sleep(3600)
    except KeyboardInterrupt:
        pass


def update_pixels(data, np):
    for index, row in enumerate(data):
        if index < np.n:
            if row["rate"] > 0:
                np[index] = (15, 0, 0)
            elif row["rate"] < 0:
                np[index] = (0, 15, 0)
            else:
                np[index] = (0, 0, 15)
            np.write()


def load_data():
    try:
        with open("data.txt", "ro") as f:
            data = json.load(f)
        print("data.txt loaded")
        f.close()
    except:
        print("no data.txt, creating template")
        data = []
        for i in range(0, RECORD_COUNT):
            data.append({"timestamp": 0, "infected": 0, "new": 0, "rate": 0})
        with open("data.txt", "w") as f:
            json.dump(data, f)
        print("wrote data.txt")
        f.close()
    return data


def write_data(data):
    try:
        with open("data.txt", "w") as f:
            json.dump(data, f)
        print("wrote data.txt")
        f.close()
    except:
        print("error writing data.txt")


def append_data(data, latest):
    if not any(d["timestamp"] == latest["timestamp"] for d in data):
        if timestamp_to_day(latest["timestamp"]) > timestamp_to_day(
            data[0]["timestamp"]
        ):
            data.insert(0, latest)
            for index, row in enumerate(data):
                if (index + 1) <= RECORD_COUNT:
                    last = data[index + 1]["infected"]
                    curr = row["infected"]
                    row["new"] = curr - last
                else:
                    pass
            for index, row in enumerate(data):
                if (index + 1) <= RECORD_COUNT:
                    last = data[index + 1]["new"]
                    curr = row["new"]
                    row["rate"] = curr - last
                else:
                    pass
        else:
            print("latest data less than a day old")

    else:
        print("timestamp already exists")

    if len(data) > RECORD_COUNT:
        data.pop()
    return data


def do_connect():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(ssid, pwd)
        while not wlan.isconnected():
            pass
    print("network config:", wlan.ifconfig())


def pull_daily_covid():
    # Download webpage
    print("requesting data...")
    response = requests.get(
        "https://api.apify.com/v2/key-value-stores/fabbocwKrtxSDf96h/records/LATEST?disableRedirect=true"
    )
    print("got data...")
    data = json.loads(response.content)
    return {"timestamp": data["lastUpdatedAtApify"], "infected": data["infected"]}


def timestamp_to_day(ts):
    return int(str(ts).split("T")[0].replace("-", ""))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
