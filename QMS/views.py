from django.shortcuts import render,HttpResponse,redirect
from rest_framework.decorators import api_view
from django.db.models import Avg, F,Max,Min

from django.http.response import JsonResponse
from rest_framework import status
from django.contrib import messages
from QMS.models import Login,Admin,QuizDetails,Questionnaire,Category,Student,Result
from QMS.forms import Questionnaireforms
#from django.forms import formset_factory

def home(request):
    return render(request,'main_homepg.html')

def admin(request):
    return render(request,'admin_home.html')

def checkuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.POST.get('user_type') == 'Student':
            is_student = 'True'
            is_admin = 'False'
            
        
        else:
            is_student = 'False'
            is_admin = 'True'
        user = Login.objects.filter(username=username, password=password, is_student=is_student,is_admin=is_admin)

        if user.exists() and is_admin == 'True':
            return admin(request)
        elif user.exists() and is_student == 'True':
            category_obj = Category.objects.all()
            student_instance = Login.objects.get(username = username)
            unique_id = student_instance.unique_id
            context = {"unique_id": unique_id, "category_obj": category_obj}
            return render(request, 'student_home.html', context)
        else:
            messages.success(request, 'Incorrect Details')
            return render(request,'login.html')
    else:
        return render(request,'login.html')
    
def register_user(request):
    if request.method == 'POST':
        #payload = request.data
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        unique_id = request.POST.get("unique_id")
        is_student = False
        is_admin = False
        if user_type == "Student":
            is_student = True
            # creating user
            user = Login.objects.filter(username=user_name)
            on_id = Login.objects.filter(unique_id=unique_id)
            if user.exists() or on_id.exists():
                messages.success(request,f"User alreadyy exists, use different details or login")
                return render(request, 'user_registration_form.html')
            else:
                created = Login.objects.get_or_create(username=user_name,password=password,unique_id = unique_id,is_student=is_student,is_admin=is_admin)
                if created:
                    messages.success(request,f"User {user_name} registered.", user_name)
                    return render(request, 'user_registration_form.html')
        else:
            is_admin = True
            user = Admin.objects.filter(admin_name=user_name)
            if user.exists():
                messages.success(request,f"Username already taken, use a different username")
                return render(request, 'user_registration_form.html')
            else:
                saveadmin = Admin()
                saveadmin.admin_name = user_name
                saveadmin.save()
                # creating user
                created = Login.objects.get_or_create(username=user_name,password=password,is_student=is_student,is_admin=is_admin)
                if created:
                    messages.success(request,f"User {user_name} registered.", user_name)
                    return render(request, 'user_registration_form.html')

    else:
        return render(request, 'user_registration_form.html')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        try:
            user = Login.objects.get(username=username)
        except Login.DoesNotExist:
            messages.success(request,'Invalid Username!')
            return render(request, 'forgot_pass.html')

        user.password = new_password
        user.save()
        messages.success(request,f'Password for {username} changed successfully!')
        return render(request,'forgot_pass.html')

    return render(request, 'forgot_pass.html')
    

