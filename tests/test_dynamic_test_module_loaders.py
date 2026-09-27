from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def test_dynamic_file_loaders_register_modules_before_exec():
    offenders = []

    for path in sorted(TESTS.glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        if "importlib.util.spec_from_file_location(" not in text:
            continue
        if "importlib.util.module_from_spec(spec)" not in text:
            continue

        assignments = list(
            re.finditer(
                r"(?m)^(?P<indent>\s*)(?P<name>[A-Za-z_]\w*)\s*=\s*"
                r"importlib\.util\.module_from_spec\(spec\)\s*$",
                text,
            )
        )
        if not assignments:
            offenders.append(f"{path.name}: no module_from_spec assignment")
            continue

        for match in assignments:
            name = match.group("name")
            registration = f"sys.modules[spec.name] = {name}"
            exec_call = f"spec.loader.exec_module({name})"

            start = match.end()
            exec_index = text.find(exec_call, start)
            register_index = text.find(registration, start)

            if exec_index < 0:
                offenders.append(
                    f"{path.name}: missing exec_module({name})"
                )
                continue
            if register_index < 0 or register_index > exec_index:
                offenders.append(
                    f"{path.name}: {registration!r} must precede exec_module"
                )

    assert not offenders, (
        "dynamic test modules must be registered in sys.modules before "
        "exec_module so dataclasses and Python 3.12 module lookup work:\n"
        + "\n".join(offenders)
    )
