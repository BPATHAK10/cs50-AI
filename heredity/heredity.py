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
            for two_geness in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_geness, have_trait)
                update(probabilities, one_gene, two_geness, have_trait, p)

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
        * everyone in set `two_geness` has two copies of the gene, and
        * everyone not in `one_gene` or `two_genes` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    zero_gene = set()
    not_have_trait = set()

    #get the set of people with zero genes and not having the trait
    for person in people:
        if person not in one_gene and person not in two_genes:
            zero_gene.add(person)
        
        if person not in have_trait:
            not_have_trait.add(person)

    probabilities = list()

    #calculating the probabiity of people having zero genes
    for p0 in zero_gene:
        mother = people[p0]["mother"]
        father = people[p0]["father"]
        prob = 1

        #calculating unconditional probabilities for parents
        if mother == None and father == None:
            if p0 in have_trait:
                prob = PROBS["gene"][0] * PROBS["trait"][0][True]
                probabilities.append(prob)
            elif p0 in not_have_trait:
                prob = PROBS["gene"][0] * PROBS["trait"][0][False]
                probabilities.append(prob)

        #for child
        else:
            notGetFrom0 = 1 - PROBS["mutation"]
            notGetFrom1 = 1 - 0.5 
            notGetfrom2 = PROBS["mutation"]


            #going through all the possible combinations of genes mother and father can have
            if mother in zero_gene and father in zero_gene:
                prob = pow((notGetFrom0),2)
                
            elif mother in zero_gene and father in one_gene:
                prob = notGetFrom0 * notGetFrom1
                
            elif mother in zero_gene and father in two_genes:
                prob = notGetFrom0 * notGetfrom2
                
            elif mother in one_gene and father in zero_gene:
                prob = notGetFrom1 * notGetFrom0
                            
            elif mother in one_gene and father in one_gene:
                prob = notGetFrom1 * notGetFrom1
                
            elif mother in one_gene and father in two_genes:
                prob = notGetfrom2 * notGetFrom1
                
            elif mother in two_genes and father in zero_gene:
                prob = notGetFrom0 * notGetfrom2
                
            elif mother in two_genes and father in one_gene:
                prob = notGetfrom2 * notGetFrom1
                
            elif mother in two_genes and father in two_genes:
                prob = notGetfrom2 * notGetfrom2
                
            #calculating the final probability including the trait probability
            if p0 in have_trait:
                finalProb = prob * PROBS["trait"][0][True]
                probabilities.append(finalProb)
            elif p0 in not_have_trait:
                finalProb = prob * PROBS["trait"][0][False]
                probabilities.append(finalProb)


    #people having one gene
    for p1 in one_gene:
        mother = people[p1]["mother"]
        father = people[p1]["father"]
        prob = 1

        #for parents
        if mother == None and father == None:
            if p1 in have_trait:
                prob = PROBS["gene"][1] * PROBS["trait"][1][True]
                probabilities.append(prob)
            elif p1 in not_have_trait:
                prob = PROBS["gene"][1] * PROBS["trait"][1][False]
                probabilities.append(prob)

        #for children
        else:
            getFrom0 = PROBS["mutation"]
            notGetFrom0 = 1 - PROBS["mutation"]

            getFrom1 = 0.5
            notGetFrom1 = 1 - getFrom1

            getFrom2 = 1 - PROBS["mutation"]
            notGetfrom2 = PROBS["mutation"]

            #going through all the possible combinations of genes mother and father can have
            if mother in zero_gene and father in zero_gene:
                prob = getFrom0 * notGetFrom0 + getFrom0 * notGetFrom0
                
            elif mother in zero_gene and father in one_gene:
                prob = getFrom0 * notGetFrom1 + getFrom1 * notGetFrom0
                
            elif mother in zero_gene and father in two_genes:
                prob = getFrom0 * notGetfrom2 + getFrom2 * notGetFrom0
                
            elif mother in one_gene and father in zero_gene:
                prob = getFrom1 * notGetFrom0 + getFrom0 * notGetFrom1
                            
            elif mother in one_gene and father in one_gene:
                prob = (getFrom1 * notGetFrom1) + (getFrom1 * notGetFrom1)
                
            elif mother in one_gene and father in two_genes:
                prob = getFrom1 * notGetfrom2 + getFrom2 * notGetFrom1
                
            elif mother in two_genes and father in zero_gene:
                prob = getFrom2 * notGetFrom0 + getFrom0 * notGetfrom2
                
            elif mother in two_genes and father in one_gene:
                prob = getFrom2 * notGetFrom1 + getFrom1 * notGetfrom2
                
            elif mother in two_genes and father in two_genes:
                prob = (getFrom2 * notGetfrom2) + (getFrom2 * notGetfrom2)
                

            #calculating the final probability
            if p1 in have_trait:
                finalProb = prob * PROBS["trait"][1][True]
                probabilities.append(finalProb)
            elif p1 in not_have_trait:
                finalProb = prob * PROBS["trait"][1][False]
                probabilities.append(finalProb)
    

    #for people having two genes
    for p2 in two_genes:
        mother = people[p2]["mother"]
        father = people[p2]["father"]
        prob = 1
        
        #for parents
        if mother == None and father == None:
            if p2 in have_trait:
                prob = PROBS["gene"][2] * PROBS["trait"][2][True]
                probabilities.append(prob)
            elif p2 in not_have_trait:
                prob = PROBS["gene"][2] * PROBS["trait"][2][False]
                probabilities.append(prob)

        #for child
        else:
            getFrom0 = PROBS["mutation"]
            getFrom1 = 0.5
            getFrom2 = 1 - PROBS["mutation"]
            
            #going through all the possible combinations of genes mother and father can have
            if mother in zero_gene and father in zero_gene:
                prob = pow((getFrom0),2)
                
            elif mother in zero_gene and father in one_gene:
                prob = getFrom0 * getFrom1
                
            elif mother in zero_gene and father in two_genes:
                prob = getFrom0 *  getFrom2 
                
            elif mother in one_gene and father in zero_gene:
                prob = getFrom1 * getFrom0 
                            
            elif mother in one_gene and father in one_gene:
                prob = pow((getFrom1),2)
                
            elif mother in one_gene and father in two_genes:
                prob = getFrom1 * getFrom2 
                
            elif mother in two_genes and father in zero_gene:
                prob = getFrom2 * getFrom0 
                
            elif mother in two_genes and father in one_gene:
                prob = getFrom2 * getFrom1
                
            elif mother in two_genes and father in two_genes:
                prob = pow((getFrom2),2)
                
            #calculating the final probability
            if p2 in have_trait:
                finalProb = prob * PROBS["trait"][2][True]
                probabilities.append(finalProb)
            elif p2 in not_have_trait:
                finalProb = prob * PROBS["trait"][2][False]
                probabilities.append(finalProb)


    jointProbability = 1 
    for probability in probabilities:
        jointProbability *= probability

    return jointProbability



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    zero_gene = set()
    not_have_trait = set()

    for person in probabilities:
        if person not in one_gene and person not in two_genes:
            zero_gene.add(person)
        
        if person not in have_trait:
            not_have_trait.add(person)

    for person in probabilities:
        #updating genes
        if person in zero_gene:
            probabilities[person]["gene"][0] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p

        #updating traits
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        elif person in not_have_trait:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
   
    for person in probabilities:
        normalizer1 = normalizer2 = 1
        total1 = total2 = 0
        for i in range(3):
            total1 += probabilities[person]["gene"][i]
        
        normalizer1 = 1 / total1

        for i in range(3):
            probabilities[person]["gene"][i] *= normalizer1

        for bol in [True,False]:
            total2 += probabilities[person]["trait"][bol]

        normalizer2 = 1 / total2

        for bol in [True,False]:
            probabilities[person]["trait"][bol] *= normalizer2


if __name__ == "__main__":
    main()
