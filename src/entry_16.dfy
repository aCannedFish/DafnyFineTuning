method test(n: int) returns (sum: int)
  requires n >= 0
  ensures sum * 2 == n * (n+1)
{
  sum := 0;
  var i:int := 0;
  while i <= n
  invariant i<=n+1
  invariant sum*2 == i*(i-1)
 
  {
    sum := sum + i;
    i := i + 1;
  }
}