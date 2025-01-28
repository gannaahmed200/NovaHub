# 3D Anatomy Organs Puzzle Game: Heart Edition

## Project Overview

This project involves the development of a 3D puzzle game where users must assemble the human heart by flipping and rotating parts in 3D space. The goal is to reconstruct the heart by manipulating its 3D pieces, similar to the Tetris game mechanics. The game is developed using Unity and Blender.

![Heart Puzzle Preview 1](https://github.com/user-attachments/assets/28015bc6-3f74-490a-bfe6-a5c53b0bd70b)
![Heart Puzzle Preview 2](https://github.com/user-attachments/assets/6fce7ad3-69ca-4e41-9552-6f9f8a594564)
![Heart Puzzle Preview 3](https://github.com/user-attachments/assets/3e743171-b6dc-4146-b9c8-428d6937c717)
![Heart Puzzle Preview 4](https://github.com/user-attachments/assets/ceb69cbc-5b21-4792-8b42-eca2bcdef9c3)
![Heart Puzzle Preview 5](https://github.com/user-attachments/assets/46aa35cb-7db3-4da8-bc1b-d0556dc6226f)

## Features

- **3D Puzzle Gameplay**: Users will randomly receive heart parts in 3D space and will need to manually assemble them by rotating and flipping the pieces.
- **Heart Organ**: The game focuses on the human heart, which is divided into 5 to 8 parts for the puzzle.
- **Interactive Controls**: Rotate and flip each part via keyboard shortcuts to place them in their correct positions.
- **3D Rendering**: Heart parts are rendered as surface models, not volume models, using Blender for 3D visualization.

## Tools and Technologies

- **Unity**: Used for game development and to handle the 3D scene, interaction, and game logic.
- **Blender**: Used for 3D visualization and creating the heart model. Ensure that the heart is a surface model before importing it into Unity.
- **C#**: Scripting language used within Unity for game logic and interaction.

## Steps to Set Up

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/3d-anatomy-organs-puzzle.git
cd 3d-anatomy-organs-puzzle
```

### 2. Install Unity

Make sure you have Unity installed. You can download it from [Unity's official website](https://unity.com/).

### 3. Import the Project into Unity

- Open Unity Hub and select "Add" to import the project folder.
- Once imported, open the project in Unity.

### 4. Import 3D Heart Model

- Use Blender to create and export 3D surface models of the heart.
- Import the heart model into Unity by dragging the `.obj` or `.fbx` files into the Unity Editor.

### 5. Set Up Scene and Game Logic

- Create the game scene in Unity, setting up the camera, lighting, and game objects.
- Implement the game logic in C# for rotating, flipping, and snapping parts together.

### 6. Run the Game

Once the setup is complete, press "Play" in Unity to test and run the game.

## How to Contribute

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Implement your changes and test thoroughly.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Special thanks to the creators of Blender and Unity for providing excellent tools for 3D modeling and game development.
