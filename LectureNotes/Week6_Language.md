# Language - CS50AI Lecture 6

## Natural Language Processing:

Algorithms that allow our AI to process and understand natural language

- Automatic summarization
- information extraction
- language identification
- machine translation
- named entity recognition
- speech recognition
- text classification
- word sense disambiguation
- ...

## Syntax and Semantics:

Just like programming languages have their own specific syntax, the languages we humans speak have their own syntax(grammar). For example, we can agree that the following sentence has good grammar,"just before nine o'clock, Sherlock Holmes stepped briskly into the room." However, this sentence does not have good grammar, "Just before Sherlock Holmes nin o'clock stepped briskly the room."

Then, there's the idea of semantics. The idea of what do sentences actually mean? "Just before nine o'clock Sherlock Holmes stepped briskly into the room." has a different structure than "Sherlock Holmes stepped briskly into the room just before nine o'clock" but they mean the same thing. We can also have a sentence that is grammatically correct but means absolutely nothing: "Colorless green ideas sleep furiously." This problem can get complicated very quickly.

## Context-Free Grammar:

**Generating sentences in a language using symbols and rewriting rules.**

Represent each word as a terminal symbol and assign a non-terminal symbol to each terminal symbol.

![symbols](images/Week6_Language/../6_Language/symbols.png)

To Help us translate non-terminal symbols into terminal symbols where the "|" represents possible choices for that non-terminal symbol.

![nttot](images/Week6_Language/../6_Language/nt-to-t.png)

New non-terminal symbols can be contstructed using existing non-terminal symbols.
- A noun phrase = a noun OR a determiner followed by a noun: `NP -> N | D N`.
- A verb phrase = a verb OR a verb followed by a noun phrase: `VP -> N | V NP`.
- Sentence = noun phrase followed by a verb phrase: `S -> NP VP`


### Syntax Trees:

Using language syntax trees, we can start to see the structure of language from while assembing sentences and/or phrases. Here are some examples.

Noun Phrase: Determiner followed by a noun

![city](images/Week6_Language/../6_Language/npTheCity.png)

Verb Phrase: A verb followed by a noun phrase

![vpnp](images/Week6_Language/../6_Language/vpnp.png)

A Sentence: Noun phrase followed by a verb phrase

![sent](images/Week6_Language/../6_Language/sent.png)