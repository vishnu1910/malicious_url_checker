import numpy as np
from keras import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Embedding, SpatialDropout1D, Conv1D, MaxPooling1D, LSTM, Dense, Bidirectional
from sklearn.model_selection import train_test_split
from keras.models import Sequential

NB_LSTM_CELLS = 256
NB_DENSE_CELLS = 256
EMBEDDING_SIZE = 100

def make_cnn_lstm_model(num_input_tokens, max_len): #function to create the DL model 
    model = Sequential()
    model.add(Embedding(input_dim=num_input_tokens, input_length=max_len, output_dim=EMBEDDING_SIZE))
    model.add(SpatialDropout1D(0.2))
    model.add(Conv1D(filters=256, kernel_size=5, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=4))
    model.add(LSTM(NB_LSTM_CELLS))
    model.add(Dense(units=2, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


class cnnlstmpred(object):
    model_name = 'cnn-lstm'

    def __init__(self):
        self.model = None
        self.num_input_tokens = None
        self.idx2char = None
        self.char2idx = None   
        self.max_url_seq_length = None

    @staticmethod
    def get_config_file_path(model_dir_path):
        return model_dir_path + '/' + cnnlstmpred.model_name + '-config.npy'

    @staticmethod
    def get_weight_file_path(model_dir_path):
        return model_dir_path + '/' + cnnlstmpred.model_name + '-weights.h5'

    def load_model(self, model_dir_path): # to load a saved model
        config_file_path = self.get_config_file_path(model_dir_path)
        weight_file_path = self.get_weight_file_path(model_dir_path)

        config = np.load(config_file_path).item()
        self.num_input_tokens = config['num_input_tokens']
        self.max_url_seq_length = config['max_url_seq_length']
        self.idx2char = config['idx2char']
        self.char2idx = config['char2idx']

        self.model = make_cnn_lstm_model(self.num_input_tokens, self.max_url_seq_length)
        self.model.load_weights(weight_file_path)

    def predict(self, url): #function which uses to model to predict if the given url is malicious or not
        data_size = 1
        X = np.zeros(shape=(data_size, self.max_url_seq_length))
        for idx, c in enumerate(url):
            if c in self.char2idx:
                X[0, idx] = self.char2idx[c]
        predicted = self.model.predict(X)[0]
        predicted_label = np.argmax(predicted)
        return predicted_label

    def extract_training_data(self, url_data): # for extracting the training data
        data_size = url_data.shape[0]
        X = np.zeros(shape=(data_size, self.max_url_seq_length))
        Y = np.zeros(shape=(data_size, 2))
        for i in range(data_size):
            url = url_data['text'][i]
            label = url_data['label'][i]
            for idx, c in enumerate(url):
                X[i, idx] = self.char2idx[c]
            Y[i, label] = 1
        return X, Y

    def fit(self, text_model, url_data, model_dir_path, batch_size=None, epochs=None,test_size=None, random_state=None): #training
        #deciding the values of various constants
        if batch_size is None:
            batch_size = 64
        if epochs is None:
            epochs = 50
        if test_size is None:
            test_size = 0.2
        if random_state is None:
            random_state = 42

        self.num_input_tokens = text_model['num_input_tokens']
        self.char2idx = text_model['char2idx']
        self.idx2char = text_model['idx2char']
        self.max_url_seq_length = text_model['max_url_seq_length']

        np.save(self.get_config_file_path(model_dir_path), text_model)

        weight_file_path = self.get_weight_file_path(model_dir_path)

        checkpoint = ModelCheckpoint(weight_file_path)

        X, Y = self.extract_training_data(url_data) 

        Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=test_size, random_state=random_state) #splitting dataset into train and test for training

        self.model = make_cnn_lstm_model(self.num_input_tokens, self.max_url_seq_length)# Calling the make model function

        history = self.model.fit(Xtrain, Ytrain, batch_size=batch_size, epochs=epochs, verbose=1,validation_data=(Xtest, Ytest), callbacks=[checkpoint])#training the model

        self.model.save_weights(weight_file_path) #saving the weights of the model to be used later

        np.save(model_dir_path + '/' + cnnlstmpred.model_name + '-history.npy', history.history)#saving the model to be used later

        return history


def make_bidirectional_lstm_model(num_input_tokens, max_len):# creating bidirectional lstm model
    model = Sequential()
    model.add(Embedding(input_dim=num_input_tokens, output_dim=EMBEDDING_SIZE, input_length=max_len))
    model.add(SpatialDropout1D(0.2))
    model.add(Bidirectional(LSTM(units=64, dropout=0.2, recurrent_dropout=0.2, input_shape=(max_len, EMBEDDING_SIZE))))
    model.add(Dense(2, activation='softmax'))

    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


class lstmbidrpred(object):
    model_name = 'bidirectional-lstm'

    def __init__(self):
        self.model = None
        self.num_input_tokens = None
        self.idx2char = None
        self.char2idx = None
        self.max_url_seq_length = None

    @staticmethod
    def get_config_file_path(model_dir_path):
        return model_dir_path + '/' + lstmbidrpred.model_name + '-config.npy'

    @staticmethod
    def get_weight_file_path(model_dir_path):
        return model_dir_path + '/' + lstmbidrpred.model_name + '-weights.h5'

    def load_model(self, model_dir_path):  # to load a saved model
        config_file_path = self.get_config_file_path(model_dir_path)
        weight_file_path = self.get_weight_file_path(model_dir_path)

        config = np.load(config_file_path).item()
        self.num_input_tokens = config['num_input_tokens']
        self.max_url_seq_length = config['max_url_seq_length']
        self.idx2char = config['idx2char']
        self.char2idx = config['char2idx']

        self.model = make_bidirectional_lstm_model(self.num_input_tokens, self.max_url_seq_length)
        self.model.load_weights(weight_file_path)

    def predict(self, url): #function which uses to model to predict if the given url is malicious or not
        data_size = 1
        X = np.zeros(shape=(data_size, self.max_url_seq_length))
        for idx, c in enumerate(url):
            if c in self.char2idx:
                X[0, idx] = self.char2idx[c]
        predicted = self.model.predict(X)[0]
        predicted_label = np.argmax(predicted)
        return predicted_label

    def extract_training_data(self, url_data): # for extracting the training data
        data_size = url_data.shape[0]
        X = np.zeros(shape=(data_size, self.max_url_seq_length))
        Y = np.zeros(shape=(data_size, 2))
        for i in range(data_size):
            url = url_data['text'][i]
            label = url_data['label'][i]
            for idx, c in enumerate(url):
                X[i, idx] = self.char2idx[c]
            Y[i, label] = 1

        return X, Y

    def fit(self, text_model, url_data, model_dir_path, batch_size=None, epochs=None,test_size=None, random_state=None): #training the model
        if batch_size is None:
            batch_size = 64
        if epochs is None:
            epochs = 30
        if test_size is None:
            test_size = 0.2
        if random_state is None:
            random_state = 42

        self.num_input_tokens = text_model['num_input_tokens']
        self.char2idx = text_model['char2idx']
        self.idx2char = text_model['idx2char']
        self.max_url_seq_length = text_model['max_url_seq_length']

        np.save(self.get_config_file_path(model_dir_path), text_model)

        weight_file_path = self.get_weight_file_path(model_dir_path)

        checkpoint = ModelCheckpoint(weight_file_path)

        X, Y = self.extract_training_data(url_data)

        Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=test_size, random_state=random_state) #splitting dataset into train and test for training

        self.model = make_bidirectional_lstm_model(self.num_input_tokens, self.max_url_seq_length)# Calling the make model function

        history = self.model.fit(Xtrain, Ytrain, batch_size=batch_size, epochs=epochs, verbose=1,validation_data=(Xtest, Ytest), callbacks=[checkpoint])#training the model

        self.model.save_weights(weight_file_path)#saving the weights of the model to be used later

        np.save(model_dir_path + '/' + lstmbidrpred.model_name + '-history.npy', history.history)#saving the model to be used later

        return history
