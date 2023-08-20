from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User, Region, BritanniaPoint

from accounts.utils import check_role_admin
from app.forms import RegionForm


# Create your views here.




@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def regionMaster(request):
    users = Region.objects.all().order_by('-id')

    items_per_page = 20
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)

    context = {
        'region': obj,
    }

    return render(request, 'b4u/cadmin/region/region-master.html', context)


@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def addRegion(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            messages.success(request, 'Region has been created successfully!')
            return redirect('region-master')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = RegionForm()
    context = {
        'form': form,
    }

    return render(request, 'b4u/cadmin/region/add-region.html', context)


@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def updateRegion(request, pk):
    region = get_object_or_404(Region, id=pk)
    if request.method == 'POST':

        region_form = RegionForm(request.POST, instance=region)
        if region_form.is_valid():

            region_form.save()
            messages.success(request, 'region successfully updated.')
            return redirect('region-master')
        else:
            pass
    else:
        form = RegionForm(instance=region)

    context = {
        'form': form,
        'region': region
    }

    return render(request, 'b4u/cadmin/region/add-region.html', context)


@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def deleteRegion(request, pk):
    obj = get_object_or_404(Region, pk=pk)
    obj.delete()
    messages.success(request, 'region successfully deleted.')
    return redirect('region-master')


@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def britaniaPoints(request):
    points = BritanniaPoint.objects.all().order_by('-id')

    items_per_page = 20
    paginator = Paginator(points, items_per_page)
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)

    context = {
        'point': obj,
    }

    return render(request, 'b4u/cadmin/points/points-master.html', context)


def process_row(row, role):
    if row.get('User Name') or row.get('Retailer Id'):
        if row.get('User Name'):
            user = row.get('User Name')

        if row.get('Retailer Id'):
            user = row.get('Retailer Id')

        user = User.objects.get(username=user)
        inserted_date_str = row.get('Retailer Id')
        try:
            inserted_date = datetime.strptime(inserted_date_str, '%d-%m-%Y').date()
        except ValueError:
            inserted_date =None

        processed_data = {
            'username': user,
            'month': row.get('Month'),
            'year': row.get('Year'),
            'amount': row.get('Pay Out In Rs'),
            'utr': row.get('UTR NO'),
            'bpu_date': row.get('BPU DATE'),
            'bpu_remark': row.get('BPU Remark'),
            'date': inserted_date,
            'bank_name': row.get('Bank Name'),
            'account_no': row.get('Account Number'),
            'ifsc_code': row.get('IFSC Code'),
            'status': row.get('Status'),
        }
        return processed_data
    else:
        return None


@login_required(login_url='send-otp')
@user_passes_test(check_role_admin)
def uploadPoints(request):
    if request.method == 'POST':
        form = UploadPointsForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded CSV file and decode it
            csv_file = request.FILES['csv_file']
            role = request.POST.get('role')

            decoded_file = csv_file.read().decode('utf-8-sig')
            csv_reader = csv.DictReader(decoded_file.splitlines())

            batch_size = 1000  # Adjust the batch size based on your dataset
            processed_rows = []

            for idx, row in enumerate(csv_reader):

                processed_data = process_row(row, role)

                if processed_data:
                    processed_rows.append(processed_data)

                if idx % batch_size == 0:
                    # Save processed data to the database in batches
                    try:
                        save_to_database(processed_rows)
                    except IntegrityError as e:
                        # Handle duplicates or other integrity errors here
                        # For example, log the error, skip the row, or update existing entries
                        print(f"IntegrityError: {e}")
                    processed_rows.clear()

            # Save any remaining rows in the last batch
            try:
                save_to_database(processed_rows)
            except IntegrityError as e:
                # Handle duplicates or other integrity errors here
                # For example, log the error, skip the row, or update existing entries
                print(f"IntegrityError: {e}")

            messages.success(request, 'User has been created successfully!')
            return redirect('user-master')
    else:
        form = UploadPointsForm()
    return render(request, 'b4u/accounts/upload-user.html', {'form': form})

@transaction.atomic
def save_to_database(rows):

    # Perform a bulk create to efficiently save data to the database in a single transaction
    User.objects.bulk_create([
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
    ])
