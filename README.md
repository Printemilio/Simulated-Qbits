

# Pseudo-Quantum Simulation via Asynchronous Loops

**A Quantum-Inspired Simulation on Classical Hardware**

This repository implements a novel approach to simulating quantum-inspired algorithms using asynchronous loops (threads) to model *pseudo-qubits*. Unlike traditional quantum simulations that require storing state vectors of size \(2^n\), our method represents a system of \(n\) pseudo-qubits as an \(n\)-element list of binary values. This results in **linear memory usage** and minimal CPU/GPU overhead, making it possible to simulate complex quantum-inspired algorithms on a standard PC.

## Overview

Quantum computers exploit phenomena such as superposition and interference to potentially solve certain problems much faster than classical computers. However, simulating quantum systems on classical hardware is usually very expensive due to the exponential growth of the state space. Our approach bypasses this issue by:
- Modeling each qubit as a simple binary value updated asynchronously by its own thread.
- Implementing quantum-inspired algorithms (e.g., Grover's search and Deutsch-Jozsa) using a candidate amplification mechanism.
- Demonstrating the method through a maze (labyrinth) solver where many candidate paths are evaluated in parallel.

## Key Features

- **Pseudo-Qubit Model:** Each pseudo-qubit is simulated as an independent thread that randomly flips its state (0 or 1) at variable time intervals.
- **Linear Memory Usage:** The system state is maintained as an \(n\)-element list, scaling linearly with the number of pseudo-qubits.
- **Quantum-Inspired Algorithms:** Implementation of a Grover-like search for optimizing paths in a labyrinth and a simplified Deutsch-Jozsa algorithm.
- **Efficient Optimization:** The approach has been tested on labyrinths (e.g., 20×20 and 40×40), showing rapid convergence with thousands of candidates while consuming minimal resources.
- **Scalability:** Demonstrated scalability up to 40 pseudo-qubits (and potentially more), making it a lightweight yet powerful simulation.

## Repository Contents

- **`main.py`**  
  The Python implementation of the pseudo-quantum simulation, including:
  - Labyrinth generation.
  - Pseudo-qubit simulation using asynchronous loops.
  - Quantum-inspired algorithms (pseudo-Grover and pseudo-Deutsch-Jozsa).
  
- **`paper.tex`** (and compiled `paper.pdf`)  
  A scientific paper describing the methodology, mathematical analysis, performance proofs, and experimental results of our approach.

- **`README.md`**  
  This file.

## Requirements

- Python 3.x
- Standard Python libraries: `threading`, `time`, `random`
- For compiling the paper: A LaTeX distribution (e.g., TeX Live, MikTeX)

## How to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/pseudo-quantum-simulation.git
   cd pseudo-quantum-simulation
   ```

2. **Run the Simulation:**
   ```bash
   python main.py
   ```
   This command will run the pseudo-quantum simulation, generate a labyrinth, and execute the quantum-inspired search algorithms. The output will be printed to the terminal.

3. **Compile the Paper (Optional):**
   To compile the paper from the LaTeX source:
   ```bash
   pdflatex paper.tex
   ```
   This will produce a `paper.pdf` file detailing the theoretical background, performance analysis, and experimental results.

## Performance and Experimental Results

Our approach demonstrates:
- **Linear memory scaling:** For \(n\) pseudo-qubits, the memory usage is approximately \(O(n)\), as opposed to the \(O(2^n)\) cost of full state-vector simulations.
- **Rapid convergence:** In our experiments, a 20×20 maze was solved in 98 iterations using 1000 candidate paths. With fewer candidates (e.g., 3), convergence was slower (52 iterations), highlighting the importance of candidate diversity.
- **Minimal resource consumption:** The simulation runs efficiently on standard hardware without significant increases in CPU, memory, or GPU usage.

Refer to the included paper for detailed mathematical proofs comparing our approach to classical simulation methods.

## Future Work

This work opens up several exciting avenues:
- Extending the simulation to larger labyrinths (e.g., 40×40, 100×100) and testing scalability.
- Applying the pseudo-quantum model to other optimization problems, such as the Traveling Salesman Problem or graph coloring.
- Developing quantum-inspired neural networks and hybrid optimization algorithms that leverage the lightweight pseudo-qubit model.
- Publishing further research on the potential of quantum-inspired algorithms on classical hardware.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests for improvements, new features, or experimental results.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

This project is inspired by foundational works in quantum computing and classical computational complexity:
- Nielsen, M. A. & Chuang, I. L. *Quantum Computation and Quantum Information*.
- Grover, L. K. "A fast quantum mechanical algorithm for database search."
- Deutsch, D. & Jozsa, R. "Rapid solution of problems by quantum computation."
- Arora, S. & Barak, B. *Computational Complexity: A Modern Approach*.

