# Player vs Bot American Checkers Game

<table>
  <tr>
    <td style="padding-right: 20px;">
      <img src="/assets/Screenshot%202023-11-16%20at%2022.26.43.png" width="500">
    </td>
    <td>
      <img src="/assets/Screenshot%202023-11-16%20at%2022.29.17.png" width="500">
    </td>
  </tr>
</table>

## Overview

Welcome to my Player vs Computer American Checkers game! This project demonstrates my software engineering and machine learning skills. The game incorporates various technologies, data manipulation, and artificial intelligence to create an engaging and challenging experience.

## Data Manipulation

### Dataset Acquisition
I acquired a dataset of 20,000+ American Checkers games, manipulated it to extract move records, and analyzed board states, resulting in 1 million+ samples. 

### Feature Extraction
Using a 2D matrix representation and leveraging an external library, I parsed and analyzed each game state to extract 11 features. \
These processes occurred in the "data_manipulation" folder.

## Agent Creation

### Model Testing
In the "agent_creation" folder, Jupyter Notebook was used to test various neural network and machine learning models on the dataset to identify the best-performing model.

### Model Deployment
The chosen model was integrated into the "checkers_game" folder, responsible for executing all game logic and gameplay, including the user interface and the Checkers bot's move handler.

### Advanced AI with Minimax Algorithm
In addition to the neural network model, I implemented a Minimax algorithm with ⍺-β pruning, that allows the Checkers bot to explore move trees up to depth 5 in hard mode, providing a formidable opponent.

## Technologies Used

Throughout the project, I utilized various technologies, including:

- numpy: For numerical operations.
- PyTorch: For implementing and training neural network models.
- scikit-learn: For machine learning algorithms and data manipulation.
- Jupyter Notebook: Facilitating model testing and analysis.
- pandas: For data manipulation and analysis.
- pygame: Enabling the creation of the graphical user interface. 
  
And more...

## How to run the code
Make sure you have python installed on your machine. Then, install requirements:
```
pip install pygame numpy scikit-learn torch joblib
```

### Run the game
From within the Checkers directory, run the following command (might take approx. 30 seconds to load on the first time)
```
python checkers_game/main.py
```

\
<img src="/assets/Screenshot%202023-11-16%20at%2022.29.38.png" style="display: block; margin: 0 auto;" width="700">

---

## Conclusion

This Checkers game showcases my skills in software engineering, data manipulation, and machine learning. The fusion of advanced AI techniques, extensive dataset analysis, and a well-designed user interface highlights my ability to deliver a comprehensive software solution.

Feel free to explore the codebase, and reach out if you have any questions or feedback!
