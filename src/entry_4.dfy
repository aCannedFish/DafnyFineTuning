method func(x: int) returns (y: int)
  requires true
  ensures x < 0 ==> y == -x
{
  y:= -x + 0;
}
