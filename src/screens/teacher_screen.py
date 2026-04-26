import streamlit as st
from src.ui.base_layout import style_background_dashboard
from src.ui.base_layout import style_base_layout
from src.components.header import header_dashboard
from src.database.db import create_teacher,teacher_login,get_teacher_subject
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_Register()
    
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    
    with c1:
      header_dashboard()
    with c2:
        st.subheader(f"""Welcome {teacher_data['name']}""")
        if st.button("Logout",type='secondary',key='logoutbtn',shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()
        
    st.space()
    
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1,tab2,tab3 = st.columns(3)
    
    with tab1:
        type1 = type3 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if  st.button("Take Attendance",type = type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()  
    
    with tab2:
        type2 = type3 = "primary" if st.session_state.current_teacher_tab == 'manage_subject' else "tertiary"
        if st.button("Manage Subject", type = type2 ,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()
    
    with tab3:
       type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
       if st.button("Attendance Records", type = type3 ,width='stretch',icon=':material/cards_stack:'):
        st.session_state.current_teacher_tab = 'attendance_records'
        st.rerun()
    
    st.divider()
    
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    
    if st.session_state.current_teacher_tab == "manage_subject":
        teacher_tab_manage_subject()
    
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_record()

def teacher_tab_take_attendance():
    st.header("TAKE ATTENDANCE")

def teacher_tab_manage_subject():
    
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1,col2 = st.columns(2)
    with col1:
      st.header("MANAGE SUBJECT",width="stretch")
    
    with col2:
       if st.button("Create New Subject",width="stretch"):
           create_subject_dialog(teacher_id)
    
    #List all subject
    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            
            def share_btn():
                if st.button(f"Share Code:{sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                st.space()
                    
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = stats,
                footer_callback=share_btn           
            )
        
    else:
        st.info("No Subject Found. Create One Above")
        
        
        
            
def teacher_tab_attendance_record():
    st.header("ATTENDANCE RECORD")
    

def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher.get("success"):
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher["teacher"]
        st.session_state.logged_in = True
        return True
    return False


def teacher_screen_login():
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    
    with c1:
      header_dashboard()
    with c2:
        st.button("← Back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace" ,on_click=lambda: st.session_state.update({'login_type': None}))
        
    st.header("Login to Your Teacher Profile",text_alignment='center')
    st.space()
    teacher_username = st.text_input("Username",placeholder="Enter your username",key='login_username')
    teacher_password = st.text_input("Password",placeholder="Enter your password",type='password',key='login_password')
    
    st.divider() 
    
    btnc1,btnc2 = st.columns(2)
    
    with btnc1:
         if st.button("Login",type='secondary',icon=':material/passkey:',width='stretch',key='teacher_login_btn'):
             if teacher_username and teacher_password:
                 if login_teacher(teacher_username, teacher_password):
                    st.toast("welcome back!", icon="👋")
                    import time
                    time.sleep(1)
                    st.rerun()
                 else:
                     st.error("Invalid username or password")
             else:
                 st.warning("Please enter both username and password")
    
    with btnc2:
       if st.button("Register Instead",type='primary',icon=':material/person_add:',width='stretch',key='teacher_switch_register_btn'):
           st.session_state['teacher_login_type'] = 'register'
           st.rerun()
            

def teacher_screen_Register():
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    
    with c1:
      header_dashboard()
    with c2:
        st.button("← Back to Home",type='secondary',key='regibackbtn',shortcut="control+backspace" ,on_click=lambda: st.session_state.update({'login_type': None}))
        
    st.header("Register Your Teacher Profile",text_alignment='center')
    st.space()
    teacher_name = st.text_input("Full Name",placeholder="Enter your full name",key='register_name')
    teacher_username = st.text_input("Username",placeholder="Choose a username",key='register_username')
    teacher_password = st.text_input("Password",placeholder="Create a password",type='password',key='register_password')
    teacher_confirm_password = st.text_input("Confirm Password",placeholder="Re-enter your password",type='password',key='register_confirm_password')
    
    st.divider()
    
    btnc1,btnc2 = st.columns(2)
    
    with btnc1:
        if st.button("Register",type='secondary',icon=':material/person_add:',width='stretch',key='teacher_register_btn'):
                if teacher_name and teacher_username and teacher_password and teacher_confirm_password:
                    if teacher_password == teacher_confirm_password:
                        result = create_teacher(teacher_name, teacher_username, teacher_password)
                        if result["success"]:
                            st.success("Registration successful! Please log in with your new credentials.")
                            import time
                            time.sleep(2)
                            st.session_state.teacher_login_type = "login"
                            st.rerun()
                        else:
                            st.error(result["message"])
                    else:
                        st.error("Passwords do not match")
                else:
                    st.warning("Please fill all fields")
                    st.error(message)
        
    with btnc2:
        if st.button("Login Instead",type='primary',icon=':material/passkey:',width='stretch',key='teacher_switch_login_btn'):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()
