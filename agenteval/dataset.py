def validate_dataset(cases: list[dict]):
    required_keys = {"id", "input", "expected_label", "category", "notes"}
    for case in cases:
        missing = required_keys - set(case.keys())
        if missing:
            raise ValueError(f"Dataset case {case.get('id', 'unknown')} missing keys: {missing}")
