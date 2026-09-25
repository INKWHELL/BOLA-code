#!/usr/bin/env bash
# BOLA demonstration script.
# Run `python manage.py runserver 7999` in one terminal, then run this
# script in another. Requires only curl.

set -euo pipefail

HOST="http://127.0.0.1:7999"

# Tokens printed by `python manage.py seed_demo`. Edit these two lines
# with the values that command prints on your machine.
TOKEN_A="${TOKEN_A:?Set TOKEN_A to User A's token from seed_demo output}"

echo "=== Request 1: User A -> own order (VULNERABLE endpoint, expected) ==="
curl -s -w "\nHTTP status: %{http_code}\n\n" \
  "$HOST/api/vuln/orders/1/" \
  -H "Authorization: Token $TOKEN_A"

echo "=== Request 2: User A -> User B's order, ID substituted (VULNERABLE endpoint) ==="
curl -s -w "\nHTTP status: %{http_code}\n\n" \
  "$HOST/api/vuln/orders/2/" \
  -H "Authorization: Token $TOKEN_A"

echo "=== Request 3: same substitution against the FIXED endpoint ==="
curl -s -w "\nHTTP status: %{http_code}\n\n" \
  "$HOST/api/orders/2/" \
  -H "Authorization: Token $TOKEN_A"

echo "=== Request 4: control — User A's own order still works on the FIXED endpoint ==="
curl -s -w "\nHTTP status: %{http_code}\n\n" \
  "$HOST/api/orders/1/" \
  -H "Authorization: Token $TOKEN_A"
