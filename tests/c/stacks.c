int main() {

  int x = 3;
  return f(&x);
}

int f(int *p) {
  return g(p);
}

int g(int *p) {
  return h(p);
}

int h(int *p) {
  printf("%d\n", *p);
  return *p;
}

