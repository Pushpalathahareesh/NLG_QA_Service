from flask import Flask, jsonify,request
from lib.memory_manager.memory_manager import MemoryManager
from lib.memory_manager.redis import Redis
from lib.nlg.nlg import Nlg
from util.config_manager import Config

app = Flask(__name__)
memory = MemoryManager()
nlg = Nlg()
#gen=answer_generate()
config = Config()
system_config = config.system_config()
#model,tokenizer=nlg.get_model1()
#opt=nlg.get_model2()
@app.route('/init', methods=['POST'])
def session_start_update():
    response = {'status': 'S001'}
    data = request.get_json()

    try:
        if 'id' in data and 'paragraph' in data :
           status=memory.set('paragraph',data['id'],data['paragraph'])
           print(status)
        else:
            response['status'] = 'E001'
    except:
        response['status'] = 'E001'

    return jsonify(response)


@app.route('/generate', methods=['POST'])
def talk():
    response = {'status': 'S001'}
    data = request.get_json()

    try:
        if 'id' in data and 'query' in data:
            #id = data['id']
            #question = data['query']
            #scope = "paragraph"
            # knowledge_base=data['para']
            # print(memory.get('paragraph',id))
            knowledge_base = memory.get("paragraph",data['id'])
            print(knowledge_base)

            #answer = gen.generate(question, knowledge_base,nlg)
            #print(answer)
            response['data'] = {
                'id': data['id'],
                'response': nlg.generate(data['query'], knowledge_base) #'response': nlg.generate(data['query'],paragraph)
            }
        else:
            response['status'] = 'E001'
    except:
        response['status'] = 'E001'

    return jsonify(response)


if __name__ == '__main__':
    app.run(host="localhost", port=system_config['port'], debug=True) # Use the config to load the port