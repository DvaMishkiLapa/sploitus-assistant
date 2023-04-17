# sploitus-assistant

Micro-library for data output from [sploitus.com](https://sploitus.com/).

- [sploitus-assistant](#sploitus-assistant)
  - [1. Dependencies](#1-dependencies)
  - [2. Implementation details](#2-implementation-details)
  - [3. Quick guide](#3-quick-guide)
  - [4. Why `curl-impersonate`?](#4-why-curl-impersonate)

## 1. Dependencies

- [curl-impersonate](https://github.com/lwthiker/curl-impersonate);
- [Python 3.10 or newer](https://www.python.org/).

## 2. Implementation details

Micro-library allows you to retrieve some targets from [sploitus.com](https://sploitus.com/).
The query is done via `curl-impersonate` using [threading](https://docs.python.org/3/library/threading.html).

## 3. Quick guide

Lib parameters:

- **`targets`**: targets for information as a `list` of `str`;
- **`headers`**: headers for `http` request as a `dict`;
- **`curl_cmd`**: version/wrapper used `curl-impersonate` (default: `curl_ff109`) **[*]**;
- **`targets_type`**: info type for targets (`exploits` or `tools`);
- **`sort`**: sort results (`default`, `date` or `score`);
- **`title`**: hide or show titles (default: `False`);
- **`offset`**: results offset (default: `0`);
- **`sploitus_url`**: URL sploitus (default: `https://sploitus.com`);
- **`semaphore`**: number of simultaneously running curl processes (default: `4`).

**[*]** - After installing curl-impersonate, one way will be to specify the script or binary used in this parameter.

## 4. Why `curl-impersonate`?

**Sploitus** changed something in his work in 2022-2023. Most likely started working with [CloudFlare](https://www.cloudflare.com/).
You can tell from other projects that apparently worked before:

- [si9int sploitus.py](https://github.com/si9int/sploitus.py);
- [sploitGET](https://github.com/0xricksanchez/sploitGET).

There were attempts to communicate via [requests](https://requests.readthedocs.io/en/latest/), but instead of a response I got a blank page.

Until recently, a simple approach using classical [curl](https://curl.se/) worked. But that approach stopped working too.
