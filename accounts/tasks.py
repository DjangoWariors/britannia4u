import json

import pandas as pd
from celery import shared_task
from django.db import transaction

from accounts.models import User


@shared_task()
def process_chunk(data):
    data_dict = json.loads(data)
    path = data_dict.get('path')
    role = data_dict.get('role')
    data = pd.read_excel(path)
    df = data.fillna('')  # Fill NaN values with empty string

    chunk_size = 1000
    total_records = len(df)
    num_chunks = (total_records + chunk_size - 1) // chunk_size

    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min((chunk_idx + 1) * chunk_size, total_records)
        chunk_df = df.iloc[start_idx:end_idx]

        records = []

        for _, row in chunk_df.iterrows():
            username = row.get('User Name')
            if username:
                existing_usernames = User.objects.values_list('username', flat=True)
                if username not in existing_usernames:
                    program = row.get('Program')
                    tier = row.get('tier')
                    status = True if row['Status'] == 'Active' else False

                    region = '' #row.get('Region')

                    record = User(
                        username=username,
                        first_name=row.get('First Name'),
                        last_name=row.get('Last Name'),
                        email=row.get('Email'),
                        region_id=region,
                        britannia_program_id=program,
                        sub_program=row.get('Sub Program'),
                        is_active=status,
                        mobile_no=row.get('Mobile'),
                        ase=row.get('ASE User Name'),
                        area_sales_manager=row.get('ASM User Name'),
                        som=row.get('SOM User Name'),
                        rsm=row.get('RSM User Name'),
                        bdm=row.get('BDM'),
                        udm=row.get('UDM'),
                        rdm=row.get('RDM'),
                        nsm=row.get('NSM'),
                        nsdm=row.get('NSDM'),
                        vp_sales=row.get('VP Sales'),
                        distributor=row.get('Distributor'),
                        address=row.get('Address1'),
                        address2=row.get('Address2'),
                        city=row.get('City'),
                        state=row.get('State'),
                        pin_code=row.get('Pin'),
                        role=row.get('ROLES'),  # Avoid using the same name 'role'
                        tier_id=tier
                    )
                    records.append(record)

        if records:
            with transaction.atomic():
                User.objects.bulk_create(records)

    return 'Data successfully stored'