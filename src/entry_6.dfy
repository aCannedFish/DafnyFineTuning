method func(x: int) returns (y: int)
  requires 0 <= -x + 5
  ensures 0 <= y
{
  y:= -x + 5;
}
