import threading
import time
import random

# =============================================================================
# Variables globales pour la simulation des pseudo-qubits
# =============================================================================
pseudo_qubit_states = []
stop_threads = False
threads = []

# =============================================================================
# 1. Définition et initialisation des pseudo-qubits
# =============================================================================
def init_pseudo_qubits(n):
    """
    Initialise l'état global pour n pseudo-qubits (tous mis à 0).
    """
    global pseudo_qubit_states
    pseudo_qubit_states = [0] * n

# =============================================================================
# 2. Estimation de la mémoire utilisée par un ensemble de pseudo-qubits
# =============================================================================
def memory_usage_loops(n):
    """
    Retourne une estimation de la mémoire utilisée par une liste de n pseudo-qubits.
    (On estime qu'un entier Python coûte environ 28 octets.)
    """
    return n * 28

# =============================================================================
# 3. Simulation de l'évolution d'un pseudo-qubit (boucle dans un thread)
# =============================================================================
def pseudo_qubit_loop(index, base_period=1.0, variation=0.5):
    """
    Simule un pseudo-qubit qui alterne son état (0/1).
      - index       : indice du pseudo-qubit dans la liste globale.
      - base_period : période de base d'oscillation (en secondes).
      - variation   : variation aléatoire ajoutée à la période pour désynchroniser.
    
    Si le pseudo-qubit "voisin" (index+1 modulo n) est en état 1, la période est
    réduite (le pseudo-qubit change plus vite), simulant ainsi une interaction.
    
    Le thread vérifie le flag global 'stop_threads' pour savoir quand s'arrêter.
    """
    # Délai initial aléatoire pour désynchroniser le démarrage
    time.sleep(random.uniform(0, base_period))
    while not stop_threads:
        try:
            # Calculer une période aléatoire avec variation
            period = base_period + random.uniform(-variation, variation)
            # Vérifier le voisin suivant (cyclique) pour simuler une interaction
            n = len(pseudo_qubit_states)
            if n > 1:
                neighbor_index = (index + 1) % n
                if pseudo_qubit_states[neighbor_index] == 1:
                    period *= 0.5  # accélère l'évolution si le voisin est 1
            period = max(0.1, period)
            # Inverser l'état (0 devient 1, 1 devient 0)
            pseudo_qubit_states[index] = 1 - pseudo_qubit_states[index]
        except IndexError:
            # En cas de réinitialisation pendant l'exécution, sortir du thread
            return
        time.sleep(period)

def start_pseudo_quantum(n):
    """
    Lance n threads, chacun représentant un pseudo-qubit.
    Retourne la liste des threads lancés.
    """
    global stop_threads, threads
    stop_threads = False
    init_pseudo_qubits(n)
    threads = []
    for i in range(n):
        t = threading.Thread(target=pseudo_qubit_loop, args=(i,), daemon=True)
        t.start()
        threads.append(t)
    return threads

def stop_pseudo_quantum():
    """
    Demande aux threads de s'arrêter en mettant à jour le flag global et attend leur terminaison.
    """
    global stop_threads, threads
    stop_threads = True
    for t in threads:
        t.join(timeout=1)
    stop_threads = False

# =============================================================================
# 4. Opérations (portes) sur les pseudo-qubits
# =============================================================================
def apply_hadamard_pseudo():
    """
    Simule l'application d'une porte Hadamard sur l'ensemble des pseudo-qubits.
    Ici, on réaffecte aléatoirement 0 ou 1 à chaque pseudo-qubit.
    """
    global pseudo_qubit_states
    n = len(pseudo_qubit_states)
    pseudo_qubit_states = [random.choice([0, 1]) for _ in range(n)]

def apply_CNOT(control, target):
    """
    Simule une porte CNOT : si le pseudo-qubit de contrôle est 1,
    on inverse l'état du pseudo-qubit cible.
    """
    global pseudo_qubit_states
    if pseudo_qubit_states[control] == 1:
        pseudo_qubit_states[target] = 1 - pseudo_qubit_states[target]

def apply_Toffoli(control1, control2, target):
    """
    Simule une porte Toffoli (CCNOT) : si les deux pseudo-qubits de contrôle
    sont à 1, on inverse l'état du pseudo-qubit cible.
    """
    global pseudo_qubit_states
    if pseudo_qubit_states[control1] == 1 and pseudo_qubit_states[control2] == 1:
        pseudo_qubit_states[target] = 1 - pseudo_qubit_states[target]

# =============================================================================
# 5. Mesure probabiliste plus réaliste
# =============================================================================
def measure_probabilistic():
    """
    Simule une mesure probabiliste en "gelant" l'état global pendant un court instant.
    Retourne l'état mesuré sous forme de chaîne binaire.
    """
    time.sleep(random.uniform(0.1, 0.3))
    return "".join(str(x) for x in pseudo_qubit_states)

# =============================================================================
# 6. Simulation d'un algorithme pseudo-Grover
# =============================================================================
def pseudo_grover(target_state, iterations=5):
    """
    Simule de façon très simplifiée un algorithme de Grover.
      - target_state : chaîne binaire (ex: "101") que l'on souhaite amplifier.
      - iterations   : nombre d'itérations.
    
    À chaque itération, on mesure l'état global avec measure_probabilistic().
    Si l'état mesuré n'est pas la cible, on applique une porte Hadamard simplifiée
    (randomisation) pour tenter d'amener le système vers l'état cible.
    """
    for i in range(iterations):
        measured = measure_probabilistic()
        print(f"Grover itération {i+1}: état mesuré = {measured}")
        if measured == target_state:
            print("État cible atteint !")
            return measured
        else:
            apply_hadamard_pseudo()
            time.sleep(0.5)
    return measure_probabilistic()

