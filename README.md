# FST-Lemmatizer
Built a basic lemmatizer for English verbs using OpenFST. A lemmatizer is a program that takes words and returns their lemma—roughly, the form of the word you would find in a dictionary. For English verbs, lemmas are the infinitive form of the verb, the form that comes after to (as in to have or to thrash). Given a list of paradigms—lists of the forms of each verb—for many known verbs, including most exceptional (or irregular) verbs. Constructed a finite-state transducer (FST), using OpenFST, which takes any of those in vocabulary forms, or any regular out-of-vocabulary (OOV) verb, and returns one or more possible lemmas.
