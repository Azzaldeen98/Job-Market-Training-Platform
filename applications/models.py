from django.db import models
from django.utils import timezone
from core.base_models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from core.utils import current_date


# Create your models here.

class JoinTrainingOpportunity(BaseModel):

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        INVITED = 'invited', _('Invited')
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        ON_TRAINING = 'on_training', _('On Training')
        COMPLETED = 'completed', _('Completed')

    # STATUS_CHOICES = [
    #     ('draft', _('Draft')),  # مسودة لدى الطالب
    #     ('invited', _('Invited')),  # دعوة مرسلة من الشركة للطالب (جديد)
    #     ('pending', _('Pending')),  # الطالب قدم أو قبل الدعوة وهي قيد المراجعة
    #     ('accepted', _('Accepted')),  # تم قبول الطالب في الفرصة
    #     ('rejected', _('Rejected')),  # تم رفض الطلب
    #     ('on_training', _('On Training')),  # الطالب يباشر التدريب حالياً
    #     ('completed', _('Completed')),  # تم إنهاء التدريب بنجاح
    # ]

    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name="applications"
    )

    # الربط مع الفرصة (يجب استيرادها من التطبيق الآخر)
    opportunity = models.ForeignKey(
        'training_entities.TrainingOpportunity',
        on_delete=models.CASCADE,
        related_name="applicants"
    )

    match_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Match Score (%)"),
        help_text=_("Matching percentage based on skills and requirements")
    )

    # الحالة والتوقيت
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Training Application")
        verbose_name_plural = _("Training Applications")
        unique_together = ('student', 'opportunity')
        # ترتيب الطلبات حسب الأعلى مطابقة تلقائياً
        ordering = ['-match_score', '-created_at']

    def __str__(self):
        return f"{self.student.user.username} -> {self.opportunity.title} ({self.status})"


    @property
    def is_pending(self):
        """هل الطلب لا يزال تحت المراجعة؟"""
        return self.status == 'pending'

    @property
    def is_accepted(self):
        """هل تم قبول الطالب (قبول مبدئي)؟"""
        return self.status == 'accepted'

    @property
    def is_rejected(self):
        """هل تم رفض الطلب؟"""
        return self.status == 'rejected'

    @property
    def is_active_training(self):
        """هل الطالب حالياً يباشر التدريب في الشركة؟"""
        return self.status == 'on_training'

    @property
    def is_completed(self):
        """هل أنهى الطالب فترة التدريب بالكامل؟"""
        return self.status == 'completed'

    @property
    def can_be_edited(self):
        """هل يمكن تعديل الطلب؟ (فقط إذا كان مسودة أو تحت الانتظار)"""
        return self.status in ['draft', 'pending']

    # دالة إضافية للحصول على التسمية المقروءة للحالة (بالعربي أو الإنجليزي)
    def get_status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status)

    @property
    def is_currently_training(self):
        """
        التحقق أن الطالب بدأ التدريب ولم ينتهِ بعد.
        الشرط: الحالة 'on_training' والتاريخ الحالي يقع بين تاريخ البدء والانتهاء.
        """
        today = current_date()
        # نصل لتاريخ الفرصة عبر العلاقة (ForeignKey)
        start = self.opportunity.start_date
        end = self.opportunity.end_date

        return self.status == 'on_training' and start <= today <= end

    @property
    def training_progress_percentage(self):
        """
        حساب نسبة الإنجاز في التدريب (اختياري - مفيد للواجهات الرسومية).
        """
        today = current_date()
        start = self.opportunity.start_date
        end = self.opportunity.end_date

        if today < start: return 0
        if today > end: return 100

        total_days = (end - start).days
        days_passed = (today - start).days

        if total_days > 0:
            return round((days_passed / total_days) * 100)
        return 0