{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.13","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"none","dataSources":[{"sourceId":2347441,"sourceType":"datasetVersion","datasetId":1417162}],"dockerImageVersionId":30732,"isInternetEnabled":false,"language":"python","sourceType":"notebook","isGpuEnabled":false}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# This Python 3 environment comes with many helpful analytics libraries installed\n# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python\n# For example, here's several helpful packages to load\n\nimport numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport re\nimport nltk\nimport string\nfrom nltk.corpus import stopwords\n\nfrom nltk.stem import LancasterStemmer\nfrom nltk.stem.porter import PorterStemmer\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.naive_bayes import MultinomialNB\nfrom sklearn.metrics import accuracy_score, classification_report\n# Input data files are available in the read-only \"../input/\" directory\n# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory\n\nimport os\nfor dirname, _, filenames in os.walk('/kaggle/input'):\n    for filename in filenames:\n        print(os.path.join(dirname, filename))\n\n# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using \"Save & Run All\" \n# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session","metadata":{"_uuid":"8f2839f25d086af736a60e9eeb907d3b93b6e0e5","_cell_guid":"b1076dfc-b9ad-4769-8c92-a6c4dae69d19","execution":{"iopub.status.busy":"2024-07-03T07:14:10.069179Z","iopub.execute_input":"2024-07-03T07:14:10.069702Z","iopub.status.idle":"2024-07-03T07:14:10.084700Z","shell.execute_reply.started":"2024-07-03T07:14:10.069662Z","shell.execute_reply":"2024-07-03T07:14:10.083291Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"markdown","source":"#  **Load Dataset**","metadata":{}},{"cell_type":"code","source":"train_path=\"/kaggle/input/genre-classification-dataset-imdb/Genre Classification Dataset/train_data.txt\"\ntrain_data=pd.read_csv(train_path,sep=':::', names=['TITLE', 'GENRE', 'DESCRIPTION'], engine='python')","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:14:10.087101Z","iopub.execute_input":"2024-07-03T07:14:10.087576Z","iopub.status.idle":"2024-07-03T07:14:10.467258Z","shell.execute_reply.started":"2024-07-03T07:14:10.087540Z","shell.execute_reply":"2024-07-03T07:14:10.466098Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"print(train_data.describe())","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:14:10.468647Z","iopub.execute_input":"2024-07-03T07:14:10.469183Z","iopub.status.idle":"2024-07-03T07:14:10.591078Z","shell.execute_reply.started":"2024-07-03T07:14:10.469141Z","shell.execute_reply":"2024-07-03T07:14:10.589703Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"print(train_data.info())","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:14:10.594243Z","iopub.execute_input":"2024-07-03T07:14:10.594911Z","iopub.status.idle":"2024-07-03T07:14:10.623218Z","shell.execute_reply.started":"2024-07-03T07:14:10.594872Z","shell.execute_reply":"2024-07-03T07:14:10.621383Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"print(train_data.isnull().sum())","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:14:10.624731Z","iopub.execute_input":"2024-07-03T07:14:10.625715Z","iopub.status.idle":"2024-07-03T07:14:10.649283Z","shell.execute_reply.started":"2024-07-03T07:14:10.625672Z","shell.execute_reply":"2024-07-03T07:14:10.647852Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"test_path=\"/kaggle/input/genre-classification-dataset-imdb/Genre Classification Dataset/test_data.txt\"\ntest_data=pd.read_csv(test_path,sep=':::', names=['ID', 'TITLE', 'DESCRIPTION'], engine='python')\ntest_data.head()","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:14:10.651153Z","iopub.execute_input":"2024-07-03T07:14:10.651669Z","iopub.status.idle":"2024-07-03T07:14:11.133276Z","shell.execute_reply.started":"2024-07-03T07:14:10.651629Z","shell.execute_reply":"2024-07-03T07:14:11.132005Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"markdown","source":"# **Data preprocessing and Text cleaning**","metadata":{}},{"cell_type":"code","source":"stemmer = LancasterStemmer()\nstop_words = set(stopwords.words('english'))\ndef Clean_Text(text):\n    text = text.lower()  \n    text = re.sub(r'@\\S+', '', text)  \n    text = re.sub(r'http\\S+', '', text)  \n    text = re.sub(r'pic.\\S+', '', text)\n    text = re.sub(r\"[^a-zA-Z+']\", ' ', text)  \n    text = re.sub(r'\\s+[a-zA-Z]\\s+', ' ', text + ' ')  \n    text = \"\".join([i for i in text if i not in string.punctuation])\n    words = nltk.word_tokenize(text)\n    stopwords = nltk.corpus.stopwords.words('english')  \n    text = \" \".join([i for i in words if i not in stopwords and len(i) > 2])\n    text = re.sub(\"\\s[\\s]+\", \" \", text).strip()  \n    return text\ntrain_data['Text_cleaning'] = train_data['DESCRIPTION'].apply(Clean_Text)\ntest_data['Text_cleaning'] = test_data['DESCRIPTION'].apply(Clean_Text)","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:14:11.134872Z","iopub.execute_input":"2024-07-03T07:14:11.135317Z","iopub.status.idle":"2024-07-03T07:15:58.784038Z","shell.execute_reply.started":"2024-07-03T07:14:11.135276Z","shell.execute_reply":"2024-07-03T07:15:58.782644Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"markdown","source":"# **TF_IDF Vectorization**","metadata":{}},{"cell_type":"code","source":"\ntfidf_vectorizer = TfidfVectorizer()\n\n\nx_train = tfidf_vectorizer.fit_transform(train_data['Text_cleaning'])\n\n\nx_test = tfidf_vectorizer.transform(test_data['Text_cleaning'])","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:15:58.785510Z","iopub.execute_input":"2024-07-03T07:15:58.785855Z","iopub.status.idle":"2024-07-03T07:16:05.648899Z","shell.execute_reply.started":"2024-07-03T07:15:58.785827Z","shell.execute_reply":"2024-07-03T07:16:05.647743Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"markdown","source":"# **Split dataset and Train the model**","metadata":{}},{"cell_type":"code","source":"\nx = x_train\ny = train_data['GENRE']\nx_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)\n\n\nclassifier = MultinomialNB()\nclassifier.fit(x_train, y_train)\n\n\ny_pred = classifier.predict(x_val)\n\n\naccuracy = accuracy_score(y_val, y_pred)\nprint(\"Validation Accuracy:\", accuracy)\nprint(classification_report(y_val, y_pred))","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:16:05.650350Z","iopub.execute_input":"2024-07-03T07:16:05.650909Z","iopub.status.idle":"2024-07-03T07:16:06.373398Z","shell.execute_reply.started":"2024-07-03T07:16:05.650827Z","shell.execute_reply":"2024-07-03T07:16:06.372406Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"markdown","source":"# **Predict on Test data**","metadata":{}},{"cell_type":"code","source":"x_test_prediction = classifier.predict(x_test)\ntest_data['Predicted_Genre'] = x_test_prediction","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:32:44.240958Z","iopub.execute_input":"2024-07-03T07:32:44.241496Z","iopub.status.idle":"2024-07-03T07:32:44.396052Z","shell.execute_reply.started":"2024-07-03T07:32:44.241453Z","shell.execute_reply":"2024-07-03T07:32:44.394601Z"},"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"test_data.to_csv('predicted_genres.csv', index=False)\n\n\nprint(test_data)","metadata":{"execution":{"iopub.status.busy":"2024-07-03T07:32:48.740128Z","iopub.execute_input":"2024-07-03T07:32:48.740558Z","iopub.status.idle":"2024-07-03T07:32:50.375816Z","shell.execute_reply.started":"2024-07-03T07:32:48.740527Z","shell.execute_reply":"2024-07-03T07:32:50.374307Z"},"trusted":true},"execution_count":null,"outputs":[]}]}