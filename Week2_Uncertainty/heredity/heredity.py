import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    jointProb = 1
    peopleInfo = getPeopleInfo(people, one_gene, two_genes, have_trait)

    for person in peopleInfo:
        # Info about the person
        personGene = peopleInfo[person][0]
        personTrait = peopleInfo[person][1]

        # Info about the parents if they exist
        p1 = people[person]["mother"]
        p2 = people[person]["father"]

        if p1 == None and p2 == None:
            jointProb *= PROBS["gene"][personGene] * PROBS["trait"][personGene][personTrait]
        else:
            if personGene == 1:
                if p1 in one_gene:
                    p1Prob = 0.5
                elif p1 in two_genes:
                    p1Prob = 1 - PROBS["mutation"]
                else:
                    p1Prob = PROBS["mutation"]

                if p2 in one_gene:
                    p2Prob = 0.5
                elif p2 in two_genes:
                    p2Prob = 1 - PROBS["mutation"]
                else:
                    p2Prob = PROBS["mutation"]
                
                geneProb = (p1Prob * (1 - p2Prob) + p2Prob * (1 - p1Prob))
                jointProb *= PROBS["trait"][personGene][personTrait] * geneProb
            elif personGene == 2:
                if p1 in one_gene:
                    p1Prob = 0.5
                elif p1 in two_genes:
                    p1Prob = 1 - PROBS["mutation"]
                else:
                    p1Prob = PROBS["mutation"]

                if p2 in one_gene:
                    p2Prob = 0.5
                elif p2 in two_genes:
                    p2Prob = 1 - PROBS["mutation"]
                else:
                    p2Prob = PROBS["mutation"]

                geneProb = p1Prob * p2Prob
                jointProb *= PROBS["trait"][personGene][personTrait] * geneProb
            else:
                if p1 in one_gene:
                    p1Prob = 0.5
                elif p1 in two_genes:
                    p1Prob = PROBS["mutation"]
                else:
                    p1Prob = 1 - PROBS["mutation"]

                if p2 in one_gene:
                    p2Prob = 0.5
                elif p2 in two_genes:
                    p2Prob = PROBS["mutation"]
                else:
                    p2Prob = 1 - PROBS["mutation"]

                geneProb = p1Prob + p2Prob
                jointProb *= PROBS["trait"][personGene][personTrait] * geneProb

    return jointProb
                

def getPeopleInfo(people, one_gene, two_genes, have_trait):
    peopleInfo = dict()

    for person in people:
        if person in one_gene:
            if person in have_trait:
                peopleInfo[person] = [1, True]
            else:
                peopleInfo[person] = [1, False]
        elif person in two_genes:
            if person in have_trait:
                peopleInfo[person] = [2, True]
            else:
                peopleInfo[person] = [2, False]
        else:
            if person in have_trait:
                peopleInfo[person] = [0, True]
            else:
                peopleInfo[person] = [0, False]

    return peopleInfo

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    peopleSpecs = getPeopleInfo(probabilities.keys(), one_gene, two_genes, have_trait)

    for person in peopleSpecs:
        personGene = peopleSpecs[person][0]
        personTrait = peopleSpecs[person][1]

        probabilities[person]["gene"][personGene] += p
        probabilities[person]["trait"][personTrait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        for field in probabilities[person]:
            sumOfVals = sumOfValues(probabilities[person][field])
            scaleFactor = 1 / sumOfVals
            for value in probabilities[person][field]:
                probabilities[person][field][value] *= scaleFactor

def sumOfValues(field):
    sumOfVals = 0
    for value in field:
        sumOfVals += field[value]
    return sumOfVals


if __name__ == "__main__":
    main()
