import csv
import itertools
import sys

#python heredity.py data/family2.csv

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
    joined = 1

    for person in people:
        #get the gene of the current person
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        #get the trait of the current person 
        trait = True if person in have_trait else False
        #if we have no info about the parents
        if people[person]['mother'] is None:   
            #use probability distribution
            joined *= PROBS['gene'][gene_number] * PROBS['trait'][gene_number][trait]
        #if we have info about the parents
        else:
            mother = people[person]['mother']
            father = people[person]['father']
            #create a dictionary with parents probabilities of transmition 
            percentages = {}
            for parent in [mother, father]:
                #get parent's gene number
                parent_gene = 1 if parent in one_gene else 2 if parent in two_genes else 0
                #get the probabilities of transmition to the son
                #0.01 if parent gene is 0
                #0.5 if parent gene is 1 
                #0.99 if parent gene is 2
                probs = PROBS['mutation'] if parent_gene == 0 else 0.5 if parent_gene == 1 else 1 - PROBS['mutation']
                #add to dictionary
                percentages[parent] = probs

            if gene_number == 0:
                # probabilities that son has 0 genes given the probabilities of parent's transmition,
                # none of them has passed the gene
                joined *= (1 - percentages[mother]) * (1 - percentages[father])
            elif gene_number == 1:
                # 1 gene given parents 
                joined *= (1 - percentages[mother]) * percentages[father] + percentages[mother] * (1 - percentages[father])
            else:
                # both parents have transmited the gene 
                joined *= percentages[mother] * percentages[father]

            joined *= PROBS['trait'][gene_number][trait]
    return joined
    
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    #print(probabilities)
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2]+= p
        else:
            probabilities[person]["gene"][0] += p
    for person in probabilities:
        if person not in have_trait:
            probabilities[person]["trait"][False] += p
        elif person in have_trait:
            probabilities[person]["trait"][True] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        genes = 0
        for value in probabilities[person]['gene']:
            genes += probabilities[person]['gene'][value]
        for value in probabilities[person]['gene']:
            probabilities[person]['gene'][value]/=genes
        traits = 0
        for gene in probabilities[person]['trait']:
            traits += probabilities[person]['trait'][gene]
        for gene in probabilities[person]['trait']:
            probabilities[person]['trait'][gene]/=traits
            
if __name__ == "__main__":
    main()
