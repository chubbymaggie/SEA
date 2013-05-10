int main(int argc) {

  int i;
  for (i=0; i<3; i++)
    printf("%d",i);
  
  if (argc > 1)
    printf("\nargc > 1\n");

  for (i=0; i<5; i++)
    printf("%d",i);
  
  return 0;
}
