import logging
import os
from uuid import UUID

import joblib
import librosa
import numpy as np
from tensorflow.keras.saving import load_model

from src.call.domain.interface import AbstractUnitOfWork


def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    stft = np.abs(librosa.stft(y))
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    n_bands = 4

    contrast = librosa.feature.spectral_contrast(
        S=stft, sr=sr, n_bands=n_bands
    )
    features = np.concatenate(
        (
            np.mean(mfccs, axis=1),
            np.mean(chroma, axis=1),
            np.mean(mel, axis=1),
            np.mean(contrast, axis=1),
        )
    )
    return features


def load_data(data_dir):
    labels = []
    features = []
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".wav"):
                    file_path = os.path.join(folder_path, file_name)
                    feature = extract_features(file_path)
                    features.append(feature)
                    labels.append(file_name.split(".")[0])
    return np.array(features), np.array(labels)


def predict_emotion(
    uow: AbstractUnitOfWork, file_path: str, call_detail_id: UUID
):
    with uow:
        logging.info("Initiating prediction")
        feature = np.expand_dims(extract_features(file_path), axis=0)
        logging.info(f"feature:{feature}")
        prediction = model.predict(feature)
        logging.info(f"prediction: {prediction}")
        confidence_scores = np.max(prediction, axis=1)
        logging.info(f"confidence: {confidence_scores}")
        predicted_label = label_encoder.inverse_transform(
            np.argmax(prediction, axis=1)
        )

        ## update call detail sentiment
        confidence_score_value = confidence_scores[0]
        predicted_label_value = predicted_label[0]

        logging.info(
            f"category:{predicted_label_value}, confidence:{confidence_score_value}"
        )
        if predicted_label_value == "negative":
            confidence_score_value *= -1

        uow.call_detail.update_sentiment(
            call_detail_id, float(confidence_score_value)
        )
        uow.commit()

        # return predicted_label[0], confidence_scores
        # TODO: need to update call detail


label_encoder = joblib.load("assets/models/label_encoder.pkl")
model = load_model("assets/models/sentiment.keras")

# if __name__ == "__main__":
#     file_path = 'speech emotion recognition/files/00026029e0--64991b6eef1fe70609d48edc/joyfully.wav'
#     predicted_emotion = predict_emotion(file_path)
#     print(f"Predicted Emotion: {predicted_emotion}")
#
