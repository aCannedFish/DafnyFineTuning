// entry_30.dfy
// Detect duplicate elements in array
method HasDuplicate(a: array<int>) returns (res: bool)
  ensures res <==> (exists i, j :: 0 <= i < j < a.Length && a[i] == a[j])
{
  res := false;
  var i := 0;
  while i < a.Length
    invariant 0 <= i <= a.Length
    invariant !res ==> (forall k, l :: 0 <= k < l < i ==> a[k] != a[l])
  {
    var j := 0;
    while j < i
      invariant 0 <= j <= i
      invariant !res ==> (forall k :: 0 <= k < j ==> a[k] != a[i])
    {
      if a[j] == a[i] {
        res := true;
        return;
      }
      j := j + 1;
    }
    i := i + 1;
  }
}
