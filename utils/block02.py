from __future__ import unicode_literals
import configargparse
from onmt.translate.translator import build_translator
import onmt.opts as opts
import io
import os
from tempfile import NamedTemporaryFile

def add_padding(line):    
    l= len(line.strip().split(' '))
    padding = ""
    num_of_pads = 50 - l - 1
    for i in range(num_of_pads):
        padding += "<blank> "
    out_line = " ".join(line.strip().split(' ')) + " </s> " + padding + "\n"
    
    return out_line
	

def create_temp_file(text):

    temp_file = NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False)
    temp_file.write(text)
    temp_file.close()
    
    return temp_file
	
	
def get_final_ans(opt, ques_text, ans_text):
    
    ques_text = ques_text.lower().replace('"', '')
    ans_text = ans_text.lower().replace('"', '').replace('.', '')
    
    ques_file = create_temp_file(add_padding(ques_text))
    ans_file = create_temp_file(add_padding(ans_text))
    
    translator = build_translator(opt, report_score=False)
    
    ot = translator.translate(
            src=ques_file.name,
            tgt=None,
            ans=ans_file.name,
            src_dir=opt.src_dir,
            batch_size=opt.batch_size,
            attn_debug=opt.attn_debug
            )
    
    os.remove(os.path.join(ques_file.name))
    os.remove(os.path.join(ans_file.name))
    #os.remove(os.path.join("pred.txt"))
    
    return ot[1][0][0]