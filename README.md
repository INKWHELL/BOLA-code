# BOLA demo — Django REST Framework

A minimal, runnable project demonstrating Broken Object Level Authorization
(OWASP API1:2023): one vulnerable endpoint, one fixed endpoint, same model,
same data, same test accounts. Requires only Python, `curl`, and a browser —
no interception proxy.

## Layout

```
bola_demo/          project settings, root urls
orders/
  models.py         Order model (owner, item, total)
  serializers.py     
  views.py           OrderDetailVulnerable (unscoped) and OrderDetailFixed (scoped)
  urls.py             /api/vuln/orders/<id>/  and  /api/orders/<id>/
  management/commands/seed_demo.py   creates User A and User B
test_bola.sh         curl-only exploit + verification script
```

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo
```

`seed_demo` creates two unprivileged accounts, `user_a` and `user_b`, each
owning one `Order`, and prints their API tokens:

```
User A  -> username=user_a  order_id=1  token=<TOKEN_A>
User B  -> username=user_b  order_id=2  token=<TOKEN_B>
```

Copy `TOKEN_A` — that's the only credential used in the whole demonstration.

## Run the server

```bash
python manage.py runserver 7999
```

## Reproduce the vulnerability (curl, terminal)

In a second terminal:

```bash
export TOKEN_A="<paste User A's token>"
./test_bola.sh
```

Or run the four requests by hand:

```bash
# User A retrieves their own order — expected
curl -i http://127.0.0.1:7999/api/vuln/orders/1/ -H "Authorization: Token $TOKEN_A"

# Same token, ID substituted — returns User B's order on the vulnerable endpoint
curl -i http://127.0.0.1:7999/api/vuln/orders/2/ -H "Authorization: Token $TOKEN_A"

# Same substitution against the fixed endpoint — 404
curl -i http://127.0.0.1:7999/api/orders/2/ -H "Authorization: Token $TOKEN_A"

# Control: User A's own order still works on the fixed endpoint
curl -i http://127.0.0.1:7999/api/orders/1/ -H "Authorization: Token $TOKEN_A"
```

## Reproduce in a browser (GET requests only)

Browsers can't easily set an `Authorization` header on a plain navigation,
so DRF's browsable API is used with session login instead of the token:

1. Visit `http://127.0.0.1:7999/admin/` and log in as `user_a` / `test1234`
   (create a matching session by adding `user_a` as a superuser first, or
   just use `curl`/Postman for header-based auth — this step is optional).
2. More directly: open `http://127.0.0.1:7999/api/vuln/orders/1/` — DRF's
   browsable API will prompt for login. Authenticate as `user_a`, then
   change the URL to `.../api/vuln/orders/2/` and observe User B's order
   is returned without any error.
3. Repeat against `/api/orders/2/` (the fixed endpoint) and observe a 404.

## What to look at

- Same token in every request (`TOKEN_A` never changes).
- Only the path changes (`1` vs `2`, `vuln/orders` vs `orders`).
- Vulnerable endpoint: `200 OK` with `owner: "user_b"` — data disclosed
  to a user who does not own it.
- Fixed endpoint: `404 Not Found` — the object is absent from the
  requester's queryset, not merely denied.
- Fixed endpoint, own order: still `200 OK` — the fix does not break
  legitimate access.

## The fix, in one line

```python
def get_queryset(self):
    return Order.objects.filter(owner=self.request.user)
```

Object-level authorization is enforced by scoping the queryset to the
requester before the primary-key lookup is applied, rather than trusting
the ID in the URL against the full table.
