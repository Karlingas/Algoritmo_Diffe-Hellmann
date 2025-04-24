import time
import multiprocessing
import math

def mostrarTiempo(tiempo):  # Para imprimir los tiempos con un formato bonito
    horas = int(tiempo // 3600)
    minutos = int((tiempo % 3600) // 60)
    segundos = int(tiempo % 60)
    ms = int((tiempo - int(tiempo)) * 1000000)
    return f"{horas:01d}:{minutos:02d}:{segundos:02d}.{ms:06d}"

def exponencia_modular(base, expo, mod):
    if not isinstance(base, int) or not isinstance(expo, int) or not isinstance(mod, int):
        raise TypeError("Las entradas deben ser int")
    if expo < 0:
        raise ValueError("El exponente no puede ser negativo para este algoritmo")
    if mod <= 0:
        raise ValueError("El módulo debe ser un positivo")

    i = expo  
    x = base % mod 
    r = 1  

    while i > 0:
        if i % 2 != 0:
            r = (r * x) % mod 
            
        x = (x * x) % mod
        i = i // 2 

    return r

def worker_fuerza_bruta(args):
    """
    Función ejecutada por cada proceso trabajador.
    Verifica un solo exponente.
    (Asegúrate de que esté aquí, fuera del if __name__ == "__main__":)
    """
    g, p, mensaje_Alice, mensaje_Bob, exponente = args
    try:
        resultado = exponencia_modular(g, exponente, p)
        if resultado == mensaje_Alice:
            return ("Alice", exponente)
        elif resultado == mensaje_Bob:
            return ("Bob", exponente)
        else:
            return None
    except Exception as e:
        print(f"Error en worker con exponente {exponente}: {e}")
        return None

def genera_argumentos(g, p, mensaje_Alice, mensaje_Bob, inicio=1):
    """
    Generador infinito que produce los argumentos para cada llamada
    a worker_fuerza_bruta, incrementando el exponente.
    (Asegúrate de que esté aquí, fuera del if __name__ == "__main__":)
    """
    exponente = inicio - 1
    while True:
        exponente += 1
        yield (g, p, mensaje_Alice, mensaje_Bob, exponente)


def fuerza_bruta_paralela(g, p, mensaje_Alice, mensaje_Bob, num_procesos=None):
    """
    Realiza la búsqueda de fuerza bruta en paralelo utilizando múltiples procesos.

    num_procesos: Número de procesos a utilizar. Si es None, usa todos los cores disponibles.
    """
    if num_procesos is None:
        try:
            num_procesos = multiprocessing.cpu_count()
            print(f"Detectados {num_procesos} núcleos de CPU. Usando {num_procesos} procesos.")
        except NotImplementedError:
            print("No se pudo detectar el número de núcleos. Usando 2 procesos por defecto.")
            num_procesos = 2 # Usar un valor por defecto si cpu_count falla
    else:
        print(f"Usando {num_procesos} procesos especificados.")

    t_inicio = time.time()
    soluciones_encontradas = {} # Diccionario para almacenar las soluciones {Nombre: (exponente, tiempo)}
    soluciones_final = []

    # Usamos un Pool de procesos
    # with asegura que los procesos se cierren correctamente
    with multiprocessing.Pool(processes=num_procesos) as pool:
        print(f"Iniciando búsqueda paralela para g={g}, p={p}, A={mensaje_Alice}, B={mensaje_Bob}")

        # chunksize puede ayudar a mejorar el rendimiento al enviar trabajo en lotes
        chunksize = 1000

        # pool.imap_unordered procesa las tareas y devuelve los resultados
        # tan pronto como están listos, sin mantener el orden original.
        resultados_iter = pool.imap_unordered(
            worker_fuerza_bruta,
            genera_argumentos(g, p, mensaje_Alice, mensaje_Bob),
            chunksize=chunksize
        )

        try:
            for resultado in resultados_iter:
                if resultado:  # Si el worker devolvió algo no None
                    quien, exponente = resultado
                    if quien not in soluciones_encontradas: # Solo registrar la primera vez que se encuentra
                        tiempo_transcurrido = time.time() - t_inicio
                        soluciones_encontradas[quien] = (exponente, tiempo_transcurrido)
                        print(f"¡Encontrado! Clave de {quien}: {exponente} (Tiempo: {mostrarTiempo(tiempo_transcurrido)} segundos)")

                        # Si ya hemos encontrado ambas claves, podemos detener la búsqueda
                        if len(soluciones_encontradas) == 2:
                            print("Ambas claves encontradas. Terminando procesos...")
                            pool.terminate()
                            pool.join()
                            break 

        except KeyboardInterrupt:
            print("\nBúsqueda interrumpida por el usuario.")
            pool.terminate()
            pool.join()
        except Exception as e:
            print(f"\nOcurrió un error durante la búsqueda: {e}")
            pool.terminate()
            pool.join()


    if "Alice" in soluciones_encontradas:
        exp, t = soluciones_encontradas["Alice"]
        soluciones_final.append(("Alice", exp, t))
    if "Bob" in soluciones_encontradas:
        exp, t = soluciones_encontradas["Bob"]
        soluciones_final.append(("Bob", exp, t))


    t_total = time.time() - t_inicio
    print(f"Búsqueda completada (o detenida). Tiempo total: {mostrarTiempo(t_total)} segundos.")
    return soluciones_final


if __name__ == "__main__":
    g_ejemplo = 16860409
    p_ejemplo = 32452843

    mensaje_Alice = 16728734
    mensaje_Bob = 18600915

    print(f"Buscando claves para g={g_ejemplo}, p={p_ejemplo}, A={mensaje_Alice}, B={mensaje_Bob}")
    soluciones = fuerza_bruta_paralela(g_ejemplo, p_ejemplo, mensaje_Alice, mensaje_Bob)
    print("\n--- Soluciones Encontradas ---")
    if soluciones:
        for nombre, clave, tiempo in soluciones:
            print(f"  - {nombre}: Clave privada = {clave} (encontrada en {tiempo:.6f} s)")
    else:
        print("  No se encontraron soluciones (o la búsqueda fue interrumpida).")
