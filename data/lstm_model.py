import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.backend import clear_session
from config import WINDOW_SIZE

def prepare_lstm_data(df, features):
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[features])
    X, y = [], []
    for i in range(WINDOW_SIZE, len(df_scaled)):
        X.append(df_scaled[i-WINDOW_SIZE:i])
        y.append(df_scaled[i, 0])
    return np.array(X), np.array(y), scaler

def train_lstm_model(X, y):
    clear_session()
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=10, batch_size=32, verbose=0)
    return model
