# nlp-augment
It takes an sentence as an input and augment it based on sense, pos tag synonym, and synonyms.

## Installation
```pip install nlp-augment```

For jupyter Notebook
```!pip install nlp-augment```


## How to use it?

```import augment```

<strong>Method 1:</strong> We applied word-sense disambiguation to each word of the input sentence, after the preprocessing stagethat removes stopwords and other uncommon characters. The synonymy relation was used to extract the list of sensesfor each word. Next, to find out which of these senses better fit the context of the sentence, Lesk’s algorithm wasemployed. The original version of this algorithm disambiguates words in short sentences. For that, the gloss ofthe word to disambiguate (dictionary of its senses) is compared to glosses of other words of the sentence. Then, thesense that shares the most significant number of common words with the glosses of other words of the phrase is chosenand assigned to the target word. <br>

<em>Exmaple of hate sentence aumentation</em>

```augment.sense('you are gay')```

```['you are gay', 'you are queer', 'you are homophile']```

<strong>Method 2:</strong> We apply a Part of Speech (PoS) Tagging to each sentence, which is later used to extract all meanings(synsets) and synonyms that correspond to that word #PoS combination. This approach could widely expand thesemantic space over the previously mentioned data augmentation approach (method 1), as one word could have multiplemeanings of the same part of speech.<br>

```>>> augment.pos('you are gay')```

```['you are gay', 'you are cheery', 'you are sunny', 'you are jocund', 'you are jolly', 'you are jovial', 'you are merry', 'you are mirthful', 'you are brave', 'you are braw', 'you are festal', 'you are festive', 'you are queer', 'you are homophile']```


<strong>Method 3:</strong> We extract all possible meanings (synsets) of every complete word (after preprocessing), and then weretrieve the synonyms associated with every possible meaning. This significantly expands the semantic space of eachsentence compared to the first two methods. We are considering here all possible meanings (including every PoS thatthis word may belong to) as well as the similar words of each meaning regardless of the coherence of the correspondingcontext.

```augment.synonym('you are gay')```


```['you are gay', 'you ar gay', 'you be gay', 'you exist gay', 'you equal gay', 'you constitute gay', 'you represent gay', 'you make up gay', 'you comprise gay', 'you follow gay', 'you embody gay', 'you personify gay', 'you live gay', 'you cost gay', 'you are homosexual', 'you are homophile', 'you are homo', 'you are cheery', 'you are sunny', 'you are jocund', 'you are jolly', 'you are jovial', 'you are merry', 'you are mirthful', 'you are brave', 'you are braw', 'you are festal', 'you are festive', 'you are queer']```

## License

© 2021 Md Saroar Jahan

This repository is licensed under the MIT license. See LICENSE for details.
