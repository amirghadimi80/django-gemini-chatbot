# Django Gemini Chatbot 🤖

A powerful web-based chatbot application built with Django and Google's Gemini AI model. This project demonstrates the integration of advanced AI capabilities into a modern web application.


 📌 **Note:** This project is primarily intended for Persian-speaking users. While the documentation is in English, you can localize the UI and functionality for Persian as needed.

## 🌟 Features

- Interactive chat interface
- Powered by Google's Gemini AI model
- Real-time message processing
- User-friendly web interface
- Secure API integration
- Message history tracking

## 🛠️ Technologies Used

- **Backend**: Django 5.1.7
- **AI Model**: Google Gemini AI
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Python Version**: 3.x

## 📋 Prerequisites

Before you begin, ensure you have:
- Python 3.x installed
- Google Cloud account with Gemini API access
- Basic knowledge of Django framework

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/django-gemini-chatbot.git
cd django-gemini-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Update the following variables in `.env`:
     ```
     DJANGO_SECRET_KEY=your-secret-key-here
     DEBUG=True
     GEMINI_API_KEY=your-gemini-api-key-here
     ```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## 💻 Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000/`
2. Start chatting with the AI-powered bot
3. Your conversation history will be saved in the database

## 🔧 Configuration

The main configuration files are:
- `settings.py`: Django settings
- `urls.py`: URL routing
- `views.py`: View logic
- `models.py`: Database models

## 📝 Project Structure

```
django_gemini_chatbot/
├── gemini_chatbot/        # Main project directory
├── chatbot/              # Chatbot app directory
├── manage.py            # Django management script
├── requirements.txt     # Project dependencies
└── .env                # Environment variables (not in git)
```

## 🔐 Security

This project uses environment variables to store sensitive information:
- Django Secret Key
- Gemini API Key
- Debug mode setting

Never commit the `.env` file to version control. The `.env.example` file is provided as a template.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.



## 👥 Author

Amir Hossein Ghadimi

- GitHub: https://github.com/amirghadimi80/

## 🙏 Acknowledgments

- Google Gemini AI team for their powerful AI model
- Django community for the excellent web framework
- All contributors who have helped improve this project

---

⭐ Star this repository if you find it helpful! 



# چت‌بات مبتنی بر Gemini با جنگو🤖

یک برنامه‌ی قدرتمند چت‌بات تحت وب که با فریم‌ورک Django و مدل هوش مصنوعی Gemini گوگل ساخته شده است. این پروژه ادغام قابلیت‌های پیشرفته‌ی هوش مصنوعی را در یک برنامه‌ی وب مدرن به نمایش می‌گذارد.

> 📌 **توجه:** این پروژه عمدتاً برای کاربران فارسی‌زبان طراحی شده است. در حالی که مستندات به زبان انگلیسی ارائه شده، رابط کاربری و قابلیت‌ها را می‌توانید برای زبان فارسی بومی‌سازی کنید.

## 🌟 ویژگی‌ها

- رابط چت تعاملی
- مبتنی بر مدل Gemini گوگل
- پردازش پیام‌ها به صورت بلادرنگ
- رابط کاربری ساده و کاربرپسند
- ادغام ایمن با API
- ذخیره‌سازی تاریخچه‌ی پیام‌ها

## 🛠️ تکنولوژی‌های استفاده‌شده

- **بک‌اند**: Django نسخه ۵.۱.۷
- **مدل هوش مصنوعی**: Google Gemini AI
- **پایگاه داده**: SQLite
- **فرانت‌اند**: HTML، CSS، JavaScript
- **نسخه پایتون**: ۳.x

## 📋 پیش‌نیازها

پیش از شروع، اطمینان حاصل کنید که:
- پایتون ۳.x نصب شده باشد
- حساب کاربری در Google Cloud و دسترسی به API مدل Gemini داشته باشید
- با فریم‌ورک Django آشنایی پایه داشته باشید


