def can_company_invite(student_application):
    """
    تختبر ما إذا كان يحق للشركة إرسال دعوة لهذا الطالب.
    """
    # إذا لم يوجد سجل، يسمح بالإرسال
    if student_application is None:
        return True

    # إذا وجد سجل، يسمح فقط إذا كان في حالة 'Draft'
    if student_application.status == 'draft':
        return True

    # في بقية الحالات (pending, accepted, invited, etc.) لا يسمح
    return False