api_key =  "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" #jus

def generate_questions_from_text(text, api_key, num_questions=1):
    query = "Generate a question from this text: " + text + " =>"
    #result = teachify.perform_query(query)["choices"][0]["text"]
        
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=num_questions
        #stop=["\n"]
    )

    #print(response)
    generated_questions = []
    for i in range(num_questions): 
        result = response["choices"][i]["text"]
        generated_questions.append(result)
        print(result)
        #splitted = result.split("\n\n")
        #question = splitted[1]
        #answer = splitted[2]

        #print(f"generated question: {question}")
        #print(f"generated answer: {answer}")
    return generated_questions


def generate_answer_to_the_question(question):

    response_answer = openai.Answer.create(
      search_model="ada",
      model="curie",
      question=question,
      documents=[article],
      examples_context="In 2017, U.S. life expectancy was 78.6 years.",
      examples=[["What is human life expectancy in the United States?","Human life expectency is 78 years."]],
      max_tokens=20,
      stop=["\n", "<|endoftext|>"],
    )
    true_answer = response_answer["answers"][0]
    
    return true_answer



def generate_false_answers(true_answer, num_false_answers):
    # get half answers
    half_answer = true_answer[:len(true_answer)//3]

    query = "Finish this sentence: " +  half_answer +  " => "

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt= query,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=num_false_answers
        #stop=["\n"]
    )


    false_answers = []
    for i in range(num_false_answers): 
        result = response["choices"][i]["text"]
        false_answers.append(result)

    return false_answers


def generate_MC_questions(text, num_questions, num_false_answers, api_key):

    text_multiple_choice_qa_dict = {"questions": []}

    questions = generate_questions_from_text(article, api_key, num_questions)

    for q in questions:
        question_dict = {"question":q}
        #print(f"generated question: {q}")
        answer = generate_answer_to_the_question(q)
        question_dict["true_answer"] = answer
        #print(f"generated true answer: {answer}")
        false_answers = generate_false_answers(answer, num_false_answers)
        question_dict["false_answers"] = false_answers
        #print(f"generated false answers: {false_answers}")
        text_multiple_choice_qa_dict["questions"].append(question_dict)

    return text_multiple_choice_qa_dict

if __name__ == "__main__":
    api_key = "key"
    generate_MC_questions(article, 3, 3, api_key)