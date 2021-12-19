import request
from bs4 import BeautifulSoup as bs , NavigableString
import config
import re
import json
import db
from pprint import pprint
from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint

console = Console()

class Question:

    def __init__(self,question_id,question_dict):
        # print(question_dict)
        self.question_id = question_id
        self.input = question_dict['input']
        self.problem_languages = question_dict['problem_languages']
        self.input_code = question_dict['initial_user_func']
        self.custom_input = question_dict['custom_input']

    def __str__(self):
        return self.question_id

    def get_languages(self):
        languages = [] 
        for key in self.problem_languages.keys():
            languages.append((key,self.problem_languages[key]))
        return languages

    def get_intial_code(self,language:str='cpp') -> str:
        # print(self.input_code)string
        initial_code = self.input_code[language]
        code = initial_code['initial_code']
        if language == 'cpp':
            code = code.replace('//Position this line where user code will be pasted.',"\n\n{}\n\n\n\n\n".format(initial_code['user_code']))
        else:
            code += initial_code['user_code']
        return code

    def get_custom_input(self) -> str:
        return  (self.custom_input).replace('\r\n','\n').lstrip().rstrip()


def fetch_question(question_id:str):
    cookies = config.get_cookies()
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    resp = request.get(f'/problems/{question_id}/1',cookies=cookies,headers=headers)
    if resp.status_code == 404:return None
    soup = bs(resp.content,'lxml')
    # print(soup)
    filter_func = lambda x: x.text.find('Input Format:') != -1
    input_format = soup.find_all('div',{'class':'modal-body'})
    # print(input_format)
    custom_input = list(filter(filter_func,input_format))[0]
    custom_input_text = ""
    for i in custom_input.contents:
        tag = i.name
        if tag == 'textarea':break
        if isinstance(i,NavigableString):
            custom_input_text += (i.string)
        else:
            custom_input_text += (i.text)
    scripts = soup.find_all('script')
    pattern = r'var currentProblem =(.*);'
    problem_str = None
    for script in scripts:
        if script.string:
            match = re.search(pattern,script.string)
            if match:
                problem_str = match.group(1).strip()
                break
    if problem_str:
        problem_str = json.loads(problem_str)
        problem_str['custom_input'] = custom_input_text
        problem_str = json.dumps(problem_str)
    return problem_str
   
def get_question(question_id:str) -> Question:
    question = db.find_question(question_id)
    if not question:
        question = fetch_question(question_id) 
        if not question:
            rprint("[red]Question not found")
        # print(question)
        db.save_question(question_id,question)
    # TODO Return None if not found
    question = Question(question_id,json.loads(question))
    return question
    
def show_question(question_id:str,status=None) -> None:
    resp = request.get(f'/problems/{question_id}/1')
    soup = bs(resp.content,'lxml')
    problem_statement = soup.find('div',{'class':'problem-statement'}).text
    if status:status.stop()
    # print(problem_statement)
    syntax = Syntax(problem_statement,'text',word_wrap=True)
    console.print(syntax)


if __name__ == '__main__':
    question = get_question('largest-element-in-array4009')
    print(question.get_custom_input())
    # print(question.get_intial_code())
