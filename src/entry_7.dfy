method func(x: int) returns (y: int)
  requires 0 <= x && (x >= 0 || x == 0)
  ensures 0 <= y
  ensures x < 0 ==> y == -x
{
  y:= x + 0;
}
