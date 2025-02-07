import threading
import time
import random

# -------------------------------------------------------------------
# Configuration : nombre de pseudo-qubits à simuler
# -------------------------------------------------------------------
NUM_QUBITS = 5  # Tu peux augmenter ce nombre pour simuler plus de qubits

# Liste globale qui contiendra l'état (0 ou 1) de chaque pseudo-qubit
qubit_states = [0] * NUM_QUBITS

# -------------------------------------------------------------------
# Fonction qui simule le comportement d'un pseudo-qubit
# -------------------------------------------------------------------
def pseudo_qubit_loop(index, min_freq=1.0, max_freq=5.0):
    """
    Simule un pseudo-qubit qui oscille entre 0 et 1.
    
    Paramètres :
      - index : l'indice du pseudo-qubit dans la liste globale
      - min_freq, max_freq : plage (en Hz) pour la fréquence d'oscillation
    Chaque pseudo-qubit démarre avec un délai initial aléatoire pour simuler
    un déphasage entre les boucles, puis il alterne son état (toggle).
    """
    # Choisir une fréquence aléatoire pour ce pseudo-qubit (en Hz)
    freq = random.uniform(min_freq, max_freq)
    period = 1.0 / freq  # période d'oscillation en secondes
    
    # Démarrage décalé : attendre un délai initial aléatoire compris entre 0 et period
    initial_delay = random.uniform(0, period)
    time.sleep(initial_delay)
    
    # Boucle infinie pour simuler le fonctionnement continu du pseudo-qubit
    while True:
        # Inverser l'état : si c'était 0, passe à 1, et vice-versa
        qubit_states[index] = 1 - qubit_states[index]
        # Attendre la durée de la période pour le prochain basculement
        time.sleep(period)

# -------------------------------------------------------------------
# Fonction pour lancer la simulation du pseudo "ordinateur quantique"
# -------------------------------------------------------------------
def start_pseudo_quantum_computer():
    """
    Démarre un thread pour chaque pseudo-qubit et affiche en continu
    l'état global du système, simulant ainsi une "mesure" instantanée.
    """
    threads = []
    for i in range(NUM_QUBITS):
        # Créer un thread pour le pseudo-qubit i
        t = threading.Thread(target=pseudo_qubit_loop, args=(i,), daemon=True)
        t.start()
        threads.append(t)
    
    print("Simulation démarrée : appuyez sur Ctrl+C pour arrêter.\n")
    try:
        while True:
            # "Mesurer" l'état global en lisant simultanément tous les pseudo-qubits
            current_state = ''.join(str(state) for state in qubit_states)
            print("État des pseudo-qubits :", current_state)
            # On rafraîchit l'affichage toutes les 100 ms
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nSimulation arrêtée.")

# -------------------------------------------------------------------
# Programme principal
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Simulation d'un pseudo ordinateur quantique par boucles ===")
    print("Chaque thread représente un pseudo-qubit oscillant entre 0 et 1 à une fréquence aléatoire.")
    print("Une mesure consiste à lire simultanément l'état de tous ces pseudo-qubits.")
    print("Cela simule, de façon simplifiée, la superposition d'états d'un qubit réel.\n")
    start_pseudo_quantum_computer()
