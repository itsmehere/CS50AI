# Heredity

An AI to assess the likelihood that a person will have a particular genetic trait.

## Background:

Mutated versions of the [GJB2](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1285178/) gene are one of the leading causes of hearing impairment in newborns. Each person carries two versions of the gene, so each person has the potential to possess either 0, 1, or 2 copies of the hearing impairment version GJB2. Unless a person undergoes genetic testing, though, it’s not so easy to know how many copies of mutated GJB2 a person has. This is some “hidden state”: information that has an effect that we can observe (hearing impairment), but that we don’t necessarily directly know. After all, some people might have 1 or 2 copies of mutated GJB2 but not exhibit hearing impairment, while others might have no copies of mutated GJB2 yet still exhibit hearing impairment.

Every child inherits one copy of the GJB2 gene from each of their parents. If a parent has two copies of the mutated gene, then they will pass the mutated gene on to the child; if a parent has no copies of the mutated gene, then they will not pass the mutated gene on to the child; and if a parent has one copy of the mutated gene, then the gene is passed on to the child with probability 0.5. After a gene is passed on, though, it has some probability of undergoing additional mutation: changing from a version of the gene that causes hearing impairment to a version that doesn’t, or vice versa.

We can attempt to model all of these relationships by forming a Bayesian Network of all the relevant variables, as in the one below, which considers a family of two parents and a single child.

![BayesianNetwork](https://cs50.harvard.edu/ai/2020/projects/2/heredity/images/gene_network.png)

Each person in the family has a `Gene` random variable representing how many copies of a particular gene (e.g., the hearing impairment version of GJB2) a person has: a value that is 0, 1, or 2. Each person in the family also has a `Trait` random variable, which is `yes` or `no` depending on whether that person expresses a trait (e.g., hearing impairment) based on that gene. There’s an arrow from each person’s Gene variable to their Trait variable to encode the idea that a person’s genes affect the probability that they have a particular trait. Meanwhile, there’s also an arrow from both the mother and father’s `Gene` random variable to their child’s `Gene` random variable: the child’s genes are dependent on the genes of their parents.

Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, the AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.

## Understanding:

Open up `heredity.py` and take a look first at the definition of `PROBS`. `PROBS` is a dictionary containing a number of constants representing probabilities of various different events. All of these events have to do with how many copies of a particular gene a person has (hereafter referred to as simply “the gene”), and whether a person exhibits a particular trait (hereafter referred to as “the trait”) based on that gene. The data here is loosely based on the probabilities for the hearing impairment version of the GJB2 gene and the hearing impairment trait, but by changing these values, you could use your AI to draw inferences about other genes and traits as well!

First, `PROBS["gene"]` represents the unconditional probability distribution over the gene (i.e., the probability if we know nothing about that person’s parents). Based on the data in the distribution code, it would seem that in the population, there’s a 1% chance of having 2 copies of the gene, a 3% chance of having 1 copy of the gene, and a 96% chance of having 0 copies of the gene.

Next, `PROBS["trait"]` represents the conditional probability that a person exhibits a trait (like hearing impairment). This is actually three different probability distributions: one for each possible value for gene. So PROBS["trait"][2] is the probability distribution that a person has the trait given that they have two versions of the gene: in this case, they have a 65% chance of exhibiting the trait, and a 35% chance of not exhibiting the trait. Meanwhile, if a person has 0 copies of the gene, they have a 1% chance of exhibiting the trait, and a 99% chance of not exhibiting the trait.

Finally, `PROBS["mutation"]` is the probability that a gene mutates from being the gene in question to not being that gene, and vice versa. If a mother has two versions of the gene, for example, and therefore passes one on to her child, there’s a 1% chance it mutates into not being the target gene anymore. Conversely, if a mother has no versions of the gene, and therefore does not pass it onto her child, there’s a 1% chance it mutates into being the target gene. It’s therefore possible that even if neither parent has any copies of the gene in question, their child might have 1 or even 2 copies of the gene.

Ultimately, the probabilities you calculate will be based on these values in PROBS.

Ultimately, we’re looking to calculate these probabilities based on some evidence: given that we know certain people do or do not exhibit the trait, we’d like to determine these probabilities. We can calculate a conditional probability by summing up all of the joint probabilities that satisfy the evidence, and then normalize those probabilities so that they each sum to 1.

## Solution Explanation:

Rather than explain some parts of the solution using comments, I chose to do it here so it's more clear.

**`parentProbability()`**  
This function determins the probability of a parent giving 1 copy of the gene. Let's consider the case where `parent` is in `two_genes`, then 'one_gene', and finally 0. 
- **2:** The probability of the parent giving a copy of the sick gene if they have 2 is 100%. But this is without accounting for mutation. There is a small chance, represented by `PROBS["mutation"]` that the gene **will** mutate into no longer being a target gene(won't be sick anymore). Conversely, if we want to know the probability of the child receiving the **sick** gene, it can be represented as `1 - PROBS["mutation"]`.
- **1:** The probability of the parent giving a copy of the sick gene if they have 1 is 50%. Once again, this is without accounting for mutation. This is a little more complicated because the single gene could be either sick or not sick. Given the 1 gene, the child could get the 1 copy of the gene that's mutated with probability `0.5 * PROBS["mutation"]`. Also, the child could get 1 copy of the gene that's not mutated with probability `0.5 * (1 - PROBS["mutation"])`. If we add these together, it will represent the probability of the child getting one copy of the gene from a parent with 1 copy. Well...hold on a second...that just simplifies to `0.5`!
- **0:** The probability of the parent giving a copy of the sick gene if they have 0 is 0% without mutation. This one is simple because the only way the parent can give 1 copy of the gene is if a mutation occurs; with probability of `PROBS["mutation"]`.

**Line 162: `geneProb = (p1Prob * (1 - p2Prob) + p2Prob * (1 - p1Prob))`**  
There are two ways a child can get 1 copy of the gene. Either they get the gene from their mother and not their father, or they get the gene from their father and not their mother. Let's say their mother has 0 copies of the gene, so the child will get the gene from his mother with probability `0.01` (this is `PROBS["mutation"])`, since the only way to get the gene from their mother is if it mutated; conversely, they will not get the gene from their mother with probability `0.99`. Let's say their father has 2 copies of the gene, so they will get the gene from their father with probability `0.99` (this is `1 - PROBS["mutation"]`), but will get the gene from their mother with probability `0.01` (the chance of a mutation). Both of these cases can be added together to get `0.99 * 0.99 + 0.01 * 0.01 = 0.9802`, the probability that they have 1 copy of the gene.

TLDR:
- First1 `0.99`: represents probability of getting gene from father(given he has 2 copies)
- Second1 `0.99`: represents probability of not getting gene from mother(given she has 0 copies)  
Multiply First1 and Second1 to get first case joint probability - we'll call this value `jprob1`.
- First2 `0.01`: represents probability of getting gene from mother(given she has 0 copies)
- Second2 `0.01`: represents probability of not getting gene from father(given he has 2 copies)
Multiply First2 and Second2 to get second case joint probability - we'll call this value `jprob2`.

Add `jprob1` to `jprob2` to get the final probability of the child receiving 1 copy.



## Usage:

Needs command line argument of `.csv` file in `/data`

To run using `family0.csv`
```bash
python heredity.py data/family0.csv
```

## Other Links:

Read more about cs50ai [here](https://cs50.harvard.edu/ai/2020/)
[Original Problem Page](https://cs50.harvard.edu/ai/2020/projects/2/heredity/)