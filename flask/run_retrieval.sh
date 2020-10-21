#export FLASK_APP=retrieval_news.py
export FLASK_APP=retrieval_mcv.py
echo "http://$(hostname):8001/1F9CA1488A7B6935181ECA5E936B7C51CF6E4069FFCTBMQJLMC"
flask run --host=0.0.0.0 --port=8001
