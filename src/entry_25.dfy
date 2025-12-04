// entry_25.dfy
// Factorial using a recursive function for the specification and an iterative method for computation
function factRec(n: nat): nat
  decreases n
{
  if n == 0 then 1 else n * factRec(n-1)
}

method Factorial(n: nat) returns (f: nat)
  ensures f == factRec(n)
{
  f := 1;
  var i := 1;
  while i <= n
    invariant 1 <= i <= n+1
    invariant f == factRec(i-1)
  {
    f := f * i;
    i := i + 1;
  }
}
