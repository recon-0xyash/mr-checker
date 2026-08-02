def mask_secret(secret: str) -> str:
    if len(secret) <= 8:
        return "*" * len(secret)

    return f"{secret[:4]}{'*' * (len(secret) - 8)}{secret[-4:]}"
