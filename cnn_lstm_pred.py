from m_url.lib.cnn_lstm import cnnlstmpred
from m_url.lib.utility.url_data_loader import load_url_data
import numpy as np

def main():
    data_dir_path = './data'
    model_dir_path = './models'
    predictor = cnnlstmpred()
    np_load_old = np.load
    np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
    predictor.load_model(model_dir_path)#loading the model 
    url_data = load_url_data(data_dir_path)
    np.load = np_load_old
    url_data = load_url_data(data_dir_path)
    count = 0
    
    '''for url, label in zip(url_data['text'], url_data['label']):
        predicted_label = predictor.predict(url)
        print('predicted: ' + str(predicted_label) + ' actual: ' + str(label))
        count += 1
        if count > 20:
            break
    '''

    url_inp=input("\nEnter the URL:") #asking user to put a url to be judged
    fin=predictor.predict(url_inp) #getting the result of user input url
    if fin ==0:
        print("\nIts SAFE!!\n")
    else:
        print("\nThe website seems to be malicious!!\n")


if __name__ == '__main__':
    main()