CWT Usage Examples
==================

The following is a simple sample code using CWT API:

.. code-block:: pycon

    >>> import cwt
    >>> from cwt import Claims, COSEKey
    >>> key = COSEKey.from_symmetric_key(alg="HS256", kid="01")
    >>> token = cwt.encode({"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, key)
    >>> token.hex()
    'd18443a10105a05835a60172636f6170733a2f2f61732e6578616d706c65026764616a69616a690743313233041a609097b7051a609089a7061a609089a758201fad9b0a76803194bd11ca9b9b3cbbf1028005e15321665a768994f38c7127f7'
    >>> cwt.decode(token, key)
    {1: 'coaps://as.example', 2: 'dajiaji', 7: b'123', 4: 1620088759, 5: 1620085159, 6: 1620085159}

This page shows various examples to use CWT API in this library.

.. contents::
   :local:

MACed CWT
---------

Create a MACed CWT, verify and decode it as follows:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    try:
        key = COSEKey.from_symmetric_key(alg="HS256", kid="01")
        token = cwt.encode(
            {"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"},
            key,
        )
        decoded = cwt.decode(token, key)

        # If you want to treat the result like a JWT;
        readable = Claims.new(decoded)
        assert readable.iss == "coaps://as.example"
        assert readable.sub == "dajiaji"
        assert readable.cti == "123"
        # readable.exp == 1620088759
        # readable.nbf == 1620085159
        # readable.iat == 1620085159

    except Exception as err:
        # All the other examples in this document omit error handling but this CWT library
        # can throw following errors:
        #   ValueError: Invalid arguments.
        #   EncodeError: Failed to encode.
        #   VerifyError: Failed to verify.
        #   DecodeError: Failed to decode.
        print(err)


A raw CWT structure (Dict[int, Any]) can also be used as follows:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    key = COSEKey.from_symmetric_key(alg="HS256", kid="01")
    token = cwt.encode({1: "coaps://as.example", 2: "dajiaji", 7: b"123"}, key)
    decoded = cwt.decode(token, key)

Algorithms other than ``HS256`` are listed in `Supported COSE Algorithms`_ .

Signed CWT
----------

Create an ``Ed25519`` (Ed25519 for use w/ EdDSA only) key pair:

.. code-block:: console

    $ openssl genpkey -algorithm ed25519 -out private_key.pem
    $ openssl pkey -in private_key.pem -pubout -out public_key.pem

Create a Signed CWT, verify and decode it with the key pair as follows:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    with open("./private_key.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="01")
    with open("./public_key.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="01")


    token = cwt.encode(
        {"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, private_key
    )

    decoded = cwt.decode(token, public_key)

JWKs can also be used instead of the PEM-formatted keys as follows:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    private_key = COSEKey.from_jwk(
        {
            "kty": "OKP",
            "d": "L8JS08VsFZoZxGa9JvzYmCWOwg7zaKcei3KZmYsj7dc",
            "use": "sig",
            "crv": "Ed25519",
            "kid": "01",
            "x": "2E6dX83gqD_D0eAmqnaHe1TC1xuld6iAKXfw2OVATr0",
            "alg": "EdDSA",
        }
    )
    public_key = COSEKey.from_jwk(
        {
            "kty": "OKP",
            "use": "sig",
            "crv": "Ed25519",
            "kid": "01",
            "x": "2E6dX83gqD_D0eAmqnaHe1TC1xuld6iAKXfw2OVATr0",
        }
    )

    token = cwt.encode(
        {"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, private_key
    )
    decoded = cwt.decode(token, public_key)

Algorithms other than ``Ed25519`` are also supported. The following is an example of ``ES256``:

.. code-block:: console

    $ openssl ecparam -genkey -name prime256v1 -noout -out private_key.pem
    $ openssl ec -in private_key.pem -pubout -out public_key.pem

.. code-block:: python

    import cwt
    from cwt import COSEKey

    with open("./private_key.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="01")
    with open("./public_key.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="01")

    token = cwt.encode(
        {"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, private_key
    )

    decoded = cwt.decode(token, public_key)

Other supported algorithms are listed in `Supported COSE Algorithms`_.

Encrypted CWT
-------------

Create an encrypted CWT with ``ChaCha20/Poly1305`` (ChaCha20/Poly1305 w/ 256-bit key, 128-bit tag),
and decrypt it as follows:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    enc_key = COSEKey.from_symmetric_key(alg="ChaCha20/Poly1305", kid="01")
    token = cwt.encode(
        {"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, enc_key
    )
    decoded = cwt.decode(token, enc_key)

Algorithms other than ``ChaCha20/Poly1305`` are also supported. The following is an example of
``AES-CCM-16-64-256``:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    enc_key = COSEKey.from_symmetric_key(alg="AES-CCM-16-64-256", kid="01")
    token = cwt.encode(
        {"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, enc_key
    )
    decoded = cwt.decode(token, enc_key)

Other supported algorithms are listed in `Supported COSE Algorithms`_.

Nested CWT
----------

Create a signed CWT and encrypt it, and then decrypt and verify the nested CWT as follows.

.. code-block:: python

    import cwt
    from cwt import COSEKey

    with open("./private_key.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="sig-01")
    with open("./public_key.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="sig-01")

    # Creates a CWT with ES256 signing.
    token = cwt.encode(
        {"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, private_key
    )

    # Encrypts the signed CWT.
    enc_key = COSEKey.from_symmetric_key(alg="ChaCha20/Poly1305", kid="enc-01")
    nested = cwt.encode(token, enc_key)

    # Decrypts and verifies the nested CWT.
    decoded = cwt.decode(nested, [enc_key, public_key])

CWT with User Settings
----------------------

The ``cwt`` in ``cwt.encode()`` and ``cwt.decode()`` above is a global ``CWT`` class instance created
with default settings in advance. The default settings are as follows:

* ``expires_in``: ``3600`` seconds. This is the default lifetime in seconds of CWTs.
* ``leeway``: ``60`` seconds. This is the default leeway in seconds for validating ``exp`` and ``nbf``.

If you want to change the settings, you can create your own ``CWT`` class instance as follows:

.. code-block:: python

    from cwt import COSEKey, CWT

    key = COSEKey.from_symmetric_key(alg="HS256", kid="01")
    mycwt = CWT.new(expires_in=3600 * 24, leeway=10)
    token = mycwt.encode({"iss": "coaps://as.example", "sub": "dajiaji", "cti": "123"}, key)
    decoded = mycwt.decode(token, key)

CWT with User-Defined Claims
----------------------------

You can use your own claims as follows:

Note that such user-defined claim's key should be less than -65536.

.. code-block:: python

    import cwt
    from cwt import COSEKey

    with open("./private_key.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="01")
    with open("./public_key.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="01")
    token = cwt.encode(
        {
            1: "coaps://as.example",  # iss
            2: "dajiaji",  # sub
            7: b"123",  # cti
            -70001: "foo",
            -70002: ["bar"],
            -70003: {"baz": "qux"},
            -70004: 123,
        },
        private_key,
    )
    raw = cwt.decode(token, public_key)
    assert raw[-70001] == "foo"
    assert raw[-70002][0] == "bar"
    assert raw[-70003]["baz"] == "qux"
    assert raw[-70004] == 123

    readable = Claims.new(raw)
    assert readable.get(-70001) == "foo"
    assert readable.get(-70002)[0] == "bar"
    assert readable.get(-70003)["baz"] == "qux"
    assert readable.get(-70004) == 123

User-defined claims can also be used with JSON-based claims as follows:

.. code-block:: python

    import cwt
    from cwt import Claims, COSEKey

    with open("./private_key.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="01")
    with open("./public_key.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="01")

    my_claim_names = {
        "ext_1": -70001,
        "ext_2": -70002,
        "ext_3": -70003,
        "ext_4": -70004,
    }

    cwt.set_private_claim_names(my_claim_names)
    token = cwt.encode(
        {
            "iss": "coaps://as.example",
            "sub": "dajiaji",
            "cti": b"123",
            "ext_1": "foo",
            "ext_2": ["bar"],
            "ext_3": {"baz": "qux"},
            "ext_4": 123,
        },
        private_key,
    )
    claims.set_private_claim_names()
    raw = cwt.decode(token, public_key)
    readable = Claims.new(
        raw,
        private_claim_names=my_claim_names,
    )
    assert readable.get("ext_1") == "foo"
    assert readable.get("ext_2")[0] == "bar"
    assert readable.get("ext_3")["baz"] == "qux"
    assert readable.get("ext_4") == 123

CWT with PoP key
----------------

Create a CWT which has a PoP key as follows:

On the issuer side:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    # Prepares a signing key for CWT in advance.
    with open("./private_key_of_issuer.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")

    # Sets the PoP key to a CWT for the presenter.
    token = cwt.encode(
        {
            "iss": "coaps://as.example",
            "sub": "dajiaji",
            "cti": "123",
            "cnf": {
                "jwk": {  # Provided by the CWT presenter.
                    "kty": "OKP",
                    "use": "sig",
                    "crv": "Ed25519",
                    "kid": "presenter-01",
                    "x": "2E6dX83gqD_D0eAmqnaHe1TC1xuld6iAKXfw2OVATr0",
                    "alg": "EdDSA",
                },
            },
        },
        private_key,
    )

    # Issues the token to the presenter.

On the CWT presenter side:

.. code-block:: python

    import cwt
    from cwt import COSEKey

    # Prepares a private PoP key in advance.
    with open("./private_pop_key.pem") as key_file:
        pop_key_private = COSEKey.from_pem(key_file.read(), kid="presenter-01")

    # Receives a message (e.g., nonce)  from the recipient.
    msg = b"could-you-sign-this-message?"  # Provided by recipient.

    # Signs the message with the private PoP key.
    sig = pop_key_private.sign(msg)

    # Sends the msg and the sig with the CWT to the recipient.

On the CWT recipient side:

.. code-block:: python

    import cwt
    from cwt import Claims, COSEKey

    # Prepares the public key of the issuer in advance.
    with open("./public_key_of_issuer.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")

    # Verifies and decodes the CWT received from the presenter.
    raw = cwt.decode(token, public_key)
    decoded = Claims.new(raw)

    # Extracts the PoP key from the CWT.
    extracted_pop_key = COSEKey.new(decoded.cnf)  #  = raw[8][1]

    # Then, verifies the message sent by the presenter
    # with the signature which is also sent by the presenter as follows:
    extracted_pop_key.verify(msg, sig)

In case of another PoP confirmation method ``Encrypted_COSE_Key``:

.. code-block:: python

    import cwt
    from cwt import Claims, COSEKey, EncryptedCOSEKey

    with open("./private_key.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")

    enc_key = COSEKey.from_symmetric_key(
        "a-client-secret-of-cwt-recipient",  # Just 32 bytes!
        alg="ChaCha20/Poly1305",
        kid="recipient-01",
    )
    pop_key = COSEKey.from_symmetric_key(
        "a-client-secret-of-cwt-presenter",
        alg="HMAC 256/256",
        kid="presenter-01",
    )

    token = cwt.encode(
        {
            "iss": "coaps://as.example",
            "sub": "dajiaji",
            "cti": "123",
            "cnf": {
                # 'eck'(Encrypted Cose Key) is a keyword defined by this library.
                "eck": EncryptedCOSEKey.from_cose_key(pop_key, enc_key),
            },
        },
        private_key,
    )

    with open("./public_key.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")
    raw = cwt.decode(token, public_key)
    decoded = Claims.new(raw)
    extracted_pop_key = EncryptedCOSEKey.to_cose_key(decoded.cnf, enc_key)
    # extracted_pop_key.verify(message, signature)

In case of another PoP confirmation method ``kid``:

.. code-block:: python

    import cwt
    from cwt import Claims, COSEKey

    with open("./private_key.pem") as key_file:
        private_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")

    token = cwt.encode(
        {
            "iss": "coaps://as.example",
            "sub": "dajiaji",
            "cti": "123",
            "cnf": {
                "kid": "pop-key-id-of-cwt-presenter",
            },
        },
        private_key,
    )

    with open("./public_key.pem") as key_file:
        public_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")
    raw = cwt.decode(token, public_key)
    decoded = Claims.new(raw)
    # decoded.cnf(=raw[8][3]) is kid.

.. _`Supported COSE Algorithms`: ./algorithms.html
