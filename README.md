# Project 3: `/r/TheOnion` vs. `/r/nottheonion`
## Introduction
The Onion is a well-known satirical news organization, and `/r/TheOnion`
subreddit is dedicated to the content it produces.
On the other hand, `/r/nottheonion` is a subreddit devoted to news media
written by reputable sources that sound absurd or surreal.

[Poe's law](https://en.wikipedia.org/wiki/Poe%27s_law) is an internet adage
that gets to the heart of communication on the internet --- in the absence of body language,
facial cues, and other nonverbal means of communication, it can be difficult to
impossible to determine if a statement is ironic or sincere.

Satire and sarcasm detection is an active area of research, and still not considered
a trivial problem. In this project, we build models that attempt to differentiate
between real absurdity and human-generated unreality.
## Executive Summary
In this project, we're using news headlines curated by these two subreddits as
proxies for serious content and satire. Assuming that we don't end up measuring
other signals (like what the moderation policies include/exclude, for example),
then we hope this project will be a reasonable introductory attempt at detecting
satire. We built over a dozen models, with many slight variations, and show that
we can correctly predict whether a headline is serous or from The Onion with about
80% accuracy. In fact, the overall consistency of our models suggests that this
particular problem is not as hard as the more general problem of detecting satire
or sarcasm in context.

In future projects, we would definitely explore using word embeddings as lower-dimensional
features.
## Directory Structure
```
.
├── data
├── Jupyter notebooks, ordered in order of execution
├── JsonCollector.py
├── plots
├── presentation
└── README.md
```

## Data
Our data consists of posts from the two subreddits `/r/TheOnion` and `/r/nottheonion`.
The data was gathered via requests to the [Pushshift API](https://github.com/pushshift/api).
Our collection is everything that Pushshift has from these two subreddits; we iteratively
scraped data from the time each subreddit was founded up till the present time.
After we cleaned out pathological posts, we ended up with 8.5k high-quality Onion titles,
and around 440k high-quality real and really absurd news titles.

These are stored in the `data` directory, which is not uploaded to this repo due to size constraints.


In the tables below, "h-opt" refers to hyperparameter optimization via RandomizedSearchCV.

## Model summaries
In the following tables, we describe the models we built with some brief summary statistics.
Each model was trained on a equally-stratified set of 4000+4000 titles. In addition to
the cross-validated test score, we evaluated the models on the remainder of the corpus
of posts.
#### CountVectorizer models

| Model        |Training time (s)| Train Accuracy           | Test Accuracy  |`/r/theonion` corpus accuracy|`/r/nottheonion` corpus accuracy|
|:-------------|---:|-------------:| -----:|------:|------:|
| LogReg                 | 43|.984|.800|.791|.805|
| ...with h-opt          | 15|.969|.801|.793|.805|
| MultinomNB             | .1|.954|.812|.811|.806|
| ...with h-opt          | 10|.944|.812|.805|.803|
| ComplementNB           | .1|.954|.812|.810|.807|
| ...with h-opt          | 11|.955|.812|.800|.799|
| BernoulliNB            | .1|.955|.813|.801|.816|
| ...with h-opt          | 11|.962|.810|.795|.811|

#### Tf-idf models

| Model        |Training time (s)| Train Accuracy           | Test Accuracy  |`/r/theonion` corpus accuracy|`/r/nottheonion` corpus accuracy|
|:-------------|---:|-------------:| -----:|------:|------:|
| LogReg                 | 26|.976|.799|.810|.795|
| ...with h-opt          | 13|.913|.783|.797|.783|
| MultinomNB             | .1|.955|.805|.826|.792|
| ...with h-opt          | 11|.999|.819|.824|.789|
| ComplementNB           | .1|.955|.807|.823|.797|
| ...with h-opt          | 11|.940|.815|.812|.799|
| BernoulliNB            | .1|.956|.807|.813|.812|
| ...with h-opt          | 11|.904|.806|.781|.815|
| SVC                   |281*|.997|.797|.804|.812|
| ...with h-opt         |382*|.997|.796|.804|.812|

\*SVCs trained extremely quickly, but evaluating them on the holdouts took so long
that I included that time.

## Future Work
Word embeddings are frequently employed for text classification tasks. Unfortunately,
we were unable to get an implementation working
