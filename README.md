# tweets2polarity

Ce projet regroupe les scripts et notebooks pythons utilisés dans le cadre de notre projet de l'UCE application innovation.

## Structure

### datasets

Contient les différents corpus utilisés. Annotés de différentes façons.

### notebooks

[Google colaboratory](https://colab.research.google.com/notebooks/welcome.ipynb?hl=fr) notebooks.

### polarityComputers

Contient les classes utilisées par le script "tweets2polarity.py" pour annoter les tweets.
On y trouve deux classes, une permettant d'obtenir un score en fonction des hashtags et l'autre en fonction du résultat de l'outil [textblob](https://textblob.readthedocs.io/en/dev/).

### polarityCsv

Les CSV représentant l'annotation manuelle de hashtags issus du corpus initial du projet.

### SVM

Les modèles SVM obtenus au fur et à mesure.

### Scripts python

| script  | fonction |
|---------|----------|
| hashtagsExtractor.py | extrait les hashtags des tweets dans un fichiers |
| setSplitter.py | sépare un corpus en 3 fichiers : training, validation, test |
| SVMFormatter.py | formate des tweets issus d'un fichier au fomat attendu par SVM (cf sujet TP initiation) |
| svmOutToTestId.py | utilise le résultat de SVM pour construire le fichier attendu par la plateforme (idTweet polarité), avec la liste des tweets de test (e-uapv)|
| svmOutToTweet.py | résultat SVM -> liste de tweets avec polarité |
| testFileToJson.py | transforme le fichier de test de la palteforme euapv en json |
| tweets2polarity.py | annote les tweets d'un fichier |
