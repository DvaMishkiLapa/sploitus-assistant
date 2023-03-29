# sploitus-assistant

Micro-library for data output from [sploitus.com](https://sploitus.com/).

- [sploitus-assistant](#sploitus-assistant)
  - [1. Dependencies](#1-dependencies)
  - [2. Implementation details](#2-implementation-details)
  - [3. Why curl?](#3-why-curl)

## 1. Dependencies

- [curl](https://curl.se/);
- [Python 3.10 or newer](https://www.python.org/).

## 2. Implementation details

Micro-library allows you to retrieve some targets from [sploitus.com](https://sploitus.com/). The query is done via **curl** using [threading](https://docs.python.org/3/library/threading.html).

## 3. Why curl?

**Sploitus** changed something in his work in 2022-2023. Most likely started working with [CloudFlare](https://www.cloudflare.com/).
You can tell from other projects that apparently worked before:

- [si9int sploitus.py](https://github.com/si9int/sploitus.py);
- [sploitGET](https://github.com/0xricksanchez/sploitGET).

There were attempts to communicate via [requests](https://requests.readthedocs.io/en/latest/), but instead of a response I got a blank page.
It is likely that the **curl** approach may even stop working.

You could try using [libcurl](https://curl.se/libcurl/) via [PycURL](https://pypi.org/project/pycurl/#files), but I'm too old for that.
