# GraDiAn
The Grammatical Distribution Analyser (GraDiAn) is used for analysing grammatical distributions; particularly the distributions of popular NLP datasets.

At the moment, GraDiAn does this by providing two abstract data types: the Syntactic Dependency Counter and the SentTree.

## SentTree
`SentTree` represents a given sentence in a tree structure.
Importantly, the `SentTree` can be used to analyse the parse-tree with regards to different properties of the text including part-of-speech tags, syntactic dependencies and (with the help of [spaCyTextBlob](https://spacy.io/universe/project/spacy-textblob)) sentiment.

## Syntactic Dependency Counter (SDC)
An `SDC` does what it says on the tin.
Inheriting from python's `collections.Counter` class, it maintains a count of syntactic dependency labels.

## Usage

### Syntactic Dependency Counter
Syntactic Dependency Counter from text:
```
>>> from gradian import SDC
>>> sdc = SDC.from_string('This is a test sentence!')
>>> sdc
SDC({'nsubj': 1, 'ROOT': 1, 'det': 1, 'compound': 1, 'attr': 1, 'punct': 1})
```

Or from a series of texts:
```
>>> from gradian import SDC
>>> sdc = SDC.from_string_arr(['This is a test sentence!', 'This is another sentence',
                               'How about another?'])
>>> sdc
SDC({'ROOT': 3, 'nsubj': 2, 'det': 2, 'attr': 2, 'punct': 2, 'compound': 1, 'advmod': 1, 'pobj': 1}
```

### SentTree
SentTree from text:
```
>>> from gradian import SentTree
>>> sent_trees = SentTree.from_string('This is a test sentence! But this is another!')
>>> # Sent_Tree.from_string produces a list of trees; one for each sentence
>>> sent_trees[0].attr_tree('pos')  # Get the Tree with respect to the sentence's POS-Tags
Tree('AUX', ['DET', Tree('NOUN', ['DET', 'NOUN']), 'PUNCT'])
```

`attr_tree` can be used with any attribute of the tree including syntactic dependencies, POS-tags and (if spaCyTextBlob is enabled) sentiment.
```
>>> sent_trees[0].attr_tree('dependency')
Tree('ROOT', ['nsubj', Tree('attr', ['det', 'compound']), 'punct'])
```
The function can be called with `token=True` to see the attributes alongside the relevant tokens:
```
>>> # token is a positional argument so does not need to be explicitly provided by keyword
>>> sent_trees[0].attr_tree('pos', token=True)  
Tree('is:  AUX', ['This: DET', Tree('sentence:  NOUN', ['a: DET', 'test: NOUN']), '!: PUNCT'])
```

`SentTrees` also come with the ability to create multi-attribute trees.
```
>>> sent_trees[0].multi_attr_tree(['pos', 'dependency'], True)
Tree('is:AUX:ROOT', ['This:DET:nsubj', Tree('sentence:NOUN:attr', ['a:DET:det', 'test:NOUN:compound']), '!:PUNCT:punct'])
```
