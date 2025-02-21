from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from company.models import Company, CompanyApprovalValidationApplication, EvaluationByStudent
from users.models import EngineeringDepartment
from users.models import Student, Course, Instructor

# Create your models here.

yes_no_choices = ('Yes', 'Yes'), ('No', 'No')
satisfactory_choices = ('Satisfactory', 'Satisfactory'), ('Revision Required',
                                                          'Revision Required'), ('Unsatisfactory', 'Unsatisfactory')


class Status(models.TextChoices):
    PENDING = 'PE', 'Pending'
    ACCEPTED = 'AC', 'Accepted'
    REJECTED = 'RE', 'Rejected'


class SubmissionStatus(models.TextChoices):
    SATISFACTORY = 'SA', 'Satisfactory',
    REVISION_REQUIRED = 'RR', 'Revision Required',
    UNSATISFACTORY = 'UN', 'Unsatisfactory',
    PENDING = 'PE', 'Pending'


class Task(models.Model):
    creation_date = models.DateTimeField(null=True)
    description = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='uploads/', null=True)


class Submission(Task):
    internship = models.ForeignKey('Internship', on_delete=models.CASCADE, null=True, related_name='submissions')
    status = models.CharField(
        max_length=2,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING,
    )
    due_date = models.DateTimeField()


class Feedback(Task):
    submission_field = models.OneToOneField(
        Submission, on_delete=models.CASCADE, null=True, related_name='feedback')


class FormModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    submission_date = models.DateTimeField(auto_now=True, editable=False)
    description = models.CharField(max_length=100, null=True)


class ConfidentialCompany(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    company_name = models.CharField(max_length=100)
    is_work_related = models.CharField(max_length=3, choices=yes_no_choices)
    supervisor_background = models.CharField(
        max_length=3, choices=yes_no_choices)


class ExtensionRequest(models.Model):
    extension_date = models.DateTimeField()
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, null=True, related_name='extension')


class WorkAndReportEvaluation(models.Model):
    grade_of_performing_work = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    grade_of_solving_engineering_problems = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    grade_of_recognizing_ethics = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    grade_of_acquiring_knowledge = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                       blank=True, null=True)
    grade_of_applying_knowledge = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                      blank=True, null=True)
    grade_of_has_awareness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                 blank=True, null=True)
    grade_of_making_judgements = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                     blank=True, null=True)
    grade_of_preparing_reports = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                     blank=True, null=True)

    exp_is_able_to_perform_work = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_solve_engineering_problems = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_recognize_ethics = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_acquire_knowledge = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_apply_new_knowledge = models.CharField(
        max_length=100, blank=True, null=True)
    exp_has_awareness = models.CharField(max_length=100, blank=True, null=True)
    exp_is_make_informed_judgments = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_prepare_reports = models.CharField(
        max_length=100, blank=True, null=True)

    total_work_grade = models.IntegerField(null=True)

    def calculate_total_grade(self):

        self.total_work_grade = 0
        grade_list = list()
        grade_list.append(self.grade_of_performing_work)
        grade_list.append(self.grade_of_solving_engineering_problems)
        grade_list.append(self.grade_of_recognizing_ethics)
        grade_list.append(self.grade_of_acquiring_knowledge)
        grade_list.append(self.grade_of_applying_knowledge)
        grade_list.append(self.grade_of_has_awareness)
        grade_list.append(self.grade_of_making_judgements)
        grade_list.append(self.grade_of_preparing_reports)
        for grade in grade_list:
            if grade is not None:
                self.total_work_grade = self.total_work_grade + grade
        self.save()
        if self.total_work_grade:
            return self.total_work_grade
        else:
            return None


