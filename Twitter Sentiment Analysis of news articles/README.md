# Twitter Sentiment Analysis of News Articles
There are various news articles present today, and every moment new ones are coming in. To see the impact of these news on people’s emotion in various geographical location is of mass interest. For eg. if India wins a match against Pakistan, how are people reacting to its win, and in which geographical location this news is popular. This information is critical for companies to plan their marketing campaigns and also strategize on how to make their products and services better. Firstly, using the NewsAPI we extract the news related to the keyword we provide. For example, if we provide the keyword ‘Trump’ the API will fetch recent news headlines related to Trump. We then use another API called Tweepy to use these headlines as reference and then it fetches the tweets from Twitter relevant to the news articles. 
These tweets will then be analyzed and classified into positive, negative or neutral. We will then visualize the analysis by displaying the different sentiments in the geo map.   


## Dataset Link from Kaggle
https://www.kaggle.com/kazanova/sentiment140
 
## Dependencies
- [Python v3.6.2](https://www.python.org/downloads/release/python-370/)
- [Natural Language ToolKit](https://www.nltk.org/)

## License
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE) file for details
