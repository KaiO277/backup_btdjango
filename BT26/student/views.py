from django.shortcuts import render, redirect
from .models import student
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.models import  auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
#
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from social_django.models import UserSocialAuth
from django.contrib.auth.models import Group

from .forms import TestForm

from utils.utils import send_email


# Create your views here.

@login_required(login_url='check_login')
def index(request):
    students = student.objects.all()
    paginator = Paginator(students, 10)  # 10 items per page

    page = request.GET.get('page')
    my_data = paginator.get_page(page)
    use_bootstrap = True  
    template_name = 'index.html' if use_bootstrap else 'tailwind_layout.html'
    return render(request, template_name,{'students':students, 'my_data':my_data})

@login_required(login_url='check_login')
def testMedia(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'testMedia.html',{'context':context})

@login_required(login_url='check_login')
def add(request):
    students = student.objects.all()
    return render(request, 'insert.html',{'students':students})

@login_required(login_url='check_login')
def insert(request):
    if request.method == 'POST':
        name = request.POST['username']
        age = request.POST['age']
        avatar = request.FILES.get('avatar')
        document_file = request.FILES.get('document_file')
        description = request.POST.get('description', '')
        if student.objects.filter(name=name).exists():
            error_message = "Tên sinh viên đã tồn tại. Vui lòng chọn tên khác."
            students = student.objects.all()
            return render(request, 'insert.html', {'students': students, 'error_message': error_message})
        else:
            new_student = student.objects.create(name= name, age=age, avatar=avatar, document_file=document_file, description=description)
            new_student.save()
    else:
        return redirect('add')
    return redirect('index')  

@login_required(login_url='check_login')
def remove(request, pk):
    if request.method == 'POST':
        post = student.objects.filter(id=pk)
        post.delete()
    return redirect('index') 

@login_required(login_url='check_login')
def update(request, pk):
    if request.method == 'POST':
        name = request.POST['username']
        age = request.POST['age']
        avatar = request.FILES.get('avatar')
        document_file = request.FILES.get('document_file')
        description = request.POST.get('description', '')
        up_st = student.objects.get(id=pk)

        # Check if a new avatar file is provided
        if avatar:
            up_st.avatar = avatar

        up_st.name = name
        up_st.age = age
        up_st.document_file = document_file
        up_st.description = description
        up_st.save()
    else:
        return redirect('edit')

    return redirect('index')    

@login_required(login_url='check_login')
def edit(request, pk):
    st = student.objects.get(id=pk)
    return render(request, 'edit.html', {'student': st})   

@login_required(login_url='check_login')
def main(request):
    return render(request, 'base.html')

@login_required(login_url='check_login')
def send(request):
    return render(request, 'sendEmail.html')

@login_required(login_url='check_login')
def mainHome(request):
    user = request.user 
    if user.groups.filter(name='superadmin').exists():
        return render(request, 'main.html',{'content':'superadmin'})
    elif user.groups.filter(name='admin').exists():
        return render(request, 'main.html',{'content':'admin'})
    elif user.groups.filter(name='user').exists():
        return render(request, 'main.html',{'content':'user'})
    else:
        # Nếu người dùng không thuộc bất kỳ nhóm nào, thêm họ vào nhóm 'user'
        user_group, created = Group.objects.get_or_create(name='user')
        user.groups.add(user_group)
        return render(request, 'main.html', {'content': 'user'})
    # return render(request, 'main.html')

#sử dụng utils.py
@login_required(login_url='check_login')
def testSendMail2(request):
    return render(request, 'formEmail2.html')

#sử dụng utils.py
@login_required(login_url='check_login')
def sendEmail2(request):
    # Logic để tạo bài viết
    # if request.method == "POST":
    #     if
    # Sau khi tạo bài viết, gửi email thông báo
    subject = "Bài viết mới đã được tạo"
    message = request.POST.get('content')
    recipient_list = request.POST.get('email')

    send_email(subject, message, recipient_list)

    return render(request, 'formEmail2.html')


@login_required(login_url='check_login')
def testForm(request):
    form = TestForm()
    return render(request, 'testForm.html', {'form': form})

