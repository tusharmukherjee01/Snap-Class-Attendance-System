from src.database.config import supabase
import bcrypt

def check_teacher_exist(username):
    try:
        response = supabase.table('teachers').select('*').eq('username', username).execute()
        return len(response.data) > 0
    except Exception as e:
        print("Error checking teacher existence:", e)
        return False

def create_teacher(teacher_name, teacher_username, teacher_password):
    if check_teacher_exist(teacher_username):
        return {"success": False, "message": "Username already exists."}
    
    hashed_password = bcrypt.hashpw(teacher_password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        response = supabase.table('teachers').insert({
            'name': teacher_name,
            'username': teacher_username,
            'password': hashed_password.decode('utf-8')
        }).execute()
        return {"success": True, "message": "Teacher created successfully."}
    except Exception as e:
        print("Error creating teacher:", e)
        return {"success": False, "message": "Failed to create teacher."}


def teacher_login(username, password):
    try:
        response = supabase.table('teachers').select('*').eq('username', username).execute()
        
        if len(response.data) == 0:
            return {"success": False, "message": "Username not found."}
        
        teacher = response.data[0]
        stored_password = teacher['password'].encode('utf-8')
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return {"success": True, "message": "Login successful.", "teacher": teacher}
        else:
            return {"success": False, "message": "Incorrect password."}
    except Exception as e:
        print("Error fetching teacher:", e)
        return {"success": False, "message": "Failed to fetch teacher."}


def get_all_students():
    response = supabase.table('students').select('*').execute()
    return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    
    data = {'name':new_name,'face_embedding':face_embedding,'voice_embedding':voice_embedding}
    response = supabase.table('students').insert(data).execute()
    
    return response.data

def create_subject(sub_code,name,section,teacher_id):
    data = {"subject_code":sub_code,"name":name,"section":section,"teacher_id":teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subject(teacher_id):
    response = supabase.table('subjects').select("*, subject_student(count), attendance_log(timestamp)").eq("teacher_id",teacher_id).execute()
    
    subjects = response.data
    
    for sub in subjects:
        sub["total_students"] = sub.get("subject_student",[{}])[0].get('count',0) if sub.get('subject_student') else 0
        attendance = sub.get('attendance_log',[])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions
        
        
        sub.pop('subject_student', None)
        sub.pop('attendance_log', None)
        
    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id':student_id,"subject_id":subject_id}
    response = supabase.table("subject_student").insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table("subject_student").delete().eq("student_id",student_id).eq("subject_id",subject_id).execute()   
    return response.data 

def get_student_subjects(student_id):
    response = supabase.table('subject_student').select("*, subjects(*)").eq('student_id',student_id).execute()
    return response.data

def get_students_attendance(student_id):
    response = supabase.table('attendance_log').select("*, subjects(*)").eq('student_id',student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table('attendance_log').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_log').select("*,subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data
    
    