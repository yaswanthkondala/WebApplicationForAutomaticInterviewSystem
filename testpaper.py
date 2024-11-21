import mysql.connector
def fetch_questions(n, m, o, subjects):
    connection=mysql.connector.connect(host="localhost",user="root",passwd="root",database="interviewbase")

    try:
        with connection.cursor() as cursor:
            # Prepare the subject list for the SQL query
            subject_list = ', '.join(f"'{subject}'" for subject in subjects)
            
            # MySQL query to fetch n easy, m medium, and o hard questions
            query = f"""
                (
                    SELECT questionId, question, subject, difficulty
                    FROM questionbank
                    WHERE difficulty = 'easy' 
                    AND subject IN ({subject_list})
                    ORDER BY RAND()
                    LIMIT {n}
                )
                UNION ALL
                (
                    SELECT questionId, question, subject, difficulty
                    FROM questionbank
                    WHERE difficulty = 'medium' 
                    AND subject IN ({subject_list})
                    ORDER BY RAND()
                    LIMIT {m}
                )
                UNION ALL
                (
                    SELECT questionId, question, subject, difficulty
                    FROM questionbank
                    WHERE difficulty = 'hard' 
                    AND subject IN ({subject_list})
                    ORDER BY RAND()
                    LIMIT {o}
                );
            """
            
            # Execute the query
            cursor.execute(query)
            
            # Fetch the results
            results = cursor.fetchall()
            
            # Return the fetched questions
            return results

    finally:
        # Close the database connection
        connection.close()

# 1:fullstack
# 2:frontend developer
# 3:data analyst
# 4:data scientist
# 5:devops engineer
# 6:backend developer
# 7:associative software engineer

def generateQuestion(topics,exp):
        if exp<5:
            return fetch_questions(15,6,3,topics)
        if exp>=5 and exp<10:
            return fetch_questions(3,15,6,topics)
        else:
            return fetch_questions(3,6,15,topics)
def generate(ch,exp):
    
    if ch=="fullstack":
        topics=tuple(['JS', 'HTML&CSS','MERN','SQL'])
        
        return generateQuestion(topics,exp)   
    elif ch=="frontend developer":
        topics=tuple(['java','JS','python', 'HTML&CSS','DataStructures','DBMS','Django','MERN','SQL','Linux','Unix'])
        return generateQuestion(topics,exp)
    elif ch=="data analyst":
        topics=tuple(['python', 'DataAnalytics','ML','Power BI','statistics','SQL','EDA','BigData','MS-Office'])
        return generateQuestion(topics,exp)
    elif ch=="data scientist":
        topics=tuple(['python', 'DataAnalytics','ML','statistics','SQL','EDA','MLOps','DL','BigData'])
        return generateQuestion(topics,exp)
    elif ch=="devops engineer":
        topics=tuple(['SQL','Linux','Unix','python','DataStructures','CN','MLOps'])
        return generateQuestion(topics,exp)
        
    elif ch=="backend developer":
        topics=tuple(['java','JS','python','DataStructures','DBMS','CN','HTML&CSS','MERN','SQL'])
        return generateQuestion(topics,exp)
        
    elif ch=="associative software engineer":
        topics=tuple(['java','JS','python','DataStructures','SQL'])
        return generateQuestion(topics,exp)
        
def questions(jobrole,exp):
    return generate(jobrole,exp)