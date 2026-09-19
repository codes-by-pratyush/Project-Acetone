from Blockchain.attribution.vasp_attribution import (
    attribute_trace,
    attribute_trace_path,
)


def test_unknown_wallet():
    path = {
        "wallets": [
            "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        ],
        "transactions": [],
        "hops": 1,
    }

    result = attribute_trace_path(path)

    print("\n=== UNKNOWN WALLET TEST ===")
    print(result)

    assert result["attributed"] is False
    assert result["vasp"] is None
    assert result["confidence"] == 0.0


def test_known_vasp_wallet():
    path = {
        "wallets": [
            "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "0xexchange00000000000000000000000000000001",
        ],
        "transactions": [],
        "hops": 1,
    }

    result = attribute_trace_path(path)

    print("\n=== KNOWN VASP TEST ===")
    print(result)

    assert result["attributed"] is True
    assert result["vasp"] == "Demo Exchange"
    assert result["confidence"] == 0.90


def test_complete_trace_attribution():
    paths = [
        {
            "wallets": [
                "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "0xexchange00000000000000000000000000000001",
            ],
            "transactions": [],
            "hops": 1,
        }
    ]

    result = attribute_trace(paths)

    print("\n=== COMPLETE ATTRIBUTE TEST ===")
    print(result)

    assert result["overall"]["attributed"] is True
    assert result["overall"]["vasp"] == "Demo Exchange"
    assert result["overall"]["confidence"] == 0.90


if __name__ == "__main__":
    test_unknown_wallet()
    test_known_vasp_wallet()
    test_complete_trace_attribution()