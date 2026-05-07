#!/usr/bin/env python3
import json
import sys
import urllib.parse
import urllib.request

API = "https://verification.fda.gov.ph/api/search?q={}"


def norm(s):
    return " ".join(str(s).strip().lower().split())


def main():
    if len(sys.argv) < 2:
        print('usage: lookup.py "<registration number or product name>"', file=sys.stderr)
        return 1

    query = " ".join(sys.argv[1:]).strip()
    url = API.format(urllib.parse.quote(query, safe=""))

    print("Checking FDA record...", file=sys.stderr, flush=True)

    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as e:
        print(f"error: failed to fetch FDA data: {e}", file=sys.stderr)
        return 2

    qn = norm(query)
    matches = []

    for group_name, group in data.items():
        if not isinstance(group, list):
            continue
        for item in group:
            if not isinstance(item, dict):
                continue
            haystack = " ".join(norm(v) for v in item.values() if v is not None)
            if qn in haystack or norm(item.get("ACCOUNTCODE", "")) == qn:
                matches.append((group_name, item))

    print(f"Query: {query}")
    print(f"Matches: {len(matches)}")

    if not matches:
        print("No matching FDA record found.")
        return 0

    for idx, (group_name, item) in enumerate(matches, 1):
        print(f"\n[{idx}] {group_name}")
        print(f"  ACCOUNTCODE: {item.get('ACCOUNTCODE', '-')}")
        print(f"  PRODUCT_NAME: {item.get('PRODUCT_NAME', '-')}")
        print(f"  BRAND_NAME: {item.get('BRAND_NAME', '-')}")
        print(f"  COMPANY_NAME: {item.get('COMPANY_NAME', '-')}")
        print(f"  DATE_VALIDITY: {item.get('DATE_VALIDITY', '-')}")
        print(f"  IS_CANCELED: {item.get('IS_CANCELED', '-')}" )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
