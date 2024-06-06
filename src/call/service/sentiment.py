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
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=100)
    stft = np.abs(librosa.stft(y))
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    mel = librosa.feature.melspectrogram(y=y, sr=sr)  # fmax=fmax_mel
    n_bands = 4

    contrast = librosa.feature.spectral_contrast(
        S=stft, sr=sr, n_bands=n_bands
    )  # , fmin=fmin
    features = np.concatenate(
        (
            np.mean(mfccs, axis=1),
            np.mean(chroma, axis=1),
            np.mean(mel, axis=1),
            np.mean(contrast, axis=1),
        )
    )
    return features


def predict_emotion(
    uow: AbstractUnitOfWork, file_path: str, call_detail_id: UUID
):
    with uow:
        logging.info("Initiating prediction")
        feature = np.expand_dims(extract_features(file_path), axis=0)
        logging.info(f"feature:{feature}")

        prediction = model.predict(feature)
        logging.info(f"prediction: {prediction}")

        if prediction > 0.5:
            confidence_scores = prediction
        else:
            confidence_scores = 1 - prediction

        logging.info(f"confidence: {confidence_scores}")

        predicted_labels = (prediction > 0.5).astype(int)

        # predicted_label = label_encoder.inverse_transform(
        #     np.argmax(prediction, axis=1)
        # )

        predicted_label = label_encoder.inverse_transform(predicted_labels)

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
