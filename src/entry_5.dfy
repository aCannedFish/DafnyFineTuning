method func(x: int) returns (y: int)
  requires x >= 0
  ensures x < 0 ==> y == -x
{
  y:= x + 1;
}
