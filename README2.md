
#### الإصدارات المستخدمة في Python & Django  
```bash
Python 3.14.3 # python version
django 6.0.2 # django version

# System Environ ment
C:\Users\pc\AppData\Local\Programs\Python\Python314\Scripts\
C:\Users\pc\AppData\Local\Programs\Python\Python314\

```



##  إنشاء البيئة الوهمية وتفعيلها
### Create New Environment 
```bash
python -m venv venv314 
```
#### OR
```bash
 py -3.14 -m venv venv314
```

### Activating the environment 
#### In windows system
```bash
venv\Scripts\activate 
```
####  In other systems 
```bash     
source venv/bin/activate  
```


## . تحديث pip  

```bash 
python.exe -m pip install --upgrade pip
```



##  تثبيت المكتبات المطلوبة 

```bash 
pip install -r requirements.txt
```



# . مزامنة قاعدة البيانات (سيقوم النظام بإنشاء الأدوار تلقائياً)#
```bash
python manage.py migrate
```



## . إنشاء مدير النظام
```bash
python manage.py createsuperuser
```

### حساب المدير (Admin) 

Email address: 
```bash 
admin@gmail.com
```

Username:
```bash 
admin
```

Password:
```bash 
Admin@123
```


##  توليد بيانات إفتراضية  
```bash
.\venv\Scripts\python.exe Seeds/seeds.py
```


## . 📂 تنظيم الملفات الساكنة (Static Files) 

إنشاء المجلدات التنظيمية:

```Bash
mkdir -p static/css static/js static/img
```

تجميع الملفات للنشر (Production):

```Bash
python manage.py collectstatic
```




### 5. 🌍 نظام تعدد اللغات (Internationalization) 

الاستخراج: جمع النصوص الجديدة من القوالب:

```Bash
#python manage.py makemessages -l ar
````
التفعيل: تحويل الترجمات إلى صيغة ثنائية سريعة:

```Bash
python manage.py compilemessages
```


## تشغيل المشروع

أفتح Terminal جديد\
 ونفذ الامر التالي  لتشغيل المراقبة بهدف تطبيق تنسيقات tailwind على الواجهات 
```bash
 python manage.py tailwind start 
```

أفتح Terminal ثاني\
ونفذ الامر التالي لتشغيل السرفر 

```bash
python manage.py runserver 
```

### لعرض  الموقع على المتصفح قم بالنقر الرابط التالي   
- **[Website](http://127.0.0.1:8000)**

### لعرض لوحة التحكم الآدمن قم بالنقر الرابط التالي    
- **[Admin Dashboard](http://127.0.0.1:8000/admin)**




[//]: # ()
[//]: # (### Generated Apps)

[//]: # (```bash)

[//]: # (python manage.py startapp  app_name)

[//]: # (```)

[//]: # ()
[//]: # (### Clear Cash)

[//]: # (```bash)

[//]: # (Get-ChildItem -Path . -Include *.pyc -Recurse | Remove-Item -Force)

[//]: # (```)

[//]: # ()
[//]: # (### Githup push commands)

[//]: # (```commandline)

[//]: # (git add .)

[//]: # (git commit -m "Last Copy " )

[//]: # (c)

[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (pip freeze > requirements.txt #  إستعراض جميع المكتبات المثبتة حالياً مع أرقام إصداراتها الدقيقة وتحويلها الى ملف نصي  يجب تنفيذه بعد كل مكتبه يتم تثبيتها)

[//]: # (Example:)

[//]: # ()
[//]: # (SITE_ROLES = [)

[//]: # ()
[//]: # (    {)

[//]: # (        'code': 'user',)

[//]: # (        'name': 'user',)

[//]: # (        'is_identity': True,      # هل له بروفايل وهوية مستقلة؟)

[//]: # (        'requires_approval': False, # هل يحتاج تفعيل من الإدارة؟)

[//]: # (        'view_in_register': True,  # هل يظهر في خيارات التسجيل؟)

[//]: # (    },)

[//]: # (    {)

[//]: # (        'code': 'emp__',)

[//]: # (        'name': 'emp__',)

[//]: # (        'is_identity': True,      # هل له بروفايل وهوية مستقلة؟)

[//]: # (        'requires_approval': True, # هل يحتاج تفعيل من الإدارة؟)

[//]: # (        'view_in_register': True,  # هل يظهر في خيارات التسجيل؟)

[//]: # (    },)

[//]: # (   )
[//]: # (])

[//]: # ()
