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
        full_path = CheckersAgent.get_file_path(model_filename)
        model = torch.load(full_path)
        return model

    @staticmethod
    def load_scaler(scaler_filename):
        full_path = CheckersAgent.get_file_path(scaler_filename)
        with open(full_path, 'rb') as file:
            scaler = joblib.load(file)
        return scaler

    @staticmethod
    def get_file_path(filename):
        """
        Get the full path to the file based on the provided filename.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_directory, filename)
        return full_path

    def predict(self, board_eval):
        board_eval = self.scale_first_feature_value(board_eval)
        board_eval = torch.tensor(board_eval, dtype=torch.float32)
        with torch.no_grad():
            prediction = self.model(board_eval)
        # Convert the prediction tensor to a numerical value
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
