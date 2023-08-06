<div align="center">

# python-crisp-api
*🐍 Crisp API Python Wrapper.*

[![](https://img.shields.io/github/license/lvillis/python-crisp-api?style=flat-square)](https://github.com/lvillis/python-crisp-api)
[![](https://img.shields.io/github/repo-size/lvillis/python-crisp-api?style=flat-square&color=328657)](https://github.com/lvillis/python-crisp-api)
[![Github Actions](https://img.shields.io/github/workflow/status/lvillis/python-crisp-api/Publish?style=flat-square)](https://github.com/lvillis/python-crisp-api/actions) 
[![](https://img.shields.io/github/last-commit/lvillis/python-crisp-api?style=flat-square&label=commits)](https://github.com/lvillis/python-crisp-api)
[![](https://img.shields.io/pypi/dm/python-crisp?style=flat-square)](https://github.com/lvillis/python-crisp-api)

</div>

---

Unofficial Crisp API Python wrapper. Use Python code to authenticate, send messages, get conversations, and access your proxy account.


* **😘 Official Repository**: [python-crisp-api](https://github.com/crisp-im/python-crisp-api)
* **📝 Implements**: [Crisp Platform - API ~ v1](https://docs.crisp.chat/api/v1/) at reference revision: 12/31/2017

## Usage

Install the library:

```bash
pip install python-crisp
```

Then, import it:

```python
from python_crisp import Crisp
```

Construct a new authenticated Crisp client with your `identifier` and `key` tokens.

```python
client = Crisp()

client.authenticate(identifier, key)
```

Then, your client is ready to be consumed!

## Authentication

To authenticate against the API, generate your session identifier and session key **once** using the [Crisp token generation utility](https://go.crisp.chat/account/token/). You'll get a token keypair made of 2 values.

**Keep your token keypair values private, and store them safely for long-term use.**

Then, add authentication parameters to your `client` instance right after you create it:

```python
client = Crisp()

# Make sure to use the correct tier if you are authenticating a plugin
# eg. with a permanent token generated from Crisp Marketplace
client.set_tier("plugin")

# Authenticate to API (identifier, key)
# eg. client.authenticate("13937834-f6ce-4556-ae4f-9e0c54faf038", "eb6c3623245521d7a6c35f5b29f3fa756e893f034ed551d84518961c5ff16dec")
client.authenticate(identifier, key)

# Now, you can use authenticated API sections.
```

**🔴 Important: Make sure to generate your token once, and use the same token keys in all your subsequent requests to the API. Do not generate too many tokens, as we may invalidate your older tokens to make room for newer tokens.**

## Resource Methods

Most useful available Crisp API resources are implemented. **Programmatic methods names are named after their label name in the [API Reference](https://docs.crisp.chat/api/v1/)**.

Thus, it is straightforward to look for them in the library while reading the [API Reference](https://docs.crisp.chat/api/v1/).

In the following method prototypes, `crisp` is to be replaced with your Crisp API instance. For example, instanciate `client = Crisp()` and then call eg: `client.website.list_conversations(website_id, 1)`.

When calling a method that writes data to the API (eg. send a message with: `client.website.send_message_in_conversation()`), you need to submit it this way:

```python
website_id = "88972681-a00c-4b3b-a383-cab281636484"
session_id = "session_9df2a21e-f113-41d4-8ed2-bad8b49cafd1"

client.website.send_message_in_conversation(
    website_id, 
    session_id,
    {
    "type": "text",
    "content": "This message was sent from python-crisp-api! :)",
    "from": "operator",
    "origin": "chat"
    }
)
```
