import random

def generar_numero_de_n_digitos(n):
  """Genera un numero de N digitos y lo devuelve
  """
  if not isinstance(n, int) or n <= 0:
    print("Error: n tiene que ser positivo.")
    return None

  if n == 1:
    return str(random.randint(0, 9))  # pequeño

  # Generar primer digito
  primer_digito = str(random.randint(1, 9))

  # Generar el resto de digitos
  tolresto_digitos = ''.join(str(random.randint(0, 9)) for _ in range(n - 1))

  return int(primer_digito + tolresto_digitos)

n_digitos = 2466
numero = generar_numero_de_n_digitos(n_digitos)
if numero:
  print(f"A {n_digitos}-digit number: {numero}")