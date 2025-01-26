from flask import Flask, jsonify, request

app = Flask(__name__)

# HTML 内容直接写在这里
HTML_CONTENT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>给可爱的你的解密游戏 ❤</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #fff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        .question {
            white-space: pre-line;
            margin: 20px 0;
            font-size: 1.2em;
            color: #333;
        }
        .input-box {
            width: 80%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #000;
            border-radius: 5px;
            font-size: 1.1em;
        }
        .submit-btn {
            background-color: #ffc0cb;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1.1em;
            color: #fff;
            cursor: pointer;
            margin: 10px 0;
        }
        .message {
            margin: 20px 0;
            font-size: 1.1em;
            color: #ffc0cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="question" class="question"></div>
        <input type="text" id="answer" class="input-box" placeholder="在这里输入答案">
        <button onclick="checkAnswer()" class="submit-btn">确认</button>
        <div id="message" class="message"></div>
    </div>

    <script>
        let currentRiddle = 0;
        
        function init() {
            document.getElementById('question').textContent = "欢迎来玩解密游戏！\\n准备好了吗？输入：好";
        }

        function checkAnswer() {
            const answer = document.getElementById('answer').value;
            
            fetch('/check_answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
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
                            document.getElementById('question').textContent = '恭喜通关！爱你哦~';
                            document.getElementById('answer').style.display = 'none';
                            document.querySelector('.submit-btn').style.display = 'none';
                        }
                    }, 2000);
                } else if (data.status === 'wrong') {
                    document.getElementById('message').textContent = data.message;
                }
            });
        }

        window.onload = init;

        document.getElementById('answer').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkAnswer();
            }
        });
    </script>
</body>
</html>
'''

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return HTML_CONTENT, 200, {'Content-Type': 'text/html; charset=utf-8'}

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

def handler(request):
    if request.method == 'POST' and request.path == '/check_answer':
        with app.request_context(request):
            return check_answer()
    return catch_all('')