def create_quiz(request):
    categories = Category.objects.all() 
    if request.method == 'POST':
        if request.POST.get('question_count') == '':
            messages.success(request,'Enter a minimum of 2 questions')
            return render(request,'create_quiz.html',{'data':categories})
        timer = request.POST.get('timer')
        print(type(timer))
        if timer == 'e' or int(timer) < 0 :
            messages.error(request,'Enter a valid value')
            return render(request,'create_quiz.html',{'data':categories})
        admin_obj = Admin.objects.filter(admin_name=request.POST.get('adminName'))
        print(admin_obj)
        if admin_obj.exists() == False:
            messages.error(request,'Enter a valid admin username')
            return render(request,'create_quiz.html',{'data':categories})
        saverecord = QuizDetails()
        category_obj = Category.objects.filter(category_name = request.POST.get('category'))
        saverecord.description = request.POST.get('quizDescription')
        saverecord.quiz_name = request.POST.get('quizName')
        if request.POST.get('category') == 'AddNew':
            saverecord.category = Category.objects.create(category_name=request.POST.get('newCategory'))
        elif category_obj.exists():
            saverecord.category = category_obj.first()
        saverecord.admin = Admin.objects.get(admin_name=request.POST.get('adminName'))
        saverecord.time = request.POST.get('timer')
        saverecord.save()
        
        question_count = request.POST.get('question_count')
        print(question_count)
        for i in range(1,int(question_count)+ 1):
            save_questionnaire = Questionnaire()
            save_questionnaire.questions = request.POST.get(f'question[{i}]')
            save_questionnaire.option1 = request.POST.get(f'option1[{i}]')
            save_questionnaire.option2 = request.POST.get(f'option2[{i}]')
            save_questionnaire.option3 = request.POST.get(f'option3[{i}]')
            save_questionnaire.option4 = request.POST.get(f'option4[{i}]')
            payload = request.POST
            #print(payload.lists())
            correct_option = request.POST.get(f'correct_answer[{i}]')
            
            #correct_options = request.POST.getlist(f'correctAnswer[{i}][]')
            #print(correct_options)
            save_questionnaire.correct_option = correct_option
            save_questionnaire.quiz = QuizDetails.objects.get(quiz_name = request.POST.get('quizName'))
            if request.POST.get('category') == 'AddNew':
                save_questionnaire.category = Category.objects.get(category_name=request.POST.get('newCategory'))
            else:
                save_questionnaire.category = Category.objects.get(category_name = request.POST.get('category'))
            save_questionnaire.save()


       
    return render(request,'create_quiz.html',{'data':categories})

def view_all_quizzes(request):
    showall = QuizDetails.objects.all()
    return render(request,'view_quiz.html',{'data':showall})

def view_quiz(request,id):
    #selected_quiz = Questionnaire.objects.get(id=id)
    #print(selected_quiz.id)
    #quiz_id = selected_quiz.id
    #print(quiz_id)
    questionnaire_objs = Questionnaire.objects.filter(quiz = id)
    #print(questionnaire_objs)
    data = []
    for questionnaire_obj in questionnaire_objs:
        question_text = questionnaire_obj.questions
        option1 = questionnaire_obj.option1
        option2 = questionnaire_obj.option2
        option3 = questionnaire_obj.option3
        option4 = questionnaire_obj.option4
        correct_option = questionnaire_obj.correct_option

        data.append({
            'question_text': question_text,
            'option1': option1,
            'option2': option2,
            'option3':option3,
            'option4':option4 ,
            'correct_option': correct_option,
        })
    #print(data)
    return render(request,'view_quiz_qa.html',{'data':data})

def modify_quizzes(request):
    showall = QuizDetails.objects.all()
    return render(request,'modify_quiz.html',{'data':showall})

def quiz_to_be_modified(request,id):
    #selected_quiz = Questionnaire.objects.get(id=id)
    #quiz_id = selected_quiz.id
    questionnaire_objs = Questionnaire.objects.filter(quiz = id)
    data = []
    for questionnaire_obj in questionnaire_objs:
        question_text = questionnaire_obj.questions
        option1 = questionnaire_obj.option1
        option2 = questionnaire_obj.option2
        option3 = questionnaire_obj.option3
        option4 = questionnaire_obj.option4
        correct_option = questionnaire_obj.correct_option
        ques_id = questionnaire_obj.id

        data.append({
            'question_text': question_text,
            'option1': option1,
            'option2': option2,
            'option3': option3,
            'option4': option4,  
            'correct_option': correct_option,
            'ques_id':ques_id
        })
    return render(request,'update.html',{'data':data,'id':id})

def update_quiz(request,id):
    selected_quiz = Questionnaire.objects.get(id=id)
    form = Questionnaireforms(request.POST, instance = selected_quiz)
    print(form)
    if form.is_valid(): 
        form.save()
        messages.success(request,"Question Updated")
        return quiz_to_be_modified(request,id= selected_quiz.quiz.id)
    
