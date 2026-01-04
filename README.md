# Proiect pentru IA4

### **Team Members**
* **Murgu Andrei**
* **Berea George-Alexandru**

## Project Overview
5NoptiInStudentie is a horror-comedy survival game that reimagines the tension of Five Nights at Freddy's (FNAF) within the chaotic setting of a university dorm.

Players step into the shoes of a student assigned to a filthy, infestation-prone room left behind by a negligent predecessor. The objective is to survive the nights against a relentless "Big Bug" and its swarming army of smaller pests. Staying true to the FNAF formula, gameplay revolves around high-stakes surveillance and strategic resource management. Players must utilize a security camera system to track the Big Bug's movement through the building while rationing a limited supply of bug spray to keep the room clear.

**GitHub Repository:** [https://github.com/viktorunix/5NoptiInStudentie/](https://github.com/viktorunix/5NoptiInStudentie/)
We higly recommend visiting the repository to view the detail commit history, issue tracking, and the practical application of the concepts described below.

---
## Development Methodology & Concepts
We aimed to simulate a professional development environment by utilizing the following as many concept presented in the course:

### 1. Project Management 
Instead of using simple "to-do" lists we utilized **Github Issues** as our primary project management tool where we tracked bugs, features requests and feedback from our game-testers

### 2. Planning with Milestones
To manage the development lifecycle effectively, we established self-imposed deadlines groupt into **Milestones**. This helped us break down the project implementation into manageable stages ("Alpha", "Beta", "Release")

### 3. Containerization (Docker)
We attepted to containerize the application to ensure consistency across environments.
* **The Challenge:** Since the game requires a display output, a standard Docker container cannot render graphics easily.
* **The Solution:** We created a script that builds the images and forwards the output to an **X Server**
* **Keep in mind:** Due to the relience on the X server, this feature is strictly compatible with **Linux** systems. We tried this to experiment and learn more about **Docker Containers**.

### 4. CI/CD with Github Actions
We implemented a CI/CD pipeline with two workflows that are triggered on each commit:

* **Linter (Code Quality):** Automated checks to enforce certain coding standards so we can understand eachothers code.
* **Windows Build (Automated)**: A workflow that uses `PyInstaller` to automatically comple the Python source code into a standalone `.exe` file

### 5. Libraries Used
* **Pygame:** Core engine for rendering graphics, input handling.
* **OpenCV:** Used for working with video files.
* **PyInstaller**: Used for compiling the source code

---
## Instalation

Please visit [**Releases Page**](https://github.com/viktorunix/5NoptiInStudentie/tags) to download the latest version suitable for your OS.

### Option A: UNIX-LIKE Systems (MacOS/Linux/BSD)
1. Clone the repository.
2. Run the launch script:
	```bash
	./launch.sh 
	```

### Option B: LINUX + Docker
1. Clone the repository.
2. Run the local script that builds and runs the images
	```bash
	./local.sh
	```

### Option C: WINDOWS
1. Download the latest `.exe` from the link above

--- 
## Technical Challanges

### 1. Responsive GUI Scaling
**The Problem**: Pygame lacks built-in responsive UI tools. Static pixel coordinates caused the interface layout to break on different monitor resolutions.
**The Solution**: We made every element's position scaled to the screen resolution and for scaling we used a resolution as reference and scaled based on the ratio between the player's resolution and the reference.

### 2. Game Balancing
**The Problem**: Initial iterations were either too difficult or too easy, disrupting the game balance.
**The Solution:** We contacted a few people to test our game, log their feedback on **Github** and tweaked the mechanics based on their input

## Contributions

### **Murgu Andrei**
* **Core GUI Framework:** Designed custom UI elements (buttons, image renderer, text) from scratch.
* **Game Logic:** Implemented enemy AI and resource management mechanics.
* **Asset Management**: Handled the integration and optimization of game assets.

### **Berea George-Alexandru**
* **Display Logic:** Implemented Fullscreen and window management.
* **Jumpscare Animation:** Handled the timing and animation logic for "Game Over" states.
* **GUI Refinement:** Assisted in fine-tuning UI scaling for visual cosistency.