# =============================================================================
# 7. Simulation d'un algorithme Deutsch-Jozsa simplifié
# =============================================================================
def simulate_deutsch_jozsa(n, oracle_type='balanced'):
    """
    Simule un algorithme Deutsch-Jozsa simplifié sur n pseudo-qubits.
      - oracle_type : 'constant' ou 'balanced'
    
    L'idée (très simplifiée) est la suivante :
      1. Initialiser tous les pseudo-qubits à 0.
      2. Appliquer une porte Hadamard pseudo (randomisation).
      3. Appliquer l'oracle :
         - Pour une fonction constante, ne rien changer.
         - Pour une fonction équilibrée, inverser l'état d'un pseudo-qubit choisi aléatoirement.
      4. Appliquer à nouveau une porte Hadamard pseudo.
      5. Mesurer l'état ; idéalement, pour une fonction constante, le résultat devrait être "000...0".
    """
    init_pseudo_qubits(n)
    apply_hadamard_pseudo()
    if oracle_type == 'balanced':
        idx = random.randint(0, n-1)
        pseudo_qubit_states[idx] = 1 - pseudo_qubit_states[idx]
    apply_hadamard_pseudo()
    measured = measure_probabilistic()
    print("Deutsch-Jozsa mesure :", measured)
    if measured == "0" * n:
        return "Constant"
    else:
        return "Balanced"

# =============================================================================
# 8. Fonction principale regroupant toutes les parties
# =============================================================================
def main():
    print("=== Définition du pseudo-qubit ===")
    print("Dans ce modèle, un pseudo-qubit est simulé par une boucle infinie (dans un thread),")
    print("où l'état alterne entre 0 et 1 à une période aléatoire.")
    print("L'état global d'un système de n pseudo-qubits est représenté par une liste de n valeurs (0 ou 1).\n")
    
    # ----- Test 1 : Simulation de pseudo-qubits avec interactions (mode 16 qubits) -----
    n = 16  # Par exemple, simuler 16 pseudo-qubits (on peut tester jusqu'à 32 ou 64)
    print(f"=== Démarrage de la simulation des pseudo-qubits (mode {n} qubits) ===")
    print(f"Mémoire estimée : {memory_usage_loops(n)} octets")
    start_pseudo_quantum(n)
    try:
        for _ in range(10):
            current_state = measure_probabilistic()
            print("État actuel des pseudo-qubits :", current_state)
    except KeyboardInterrupt:
        pass
    stop_pseudo_quantum()
    print("\nSimulation des pseudo-qubits terminée.\n")
    
    # ----- Test 2 : Simulation de l'algorithme pseudo-Grover sur 3 pseudo-qubits -----
    print("=== Simulation de l'algorithme pseudo-Grover (3 pseudo-qubits) ===")
    n = 3
    start_pseudo_quantum(n)
    target_state = "101"
    print("État cible :", target_state)
    final_state = pseudo_grover(target_state, iterations=5)
    print("État final mesuré :", final_state)
    stop_pseudo_quantum()
    
    # ----- Test 3 : Simulation de l'algorithme Deutsch-Jozsa sur 4 pseudo-qubits -----
    print("\n=== Simulation de l'algorithme Deutsch-Jozsa (4 pseudo-qubits) ===")
    result_constant = simulate_deutsch_jozsa(4, oracle_type='constant')
    print("Résultat pour oracle constant :", result_constant)
    result_balanced = simulate_deutsch_jozsa(4, oracle_type='balanced')
    print("Résultat pour oracle équilibré :", result_balanced)
    
    # ----- Test 4 : Simulation des portes CNOT et Toffoli sur 4 pseudo-qubits -----
    print("\n=== Simulation des portes CNOT et Toffoli sur 4 pseudo-qubits ===")
    init_pseudo_qubits(4)
    # État initial connu : par exemple, [1, 0, 1, 0]
    pseudo_qubit_states[:] = [1, 0, 1, 0]
    print("État initial :", "".join(str(x) for x in pseudo_qubit_states))
    # Appliquer une porte CNOT avec contrôle sur le bit 0 et cible le bit 1
    apply_CNOT(0, 1)
    print("Après CNOT (control=0, target=1) :", "".join(str(x) for x in pseudo_qubit_states))
    # Appliquer une porte Toffoli avec contrôle sur les bits 0 et 2 et cible le bit 3
    apply_Toffoli(0, 2, 3)
    print("Après Toffoli (control1=0, control2=2, target=3) :", "".join(str(x) for x in pseudo_qubit_states))
    
    # ----- Test 5 : Simulation continue des pseudo-qubits avec interactions (mode 8 qubits) -----
    print("\n=== Simulation continue des pseudo-qubits (mode 8 qubits) ===")
    n = 8
    start_pseudo_quantum(n)
    try:
        for _ in range(10):
            current_state = measure_probabilistic()
            print("État des pseudo-qubits :", current_state)
    except KeyboardInterrupt:
        pass
    stop_pseudo_quantum()
    print("Simulation arrêtée.")

if __name__ == "__main__":
    main()
