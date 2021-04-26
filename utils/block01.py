import torch
import json 
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

def find_ans_pt1(model, tokenizer, text, question):
    
    text = text.strip().replace("\n","")
    
    inputs = tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]


    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores = model(**inputs)[0]
    answer_end_scores   = model(**inputs)[1]


    answer_start = torch.argmax(answer_start_scores)  
    answer_end = torch.argmax(answer_end_scores) + 1  

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    
    ans_start_token = tokenizer.convert_ids_to_tokens(input_ids[answer_start])

    if (ans_start_token == "[CLS]" or ans_start_token == "" or ans_start_token == "[SEP]" or ans_start_token == '') :
        answer = ""
        
    return answer
