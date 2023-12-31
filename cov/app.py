from flask import Flask,request,render_template,jsonify
import requests,time
from jieba.analyse import extract_tags
import utils,string
from utils import get_time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route("/time")
def get_time():

    return utils.get_time()

@app.route("/c1")
def get_c1_data():
    data=utils.get_c1_data()
    return jsonify({"confirm": data[0], "suspect": data[1], "heal": data[2], "dead":data[3]})

@app.route("/c2")
def get_c2_data():
    data = utils.get_c2_data()
    res=[]
    for tup in data:
        # print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

@app.route("/l1")
def get_l1_data():
    data=utils.get_l1_data()
    day,confirm,suspect,heal,dead=[],[],[],[],[]
    for a,b,c,d,e in data:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day":day,"confirm":confirm,"suspect":suspect,"heal":heal,"dead":dead})

@app.route("/l2")
def get_l2_data():
    data=utils.get_l2_data()
    day,confirm_add,suspect_add=[],[],[]
    for a,b,c in data:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day":day,"confirm_add":confirm_add,"suspect_add":suspect_add})

@app.route("/r1")
def get_r1_data():
    data= utils.get_r1_data()
    city=[]
    confirm=[]
    for k, v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city":city,"confirm":confirm})

@app.route("/r2")
def get_r2_data():
    data=utils.get_r2_data()
    d=[]
    for i in data:
        k = i[0].rstrip(string.digits)  # 移除热搜数字
        v = i[0][len(k):]  # 获取热搜数字
        ks = extract_tags(k)  # 使用jieba提取关键字
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})

    return jsonify({"kws": d})


@app.route("/login")
def hello_world2():
    name=request.values.get("name")
    pwd=request.values.get("pwd")
    return f'name={name},pwd={pwd}'

@app.route("/abc")
def hello_world1():
    id1 = request.values.get("id1")

    return f"""
    <form action="/login">
    账号:<input name="name",value="{id1}"><br>
    密码:<input name="pwd">
    <input type="submit">
    </form>
    """

@app.route('/tem')
def hello_world3():
    return render_template("index.html")

@app.route('/ajax',methods=['GET','POST'])
def hello_world4():
    name=request.values.get(("name"))
    score=request.values.get("score")
    print(f'name:{name},score:{score}')
    return '10000'



if __name__ == '__main__':
    app.run()
