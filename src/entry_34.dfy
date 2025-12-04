// entry_34.dfy
// Check all elements even
method AllEven(a: array<int>) returns (res: bool)
  ensures res <==> (forall i :: 0 <= i < a.Length ==> a[i] % 2 == 0)
{
  res := true;
  var i := 0;
  while i < a.Length
    invariant 0 <= i <= a.Length
    invariant res ==> (forall j :: 0 <= j < i ==> a[j] % 2 == 0)
  {
    if a[i] % 2 != 0 {
      res := false;
      return;
    }
    i := i + 1;
  }
}
