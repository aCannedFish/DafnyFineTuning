// entry_33.dfy
// Count occurrences equal to x
method CountEqual(a: array<int>, x: int) returns (cnt: nat)
  ensures cnt == (sum i | 0 <= i < a.Length :: if a[i] == x then 1 else 0)
{
  cnt := 0;
  var i := 0;
  while i < a.Length
    invariant 0 <= i <= a.Length
    invariant cnt == (sum j | 0 <= j < i :: if a[j] == x then 1 else 0)
  {
    if a[i] == x {
      cnt := cnt + 1;
    }
    i := i + 1;
  }
}
