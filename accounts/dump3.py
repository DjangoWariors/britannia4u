import concurrent
import csv
import io
import uuid
from datetime import datetime
from io import TextIOWrapper
from itertools import islice
from pathlib import Path
import threading
import pyotp
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AbstractBaseUser
from accounts.forms import UserInfoForm, UserForm, CSVUploadForm
from accounts.models import User, Region, State, BritanniaProgram, Tier, AboutProgram, RetailerPayout
from accounts.utils import detectUser, check_role_admin, generate_otp, send_sms
from britannia4u import settings
from britannia4u.utils import *
import pandas as pd


def send_otp(request):
    if request.method == 'POST':
        pass




def process_row(row, role):
    required_columns = ['User Name', 'First Name', 'Last Name', 'Email', 'Region', 'Program', 'Sub Program', 'Status']
    username = row.get('User Name')

    existing_usernames = User.objects.values_list('username', flat=True)

    if not username or username in existing_usernames:

        return None

    program = row['Program']
    try:
        program_obj = BritanniaProgram.objects.get(title=program)
    except:
        program_obj = None

    tier = row.get('tier')
    try:
        tier_obj = Tier.objects.get(name=tier)
    except:
        tier_obj = None

    status = True if row['Status'] == 'Active' else False
    try:
        region_obj = Region.objects.get(name=row['Region'])
    except:
        region_obj = None


    processed_data = {
        'username': username,
        'first_name': row.get('First Name'),
        'last_name': row.get('Last Name'),
        'role': row.get('ROLES'),  # Update this line with the 'role' parameter
        'email': row.get('Email'),
        'region': region_obj,
        'britannia_program': program_obj,
        'sub_program': row.get('Sub Program'),
        'is_active': status,
        'mobile_no': row.get('Mobile'),
        'ase': row.get('ASE User Name'),
        'area_sales_manager': row.get('ASM User Name'),
        'som': row.get('SOM User Name'),
        'rsm': row.get('RSM User Name'),
        'bdm': row.get('BDM'),
        'udm': row.get('UDM'),
        'rdm': row.get('RDM'),
        'nsm': row.get('NSM'),
        'nsdm': row.get('NSDM'),
        'vp_sales': row.get('VP Sales'),
        'distributor': row.get('Distributor'),
        'address': row.get('Address1'),
        'address2': row.get('Address2'),
        'city': row.get('City'),
        'state': row.get('State'),
        'pin_code': row.get('Pin'),
        'tier': tier_obj
    }



    return processed_data



