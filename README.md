# AutoNav

**QMUL Final Year Project**  
**Grade Achieved:** First Class

AutoNav is a two-part project consisting of a **software application** and a **robot prototype** designed to autonomously navigate between two chosen points. The system allows users to explore maze-solving algorithms virtually and see them executed physically with a robot.  

The project is implemented using **Python** for the application and **Arduino** for the robot.

---

## Features

### Maze Application

**Primary Functionalities**
- **Main Screen:** Central interface to generate, solve, and test mazes.
- **Maze Generation:** Users can input dimensions to generate random mazes.
- **Algorithms:** Supports DFS, BFS, Dijkstra, and A* for solving mazes.
- **Time Tracking:** Measures solution time, total steps, and shortest path steps.

**Secondary Functionalities**
- **Save & Load Mazes:** Store generated mazes for future testing or demonstration.
- **Results Management:** View, compare, and save algorithm performance results.

**Non-Functional Requirements**
- **Portability:** Runs on Windows, macOS, and Linux.
- **Efficiency:** Optimized storage for maze and result files.
- **Usability:** Intuitive interface for easy learning and experimentation.

---

### Maze-Solving Robot

**Primary Functionalities**
- **Movement Control:** Arduino-based control for precise navigation.
- **Sensors:** Detect line-following cues using reflected light sensors.
- **Power Supply:** Operates reliably on standard batteries.
- **Maze Algorithm:** Implements the Left-Hand-on-the-Wall Rule (LSRB) to traverse mazes.

**Secondary Functionalities**
- **Object Detection:** Optional ultrasonic sensors for obstacle avoidance.
- **External Maze Solving:** Can follow algorithm instructions calculated externally.

**Non-Functional Requirements**
- **Portability & Reliability:** Robot can be programmed and tested on major OSs and reliably complete maze tasks.
- **Usability & Learnability:** Designed to be intuitive and simple for anyone to operate.
