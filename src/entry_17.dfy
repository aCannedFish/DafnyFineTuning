function gcd(x: nat, y: nat): nat
  decreases y
{
  if y == 0 then x else gcd(y, x % y)
}

method EuclidGcd(a: nat, b: nat) returns (g: nat)
  requires a >= 0 && b >= 0
  requires a != 0 || b != 0
  ensures g == gcd(a, b)
{
  var x := a;
  var y := b;
  while y != 0
    invariant x >= 0 && y >= 0
    invariant gcd(x, y) == gcd(a, b)
  {
    var t := x % y;
    x := y;
    y := t;
  }
  g := x;
}
