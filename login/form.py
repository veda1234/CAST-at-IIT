from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired

from login.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    organisation = StringField('Organisation',
                               validators=[DataRequired()])
    country = StringField('Country',
                          validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one')


class UserDatabaseForm(FlaskForm):
    Site_Unit = StringField('Site Unit', validators=[DataRequired()])
    Compound = StringField('Compound', validators=[DataRequired()])
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[DataRequired()])
    Plume_length = FloatField('Plume Length', validators=[DataRequired()])
    Plume_Width = FloatField('Plume Width', validators=[DataRequired()])
    Hydraulic_conductivity = FloatField('Hydraulic Conductivity', validators=[DataRequired()])
    Electron_Donor = FloatField('Electron Donor', validators=[DataRequired()])
    O2 = FloatField('O2', validators=[DataRequired()])
    NO3 = FloatField('NO3', validators=[DataRequired()])
    SO4 = FloatField('SO4', validators=[DataRequired()])
    Fe = FloatField('Fe', validators=[DataRequired()])
    Plume_state = StringField('Plume State', validators=[DataRequired()])
    Chem_Group = StringField('Chemical Group', validators=[DataRequired()])
    Country = StringField('Country', validators=[DataRequired()])
    Literature_Source = StringField('Literature Source', validators=[DataRequired()])
    submit = SubmitField('Add Data')


class LiedlForm(FlaskForm):
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[DataRequired()])
    Transverse_Dispersivity = FloatField('Transverse Dispersivity', validators=[DataRequired()])
    Stoichiometry_coefficient = FloatField('Stoichiometry coefficient', validators=[DataRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[DataRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')


class ChuForm(FlaskForm):
    Width = FloatField('Width', validators=[DataRequired()])
    Transverse_Horizontal_Dispersivity = FloatField('Transverse Horizontal Dispersivity', validators=[DataRequired()])
    Reaction_Stoichiometric_Ratio = FloatField('Reaction Stoichiometric Ratio', validators=[DataRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[DataRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[DataRequired()])
    Biological_Factor = FloatField('Biological Factor', validators=[InputRequired("Please enter a valid value")])
    submit = SubmitField('Generate Graph')


class HamForm(FlaskForm):
    Width = FloatField('Width', validators=[DataRequired()])
    Horizontal_Transverse_Dispersivity = FloatField('Horizontal Transverse Dispersivity', validators=[DataRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[DataRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')


class Liedl3DForm(FlaskForm):
    Source_Thickness = FloatField('Source Thickness', validators=[DataRequired()])
    Vertical_Transverse_Dispersivity = FloatField('Vertical Transverse Dispersivity', validators=[DataRequired()])
    Source_Width = FloatField('Source Width', validators=[DataRequired()])
    Horizontal_Transverse_Dispersivity = FloatField('Horizontal Transverse Dispersivity', validators=[DataRequired()])
    Stoichiometric_Ratio = FloatField('Stoichiometric Ratio', validators=[DataRequired()])
    Partner_Reactant_Concentration = FloatField('Partner Reactant Concentration', validators=[DataRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[DataRequired()])
    Threshold_Contaminant_Concentration = FloatField('Threshold Contaminant Concentration', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')


class BirlaForm(FlaskForm):
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[DataRequired()])
    Vertical_Transverse_Dispersivity = FloatField('Vertical Transverse Dispersivity', validators=[DataRequired()])
    Stoichiometry_coefficient = FloatField('Stoichiometry coefficient', validators=[DataRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[DataRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[DataRequired()])
    Recharge_Rate = FloatField('Recharge Rate', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')


class MaierGrathwohlForm(FlaskForm):
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[DataRequired()])
    Vertical_Transverse_Dispersivity = FloatField('Vertical Transverse Dispersivity', validators=[DataRequired()])
    Stoichiometry_coefficient = FloatField('Stoichiometry coefficient', validators=[DataRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[DataRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')


class NumericalForm(FlaskForm):
    # Domain
    Lx = FloatField('Lx', validators=[DataRequired()])
    Ly = FloatField('Ly', validators=[DataRequired()])
    ztop = IntegerField('ztop', validators=[InputRequired()])
    zbot = FloatField('zbot', validators=[DataRequired()])
    ncol = IntegerField('ncol', validators=[DataRequired()])
    nrow = IntegerField('nrow', validators=[DataRequired()])
    nlay = IntegerField('nlay', validators=[DataRequired()])
    # Parameters
    prsity = FloatField('prsity', validators=[DataRequired()])
    al = FloatField('al', validators=[DataRequired()])
    trpt = FloatField('trpt', validators=[DataRequired()])
    Gamma = FloatField('Gamma', validators=[DataRequired()])
    Cd = FloatField('Cd', validators=[DataRequired()])
    Ca = FloatField('Ca', validators=[DataRequired()])
    h1 = FloatField('h1', validators=[DataRequired()])
    h2 = FloatField('h2', validators=[InputRequired()])
    hk = FloatField('hk', validators=[DataRequired()])
    perlen = FloatField('perlen', validators=[DataRequired()])
    # Flow
    flow_bound_1 = FloatField('flow_bound_1', validators=[DataRequired()])
    flow_bound_2 = FloatField('flow_bound_2', validators=[DataRequired()])
    # Transport
    tran_bound_1 = FloatField('tran_bound_1', validators=[DataRequired()])
    tran_bound_2 = FloatField('tran_bound_2', validators=[DataRequired()])
    tran_bound_3 = FloatField('tran_bound_3', validators=[DataRequired()])
    tran_bound_4 = FloatField('tran_bound_4', validators=[DataRequired()])
    submit = SubmitField('Run')
