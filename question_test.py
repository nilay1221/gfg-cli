import question as qst
import request
import config
import time
from rich import print as rprint
from rich.status import Status
from typing import Dict
import traceback
import sys

SOURCE = 'https://practice.geeksforgeeks.org'



def _get_result(post_url:str,data:Dict,cookies:Dict,sub_type:str) -> Dict:
    response = request.post(post_url,data=data,cookies=cookies).json()
    sub_id = response['results']['submission_id']
    result = None
    data = {'sub_id':sub_id,'sub_type':sub_type}
    for _ in range(10):
        sub_res = request.post('/problems/submission/result/',data=data,cookies=cookies).json()
        if sub_res['status'] == 'SUCCESS':
            result = sub_res
            break
    if result:
        return result
    else:
        raise Exception()

def test_code(question_id:str,code:str,language:str,inp:str=None,status:Status=None):
    # start_time = time.time()
    try:
        question = qst.get_question(question_id)
        # https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
        code_input = question.input if inp is None else bytes(inp,'utf-8').decode('unicode_escape')
        data = {'request_type':'testSolution','input':code_input,'code':code,'language':language,'source':SOURCE}
        judge_data = {'request_type':'expectedOutput','input':code_input,'source':SOURCE}
        cookies = config.get_cookies()
        post_url = '/problems/' + question_id + '/compile/'
        code_result = _get_result(post_url,data,cookies,sub_type='testSolution')
        judge_result = _get_result(post_url,judge_data,cookies,sub_type='expectedOutput')
        sub_result = (code_result)['message']
        if status:status.stop()
        sanitize = lambda x:x.replace('\r\n','\n')
        if code_result['view_mode'] == 'compilation':
            output_str = []
            output_str.append('[bold red]Compilation Error[/bold red]')
            output_str.append(sanitize(sub_result['error']))
            rprint('\n'.join(output_str))
        elif code_result['view_mode'] == 'runtime':
            output_str = []
            output_str.append('[bold red]Runtime Error[/bold red]')
            output_str.append(sanitize(sub_result['error']))
            rprint('\n'.join(output_str))
        else:
            output_str = []
            output_str.append('[bold green]Success[/bold green]')
            output_str.append('Your input is \n{}\n'.format(sanitize(sub_result['input'])))
            output_str.append('Your output is \n{}'.format(sanitize(sub_result['output'])))
            output_str.append('Expected Output is \n{}'.format(sanitize(judge_result['message']['output'])))
            rprint('\n'.join(output_str))
            # print('''Your input is\n{}\n\nYour output is\n{}\nExpected Output\n{}'''.format(sub_result['input'],sub_result['output'],judge_result['message']['output']))
    except Exception as e:
        traceback.print_exc()
        print(e)
        print('Something went wrong. Please try again later')


