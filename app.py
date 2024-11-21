from flask import Flask,render_template,request,jsonify
import mysql.connector
import testpaper
import google.generativeai as genai
# import validation
genai.configure(api_key="")
app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(host="localhost",user="root",passwd="root",database="interviewbase")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/registerpage')
def registerpage():
    return render_template('registration.html')
    
@app.route('/instructionspage')
def instructionspage():
    return render_template('instructions.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/get-questions',methods=['POST'])
def get_questions():
    data = request.json
    user_id = data.get('userId')  
    print(user_id)# Get userId from the frontend

    try:
        db=get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Step 1: Fetch user details
        user_query = "SELECT lastname,jobrole, experience FROM users WHERE userId = %s;"
        cursor.execute(user_query, (user_id,))
        user_info = cursor.fetchone()

        if not user_info:
            return jsonify({"status": "error", "message": "User not found"}), 404

        job_role = user_info['jobrole']
        experience = user_info['experience']
        question=testpaper.questions(job_role,experience)
        print(job_role,experience,question[0][1])
        #[1]
        if not question:
            return jsonify({"status": "error","message": "No questions found"}), 404

        return jsonify({"status": "success","name":user_info['lastname'] , "questions": question})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 500

    finally:
        cursor.close()
        db.close()
        

@app.route('/register', methods=['POST'])
def register():
    
    user_data = request.json
    userId = user_data.get('userId')
    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    email = user_data.get('email')
    password = user_data.get('password')
    college = user_data.get('college')
    phone_number = user_data.get('phone_number')
    branch = user_data.get('branch')
    yearofpass = user_data.get('yearofpass')
    jobrole = user_data.get('jobrole')
    experience = user_data.get('experience')
    dateofbirth = user_data.get('dateofbirth')
    
    insert_query = """
    INSERT INTO users (
        userId, firstname, lastname, email, password, college,
        phone_number, branch, yearofpass, jobrole, experience, dateofbirth
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Insert data into database
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(insert_query, (userId, firstname, lastname, email, password, college, phone_number, branch, yearofpass, jobrole, experience, dateofbirth))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'status': 'success'})
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)})
    
#for login validation
@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
    email = user_data.get('userid')
    password = user_data.get('password')
    query = "SELECT * FROM users WHERE userid = %s AND password = %s"
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        if user:   
            return jsonify({'status': 'success', 'message': 'Login successful', 'userId': user['userId']})
        else:  
            return jsonify({'status': 'error', 'message': 'Invalid email or password'})
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)})
    finally:
        cursor.close()
        connection.close()   

@app.route('/receive-list', methods=['POST'])
def receive_list():
    data = request.get_json()  # Get the JSON data from the request
    if 'list' in data:
        received_list = data['list']
        # print("Received list:", received_list)
        # Example response back to the frontend
        c=score(received_list)
        conn=get_db_connection()
        cur=conn.cursor()
        query="""insert into results (userid,correct,wrong,partial,not_attempted,score)
        values(%s,%s,%s,%s,%s,%s)"""
        try:
            cur.execute(query,[data['user']]+list(c))
            print("inserted")
            conn.commit()
            conn.close()
        except Exception as e:
            print("error",e)
        return jsonify({"message": "List received successfully!", "received_list": received_list})
    return jsonify({"error": "No list received"}), 400
@app.route("/sendresults", methods=["POST"])
def send_results():
    data = request.json
    user_id = data.get('userId')
    conn=get_db_connection()
    cur=conn.cursor()
    query="select firstname,lastname,jobrole from users where userid=%s"
    cur.execute(query,(user_id,))
    user = cur.fetchone()
    conn.close()
    if user: 
        conn=get_db_connection()
        cur=conn.cursor()
        query="select * from results where userid=%s"
        cur.execute(query,(user_id,))
        results=cur.fetchone()
        conn.close()
        if results:
            return jsonify({'status': 'success', 'message': 'Login successful','userdetails':user, 'results': results})
        else:
            return jsonify({'status': 'error', 'message': 'results not announced'})
    else:  
        return jsonify({'status': 'error', 'message': 'Invalid email or password'})
    
    
n=24
def validate_gemini(id,ans):
    try:
        conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="interviewbase")
        cur=conn.cursor()
        print(id)
        cur.execute("select question from questionbank where questionId=%s",[id])
        correctans=cur.fetchone()
        conn.close()
        print(correctans)
    except Exception as e:
        n-=1
        print("Error",e)
    try:
        prompt = """you are a question validator. i will give you the both question and answer you have to check wheather the answer was correct or not with respect to the question. you have to tell wheather the question was  correct or  wrong or partially correct select one from the above  and another was how much percent it was correct give the value 0-100 / i want two values as output seperated with comma. if iam not provide any one of  return wrong. the question was:  """
         
        question=correctans[0]
        answer=""" \n the answer is: """+ans
        prompt=prompt+question+answer
        model = genai.GenerativeModel('gemini-pro')
        responses = model.generate_content(
            prompt,
        )
        return responses.text
    except Exception as e:
        n=1
        print(e)

def score(questions):
    
    correct,wrong,partial,not_attempt=0,0,0,0
    score = 0
    for i in range(len(questions)):
        if questions[i][1]==None:
            not_attempt += 1
        else:
            try:
                response=validate_gemini(questions[i][0],questions[i][1])
                response=list(response.split(","))
                score+=int(response[1].strip())
                if response[0].lower()=='correct':
                    correct+=1
                elif response[0].lower()=='wrong':
                    wrong+=1
                else:
                    partial+=1
            except Exception as e:
                pass
    return [correct,wrong,partial,not_attempt,score/n]

  
if __name__ == '__main__':
    app.run(debug=True)
