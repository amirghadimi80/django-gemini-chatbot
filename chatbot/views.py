from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from .models import UserProfile, ChatSession, ChatMessage
import google.generativeai as genai
import markdown
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django.views.decorators.csrf import csrf_exempt
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Gemini API Key from environment variable
GENAI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GENAI_API_KEY)



def register(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        name = request.POST.get("name")
        email = request.POST.get("email")

        # Validate phone number format
        if not phone.startswith('09') or len(phone) != 11 or not phone.isdigit():
            messages.error(request, "شماره تلفن باید با ۰۹ شروع شود و ۱۱ رقم باشد.")
            return redirect('chatbot')

        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "این شماره تلفن قبلا ثبت شده است.")
            return redirect('chatbot')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلا ثبت شده است.")
            return redirect('chatbot')

        # Create user with hashed password
        user = UserProfile(phone=phone, name=name, email=email)
        user.set_password(password)
        user.save()

        # Create first chat session for new user
        chat_session = ChatSession.objects.create(
            user=user,
            title="چت 1"
        )
        ChatMessage.objects.create(
            session=chat_session,
            is_user=False,
            message="سلام! من هوشتو AI هستم. چطور می‌توانم به شما کمک کنم؟"
        )
        request.session['user_id'] = user.id
        return redirect('user_panel')

    return redirect('chatbot')


def user_panel(request):
    if 'user_id' not in request.session:
        return redirect('chatbot')
    
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    chat_sessions = ChatSession.objects.filter(user=user)
    
    # Get the latest session or create one if none exists
    current_session = chat_sessions.first()
    if not current_session:
        current_session = ChatSession.objects.create(user=user, title="چت جدید")
        ChatMessage.objects.create(
            session=current_session,
            is_user=False,
            message="سلام! من هوشتو AI هستم. چطور می‌توانم به شما کمک کنم؟"
        )
    
    messages = ChatMessage.objects.filter(session=current_session)
    
    return render(request, "chatbot/user_panel.html", {
        "user": user,
        "chat_sessions": chat_sessions,
        "current_session": current_session,
        "messages": messages
    })


def chat_view(request, session_id):
    if 'user_id' not in request.session:
        return redirect('chatbot')
    
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    current_session = get_object_or_404(ChatSession, id=session_id, user=user)
    chat_sessions = ChatSession.objects.filter(user=user)
    messages = ChatMessage.objects.filter(session=current_session)
    
    return render(request, "chatbot/user_panel.html", {
        "user": user,
        "chat_sessions": chat_sessions,
        "current_session": current_session,
        "messages": messages
    })


@csrf_exempt
def create_chat(request):
    if request.method == "POST" and 'user_id' in request.session:
        user = get_object_or_404(UserProfile, id=request.session['user_id'])
        # Get the count of existing chats for this user
        chat_count = ChatSession.objects.filter(user=user).count()
        # Create new chat with sequential number
        session = ChatSession.objects.create(
            user=user,
            title=f"چت {chat_count + 1}"
        )
        ChatMessage.objects.create(
            session=session,
            is_user=False,
            message="سلام! من هوشتو AI هستم. چطور می‌توانم به شما کمک کنم؟"
        )
        return JsonResponse({"success": True, "session_id": session.id})
    return JsonResponse({"success": False})


@csrf_exempt
def send_message(request):
    if request.method == "POST" and 'user_id' in request.session:
        data = json.loads(request.body)
        message = data.get('message')
        session_id = data.get('session_id')
        
        user = get_object_or_404(UserProfile, id=request.session['user_id'])
        session = get_object_or_404(ChatSession, id=session_id, user=user)
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            is_user=True,
            message=message
        )
        
        # Get AI response
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(message)
        formatted_response = format_code_blocks(response.text)
        bot_response = mark_safe(
            markdown.markdown(formatted_response, extensions=['fenced_code', 'codehilite'])
        )
        
        # Save bot response
        ChatMessage.objects.create(
            session=session,
            is_user=False,
            message=bot_response
        )
        
        return JsonResponse({
            "success": True,
            "response": bot_response
        })
    
    return JsonResponse({"success": False})


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('chatbot')


def login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        
        try:
            user = UserProfile.objects.get(phone=phone)
            if user.check_password(password):
                request.session['user_id'] = user.id
                return redirect('user_panel')
            else:
                messages.error(request, "رمز عبور اشتباه است.")
        except UserProfile.DoesNotExist:
            messages.error(request, "کاربری با این شماره تلفن یافت نشد.")
        
        return redirect('chatbot')
    return redirect('chatbot')


def chatbot(request):
    user = None
    if 'user_id' in request.session:
        user = get_object_or_404(UserProfile, id=request.session['user_id'])
        return redirect('user_panel')
    
    chat_history = request.session.get('chat_history', [])
    return render(request, "chatbot/chat.html", {
        "user": user,
        "chat_history": chat_history,
        "registered": False
    })


def format_code_blocks(text):
    """Format code blocks with syntax highlighting and bold text."""
    lines = text.split('\n')
    formatted_lines = []
    in_code_block = False
    current_code = []
    language = ''

    for line in lines:
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block
                try:
                    lexer = get_lexer_by_name(language) if language else PythonLexer()
                    formatter = HtmlFormatter(style='monokai', cssclass='code-block')
                    highlighted_code = highlight('\n'.join(current_code), lexer, formatter)
                    formatted_lines.append(highlighted_code)
                except:
                    # Fallback if language not supported
                    formatted_lines.append(f'<div class="code-block"><pre>{current_code}</pre></div>')
                in_code_block = False
                current_code = []
                language = ''
            else:
                # Start of code block
                in_code_block = True
                language = line.strip('```').strip()
        elif in_code_block:
            current_code.append(line)
        else:
            # Format bold text using ** or __
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'__(.*?)__', r'<strong>\1</strong>', line)
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)


def ajax_chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        bot_response = ""

        if user_message:
            # Check for developer-related questions
            developer_keywords = ["توسعه دهنده", "سازنده", "برنامه نویس", "توسعه", "ساخته شده", "ساخته", "توسط چه کسی", "چه کسی ساخته"]
            if any(keyword in user_message.lower() for keyword in developer_keywords):
                bot_response = mark_safe("من توسط Amir_Ghadimi توسعه داده شده‌ام. 😊")
            else:
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(user_message)
                
                # Format the response with proper code blocks
                formatted_response = format_code_blocks(response.text)
                bot_response = mark_safe(
                    markdown.markdown(formatted_response, extensions=['fenced_code', 'codehilite'])
                )

            chat_history = request.session.get("chat_history", [])
            chat_history.append({
                "user": user_message,
                "bot": bot_response,
                "time": datetime.now().strftime("%H:%M")
            })
            request.session["chat_history"] = chat_history
            request.session.modified = True

        return JsonResponse({
            "user": user_message,
            "bot": bot_response,
            "time": datetime.now().strftime("%H:%M")
        })