import os
import pickle

class CheckersAgent():
    def __init__(self):
        self.model = self.load_model("agent_model.pkl")
        
    def load_model(self, model_filename):
        # Get the current directory where this Python file is located
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the pickle file
        full_path = os.path.join(current_directory, model_filename)

        # Load the saved model from the pickle file
        with open(full_path, 'rb') as file:
            loaded_model = pickle.load(file)
        return loaded_model
    
    def predict(self, board_eval):
        return self.model.predict(board_eval)