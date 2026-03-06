////
//////    // عند الضغط على زر التبديل
////    function toggleDarkMode() {
////        if (document.documentElement.classList.contains('dark')) {
////            document.documentElement.classList.remove('dark');
////            localStorage.setItem('theme', 'light');
////        } else {
////            document.documentElement.classList.add('dark');
////            localStorage.setItem('theme', 'dark');
////        }
////    }
////
////    // التحقق من الثيم المفضل عند تحميل الصفحة
////    if (localStorage.getItem('theme') === 'dark' ||
////        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
////        document.documentElement.classList.add('dark');
////    }
//
////
//
//
//// 1. وظيفة التطبيق (تنفيذ التغيير البصري)
//function applyTheme(theme) {
//    const root = document.documentElement;
//    if (theme === 'dark') {
//        root.classList.add('dark');
//        root.setAttribute('data-theme', 'dark'); // دعم DaisyUI وأي مكتبة Attributes
//    } else {
//        root.classList.remove('dark');
//        root.setAttribute('data-theme', 'light');
//    }
//}
//
//// 2. وظيفة التبديل والمزامنة (القلب النابض)
//// يدعم الزوار (غير المسجلين) والأعضاء (المسجلين) معاً،
//async function toggleTheme() {
//alert(6666)
//    const currentTheme = localStorage.getItem('theme') || 'light';
//    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
//
//    // 1. التنفيذ البصري والمحلي (يعمل للجميع: زوار وأعضاء)
//    applyTheme(newTheme);
//    localStorage.setItem('theme', newTheme);
//
//    // 2. المزامنة مع السيرفر (فقط إذا كان المستخدم مسجلاً)
//    // نتحقق من وجود المستخدم عبر متغير يمرره Django
//    const isUserAuthenticated = "{{ user.is_authenticated|yesno:'true,false' }}" === 'true';
//
//    if (isUserAuthenticated) {
//        try {
//            await fetch('{% url "core:toggle_theme" %}', {
//                method: 'POST',
//                headers: {
//                    'X-CSRFToken': '{{ csrf_token }}',
//                    'Content-Type': 'application/json'
//                },
//                body: JSON.stringify({ 'theme': newTheme })
//            });
//        } catch (err) {
//            console.warn("Server sync failed.");
//        }
//    }
//}
//
//// 3. التشغيل الفوري (Anti-Flash Logic)
//
//(function initTheme() {
//    // 1. جلب الثيم من السيرفر (تعمل فقط إذا كان الكود داخل HTML)
//    const serverTheme = "{{ request.session.theme }}".trim();
//
//    // 2. جلب الثيم من المتصفح
//    const localTheme = localStorage.getItem('theme');
//
//    // 3. جلب إعدادات النظام
//    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
//
//    // المنطق المصلح: إذا كان هناك ثيم في السيرفر استخدمه،
//    // إذا لم يكن هناك (أو كان فارغاً) استخدم التخزين المحلي، وإلا فالنظام.
//    let finalTheme = 'light';
//
//    if (serverTheme && serverTheme !== "" && serverTheme !== "None") {
//        finalTheme = serverTheme;
//    } else if (localTheme) {
//        finalTheme = localTheme;
//    } else {
//        finalTheme = systemTheme;
//    }
//
//    applyTheme(finalTheme);
//
//    // تحديث التخزين المحلي لضمان المزامنة في المرة القادمة
//    localStorage.setItem('theme', finalTheme);
//})();
//
//
////(function initTheme() {
////    // الأولوية 1: القيمة القادمة من Django (لو مررتها في الـ context)
////    // الأولوية 2: القيمة المحفوظة في المتصفح
////    // الأولوية 3: إعدادات نظام تشغيل المستخدم
////    const savedTheme = localStorage.getItem('theme') ||
////                      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
////    applyTheme(savedTheme);
////})();