def show_quizzes(request):
    showall = QuizDetails.objects.all()
    return render(request,'delete_quiz.html',{'data':showall})

def delete_quiz(request,id):
    selected_quiz = QuizDetails.objects.get(id=id)
    #selected_questionnaire = Questionnaire.objects.get(id=id)

    if selected_quiz.delete():
        return show_quizzes(request)

def add_question(request,id):
    if request.method == 'POST':
        #print(request.POST)
        save_question = Questionnaire()
        save_question.questions = request.POST.get('new_question')
        save_question.option1 = request.POST.get('new_option1')
        save_question.option2 = request.POST.get('new_option2')
        save_question.option3 = request.POST.get('new_option3')
        save_question.option4 = request.POST.get('new_option4') 
        save_question.correct_option = request.POST.get('new_correct_option')
        selected_quiz = QuizDetails.objects.get(id=id)
        save_question.quiz = selected_quiz
        save_question.category =selected_quiz.category 
        print(save_question)
        save_question.save()
        return redirect('modify_quiz', id=id)
    return redirect('modify_quiz', id=id)

def delete_question(request,id):
    selected_question = Questionnaire.objects.get(id=id)
    quiz_id = selected_question.quiz.id
    if selected_question.delete():
        return  redirect ('modify_quiz' ,id=quiz_id)

def quiz_result(request,id):
    questionnaire_objs = Questionnaire.objects.filter(quiz = id)
    
    for quiz in questionnaire_objs:
        quiz_id = quiz.quiz.id
        #print(quiz.questions)

    result = Student.objects.filter(quiz_id=quiz_id).order_by('-score')
    #print(result)

    top3_students = result[:3]
    bottom3_students = result.reverse()[:3]

    average_score = result.aggregate(avg_score=Avg('score'))['avg_score']
    highest_score = result.aggregate(max_score=Max('score'))['max_score']
    lowest_score = result.aggregate(min_score=Min('score'))['min_score']
    stats = [{
        'average':average_score,
        'highest':highest_score,
        'lowest':lowest_score
    }]

    data = []
    for student in result:
        name = student.student_name
        score = student.score
        data.append({
            'student_name':name,
            'score':score
        })

    top3_data = []
    for student in top3_students:
        name = student.student_name
        score = student.score
        top3_data.append({
            'student_name': name,
            'score': score
        })

    bottom3_data = []
    for student in bottom3_students:
        name = student.student_name
        score = student.score
        bottom3_data.append({
            'student_name': name,
            'score': score
        })
    return render(request,'quiz_results.html',{'data':data,'stats':stats,'data_top': top3_data, 'data_bottom': bottom3_data})

# ---------- Student views -----------------


@api_view(['GET'])
def quiz_dashboard(request, student_id, category_id):
    global quiz_id_list
    if request.method == "GET":
        quiz_obj = QuizDetails.objects.filter(category=category_id)
        stud_obj = Student.objects.filter(unique_id=student_id)
        student_obj = list(stud_obj.order_by('quiz_id','-id').distinct('quiz_id').values())
        if len(student_obj) > 0:
            quiz_id_list = [student['quiz_id'] for student in student_obj]
        data = {}
        attempt_1_score = [stud.score for stud in stud_obj if stud.no_of_attempts == 1]
        attempt_2_score = [stud.score for stud in stud_obj if stud.no_of_attempts == 2]
        for quiz in quiz_obj:
            print(quiz.id)
            if len(student_obj) > 0:
                # student has given the quiz for the category
                for student in student_obj:
                    if quiz.id == student['quiz_id']:
                        # if student has given the quiz
                        data[quiz.id] = {"quiz_name": quiz.quiz_name, "score_1": round(attempt_1_score[0],2) if len(attempt_1_score) > 0 else 0,
                                         "score_2": round(attempt_2_score[0],2) if len(attempt_2_score) > 0 else 0,
                                         "no_of_attempts": student['no_of_attempts'],
                                         "take_quiz": True if student['no_of_attempts'] < 2 else False}
                        break
                    elif quiz.id not in quiz_id_list:
                        # student has not given the quiz
                        data[quiz.id] = {"quiz_name": quiz.quiz_name, "score_1":  "N/A",
                                         "score_2":  "N/A",
                                         "no_of_attempts": 0,
                                         "take_quiz": True}
            else:
                # student has not given any quiz
                data[quiz.id] = {"quiz_name": quiz.quiz_name, "score_1": "N/A",
                                  "score_2":  "N/A",
                                 "no_of_attempts": 0,
                                 "take_quiz": True}

        context = {
            'quiz_obj': quiz_obj,
            'student_data': data,
            'category': category_id,
            'unique_id': student_id
        }
        return render(request, 'quiz_comparison.html', context)
    

