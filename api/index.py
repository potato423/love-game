from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>解密游戏</title>
        <style>
            body { text-align: center; padding: 20px; }
            input { margin: 10px; padding: 5px; }
            button { margin: 10px; padding: 5px 10px; }
        </style>
    </head>
    <body>
        <div id="question"></div>
        <input type="text" id="answer" placeholder="输入答案">
        <button onclick="checkAnswer()">提交</button>
        <div id="message"></div>
        <script>
            let currentRiddle = 0;
            
            function init() {
                document.getElementById('question').textContent = "欢迎来玩解密游戏！\\n准备好了吗？输入：好";
            }
            
            function checkAnswer() {
                const answer = document.getElementById('answer').value;
                fetch('/check_answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        riddle_id: currentRiddle,
                        answer: answer
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'correct') {
                        document.getElementById('message').textContent = data.reward;
                        document.getElementById('answer').value = '';
                        currentRiddle++;
                        setTimeout(() => {
                            if (data.next_question) {
                                document.getElementById('question').textContent = data.next_question;
                                document.getElementById('message').textContent = '';
                            } else {
                                document.getElementById('question').textContent = '恭喜通关！';
                                document.getElementById('answer').style.display = 'none';
                                document.querySelector('button').style.display = 'none';
                            }
                        }, 2000);
                    } else {
                        document.getElementById('message').textContent = '答错了，再试试！';
                    }
                });
            }
            
            window.onload = init;
        </script>
    </body>
    </html>
    '''

@app.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        data = request.get_json()
        riddle_id = int(data['riddle_id'])
        answer = data['answer']
        
        if riddle_id >= len(riddles):
            return jsonify({'status': 'finished'})
        
        if answer == riddles[riddle_id]['answer']:
            next_question = riddles[riddle_id + 1]['question'] if riddle_id + 1 < len(riddles) else None
            return jsonify({
                'status': 'correct',
                'reward': riddles[riddle_id]['reward'],
                'next_question': next_question
            })
        else:
            return jsonify({
                'status': 'wrong',
                'message': '答错啦，再想想~'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Vercel handler
def handler(request):
    with app.request_context(request):
        return app.handle_request()