def send_custom_email(email, content):
    subject = 'Thông Báo'
    html_message = render_to_string('template_email.html', {'center_text': content})
    
    email_message = EmailMessage(
        subject,  # Tiêu đề email
        strip_tags(html_message),  
        settings.EMAIL_HOST_USER, 
        [email],  
    )
    
    # Thêm nội dung định dạng HTML
    email_message.content_subtype = 'html'
    email_message.body = html_message

    # Gửi email
    email_message.send()

@login_required(login_url='check_login')
def sendEmail(request):
    if request.method == 'POST':
        # Kiểm tra xem người dùng đã đăng nhập chưa trước khi gửi email
        if request.user.is_authenticated:
            email = request.POST.get('email')
            content = request.POST.get('content')

            # Gọi hàm để gửi email
            send_custom_email(email, content)

            return render(request, 'sendEmail.html')
        else:
            # Nếu người dùng chưa đăng nhập, xử lý theo ý muốn của bạn
            return HttpResponse('Bạn cần đăng nhập để gửi email.')
    
    return render(request, 'sendEmail.html')

def login(request):
    return render(request, 'login.html')

def thongbao(request):
    return render(request, 'thongbao.html')

def login_success_google(request):
     # Kiểm tra xem người dùng có được xác thực hay không
    is_authenticated = request.user.is_authenticated
    
    # Tạo một chuỗi để hiển thị liệu người dùng có được xác thực hay không
    check_au = "Người dùng đã xác thực: " + str(request.user.is_authenticated)

    # Nếu người dùng đã xác thực, trả về một thông báo thành công
    if is_authenticated:
        return HttpResponse('Đăng nhập thành công, '+ check_au)
    else:
        return HttpResponse('Đăng nhập tb, '+check_au)

@login_required(login_url='check_login') 
def change_pass(request):
    return render(request, 'changepass.html')

@login_required(login_url='check_login') 
def check_change_password(request):
    user = request.user

    if request.method == 'POST':
        old_pass = request.POST.get('password')
        new_pass = request.POST.get('new_password')
        cof_pass = request.POST.get('confirm_new_password') 
        if not authenticate(username = user.username, password = old_pass):
            messages.error(request,'Mật khẩu cũ không đúng')
            return render(request,'changepass.html')
        elif not (new_pass == cof_pass):
            messages.error(request,'Mật khẩu mới không khớp')
            return render(request,'changepass.html')
        else:
            user.set_password(new_pass)
            user.save()

            # email = user.email
            content = 'Mật khẩu mới của bạn là: '+ new_pass
            email = user.email
            send_custom_email(email, content)

            update_session_auth_hash(request, user)
            auth.logout(request)
            return render(request,'thongbao.html',{'title':'Thông Báo','content':'Đổi mật khẩu thành công. Xin hãy đăng nhập lại!'})

def check_login(request):
    User = get_user_model()
    

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Thử lấy người dùng bằng email
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # Xác thực thành công
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth.login(request, user)
                if user.groups.filter(name='superadmin').exists():
                    return render(request, 'main.html',{'content':'superadmin'})
                elif user.groups.filter(name='admin').exists():
                    return render(request, 'main.html',{'content':'admin'})
                elif user.groups.filter(name='user').exists():
                    return render(request, 'main.html',{'content':'user'})
                else:
                    return render(request, 'main.html',{'content':'Người dùng không thuộc nhóm nào'})
                
                # return redirect('index')
            else:
                return HttpResponse('Sai mật khẩu')
        else:
            # Thử xác thực với tên người dùng trực tiếp
            authentication_form = AuthenticationForm(request, data=request.POST)
            if authentication_form.is_valid():
                user = authentication_form.get_user()
                auth.login(request, user)
                if user.groups.filter(name='superadmin').exists():
                    return render(request, 'main.html',{'content':'super admin'})
                elif user.groups.filter(name='admin').exists():
                    return render(request, 'main.html',{'content':'admin'})
                elif user.groups.filter(name='user').exists():
                    return render(request, 'main.html',{'content':'user'})
                else:
                    
                    return render(request, 'main.html',{'content':'Người dùng không thuộc nhóm nào'})
                # return redirect('index')
            else:
                return HttpResponse('Sai tên người dùng hoặc mật khẩu')

    is_authenticated = request.user.is_authenticated


    # Nếu người dùng đã xác thực, trả về một thông báo thành công
    if is_authenticated:
        
        return redirect('index')
    else:
        return redirect('login')

