import spacy
import numpy as np

def NLPProcess(druglist, df_interaction):
    def addMechanism(node):
        if int(sonsNum[node - 1]) == 0:
            return
        else:
            for k in sons[node - 1]:
                if k == 0:
                    break
                if dependency[k - 1].text == drugA[i] or dependency[k - 1].text == drugB[i]:
                    continue
                quene.append(k)
                addMechanism(k)
        return quene

   
    nlp = spacy.load("en_core_web_sm")

    event = df_interaction['interaction']  # Interaction text from DataFrame
    mechanism = []  # To store mechanism of interactions
    action = []     # To store root actions
    drugA = []      # To store the first drug in interaction
    drugB = []      # To store the second drug in interaction

    for i in range(len(event)):
        doc = nlp(event[i])  # Process each interaction event with spaCy
        
    
        dependency = [token for token in doc]
        sons = np.zeros((len(dependency), len(dependency)))  # Create sons matrix
        sonsNum = np.zeros(len(dependency))  # Track number of children per token
        flag = False
        count = 0
        

        for token in dependency:
            if token.dep_ == 'ROOT':  # Find the root (main verb/action)
                root = token.i + 1
                action.append(token.lemma_)  # Store the root action's lemma

            if token.text in druglist:  # Check if token is in the drug list
                if count < 2:
                    if flag:
                        drugB.append(token.text)  # Assign the second drug
                        count += 1
                    else:
                        drugA.append(token.text)  # Assign the first drug
                        flag = True
                        count += 1

           
            if token.head.i >= 0:
                sonsNum[token.head.i] += 1
                sons[token.head.i, int(sonsNum[token.head.i] - 1)] = token.i + 1
        
        quene = []  
        for j in range(int(sonsNum[root - 1])):  #
            if dependency[int(sons[root - 1, j] - 1)].dep_ in ['obj', 'nsubjpass']:
                quene.append(int(sons[root - 1, j]))
                break

        if quene:
            quene = addMechanism(quene[0])  # Recursively add more mechanism components
            quene.sort()
            mechanism.append(" ".join(dependency[j - 1].text for j in quene))
        else:
            mechanism.append("")

        # Post-process mechanism to correct specific cases
        if mechanism[i] == "the fluid retaining activities":
            mechanism[i] = "the fluid"
        if mechanism[i] == "atrioventricular blocking ( AV block )":
            mechanism[i] = 'the atrioventricular blocking ( AV block ) activities increase'

    return mechanism, action, drugA, drugB
