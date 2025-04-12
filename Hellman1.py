import random

def es_primo(numero):
  """
  Verifica si un número entero es primo.
  True si el número es primo, False de lo contrario.
  """
  if not isinstance(numero, int):
      raise TypeError("El input debe ser un número entero.")
  if numero <= 1:
    return False
  if numero <= 3:
      return True # 2 y 3 son primos
  if numero % 2 == 0 or numero % 3 == 0:
      return False # Eliminar múltiplos de 2 y 3
  # Solo necesitamos comprobar divisores de la forma 6k ± 1 hasta sqrt(n)
  i = 5
  while i * i <= numero:
    if numero % i == 0 or numero % (i + 2) == 0:
      return False
    i += 6
  return True

def _genera_un_primo_aleatorio(min_val, max_val, intentos_max=10000):
    """
    Función auxiliar para generar un único primo aleatorio en el rango [min_val, max_val).
    """
    if min_val >= max_val:
        raise ValueError("El valor mínimo debe ser estrictamente menor que el máximo.")

    for _ in range(intentos_max):
        candidato = random.randrange(min_val, max_val)
        if es_primo(candidato):
            return candidato

    # Si llegamos aquí, no se encontró un primo en los intentos dados
    raise ValueError(f"No se pudo encontrar un primo en el rango [{min_val}, {max_val}) "
                     f"después de {intentos_max} intentos.")

def generaPrimos(mini, maxi):
    """
    Genera 2 primos aleatorios DISTINTOS en el rango [mini, maxi).
    Devuelve primero Publica y luego Privada
    """
    # Genera el primer primo
    publica = _genera_un_primo_aleatorio(mini, maxi)
    privada = None
    
    while publica != privada:
        privada = _genera_un_primo_aleatorio(mini, maxi)
        if privada != publica:
            return publica, privada # Devuelve en el orden original