def is_valid_email(email):
    return '@' in email

@login_required(login_url='check_login')  
def logout(request):
  auth.logout(request)
  return redirect('login')

#username: kaio
#pass: nghia1234@

def form_email_reset(request):
    return render(request, 'form_email_reset.html')

def CustomPasswordReset(request):
    User = get_user_model()
    if request.method == 'POST':
        email_check = request.POST['email_user']
        try:
            user = get_user_model().objects.get(email=email_check)
        except get_user_model().DoesNotExist:
            user = None
        if not user:
            messages.error(request,'Email không tồn tại')
            return render(request, 'form_email_reset.html')
        else :
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))#Mã hóa dữ liệu dạng bytes thành một chuỗi base64 
            token = default_token_generator.make_token(user)#Tạo một token xác nhận từ user object
            content = f"http://127.0.0.1:8000/reset/{uidb64}/{token}/"
            
            send_custom_email(email_check, content)
            return render(request,'thongbao.html',{'title':'Thông Báo','content':'Check mail'}) 
    else:
        return render(request,'thongbao.html',{'title':'Thông Báo','content':'error'})     
    
def CustomPasswordResetConfirmView(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    valid_link = user is not None and default_token_generator.check_token(user, token)

    return render(request, 'PasswordResetConfirm.html', {'valid_link': valid_link,'uidb64':uidb64})

def CheckPassReset(request,uidb64):
    User = get_user_model()

    if request.method == 'POST':
        pass1 = request.POST['password']
        pass2 = request.POST['password1']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if not (pass1 == pass2):
            messages.error(request,'Mật khẩu mới không khớp')
            return render(request,'changepass.html')
        else:
            user.set_password(pass1)
            user.save()

            # email = user.email
            content = 'Mật khẩu mới của bạn là: '+ pass1
            email = user.email
            send_custom_email(email, content)

            update_session_auth_hash(request, user)
            auth.logout(request)
            return render(request,'thongbao.html',{'title':'Thông Báo','content':'Đổi mật khẩu thành công. Xin hãy đăng nhập lại!'})

def check_test_form(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
                # Xử lý dữ liệu form
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                print("email: "+email)
                print("password: "+password)
        else:
            form = TestForm()

    return render(request, 'testForm.html', {'form': form})

def register(request):
    return render(request,'register.html')

def register_with_google(request):
    User = get_user_model()

    if request.user.is_authenticated:
        try:
            google_login = UserSocialAuth.objects.get(user=request.user, provider='google')
        except UserSocialAuth.DoesNotExist:
            google_login = None

        if google_login:
            # Người dùng đã đăng nhập bằng Google, kiểm tra xem có tài khoản trong hệ thống không
            try:
                user = User.objects.get(email=google_login.extra_data['email'])
            except User.DoesNotExist:
                # Tạo tài khoản mới với thông tin từ Google
                user = User.objects.create(
                    username=google_login.extra_data['email'],
                    email=google_login.extra_data['email'],
                    # Thêm các thông tin khác từ Google nếu cần
                )

            # Đăng nhập người dùng vào hệ thống
            auth_login(request, user)

            # Người dùng đã đăng nhập, chuyển hướng hoặc thực hiện các hành động khác
            return redirect('index')
        else:
            # Người dùng đã đăng nhập nhưng không có thông tin xác thực , thực hiện hành động khác hoặc thông báo lỗi
            return render(request, 'error_template.html', {'error_message': 'Không có thông tin xác thực xã hội.'})
    else:
        # Người dùng chưa đăng nhập, chuyển hướng đến trang đăng nhập Google
        return redirect('social:begin', 'google-oauth2')