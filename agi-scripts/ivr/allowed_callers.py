import yaml


def _load_numbers(path: str):
    try:
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return data.get("callers", [])
    except FileNotFoundError:
        return []


def load_allowed_callers(config_path="config/allowed_callers.yml"):
    """Return list of allowed caller IDs."""
    return _load_numbers(config_path)


def load_owner_callers(config_path="config/owner_callers.yml"):
    """Return list of owner caller IDs."""
    return _load_numbers(config_path)
