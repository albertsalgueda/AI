import csv
import itertools
import sys

#python heredity.py data/family0.csv

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
    joined = set()
    #people['Harry']['gene'] = 1
    #print(people['Harry']['gene'])
    persons = {}
    mut = 0.01
    class People():
        def __init__(self,name,mother,father):
            self.name = name
            self.mother = mother
            self.father = father
        def add_gene(self,gene):
            self.gene = gene
        def add_trait(self,trait):
            self.trait = trait
        def is_parent(self):
            if self.mother == None:
                return True
            else: 
                return False
        def has_gene(self):
            if self.gene !=0:
                return 0.99
            return 0.01
    
    for person in people:
        person = People(people[person]['name'],people[person]['mother'],people[person]['father'])
        if person.name in one_gene:
            person.add_gene(1)
        elif person.name in two_genes:
            person.add_gene(2)
        elif person.name not in one_gene and person.name not in two_genes: 
            person.add_gene(0)
        if person.name in have_trait:
            person.add_trait(True)
        else:
            person.add_trait(False)
        persons[person.name] = person

    for person in people:
        if persons[people[person]['name']].is_parent():
            probabilities =  PROBS["gene"][persons[people[person]['name']].gene]*PROBS["trait"][persons[people[person]['name']].gene][persons[people[person]['name']].trait]
            joined.add(probabilities)
        #bug must be heref
        else:
            #gets 0.99 if parent has get and 0.01 otherwise  
            mother = persons[persons[people[person]['name']].mother].gene
            father = persons[persons[people[person]['name']].father].gene
            if persons[people[person]['name']].gene == 0:
                if mother==0 and father==0:
                    probs1 = (0.99*0.99) #good
                elif (mother==0 and father==1) or  (mother==1 and father==0):
                    probs1 = (0.99*.5) #good
                elif (mother==0 and father==2) or  (mother==2 and father==0):
                    probs1 = (0.99*mut) #good
                elif (mother==1 and father==1): 
                    probs1 = (.5*.5) #good
                elif (mother==0 and father==2) or  (mother==2 and father==0):
                    probs1 = (0.99*0.5) #good
                elif (mother==1 and father==2) or  (mother==2 and father==1):
                    probs1 = (0.5*mut) #good
                else:
                    probs1 = mut*mut #good 
            elif persons[people[person]['name']].gene == 1:
                if mother==0 and father==0:
                    probs1 = (mut*0.99)*2 #good 
                elif (mother==0 and father==1) or  (mother==1 and father==0):
                    probs1 = 0.99*0.5 + 0.01*0.5
                elif (mother==0 and father==2) or  (mother==2 and father==0):
                    probs1 = (0.99**2 + mut*mut) #GOOD
                elif (mother==1 and father==1): 
                    probs1 = (0.5*0.5)*2
                elif (mother==1 and father==2) or  (mother==2 and father==1):
                    probs1 = 0.5*mut + 0.5*0.99
                else: # 2,2
                    probs1 = (0.99*mut)*2 #good 
            elif persons[people[person]['name']].gene == 2:
                if mother==0 and father==0:
                    probs1 = (mut*mut) #good    
                elif (mother==0 and father==1) or  (mother==1 and father==0):
                    probs1 = mut*0.5
                elif (mother==1 and father==1):
                    probs1 = 0.5*0.5
                elif (mother==0 and father==2) or  (mother==2 and father==0):
                    probs1 = (0.99*mut) #good
                elif (mother==1 and father==2) or  (mother==2 and father==1):
                    probs1 = 0.5*0.99
                else:
                    probs1 = (0.99)**2 #good 
            probabilities = probs1*PROBS["trait"][persons[people[person]['name']].gene][persons[people[person]['name']].trait]
            joined.add(probabilities)
    joined_probabilities=1
    for prob in joined:
        joined_probabilities = joined_probabilities*prob
    return joined_probabilities
    
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
