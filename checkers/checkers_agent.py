import os
import joblib
import warnings
import numpy as np
import torch


class CheckersAgent:
    def __init__(self):
        self.model = self.load_model("agent_model.pth")
        self.scaler = self.load_scaler("scaler.pkl")

    @staticmethod
    def load_model(model_filename):
        # Get the current directory where this Python file is located
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the pickle file
        full_path = os.path.join(current_directory, model_filename)

        model = torch.load(full_path)
        return model

    @staticmethod
    def load_scaler(scaler_filename):
        # Get the current directory where this Python file is located
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the pickle file
        full_path = os.path.join(current_directory, scaler_filename)

        with open(full_path, 'rb') as file:
            scaler = joblib.load(file)
        return scaler

    def predict(self, board_eval):
        board_eval = self.scale_first_feature_value(board_eval)
        board_eval = torch.tensor(board_eval, dtype=torch.float32)

        with torch.no_grad():
            prediction = self.model(board_eval)

        # Convert the prediction tensor to a numerical value (if needed)
        predicted_value = prediction.item()
        return predicted_value

    def scale_first_feature_value(self, board_eval):
        board_eval = list(board_eval)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            new_feature_value = self.scaler.transform(board_eval[0].reshape(-1, 1))[0][0]
            board_eval[0] = new_feature_value
            board_eval = np.array(board_eval).reshape(1, -1)
        
        return board_eval
