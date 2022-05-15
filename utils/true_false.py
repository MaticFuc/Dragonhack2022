from string import punctuation
import torch
from transformers import pipeline, set_seed
from nltk import tokenize
import requests
import json
#from summa.summarizer import summarize
import benepar
import string
import nltk
from nltk import tokenize
from nltk.tokenize import sent_tokenize
import re
from random import shuffle
import spacy
import nltk
nltk.download('punkt')
#nlp = spacy.load('en')
nlp = spacy.load("en_core_web_sm")
#this package is required for the summa summarizer
nltk.download('punkt')
benepar.download('benepar_en3')
benepar_parser = benepar.Parser("benepar_en3")

def preprocess(sentences):
    output = []
    for sent in sentences:
        single_quotes_present = len(re.findall(r"['][\w\s.:;,!?\\-]+[']",sent))>0
        double_quotes_present = len(re.findall(r'["][\w\s.:;,!?\\-]+["]',sent))>0
        question_present = "?" in sent
        if single_quotes_present or double_quotes_present or question_present :
            continue
        else:
            output.append(sent.strip(punctuation))
    return output
        
    
def summarize_text(full_text):
    print('Zacni povzetek')
    classifier = pipeline("summarization", "gpt2")
    #classifier(article)
    result = classifier(full_text)[0]["summary_text"]#model(full_text, min_length=60, max_length=500, ratio=0.4)
    print('Konec povzetek')
    summarized_text = ''.join(result)
    return summarized_text
        
def get_candidate_sents(resolved_text, ratio=0.3):
    candidate_sents = summarize_text(resolved_text)#summarize(resolved_text, ratio=ratio)
    candidate_sents_list = tokenize.sent_tokenize(candidate_sents)
    candidate_sents_list = [re.split(r'[:;]+',x)[0] for x in candidate_sents_list ]
    # Remove very short sentences less than 30 characters and long sentences greater than 150 characters
    filtered_list_short_sentences = [sent for sent in candidate_sents_list if len(sent)>30 and len(sent)<150]
    return filtered_list_short_sentences


def printmd(string):
    display(Markdown(string))
    
def get_flattened(t):
    sent_str_final = None
    if t is not None:
        sent_str = [" ".join(x.leaves()) for x in list(t)]
        sent_str_final = [" ".join(sent_str)]
        sent_str_final = sent_str_final[0]
    return sent_str_final
    

def get_termination_portion(main_string,sub_string):
    combined_sub_string = sub_string.replace(" ","")
    main_string_list = main_string.split()
    last_index = len(main_string_list)
    for i in range(last_index):
        check_string_list = main_string_list[i:]
        check_string = "".join(check_string_list)
        check_string = check_string.replace(" ","")
        if check_string == combined_sub_string:
            return " ".join(main_string_list[:i])
                     
    return None
    
def get_right_most_VP_or_NP(parse_tree,last_NP = None,last_VP = None):
    if len(parse_tree.leaves()) == 1:
        return get_flattened(last_NP),get_flattened(last_VP)
    last_subtree = parse_tree[-1]
    if last_subtree.label() == "NP":
        last_NP = last_subtree
    elif last_subtree.label() == "VP":
        last_VP = last_subtree
    
    return get_right_most_VP_or_NP(last_subtree,last_NP,last_VP)


def get_sentence_completions(key_sentences):
    sentence_completion_dict = {}
    for individual_sentence in key_sentences:
        sentence = individual_sentence.rstrip('?:!.,;')
        tree = benepar_parser.parse(sentence)
        last_nounphrase, last_verbphrase =  get_right_most_VP_or_NP(tree)
        phrases= []
        if last_verbphrase is not None:
            verbphrase_string = get_termination_portion(sentence,last_verbphrase)
            phrases.append(verbphrase_string)
        if last_nounphrase is not None:
            nounphrase_string = get_termination_portion(sentence,last_nounphrase)
            phrases.append(nounphrase_string)

        longest_phrase =  sorted(phrases, key=len,reverse= True)
        if len(longest_phrase) == 2:
            first_sent_len = len(longest_phrase[0].split())
            second_sentence_len = len(longest_phrase[1].split())
            if (first_sent_len - second_sentence_len) > 4:
                del longest_phrase[1]
                
        if len(longest_phrase)>0:
            sentence_completion_dict[sentence]=longest_phrase
    return sentence_completion_dict

def generate_false_statements(half_answer, num_statements):
    generate_max_tokens = int(4*len(half_answer.split()))
    generator = pipeline('text-generation', model='gpt2')
    results = generator(half_answer, max_length=generate_max_tokens, num_return_sequences=num_statements)
    #print(results)
    false_statements = []

    for i in range(num_statements):
        res = results[i]['generated_text'].replace('\n', ' ')
        candidate_sents_list = tokenize.sent_tokenize(res)
        first_sent = [re.split(r'[:;]+',x)[0] for x in candidate_sents_list ][0]
        false_statements.append(first_sent)
    return false_statements


def generate_true_and_false_statements(text):
    
    cand_sents = get_candidate_sents(text)
    filter_quotes_and_questions = preprocess(cand_sents)
    
    sent_completion_dict = get_sentence_completions(filter_quotes_and_questions)
    true_sentences = list(sent_completion_dict.keys())
    half_answers = sum(sent_completion_dict.values(), [])
    #print(true_sentences)
    #print(half_answers)
    
    false_sentences = []
    for a in half_answers:
        false_sentences.extend(generate_false_statements(a, 1))
    
    return {"true_statements": true_sentences,
            "false_statements": false_sentences}




if __name__=="__main__":
    results = generate_true_and_false_statements(article)
    
