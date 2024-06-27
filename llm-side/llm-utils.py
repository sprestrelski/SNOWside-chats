from langchain_community.llms import Ollama
import pandas as pd
import numpy as np
import ollama


def matching_1(people_arr):
    llm = Ollama(model="llama3")

    description_string = "Given this list of people, please output a series of matchings between them\n\n"

    # each element of people_arr is a 2 element tuple with name and introduction

    for person in people_arr:
        name = person[0]
        description = person[1]
        description_string += f"name: {name} introduction: {description}\n"

    description_string += "Please give the data in the format [person1] : [person2], in a list of lines. That's it.\n"
    description_string += "Also note that each person must be in only one matching!"
    description_string += "If there is an odd number of people, do one triplet, indicate the triplet in the format [person1] : [person2] : [person3]"

    result = llm.invoke(description_string)
    return result


def get_word_bag(person):
    introduction = person[1]

    llm = Ollama(model="llama3")

    prompt = "Given this introduction, please output a list of words that are relevant to the person\n\n"
    prompt += "The words can be specific words from the introduction, or vibes/tones that you get from the introduction\n\n"
    prompt += "Please return a comma separated list of values. NOTHING MORE."

    prompt += f"Introduction: {introduction}\n"

    result = llm.invoke(prompt)
    print(result)
    word_bag = result.split(", ")

    return word_bag


def get_word_embedding(description):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=description)
    embedding = response["embedding"]
    return embedding


def generate_people_embedding_arr(people_arr):
    people_embedding_arr = []
    for person in people_arr:
        name = person[0]
        description = person[1]

        word_bag = get_word_bag(person)
        embedding = get_word_embedding(description)

        people_embedding_arr.append((name, word_bag, embedding))

    return people_embedding_arr


def matching_2(people_embedding_arr):
    matches = []
    names = [person[0] for person in people_embedding_arr]

    name_to_embedding_map = {person[0]: person[2] for person in people_embedding_arr}

    while len(names) > 3:
        # find the best match
        best_match = None
        best_score = -1
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                # cosine similarity
                score = np.dot(
                    name_to_embedding_map[names[i]], name_to_embedding_map[names[j]]
                ) / (
                    np.linalg.norm(name_to_embedding_map[names[i]])
                    * np.linalg.norm(name_to_embedding_map[names[j]])
                )
                if score > best_score:
                    best_score = score
                    best_match = [names[i], names[j]]
        matches += [best_match]
        names.remove(best_match[0])
        names.remove(best_match[1])
    matches += [names]
    return matches

    pass


def greeting():
    pass


def __main__():
    df = pd.read_csv("dummy_intros.csv")

    # Convert the DataFrame to a list of tuples
    data_tuples = list(df.itertuples(index=False, name=None))
    print(data_tuples)
    people_embedding_arr = generate_people_embedding_arr(data_tuples)

    matches = matching_2(people_embedding_arr)
    print(matches)
    pass


if __name__ == "__main__":
    __main__()
