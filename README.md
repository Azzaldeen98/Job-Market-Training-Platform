


### 1. إنشاء البيئة الوهمية وتفعيلها
```bash
    python -m venv venv
    # Activating the environment in Windows system:
      venv\Scripts\activate 
    # Activating the environment in other systems :
      source venv/bin/activate  
```


### 2. تثبيت المكتبات المطلوبة 

```bash 

pip freeze > requirements.txt #  إستعراض جميع المكتبات المثبتة حالياً مع أرقام إصداراتها الدقيقة وتحويلها الى ملف نصي  يجب تنفيذه بعد كل مكتبه يتم تثبيتها

pip install -r requirements.txt
```

Example:

SITE_ROLES = [

    {
        'code': 'user',
        'name': 'user',
        'is_identity': True,      # هل له بروفايل وهوية مستقلة؟
        'requires_approval': False, # هل يحتاج تفعيل من الإدارة؟
        'view_in_register': True,  # هل يظهر في خيارات التسجيل؟
    },
    {
        'code': 'emp__',
        'name': 'emp__',
        'is_identity': True,      # هل له بروفايل وهوية مستقلة؟
        'requires_approval': True, # هل يحتاج تفعيل من الإدارة؟
        'view_in_register': True,  # هل يظهر في خيارات التسجيل؟
    },
   
]

# 3. مزامنة قاعدة البيانات (سيقوم النظام بإنشاء الأدوار تلقائياً)##
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. إنشاء مدير النظام
```bash
python manage.py createsuperuser
```
### 5. 🌍 نظام تعدد اللغات (Internationalization) 

الاستخراج: جمع النصوص الجديدة من القوالب:

```
python manage.py makemessages -l ar
````
التفعيل: تحويل الترجمات إلى صيغة ثنائية سريعة:

```Bash
python manage.py compilemessages
```
### 6. 📂 تنظيم الملفات الساكنة (Static Files) 

إنشاء المجلدات التنظيمية:

```Bash
mkdir -p static/css static/js static/img
```

تجميع الملفات للنشر (Production):

```Bash
python manage.py collectstatic
```
### Install Frontend Dependencies
```bash

Run the following commands after cloning the project.

```bash
# Install cross-env (needed for Windows compatibility)
npm install -D cross-env

# Move to the Tailwind theme directory
cd theme

# Install UI components
npm install daisyui

# Install Tailwind CSS 4 and PostCSS tooling
npm install tailwindcss @tailwindcss/postcss postcss postcss-cli autoprefixer postcss-simple-vars postcss-nested

# Return to project root
cd ..
```
After installing dependencies, start the Tailwind watcher:
أفتح Terminal جديد ونفذ الامر التالي  لتشغيل المراقبة (Start/Dev) بهدف تطبيق تنسيقات tailwind على الواجهات 
```bash
 python manage.py tailwind start # لتشغيل المراقبة الحية أثناء التطوير
```

### 7. تشغيل المشروع

أفتح Terminal أخر ونفذ الامر التالي لتشغيل السرفر 
```bash
python manage.py runserver
```

### Generated Apps 

```bash
python manage.py startapp  app_name
```
### Clear Cash 

```bash
Get-ChildItem -Path . -Include *.pyc -Recurse | Remove-Item -Force
```

### Githup push commands
```commandline
git add .
git commit -m "Last Copy " 
git push -u origin main
```

### 🚀 Roadmap
[x] Building a dynamic role system (Post-migrate Sync).

[x] Setting up intelligent redirection logic.

[x] Building student dashboard interfaces (students app).

[x] Integrating a job posting system for companies.

[x] Enabling the push notification system.

### 📝 Important Notes for Developers
- `Q` Principle: Logic first, relationships between tables second, design last.

- Update: When adding a new role in SITE_ROLES using settings.py, run `python manage.py migrate` to update the database immediately.

- Security: Do not manually modify the role table from the database; always rely on the settings file.


### 🚀 خارطة الطريق (Roadmap) 
[x] بناء نظام الأدوار الديناميكي (Post-migrate Sync).

[x] إعداد منطق التوجيه الذكي (Role-based Redirect).

[X] بناء واجهات لوحة تحكم الطالب (students app).

[X] دمج نظام رفع الوظائف للشركات.

[X] تفعيل نظام الإشعارات الفوري.

### 📝 ملاحظات هامة للمطورين 

- **دستور القاف: المنطق (Logic)** أولاً، العلاقات بين الجداول ثانياً، والتصميم آخراً. 

- التحديث: عند إضافة دور جديد في SITE_ROLES بالـ settings.py قم بتشغيل python manage.py migrate لتحديث قاعدة البيانات فوراً.

- الأمن: لا تقم بتعديل جدول الأدوار يدوياً من الـ DB؛ اعتمد دائماً على ملف الإعدادات.