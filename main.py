import machine
import neopixel
import utime as time
import urandom as random
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
            n = np.n

            do_connect()

            latest = pull_daily_covid()
            print("latest: ", latest)

            data = load_data()
            print("loaded data: ", data)

            data = append_data(data, latest)
            print("updated data: ", data)

            write_data(data)

            update_pixels(data, np)

            time.sleep(60)
    except KeyboardInterrupt:
        pass


def update_pixels(data, np):
    for index, row in enumerate(data):
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
    if not any(latest["timestamp"] for latest in data):
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


def randint(min, max):
    span = max - min + 1
    div = 0x3FFFFFFF // span
    offset = random.getrandbits(30) // div
    val = min + offset
    return val


def random_sparkle():
    for i in range(n):
        red = randint(0, 30)
        green = randint(0, 30)
        blue = randint(0, 30)
        print(i, red, green, blue)
        np[i] = (red, green, blue)
        np.write()
        time.sleep(0.1)


def chase(red=0, green=0, blue=0):
    if (red == 0) and (green == 0) and (blue == 0):
        red = randint(0, 30)
        green = randint(0, 30)
        blue = randint(0, 30)
    for i in range(1, n):
        print("i: %i, r: %i, g: %i, b: %i" % (i, red, green, blue))
        np[i] = (red, green, blue)
        np.write()
        time.sleep(0.1)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
