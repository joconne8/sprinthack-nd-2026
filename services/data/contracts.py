"""v1 contract validation; standard library only.

The JSON schemas use the explicitly supported structural keywords below.
They are also usable by a full JSON Schema validator in a frontend/tool client.
"""
import hashlib
import json
import re
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CONTRACT_VERSION = "goodwill-v1"
METRIC_VERSION = "demo-net-sales-v1"
PARSER_VERSION = "sales-parser-v1"
RULE_VERSION = "trusted-data-v1"
REPORTING_ZONE = "America/New_York"


class DataError(ValueError):
    def __init__(self, code, detail):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def cents(value):
    if not isinstance(value, str) or not re.fullmatch(r"-?\d+(?:\.\d{1,2})?", value):
        raise DataError("invalid_money", "Expected a decimal string with at most two fractional digits")
    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise DataError("invalid_money", value)
    if not amount.is_finite() or abs(amount) > Decimal("1000000000"):
        raise DataError("invalid_money", "Amount outside synthetic demo bounds")
    return int(amount * 100)


def money(value):
    return format(Decimal(value) / 100, ".2f")


def day(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise DataError("invalid_date", str(value))
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise DataError("invalid_date", value)


def validate(schema_name, value):
    """Validate the exact shipped schema, including nested response/example shapes."""
    schema = json.loads((Path(__file__).resolve().parents[2] / "contracts/v1" / schema_name).read_text())

    def visit(rule, item, path):
        if "$ref" in rule:
            target = schema
            for part in rule["$ref"].removeprefix("#/").split("/"):
                target = target[part]
            return visit(target, item, path)
        if "anyOf" in rule:
            matched = False
            for option in rule["anyOf"]:
                try:
                    visit(option, item, path)
                    matched = True
                    break
                except DataError:
                    pass
            if not matched:
                raise DataError("contract_invalid", f"{path}: no allowed shape matches")
        kinds = {"object": lambda: isinstance(item, dict), "array": lambda: isinstance(item, list),
                 "string": lambda: isinstance(item, str), "integer": lambda: type(item) is int,
                 "boolean": lambda: type(item) is bool, "null": lambda: item is None}
        if "type" in rule and not kinds[rule["type"]]():
            raise DataError("contract_invalid", f"{path}: expected {rule['type']}")
        if "const" in rule and (item != rule["const"] or type(item) is not type(rule["const"])):
            raise DataError("contract_invalid", f"{path}: wrong constant")
        if "enum" in rule and item not in rule["enum"]:
            raise DataError("contract_invalid", f"{path}: invalid enum")
        if isinstance(item, str):
            if "pattern" in rule and not re.search(rule["pattern"], item):
                raise DataError("contract_invalid", f"{path}: invalid string pattern")
            if len(item) < rule.get("minLength", 0):
                raise DataError("contract_invalid", f"{path}: empty required string")
        if type(item) is int and item < rule.get("minimum", item):
            raise DataError("contract_invalid", f"{path}: too small")
        if isinstance(item, dict):
            if any(key not in item for key in rule.get("required", [])):
                raise DataError("contract_invalid", f"{path}: missing required keys")
            properties = rule.get("properties", {})
            if rule.get("additionalProperties") is False and set(item) - set(properties):
                raise DataError("contract_invalid", f"{path}: unknown keys")
            for key, child in properties.items():
                if key in item:
                    visit(child, item[key], f"{path}.{key}")
        if isinstance(item, list) and "items" in rule:
            for n, child in enumerate(item):
                visit(rule["items"], child, f"{path}[{n}]")
    visit(schema, value, "$")
    return value


def manifest_metadata(manifest):
    """Explicit legacy adapter. Preserve the original manifest separately in storage."""
    if not isinstance(manifest, dict):
        raise DataError("manifest_invalid", "Manifest must be an object")
    if manifest.get("schema_version") not in ("replica-v1", "fixture-v1", CONTRACT_VERSION):
        raise DataError("unsupported_version", str(manifest.get("schema_version")))
    keys = ("source_name", "report_type", "requested_start_date", "requested_end_date",
            "reporting_timezone", "file_name", "file_checksum", "row_count", "currency", "synthetic")
    normalized = {key: manifest.get(key) for key in keys}
    normalized["schema_version"] = CONTRACT_VERSION
    # Filters are part of coverage. A filtered report is never full-source coverage.
    normalized["filters"] = manifest.get("filters", {key: manifest.get(key, []) for key in ("channels", "accounts", "order_ids", "skus")})
    if "filters" not in manifest:
        normalized["filters"]["payment_status"] = manifest.get("payment_status", "All")
    normalized["source_schema_version"] = manifest.get("source_schema_version", manifest["schema_version"])
    validate("manifest.schema.json", normalized)
    start, end = day(normalized["requested_start_date"]), day(normalized["requested_end_date"])
    if start > end or (end - start).days > 365:
        raise DataError("invalid_period", "Period must be ordered and no longer than 366 days")
    try:
        ZoneInfo(normalized["reporting_timezone"])
    except (ZoneInfoNotFoundError, ValueError):
        raise DataError("invalid_timezone", normalized["reporting_timezone"])
    return normalized
