from m_url.lib.cnn_lstm import cnnlstmpred
from m_url.lib.utility.url_data_loader import load_url_data
import numpy as np
from m_url.lib.utility.text_model_extractor import extract_text_model

def main():
    np.random.seed(21)
    data_dir_path = './data'
    model_dir_path = './models'
    report_dir_path = './reports'
    url_data = load_url_data(data_dir_path) #loading the url dataset
    text_model = extract_text_model(url_data['text']) #preprocessing the dataset
    batch_size = 64
    epochs = 50
    classifier = cnnlstmpred()
    mod = classifier.fit(text_model=text_model,model_dir_path=model_dir_path,url_data=url_data, batch_size=batch_size, epochs=epochs)#training the model

if __name__ == '__main__':
    main()
