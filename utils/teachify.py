import openai
import requests

#
# Teachify is supposed to be a program that is supposed to help people with functional literacy
# It initializes a prototype GUI from which you load all of the necessary parameters
# The main idea is that it creates answers and checks if you answered them correctly
# You are also able to obtain the summary for the article (and export all of the results
#

questions = ""

def get_article(article_name):
    """
    Fetches the article from Wikipedia using its public API
    Parameters:
        :param article_name: - The name of the article the user wishes to fetch
        :type article_name: str
        :return: Article from wikipedia
        :type: str

    """
    response = requests.get('https://en.wikipedia.org/w/api.php', params={
        'action': 'query',
        'format': 'json',
        'titles': article_name,
        'prop': 'extracts',
        'exitintro': True,
        'explaintext': True,
    }).json()
    page = next(iter(response['query']['pages'].values()))
    res = clean_article(page['extract'])
    return res

def clean_article(article):
    """
    Cleans the article that was returned from wikipedia

    :param article: Text from the wiki article
    :type article: str
    :return: cleaned article
    :type: str
    """
    article = article.strip()
    idx = article.find("== Further reading ==")
    if idx != None:
        article = article[:idx]
    return article

def form_query(prompt,article_name="",answers=""):
    """
        Forms the requested query for the GPT3 - davinci model
        Parameters:
            :param prompt: one of the following values:  ['Summary', 'MultipleChoice', 'Questions', 'Answers', 'Flashcards']
                'Summary' returns the summary of the wiki article
                'MultipleChoice' returns three multiple choice questions
                'Questions' generates questions based on the wiki article
                'Answers' checks whether the provided answers are correct
                'Flashcards' creates flashcards based on the given wiki article
                The input will work for other queries but it has to be quite detailed
            :param article_name: (default "") - the name of the article the query should be formed around
            :param answers: (default "") - the answers to the given questions
            :type prompt: str
            :type article_name: str
            :type answers: str
            :return: Result of the query
            :type: str
    """
    global questions
    article = get_article(article_name)
    if len(article) > 4000:
        article = article[:4000].strip()

    if prompt == "Summary":
        summary_query =  "Generate summary from this article: \n\n" + article + " =>"
        res = perform_query(summary_query)["choices"][0]["text"]
    elif prompt == "MultipleChoice":
        multiple_choice_query = "Generate three multiple choice questions and tell me the right answers: \n\n" + article + " =>"
        res = perform_query(multiple_choice_query)["choices"][0]["text"]
    elif prompt == "Questions":
        question_query = "Generate three questions from this article: " + article + " =>"
        res = perform_query(question_query)["choices"][0]["text"]
        questions = res
    elif prompt == "Answers":
        answer_query = article + " " + questions + "\n" + answers + " Which of these answers are correct?" + " =>"
        res = perform_query(answer_query)["choices"][0]["text"]
    elif prompt == "Flashcards":
        flashcard_query= "Generate flashcards for this article: " + article + " =>"
        res = perform_query(flashcard_query)["choices"][0]["text"]
    else:
        other_query = article + " " + prompt + " =>"
        res = perform_query(other_query)["choices"][0]["text"]
    return res

def perform_query(query):
    """
            Makes an api request for the GPT3-davinci model
            Parameters:
                :param query: the query that is to be passed to the model
                :type query: str
                :return: query result
    """
    openai.api_key = "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"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        #stop=["\n"]
    )
    return response
