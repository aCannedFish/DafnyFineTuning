method DivMod(n: nat, d: nat) returns (q: nat, r: nat)
  requires d > 0
  ensures n == q * d + r
  ensures 0 <= r < d
{
  q := 0;
  r := n;
  while r >= d
    invariant 0 <= q
    invariant 0 <= r
    invariant n == q * d + r
  {
    r := r - d;
    q := q + 1;
  }
}
