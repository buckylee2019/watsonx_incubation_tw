import re
import os
import json
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

financial_word_list_CN2EN = """
CN: 金钱买不来幸福。 但它可以让生活变得更加舒适。
EN: Money can't buy happiness, but it can make life more comfortable.
"""

financial_word_list_EN2CN = """
EN: Money can't buy happiness, but it can make life more comfortable.
CN: 金钱买不来幸福。 但它可以让生活变得更加舒适。
EN: Saving money for the future is a wise financial decision.
CN: 为未来存钱是明智的财务决定
EN: He lost all his money in a high-stakes poker game.
CN: 他在一场高风险的扑克游戏中输掉了所有的钱。
EN: Investing in stocks can be a way to grow your wealth.
CN: 投资股票可以成为增加财富的一种方式。
EN: She's been working hard to improve her financial situation.
CN: 她一直在努力改善自己的财务状况。
EN: The cost of living in the city is quite high.
CN: 城市的生活成本相当高。
EN: My monthly salary is deposited directly into my bank account.
CN: 我的每月工资直接存入我的银行账户。
EN: He's been struggling with credit card debt for years.
CN: 多年来，他一直在与信用卡债务作斗争。
EN: They are planning for their retirement savings.
CN: 他们正在规划自己的退休储蓄。
EN: Financial literacy is essential for making informed money decisions.
CN: 金融知识对于做出明智的财务决策至关重要。
EN: You have money for emergencies
CN: 你有钱应付紧急情况
EN: ten percent
CN: 百分之十
EN: 10%
CN: 百分之十
EN: yes
CN: 是的
EN: no
CN: 不是
EN: The World Bank is located in Washington D.C.
CN: 世界银行位于华盛顿特区
"""

def send_to_watsonxai(prompts,
                    model_name="google/flan-ul2",
                    decoding_method="greedy",
                    max_new_tokens=200,
                    min_new_tokens=30,
                    temperature=1.0,
                    repetition_penalty=1.0
                    ):
    '''
   helper function for sending prompts and params to Watsonx.ai
    
    Args:  
        prompts:list list of text prompts
        decoding:str Watsonx.ai parameter "sample" or "greedy"
        max_new_tok:int Watsonx.ai parameter for max new tokens/response returned
        temperature:float Watsonx.ai parameter for temperature (range 0>2)
        repetition_penalty:float Watsonx.ai parameter for repetition penalty (range 1.0 to 2.0)
    Returns: None
        prints response
    '''

    assert not any(map(lambda prompt: len(prompt) < 1, prompts)), "make sure none of the prompts in the inputs prompts are empty"

    # Instantiate parameters for text generation
    model_params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: temperature,
        GenParams.REPETITION_PENALTY: repetition_penalty,
    }


    # Instantiate a model proxy object to send your requests
    model = Model(
        model_id=model_name,
        params=model_params,
        credentials=creds,
        project_id=project_id)

    output = []
    for prompt in prompts:
        o = model.generate_text(prompt)
        output.append(o)
    return output

def get_translator_model(creds, project_id):
    decoding_method="greedy"
    max_new_tokens=500
    min_new_tokens=1
    temperature=1.0
    repetition_penalty=1.0

    model_params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: temperature,
        GenParams.REPETITION_PENALTY: repetition_penalty,
    }
    model = Model(
        model_id="meta-llama/llama-2-70b-chat",
        params=model_params,
        credentials=creds,
        project_id=project_id)

    return model


def preprocessEN2CN(translator_gen):
    result_list = translator_gen.split('\n')
    sentence = ''
    for s in result_list:
        if 'CN' in s:
            sentence = s
            break
    result = sentence.split('CN:')[-1]
    return result


def preprocessCN2EN(translator_gen):
    result_list = translator_gen.split('\n')
    sentence = ''
    for s in result_list:
        if 'EN' in s:
            sentence = s
            break
    result = sentence.split('EN:')[-1]
    return result

def postprocessEN2CN(text):
    # Define a regular expression pattern to match English words and alphabet characters
    pattern = r'[a-zA-Z]+(): '

    # Use the sub() function to replace matches with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def postprocessCN2EN(text):
    # Define a regular expression pattern to match Thai characters
    pattern = r'[ก-๏]+'
    # Use the sub() function to replace matches with an empty string
    cleaned_text = re.sub(pattern, '', text)
    result = cleaned_text.replace('\n', '')
    return result


def llm_translator_prompt(financial_word_list, sentence, mode='EN2CN'):

    if mode == 'EN2CN':
        prompt = f"""
        INSTRUCTION: 
            Translate the word into Thai language. Start the sentence by the translated TH.
            using below example
        EXAMPLE: 
            {financial_word_list}
        INPUT:
            EN: {sentence} ,
            CN:
        """
    else:
        prompt = f"""
        INSTRUCTION: 
            帮忙把英语翻译成简体中文 使用示例中的格式
            Translate the word into English language. Start the sentence by the translated EN.
        EXAMPLE: 
            {financial_word_list}
        INPUT:
            CN: {sentence} ,
            EN:
        """

    return prompt


def llm_translator(prompt, model, mode='EN2CN'):
    translator_response = model.generate_text(prompt)
    translator_gen = translator_response
    # print(translator_response)

    if mode=='EN2CN':
        result = preprocessEN2CN(translator_gen)
    else:
        result = preprocessCN2EN(translator_gen)
    print(result)

    return result


def question_prompt(sentence):
    prompt = f'''
<s>[INST] <<SYS>>
INSTRUCTION:
你是一位金融专家。 并用中文简短回答
Please answer in Chinese, you are the financial advisor. Answer in short and brief.
Produce the answer using the steps as below.
        Step 1: Understand the QUESTION.
        Step 2: WRITE the brief and easy ENGLISH answer.
        Step 3: Translate the brief and easy ENGLISH answer into Chinese language.
        Step 4: Rewrite Step 4 into Chinese simple Answer for kid in Chinese language.
AVOID the new line as much as possible.
Start your response with 'Sure, I can answer in Chinese. Here's my response:'
<</SYS>>
INPUT:
QUESTION: {sentence}
Step 1: Understand QUESTION: 
Step 2: ENGLISH BRIEF ANSWER:
Step 3: CHINESE TRANSLATED ANSWER:
Step 5: REWRITE INTO SIMPLE CHINESE ANSWER: 
[/INST]
    '''
    return prompt
IBM - Office of the CIO
IBM - Office of the CIO
