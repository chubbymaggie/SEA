void f(int x)  {

  int i;
  for (i=0; i<x; i++)
    printf("%d",i);
  
  if (x > 1)
    printf("\nx > 1\n");

  for (i=0; i<x*2; i++)
    printf("%d",i);

}


int main(int argc) {
  
  f(argc);
  return 0;
}
