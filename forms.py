from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, ValidationError
from wtforms.validators import InputRequired, Email, Length, URL
from wtforms.fields.html5 import URLField


class LinkForm(FlaskForm):
    url = URLField(validators=[URL()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])


class DataForm(FlaskForm):
    section = SelectField('Section', choices=[
                          ('1', 'Section 1'), ('2', 'Section 2'), ('3', 'Section 3')], validators=[InputRequired()])
    change = StringField('Data', validators=[InputRequired()])
    source = URLField('Source', validators=[InputRequired(), URL()])


hierarchy_choices = [('very_important', 'Very Important'), (
    'important', 'important'), ('considered', 'considered'), ('not_considered', 'Not Considered')]


class HierarchyForm(FlaskForm):
    rigor = SelectField("Rigor of secondary school record",
                        choices=hierarchy_choices,)
    rank = SelectField("Class rank", choices=hierarchy_choices,
                       )
    gpa = SelectField("Academic GPA", choices=hierarchy_choices,
                      )
    test_scores = SelectField("Standardized test scores",
                              choices=hierarchy_choices,)
    essay = SelectField("Application essay",
                        choices=hierarchy_choices,)
    recommendations = SelectField(
        "Recommendation(s)", choices=hierarchy_choices,)
    interview = SelectField(
        "Interview", choices=hierarchy_choices,)
    extracurriculars = SelectField(
        "Extracurriculars", choices=hierarchy_choices,)
    talent = SelectField(
        "Talent/ability", choices=hierarchy_choices,)
    character = SelectField("Character/personal qualities",
                            choices=hierarchy_choices,)
    first_generation = SelectField(
        "First generation", choices=hierarchy_choices,)
    alumni = SelectField(
        "Alumni/ae relation", choices=hierarchy_choices,)
    geographical = SelectField(
        "Geographical residence", choices=hierarchy_choices,)
    state_residency = SelectField(
        "State residency", choices=hierarchy_choices,)
    religion = SelectField("Religious affiliation/committment",
                           choices=hierarchy_choices,)
    race = SelectField("Racial/ethnic status",
                       choices=hierarchy_choices,)
    volunteer = SelectField(
        "Volunteer work", choices=hierarchy_choices,)
    work_experience = SelectField(
        "Work experience", choices=hierarchy_choices,)
    interest_level = SelectField(
        "Level of applicant's interest", choices=hierarchy_choices,)
    source = URLField('Source', validators=[InputRequired(), URL()])


class AidForm(FlaskForm):
    section = SelectField('Section', choices=[
                          ('1', 'FinAidSection 1'), ('2', 'FinAidSection 2'), ('3', 'FinAidSection 3')], validators=[InputRequired()])
    change = StringField('Data', validators=[InputRequired()])
    source = URLField('Source', validators=[InputRequired(), URL()])


def validate_url(form, field):
    if field.data[0:24] != 'https://www.youtube.com/' and field.data[0:17] != 'https://youtu.be/':
        raise ValidationError('Must be a YouTube link')


class AnectodeForm(FlaskForm):
    url = URLField('YouTube URL', validators=[
                   InputRequired(), URL(), validate_url])
