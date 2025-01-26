from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 谜题数据
riddles = [
    {
        "question": "欢迎来玩解密游戏！\n准备好了吗？输入：好",
        "answer": "好",
        "reward": "太棒了！让我们开始吧~"
    },
    {
        "question": "我最喜欢的人是谁？\n(提示：这个人正在玩这个游戏)",
        "answer": "你",
        "reward": "你真聪明~我最喜欢你了！"
    },
    {
        "question": "猜猜我的心是什么颜色？\n(提示：是一种很浪漫的颜色)",
        "answer": "粉色",
        "reward": "没错！因为被你染成粉色啦~"
    },
    {
        "question": "1+1=?\n(提示：不是2哦)",
        "answer": "我们",
        "reward": "1+1=我们，永远在一起！"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    riddle_id = int(data['riddle_id'])
    answer = data['answer']
    
    if riddle_id >= len(riddles):
        return jsonify({'status': 'finished'})
    
    if answer == riddles[riddle_id]['answer']:
        return jsonify({
            'status': 'correct',
            'reward': riddles[riddle_id]['reward'],
            'next_question': riddles[riddle_id + 1]['question'] if riddle_id + 1 < len(riddles) else None
        })
    else:
        return jsonify({
            'status': 'wrong',
            'message': '答错啦，再想想~'
        })

app = app.wsgi_app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