class Internship(models.Model):
    # Models
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, related_name='internship')
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, related_name='internship', default=None)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, related_name='internship')
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name='internship')

    # Forms
    work_and_report_evaluation_form = models.OneToOneField(WorkAndReportEvaluation, on_delete=models.SET_NULL,
                                                           null=True, related_name='internship', default=None)
    confidential_company_form = models.OneToOneField(
        ConfidentialCompany, on_delete=models.SET_NULL, null=True, related_name='internship', default=None)

    # Current status of the internship
    status = models.CharField(
        max_length=2,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING,
    )

    # Company Related Demands
    company_approval = models.OneToOneField(
        CompanyApprovalValidationApplication, on_delete=models.SET_NULL, null=True, related_name='internship')
    company_evaluation = models.OneToOneField(
        EvaluationByStudent, on_delete=models.SET_NULL, null=True, related_name='internship', default=None)

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name + "'s " + self.course.name + " Course"


class StudentReport(models.Model):
    report = models.FileField(upload_to='reports/', null=True)


class InstructorFeedback(models.Model):
    feedback = models.FileField(upload_to='feedbacks/', null=True)


class Statistic(models.Model):
    report_grade_average = models.FloatField(null=True)
    work_evaluation_grade_average = models.FloatField(null=True)
    company_evaluation_grade_average = models.FloatField(null=True)
    internship_satisfaction_number = models.IntegerField(null=True)
    internship_unsatisfaction_number = models.IntegerField(null=True)
    internship_pending_number = models.IntegerField(null=True)
    department = models.ForeignKey(EngineeringDepartment, on_delete=models.CASCADE, null=True, related_name='statistic')

    def calculate_report_grade_average(self):
        report_grade_average = 0
        count = 0
        for internship in Internship.objects.all().filter(student__department=self.department):
            if internship.work_and_report_evaluation_form and \
                    internship.work_and_report_evaluation_form.grade_of_preparing_reports:
                report_grade_average += internship.work_and_report_evaluation_form.grade_of_preparing_reports
                count = count + 1
        if count:
            report_grade_average /= count
        else:
            return None
        return report_grade_average

    def calculate_work_grade_average(self):
        work_grade_average = 0
        count = 0
        for internship in Internship.objects.all().filter(student__department=self.department):
            print("Inside the loop")
            if internship.work_and_report_evaluation_form and \
                    internship.work_and_report_evaluation_form.calculate_total_grade():
                work_grade_average += internship.work_and_report_evaluation_form.calculate_total_grade()
                print("Work grade average: ", work_grade_average)
                count += 1
        if count:
            work_grade_average /= count
            if self.calculate_report_grade_average():
                return work_grade_average - self.calculate_report_grade_average()
            else:
                return work_grade_average
        else:
            return None

    def calculate_company_evaluation_grade_average(self):
        confidential_company = 0
        count = 0
        for internship in Internship.objects.all().filter(student__department=self.department):
            if internship.confidential_company_form:
                confidential_company = confidential_company + internship.confidential_company_form.grade
                count = count + 1
        if count:
            confidential_company /= count
        else:
            return None
        return confidential_company

    def calculate_internship_statuses(self):
        satisfactory = 0
        unsatisfactory = 0
        pending = 0
        for internship in Internship.objects.all().filter(student__department=self.department):
            if internship.status == SubmissionStatus.PENDING:
                pending += 1
            elif internship.status == SubmissionStatus.SATISFACTORY:
                satisfactory += 1
            else:
                unsatisfactory += 1
            print("Internship with ", internship, " department: ", internship.student.department)
            if internship.confidential_company_form:
                print("Internship with confidential company grade ", internship.confidential_company_form.grade)
            if internship.work_and_report_evaluation_form:
                print("Internship with work and report evaluation grade",
                      internship.work_and_report_evaluation_form.total_work_grade)
        return satisfactory, pending, unsatisfactory

    def save(self, *args, **kwargs):
        self.calculate_all()
        super().save(*args, **kwargs)

    def calculate_all(self):
        self.report_grade_average = self.calculate_report_grade_average()
        self.work_evaluation_grade_average = self.calculate_work_grade_average()
        self.company_evaluation_grade_average = self.calculate_company_evaluation_grade_average()
        self.internship_satisfaction_number, self.internship_pending_number, \
            self.internship_unsatisfaction_number = self.calculate_internship_statuses()
        print(self.report_grade_average, self.work_evaluation_grade_average, self.company_evaluation_grade_average)