def submit_quiz(request, quiz_id,unique_id, category_id):
    if request.method == "POST":
        payload = request.POST
        data = dict()
        quest_id_list = []
        for key, val_list in payload.lists():
            print(key)
            for val in val_list:
                pass
                print(val)
            if key.startswith("answer"):
                new_key = key.split('_')[1]
                data[new_key] = val_list
                quest_id_list.append(new_key)
        student_obj = Login.objects.filter(unique_id=unique_id).first()
        student_name = student_obj.username

        ques_obj = Questionnaire.objects.filter(id__in=quest_id_list, quiz=quiz_id, category=category_id)
        final_score = 0

        for key, val in data.items():
            for ques in ques_obj:
                if ques.id == int(key):
                    correct_opt_list = list(ques.correct_option.split(','))
                    opt_len = len(list(ques.correct_option.split(',')))
                    min_score = 1 / opt_len
                    for v in val:
                        if v in correct_opt_list:
                            final_score += min_score

        try:
            stud_obj = Student.objects.filter(unique_id=unique_id)
            no_of_attempts = int(stud_obj.first().no_of_attempts) + 1
        except:
            no_of_attempts = 1

        created = Student.objects.get_or_create(
                                       student_name=student_name,
                                       quiz_id=quiz_id,
                                       score=float(final_score),
                                       unique_id=unique_id,
                                       no_of_attempts=no_of_attempts
                                     )
        context = {'score': final_score, 'student_name': student_name}
        if created:
            return render(request, 'result.html', context)
        
def take_quiz(request, category_id, quiz_id, unique_id):
    if request.method == "GET":
        questionnaire_obj = Questionnaire.objects.filter(category=category_id, quiz=quiz_id).order_by('?')[:5]
        try:
            timer = int(QuizDetails.objects.get(id=quiz_id).time) * 60
        except Exception as e:
            return JsonResponse({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        options = dict()
        for ques in questionnaire_obj:
            options[ques.questions] = {'ques_id':ques.id, 'a': ques.option1, 'b': ques.option2, 'c': ques.option3, 'd': ques.option4}
            #print(options)

        #print(options)
        data = {'questions': questionnaire_obj, 'options': options, 'quiz_id': quiz_id, 'category_id':category_id, 'unique_id': unique_id,
                'timer': timer}
        print(data)
        return render(request, 'quiz.html', data)

def view_stats(request, quiz_id, unique_id):
    student_obj = Student.objects.filter(unique_id=unique_id, quiz_id=quiz_id).last()
    students = Student.objects.filter(quiz_id=quiz_id)
    average_score = students.aggregate(avg_score=Avg('score'))['avg_score']
    highest_score = students.aggregate(max_score=Max('score'))['max_score']
    lowest_score = students.aggregate(min_score=Min('score'))['min_score']
    rank = students.filter(score__gt=student_obj.score).count() + 1

    context = {
        'student_score': round(student_obj.score,2),
        'avg_score': round(average_score,2),
        'high_score': round(highest_score,2),
        'low_score': round(lowest_score,2),
        'rank': rank,
    }
    return render(request, 'statistics.html',context)