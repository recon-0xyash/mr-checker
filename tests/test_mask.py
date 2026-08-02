from mrchecker.utils.mask import mask_secret


def test_mask_secret() -> None:
    assert mask_secret("AKIAABCDEFGHIJKLMNOP") == "AKIA************MNOP"


def test_short_secret() -> None:
    assert mask_secret("abcd") == "****"
