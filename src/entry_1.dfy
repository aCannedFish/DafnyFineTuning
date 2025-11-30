method Abs(x: int) returns (y: int)
  requires true
  ensures 0 <= y
  ensures 0 <= x ==> y == x
  ensures x < 0 ==> y == -x
{
  if x < 0 {
    return -x;
    } else {
    return x;
  }
}
