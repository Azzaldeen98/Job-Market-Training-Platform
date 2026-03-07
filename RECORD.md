# 🚀 Boilerplate

### "تحويل الطموح الأكاديمي إلى واقع مهني مدعوم بالذكاء الاصطناعي"

## 📌 رؤية المشروع
مشروع متكامل يهدف إلى:
1. **التحليل الذكي:** تحليل فجوات المهارات بين المخرجات الأكاديمية ومتطلبات سوق العمل.
2. **المنصة التنفيذية:** نظام (Matching) ذكي يربط الطلاب بفرص التدريب المهني بناءً على نتائج التحليل.

---

## 🛠 المعمارية التقنية (Tech Stack)
* **العمود الفقري:** Django (Python Framework).
* **قاعدة البيانات:** SQLite (حالياً للتطوير) / PostgreSQL (للإنتاج).
* **المنهجية:** Logic-First Architecture (التركيز على الوظائف قبل الشكل).
* **الأدوات:** Django ORM, Multi-language support, Custom User Models.

---

## 📁 هيكلية النظام (Project Structure)
تم تقسيم المشروع إلى تطبيقات (Apps) لضمان المعمارية النظيفة:
* **`config/`**: إعدادات المشروع المركزية.
* **`accounts/`**: إدارة المستخدمين (طلاب، شركات، مسؤولين) بنظام صلاحيات مخصص.
* **`core/`**: الوظائف المشتركة، الصفحات الرئيسية، والقوالب الأساسية (Base Boilerplate).
* **`companies/`**: (قيد الإنشاء) إدارة بيانات الشركات، التوثيق، ورفع الفرص.

---

## 📜 دستور العمل (The Constitution)
نحن نتبع **"دستور القاف"**:
* **الحزم:** لا انجراف خلف المشتتات السياسية أو الخيالات أثناء الكود.
* **الوضوح:** المهام تقسم إلى "مهام قزمة" (Micro-tasks).
* **المنطق أولاً:** بناء الـ Backend والعلاقات قبل الـ CSS والتصميم.

---

## 🚀 خارطة الطريق (Roadmap) - أسبوع النواة
- [x] إعداد هيكل Django الأساسي.
- [x] تفعيل نظام المصادقة واللغات والوضع الليلي.
- [ ] بناء موديلات الشركات (`companies` app).
- [ ] إنشاء محرك رفع الفرص والتقديم عليها.
- [ ] دمج أدوات تحليل البيانات (Pandas).

---

## 💻 تعليمات التشغيل السريع
1. **بيئة العمل:** `python -m venv venv`
2. **التفعيل:** `source venv/bin/activate` (أو `venv\Scripts\activate` على ويندوز)
3. **التثبيت:** `pip install -r requirements.txt`
4. **التشغيل:** `python manage.py runserver`

## ملاحظات هامه 
- ** إستعراض جميع المكتبات المثبتة حالياً مع أرقام إصداراتها الدقيقة وتحويلها الى ملف نصي  يجب تنفيذه بعد كل مكتبه يتم تثبيتها:** `pip freeze > requirements.txt`

- ## Create New app   
- `python manage.py startapp app_name`

----

## 🌍 نظام تعدد اللغات (Internationalization)

لإدارة وتحديث ترجمة المنصة، نستخدم أدوات `gettext`. اتبع الخطوات التالية:

### 1. استخراج النصوص (Extraction)
تقوم هذه الخطوة بمسح المشروع وجمع كل النصوص القابلة للترجمة في ملف `django.po`:
```bash
python manage.py makemessages -l ar 
```
> **ملاحظة:** يتطلب تثبيت أدوات `gettext-iconv` على نظام التشغيل أولاً.



```bash

    python -m pip install 'django-tailwind[cookiecutter,honcho,reload]'
    python manage.py tailwind dev #دعم تشغيل المكتبة اثناء التطوير  لظهور التنسيق على الواجهات
    python manage.py tailwind start
    
```

التفعيل: بعد إضافة الترجمات اليدوية، يجب تنفيذ هذا الأمر لتوليد ملفات الـ .mo السريعة:
```bash
python manage.py compilemessages
```
```bash
python manage.py makemigrations
```

### أنشئ المجلد الرئيسي ومجلدات فرعية للتنظيم 
```bash

mkdir static
mkdir static/css
mkdir static/js
mkdir static/img 
python manage.py compilemessages
```

### ملاحظات هامه قبل النشر 

أمر تجميع  كافة الملفات الساكنة (CSS, JS, Images) من جميع تطبيقات المشروع ووضعها في مجلد واحد نهائي (يُسمى STATIC_ROOT)  يجب تنفيذه قبل نشر الموقع على الاستضافات
```bash 
python manage.py collectstatic
```
```bash 
npx @tailwindcss/cli -i ./static/css/style.css -o ./static/css/output.css --watch
```

### install Auth system
```bash 
pip install django-allauth django-crispy-forms crispy-tailwind
```

### 🚀 خارطة الطريق (Roadmap) 
[x] بناء نظام الأدوار الديناميكي (Post-migrate Sync).

[x] إعداد منطق التوجيه الذكي (Role-based Redirect).

[X] بناء واجهات لوحات التحكم  (students app).

[X] دمج نظام رفع الوظائف للشركات.

[X] تفعيل نظام الإشعارات الفوري.

### 📝 ملاحظات هامة للمطورين 

- **دستور القاف: المنطق (Logic)** أولاً، العلاقات بين الجداول ثانياً، والتصميم آخراً. 

- التحديث: عند إضافة دور جديد في SITE_ROLES بالـ settings.py قم بتشغيل python manage.py migrate لتحديث قاعدة البيانات فوراً.

- الأمن: لا تقم بتعديل جدول الأدوار يدوياً من الـ DB؛ اعتمد دائماً على ملف الإعدادات.