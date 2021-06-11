import question as qst
import request
import config
import time
from rich import print as rprint
from rich.status import Status
from typing import Dict

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
        code_input = question.input if inp is None else inp
        data = {'request_type':'testSolution','input':code_input,'code':code,'language':language,'source':SOURCE}
        judge_data = {'request_type':'expectedOutput','input':code_input,'source':SOURCE}
        cookies = config.get_cookies()
        post_url = '/problems/' + question_id + '/compile/'
        code_result = _get_result(post_url,data,cookies,sub_type='testSolution')
        judge_result = _get_result(post_url,judge_data,cookies,sub_type='expectedOutput')
        sub_result = (code_result)['message']
        if status:status.stop()
        if code_result['view_mode'] == 'compilation':
            rprint('[bold red]Compilation Error')
            print(sub_result['error'])
        elif code_result['view_mode'] == 'runtime':
            rprint('[bold red]Runtime Error')
            print(sub_result['error'])
        else:
            rprint('[bold green]Success')
            print('''Your input is\n{}\n\nYour output is\n{}\nExpected Output\n{}'''.format(sub_result['input'],sub_result['output'],judge_result['message']['output']))
    except Exception as e:
        # print(e)
        print('Something went wrong. Please try again later')


