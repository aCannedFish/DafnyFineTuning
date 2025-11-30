method func(x: int) returns (y: int)
  requires 0 <= x - 3
  ensures 0 <= y
{
  y:= x - 3;
}
