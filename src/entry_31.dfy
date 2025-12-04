// entry_31.dfy
// Fibonacci (iterative) with a recursive spec function
function fibRec(n: nat): nat
  decreases n
{
  if n == 0 then 0 else if n == 1 then 1 else fibRec(n-1) + fibRec(n-2)
}

method Fib(n: nat) returns (f: nat)
  ensures f == fibRec(n)
{
  if n == 0 { f := 0; return; }
  if n == 1 { f := 1; return; }
  var a := 0;
  var b := 1;
  var i := 2;
  while i <= n
    invariant 2 <= i <= n+1
    invariant a == fibRec(i-2)
    invariant b == fibRec(i-1)
  {
    var tmp := b;
    b := a + b;
    a := tmp;
    i := i + 1;
  }
  f := b;
}
