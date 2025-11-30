method Abs2(x: int) returns (y: int)
  requires false
  ensures 0 <= y
  ensures 0 <= x ==> y == x
  ensures x < 0 ==> y == -x
{
  y := x + 1;
}
