import google.generativeai as genai
import markdown
from django.shortcuts import render
from django.utils.safestring import mark_safe

# 🔒 Set your Gemini API key
GENAI_API_KEY = "AIzaSyD--gt4Z7-jwF4kxLOnwgOjQILw5FN8Ozo"
genai.configure(api_key=GENAI_API_KEY)

def chatbot(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []  

    user_message = ""
    bot_response = ""

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        if user_message:
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(user_message)
                
                bot_response = mark_safe(markdown.markdown(response.text, extensions=['fenced_code', 'codehilite']))

                
                chat_history = request.session["chat_history"]
                chat_history.append({"user": user_message, "bot": bot_response})
                request.session["chat_history"] = chat_history 
                request.session.modified = True  

            except Exception as e:
                bot_response = f"خطا: {str(e)}"

    return render(request, "chatbot/chat.html", {"chat_history": request.session["chat_history"]})