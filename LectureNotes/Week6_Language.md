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

Another fun example:  
"Big Rig Carrying Fruit Crashed on 210 Freeway, creates jam."

## Context-Free Grammar

Generating sentences in a language using symbols

We can represent each word as a terminal symbol. For each word, assign a non-terminal symbol - parts of speech for example.

![symbols](images/Week6_Language/../6_Language/symbols.png)