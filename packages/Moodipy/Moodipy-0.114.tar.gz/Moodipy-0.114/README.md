# Moodipy Test
Use sentiment analysis to create a playlist that matches someone's mood and also predict songs to rise in popularity.

## Installation instructions

### Required packages commands if the distribution is not found in PYPI: 
* screeninfo:
  * pip install screeninfo
* spotipy
  * pip install spotipy
* urllib3==1.26.6:
  * pip install urllib3 --upgrade
* requests>=2.25.0
  *  pip install requests --upgrade
* nltk:
  * pip install nltk
  * python3 -m nltk.downloader punkt
  * python3 -m nltk.downloader stopwords
  * python3 -m nltk.downloader averaged_perceptron_tagger
  * python3 -m nltk.downloader wordnet
* PyQt5:
  * pip3 install --user pyqt5
  * sudo apt-get install pyqt5-dev-tools
  * sudo apt-get install qttools5-dev-tools