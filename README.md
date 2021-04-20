malicious_url_checker


The aim of this project is to create a deep learning classifier which labels a given url as malicious or benign without any human intervention

There are two models included:


CNN-LSTM:

This model is created by adding an LSTM layer after many layers of CNN

This model gives an accuracy of around 55-60%

To Train this model execute:

"python cnn_lstm_train.py"

in the common folder

To predict using this model execute:

"python cnn_lstm_pred.py"

and enter the url you need to check.


Bidirectional-LSTM:

This model gives an accuracy of around 75-80%

To Train this model execute:

"python bidr_lstm_train.py"

in the common folder

To predict using this model execute:

"python bidr_lstm_pred.py"

and enter the url you need to check.


Please consider Bidirectional-LSTM model for grading the output since it has the better accuracy
