# Football Player Tracking and Heatmap Visualization

This project uses a pretrained YOLO (You Only Look Once) AI model to track players in a football game. It allows users to select a player and visualize their movement with a heatmap, showing their activity throughout the game. The system provides insights into the player's positioning, helping analyze their movements across the field.

## Features

- **Player Tracking:** Detect and track players in a football game using a YOLO model.
- **Player Selection:** Users can select a specific player for detailed tracking.
- **Movement Heatmap:** Visualize the movement of the selected player with a heatmap over time.

## Screenshots from Our Projects

### Screenshot 1:
![Image](https://github.com/user-attachments/assets/b6f61b88-9d9c-4451-859b-88398bb63b15)

### Screenshot 2:
![Image](https://github.com/user-attachments/assets/21ae4e34-461f-43ad-b5da-7eb8bf11a1dd)

### Screenshot 3:
![Image](https://github.com/user-attachments/assets/32364bf7-cd3c-42e8-9552-a77410225323)

## Requirements

- Python 3.x
- OpenCV
- PyTorch (for YOLOv5)
- NumPy
- Matplotlib (for generating and displaying the heatmap)
- Pretrained YOLO model (YOLOv5 recommended)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/football-player-tracking.git
   cd football-player-tracking
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Download the pretrained YOLOv5 model from the [YOLO website](https://github.com/ultralytics/yolov5) or use a pre-trained model and place it in the project folder, or specify its path in the script.

## Usage

1. Run the player tracking script:

   ```bash
   python track_players.py --video <path_to_video_file>
   ```

2. The script will start processing the video, detecting and tracking the players. You can then select a player to focus on.

3. Once you select a player, a heatmap will be generated, displaying their movement throughout the game.

4. The heatmap will either overlay on the video or be displayed separately, depending on your preference.

## Files and Directories

- `track_players.py`: Main script for tracking players and generating the heatmap.
- `yolo_model.py`: YOLO model loading and prediction code.
- `heatmap.py`: Code for generating and visualizing the player's movement heatmap.
- `requirements.txt`: Python dependencies for the project.
- `README.md`: Documentation for the project.

## Example

To track players and generate a heatmap for a selected player, run the following command:

```bash
python track_players.py --video football_match.mp4
```

Once the video is processed, you will be able to select a player, and their movement heatmap will be shown.

## Contributing

We welcome contributions to improve this project! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request with a description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

### Key Notes:
- **Usage Section**: Explains how to run the project.
- **File Details**: Describes the purpose of the main files.
- **Contributing**: Encourages others to contribute to the project.
