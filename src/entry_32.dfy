// entry_32.dfy
// Check whether a sequence of chars is a palindrome
method IsPalindrome(s: seq<char>) returns (res: bool)
  ensures res <==> (forall i :: 0 <= i < |s|/2 ==> s[i] == s[|s|-1-i])
{
  res := true;
  var i := 0;
  var n := |s|;
  while i < n/2
    invariant 0 <= i <= n/2
    invariant res ==> (forall j :: 0 <= j < i ==> s[j] == s[n-1-j])
  {
    if s[i] != s[n-1-i] {
      res := false;
      return;
    }
    i := i + 1;
  }
}
