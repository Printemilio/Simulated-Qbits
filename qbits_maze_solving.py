import random
import time

# =============================================================================
# 1. Génération d'un labyrinthe
# =============================================================================
def generate_labyrinth(size, free_prob=0.7):
    """
    Génère un labyrinthe de taille 'size' x 'size'.
    Chaque cellule est libre (1) avec probabilité free_prob, sinon c'est un mur (0).
    Le point de départ (0,0) est toujours libre et la sortie (size-1, size-1) est marquée par 'E'.
    """
    maze = []
    for i in range(size):
        row = []
        for j in range(size):
            # La probabilité qu'une cellule soit libre
            if random.random() < free_prob:
                row.append(1)
            else:
                row.append(0)
        maze.append(row)
    maze[0][0] = 1            # Assurer que le départ est libre
    maze[size-1][size-1] = "E"  # Placer la sortie en bas à droite
    return maze

def print_labyrinth(maze):
    for row in maze:
        print(" ".join(str(x) for x in row))
    print()

# =============================================================================
# 2. Fonctions de déplacement et de validité des mouvements
# =============================================================================
def valid_moves(pos, maze):
    """
    Retourne la liste des positions accessibles à partir de pos dans le labyrinthe.
    Les mouvements possibles sont : RIGHT, LEFT, DOWN, UP.
    """
    x, y = pos
    moves = []
    directions = {"RIGHT": (1, 0), "LEFT": (-1, 0), "DOWN": (0, 1), "UP": (0, -1)}
    for d, (dx, dy) in directions.items():
        new_x = x + dx
        new_y = y + dy
        # Vérifier les limites du labyrinthe
        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
            if maze[new_y][new_x] == 1 or maze[new_y][new_x] == "E":
                moves.append((new_x, new_y))
    return moves

def move_candidate(pos, maze):
    """
    Déplace un candidat de manière aléatoire parmi les mouvements valides.
    Si aucun mouvement n'est possible, retourne la même position.
    """
    moves = valid_moves(pos, maze)
    if moves:
        return random.choice(moves)
    return pos

# =============================================================================
# 3. Fonction d'évaluation : distance de Manhattan
# =============================================================================
def manhattan_distance(pos, exit_pos):
    """
    Calcule la distance de Manhattan entre pos et exit_pos.
    """
    return abs(pos[0] - exit_pos[0]) + abs(pos[1] - exit_pos[1])

# =============================================================================
# 4. Simulation de la recherche de sortie en superposition (inspirée de Grover)
# =============================================================================
def find_exit_superposition(maze, start_pos, exit_pos, num_candidates=40, iterations=20):
    """
    Simule la recherche de la sortie dans le labyrinthe en parallèle
    avec un ensemble de candidats (superposition de chemins).
    
    - maze       : le labyrinthe (liste de listes)
    - start_pos  : position de départ (tuple, par exemple (0,0))
    - exit_pos   : position de la sortie (tuple, par exemple (size-1, size-1))
    - num_candidates : nombre de candidats (pseudo-qubits) dans la superposition
    - iterations : nombre maximum d'itérations de mise à jour/amplification.
    
    À chaque itération, tous les candidats se déplacent de manière aléatoire.
    Ensuite, on évalue leur "proximité" à la sortie par la distance de Manhattan.
    Les candidats qui sont plus proches que la moyenne sont amplifiés (répliqués)
    pour simuler l'amplification d'amplitude.
    """
    # Initialiser tous les candidats au point de départ
    candidates = [start_pos for _ in range(num_candidates)]
    
    for it in range(iterations):
        # Chaque candidat se déplace de manière aléatoire
        candidates = [move_candidate(pos, maze) for pos in candidates]
        
        # Vérifier si un candidat a atteint la sortie
        for pos in candidates:
            if pos == exit_pos:
                print(f"🎉 Sortie trouvée en itération {it+1} ! Position finale : {pos}")
                return pos, it+1, candidates
        
        # Calculer la distance de chaque candidat par rapport à la sortie
        distances = [manhattan_distance(pos, exit_pos) for pos in candidates]
        avg_distance = sum(distances) / len(distances)
        
        # Amplification : on garde et réplique les candidats dont la distance est inférieure ou égale à la moyenne
        new_candidates = [pos for pos, d in zip(candidates, distances) if d <= avg_distance]
        # Pour maintenir le nombre de candidats, on réplique ceux qui sont les meilleurs
        if len(new_candidates) < num_candidates:
            factor = (num_candidates // len(new_candidates)) + 1
            new_candidates = (new_candidates * factor)[:num_candidates]
        candidates = new_candidates
        
        print(f"Itération {it+1} : {candidates[:5]} ... (moyenne distance = {avg_distance:.2f})")
        time.sleep(0.3)
    
    print("⛔ Sortie non trouvée après", iterations, "itérations.")
    return None, iterations, candidates

# =============================================================================
# 5. Programme principal
# =============================================================================
def main():
    # Définir la taille du labyrinthe (par exemple 10x10)
    maze_size = 10
    maze = generate_labyrinth(maze_size, free_prob=0.75)
    
    print("=== Labyrinthe généré ===")
    print_labyrinth(maze)
    
    start_pos = (0, 0)
    exit_pos = (maze_size - 1, maze_size - 1)  # Placer la sortie en bas à droite
    
    print(f"Départ : {start_pos}, Sortie : {exit_pos}\n")
    
    # Lancer la recherche avec superposition
    print("🔍 Recherche de la sortie avec superposition de chemins...")
    exit_found, iters, final_candidates = find_exit_superposition(
        maze, start_pos, exit_pos, num_candidates=40, iterations=20
    )
    
    if exit_found:
        print(f"Sortie trouvée en {iters} itérations.")
    else:
        print("Sortie non trouvée. Vous pouvez réessayer en augmentant le nombre d'itérations ou en modifiant le labyrinthe.")
    
    # Afficher quelques candidats finaux
    print("Quelques candidats finaux :", final_candidates[:10])

if __name__ == "__main__":
    main()