def upload_user(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if csv_file.name.endswith(('.csv', '.xls', '.xlsx')):
                role = request.POST.get('role')
                df = pd.read_excel(csv_file)

                batch_size = 5000  # Adjust the batch size as needed

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = []
                    for batch_start in range(0, len(df), batch_size):
                        batch_end = min(batch_start + batch_size, len(df))
                        df_chunk = df.iloc[batch_start:batch_end]
                        futures.append(executor.submit(process_chunk, df_chunk, role))

                    concurrent.futures.wait(futures)

                messages.success(request, 'Users have been created successfully!')
                # return redirect('user-master')
            else:
                messages.error(request, 'Invalid file format. Please upload a CSV, Excel (.xls or .xlsx) file.')
        else:
            messages.error(request, 'Form is not valid. Please check your inputs.')
    else:
        form = CSVUploadForm()
    return render(request, 'b4u/accounts/upload-user.html', {'form': form})


def process_chunk(df, role):
    processed_rows = []
    csv_reader = df.to_dict('records')

    for idx, row in enumerate(csv_reader):

        processed_data = process_row(row, role)

        if processed_data:
            processed_rows.append(processed_data)

    save_to_database(processed_rows)


@transaction.atomic
def save_to_database(rows):
    users_to_create = [
        User(
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            region=row['region'],
            britannia_program=row['britannia_program'],
            sub_program=row['sub_program'],
            is_active=row['is_active'],
            mobile_no=row['mobile_no'],
            ase=row['ase'],
            area_sales_manager=row['area_sales_manager'],
            som=row['som'],
            rsm=row['rsm'],
            bdm=row['bdm'],
            udm=row['udm'],
            rdm=row['rdm'],
            nsm=row['nsm'],
            nsdm=row['nsdm'],
            vp_sales=row['vp_sales'],
            distributor=row['distributor'],
            address=row['address'],
            address2=row['address2'],
            city=row['city'],
            state=row['state'],
            pin_code=row['pin_code'],
            role=row['role'],
            tier=row.get('tier')
        ) for row in rows
    ]
    User.objects.bulk_create(users_to_create)


def upload_csv_payout(request):
    file_path = '20230720163304-RetailerPayoutReport.csv'
    absolute_file_path = Path(settings.MEDIA_ROOT) / file_path

    batch_size = 1000  # Adjust the batch size based on your system's memory capacity

    with open(absolute_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        objects_to_create = []
        count = 0

        for row in reader:
            count += 1

            username = row[3].strip()
            month = row[4].strip()
            year = row[5].strip()
            amount = row[6].strip()
            utr = row[7].strip()
            inserted_date_str = row[8].strip()
            remark = row[9].strip()

            Inserted_Date = row[10].strip()
            bank_name = row[11].strip()
            account_no = row[12].strip()
            status = row[13].strip()

            user_obj = User.objects.filter(username=username).first()

            print(inserted_date_str)
            try:
                inserted_date = datetime.strptime(inserted_date_str, '%d-%m-%Y').date()
            except ValueError:
                inserted_date = None

            payout = RetailerPayout(user=user_obj, month=month, year=year, amount=amount, utr=utr, date=inserted_date,
                                    bank_name=bank_name, account_no=account_no, remark=remark, status=status)
            payout.save()

    return HttpResponse('success')


def upload_csv_pre(request):
    file_path = '20230710165315-UserMasterReport-praveen.csv'
    absolute_file_path = Path(settings.MEDIA_ROOT) / file_path

    with open(absolute_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            username = row[1].strip()
            first_name = row[2].strip()
            last_name = row[3].strip()
            mobile = row[4].strip()
            email = row[5].strip()
            entity_name = row[6].strip()
            aw_code = row[7].strip()
            aw_name = row[8].strip()
            ase_user_name = row[9].strip()
            area_sales_manager = row[10].strip()

            udm = row[11].strip()
            rdm = row[12].strip()
            nsm = row[13].strip()

            nsdm = row[14].strip()
            vp_sales = row[15].strip()
            distributor_code = row[16].strip()
            address1 = row[17].strip()
            address2 = row[18].strip()

            region = row[19].strip()
            region_obj = Region.objects.filter(name=region).first()
            #
            pin = row[20].strip()
            regional_manager = row[21].strip()
            som_user_name = row[22].strip()
            roles = row[23].strip()

            tier = row[24].strip()
            tier_obj = Tier.objects.filter(name=tier).first()
            #
            program = row[25].strip()
            program_obj = BritanniaProgram.objects.filter(title=program).first()
            #
            sub_program = row[26].strip()
            status = row[27].strip()
            if status == 'Active':
                is_active = True
            else:
                is_active = False
            print(status)
            print(is_active)
            is_active = True

            inserted_date_str = row[28].strip()

            if not inserted_date_str:  # Skip empty date strings
                continue
            try:
                # Convert the date string to a Python datetime.date object
                inserted_date = datetime.strptime(inserted_date_str, '%d-%m-%Y').date()
            except ValueError:
                # Handle invalid date strings here (e.g., log an error, skip the row)
                continue

            udf1 = row[29].strip()
            udf2 = row[30].strip()

            user = User.objects.filter(email=email).exists()
            if not user:
                data_object = User(username=username, first_name=first_name, last_name=last_name, mobile_no=mobile,
                                   email=email,
                                   entity_name=entity_name, aw_code=aw_code, aw_name=aw_name,
                                   ase_user_name=ase_user_name,
                                   area_sales_manager=area_sales_manager, udm=udm, rdm=rdm, nsm=nsm, nsdm=nsdm,
                                   vp_sales=vp_sales,
                                   distributor_code=distributor_code, address=address1, address2=address2,
                                   region=region_obj,
                                   pin_code=pin, region_manager=regional_manager, som=som_user_name, role=roles,
                                   tier=tier_obj,
                                   britannia_program=program_obj, sub_program=sub_program, is_active=is_active,
                                   inserted_date=inserted_date,
                                   udf1=udf1, udf2=udf2

                                   )
                data_object.save()

    return HttpResponse('success')


def upload_csv_britinia_program(request):
    file_path = 'britinia program convertcsv.csv'
    absolute_file_path = Path(settings.MEDIA_ROOT) / file_path

    with open(absolute_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            title = row[0].strip()
            # tier = row[2].strip()

            # program = row[3].strip()
            status = 'Active'  # row[4].strip()

            # program_obj = BritanniaProgram.objects.filter(title=program).first()
            # tier_obj = Tier.objects.filter(name=tier).first()

            data_object = BritanniaProgram(title=title, status=status)
            data_object.save()

    return HttpResponse('success')


def upload_csv_region(request):
    file_path = 'region convertcsv.csv'
    absolute_file_path = Path(settings.MEDIA_ROOT) / file_path

    with open(absolute_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name = row[1].strip()
            # tier = row[2].strip()

            # program = row[3].strip()
            status = 'Active'  # row[4].strip()

            # program_obj = BritanniaProgram.objects.filter(title=program).first()
            # tier_obj = Tier.objects.filter(name=tier).first()

            data_object = Region(name=name, status=status)
            data_object.save()

    return HttpResponse('success')


def upload_csv_about_program(request):
    file_path = 'program convertcsv.csv'
    absolute_file_path = Path(settings.MEDIA_ROOT) / file_path

    with open(absolute_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            title = row[1].strip()
            tier = row[2].strip()

            program = row[3].strip()
            status = row[4].strip()

            program_obj = BritanniaProgram.objects.filter(title=program).first()
            tier_obj = Tier.objects.filter(name=tier).first()

            data_object = AboutProgram(title=title, britannia_program=program_obj, tier=tier_obj, status=status)
            data_object.save()

    return HttpResponse('success')


def upload_csv_tier(request):
    file_path = 'tier convertcsv.csv'
    absolute_file_path = Path(settings.MEDIA_ROOT) / file_path

    with open(absolute_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name = row[1].strip()
            amount = row[2].strip()
            if not amount:
                amount = '0.0'
            line = row[3].strip()
            if not line:
                line = ''
            program = row[4].strip()
            status = row[5].strip()

            program_obj = BritanniaProgram.objects.filter(title=program).first()

            data_object = Tier(name=name, amount=amount, britannia_program=program_obj, line=line, status=status)
            data_object.save()

    return HttpResponse('success')


def send_otp(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        user = User.objects.filter(username=username, mobile_no=mobile).first()

        print(username)
        print(mobile)

        if user is not None:
            message = f"OTP successfully sent on {mobile}"
            messages.success(request, message)

            otp = '123456'  # generate_otp()
            user.password = make_password(otp)
            user.secrete_otp = otp
            user.save()
            print(otp)
            mobile = '8077281897'
            msg = f"Your Happy code is {otp} Crazibrainsolutions"
            template = "1707161596296509163"
            # send_sms(mobile, msg, template)

            request.session['otp_message'] = message
            request.session['username'] = username
            context = {
                'otp_message': message
            }
            return render(request, 'b4u/accounts/otp.html', context)

        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('send-otp')
    return render(request, 'b4u/accounts/login.html')
    # count = User.objects.filter(tier__name__icontains='KAT').count()
    # print(count)
    # return HttpResponse('success')


def otp_verification(request):
    if 'username' not in request.session:
        return redirect('send-otp')
    username = request.session['username']
    otp_message = request.session['otp_message']
    user = User.objects.get(username=username)
    # user = auth.authenticate(username=username)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if user.secrete_otp == entered_otp:
            authenticate(username=username)
            if user is not None:
                user.secrete_otp = None
                # user.password = None
                user.save()
                login(request, User.objects.get(username=username))
                # del request.session['otp_message']
                return redirect('myAccount')
            else:
                error_message = 'Invalid OTP'
        else:
            error_message = 'Invalid OTP'
    else:
        error_message = ''
    context = {
        'error_message': error_message,
        'otp_message': otp_message
    }
    return render(request, 'b4u/accounts/otp.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)

            is_active = form.cleaned_data['is_active']

            if is_active == '1':
                is_active = True
            else:
                is_active = False
            user_form.is_active = is_active
            user_form.save()

            messages.success(request, 'User has been created successfully!')
            return redirect('user-master')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'user_form': form,
    }
    return render(request, 'b4u/accounts/registerUser.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            is_active = user_form.cleaned_data['is_active']
            if is_active == '1':
                is_active = True
            else:
                is_active = False
            user_form.is_active = is_active
            user_form.save()
            messages.success(request, 'user successfully updated.')
            return redirect('user-master')
        else:
            pass
    else:
        user_form = UserForm(instance=user)

    context = {
        'user_form': user_form,
        'user': user
    }

    return render(request, 'b4u/accounts/registerUser.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def delete_user(request, pk):
    obj = get_object_or_404(User, pk=pk)
    obj.delete()
    messages.success(request, 'user successfully deleted.')
    return redirect('user-master')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are successfully logged out.')
    return redirect('login')


# @login_required(login_url='send-otp')
def myAccount(request):
    user = request.user
    print(user)
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def adminDashboard(request):
    return render(request, 'b4u/cadmin/dashboard.html')

@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def userMaster(request):
    users = User.objects.all().order_by('-id')

    items_per_page = 5
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get('page')
    user_obj = paginator.get_page(page_number)

    context = {
        'users': user_obj,
    }

    return render(request, 'b4u/accounts/users-master.html', context)

@login_required(login_url='send-otp')
def userProfile(request, pk):
    user_id = pk

    profile = get_object_or_404(UserProfile, id=user_id)
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile successfully updated.')
            # return redirect('user-profile')
        else:
            pass


    else:
        profile_form = UserProfileForm(instance=profile)

        user_form = UserInfoForm(instance=user)

    context = {
        'profile_form': profile_form,
        'profile': profile,
        'user_form': user_form,
        'user_id': user_id
    }

    return render(request, 'cadmin/accounts/profile.html', context)


def reset_password(request, pk):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # pk = request.session.get('uid')
            # pk = request.user.id
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset-password', pk)
    context = {'pk': pk}
    return render(request, 'cadmin/accounts/reset_password.html', context)
