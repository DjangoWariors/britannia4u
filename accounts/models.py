import uuid as uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission


class State(models.Model):
    STATE_CHOICE = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=80)
    status = models.CharField(max_length=50, choices=STATE_CHOICE, blank=True, null=True)
    country = models.CharField(max_length=80, default='India', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Region(models.Model):
    STATE_CHOICE = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=80)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATE_CHOICE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class BritanniaProgram(models.Model):
    STATE_CHOICE = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    title = models.CharField(max_length=80)
    status = models.CharField(max_length=50, choices=STATE_CHOICE, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Tier(models.Model):
    STATE_CHOICE = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=80)
    amount = models.FloatField(null=True, blank=True)
    line = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATE_CHOICE, blank=True, null=True)
    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AboutProgram(models.Model):
    STATE_CHOICE = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    status = models.CharField(max_length=50, choices=STATE_CHOICE, blank=True, null=True)
    title = models.CharField(max_length=80)

    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)

    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True, blank=True)

    priority = models.IntegerField(default=0)

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ROLE_CHOICE = (
        ('Admin', 'Admin'),
        ('ASE', 'ASE'),
        ('ASM', 'ASM'),
        ('BDM', 'BDM'),
        ('Distributor', 'Distributor'),
        ('KYC', 'Approver'),
        ('NSDM', 'NSDM'),
        ('NSM', 'NSM'),
        ('Program Admin', 'Program Admin'),
        ('RDM', 'RDM'),

        ('Readonly Admin', 'Readonly Admin'),
        ('Retailer', 'Retailer'),

        ('RSM', 'RSM'),
        ('SOM', 'SOM'),
        ('UDM', 'UDM'),
        ('VP Sales', 'VP Sales'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, )
    role = models.CharField(max_length=50, choices=ROLE_CHOICE, null=True, blank=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    username = models.CharField(max_length=80, unique=True)
    email = models.CharField(max_length=80)
    phone_no = models.CharField(max_length=15, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    entity_name = models.CharField(max_length=80, blank=True)

    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True, blank=True)

    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)

    region_manager = models.CharField(max_length=80, blank=True)
    area_sales_manager = models.CharField(max_length=80, blank=True)
    som = models.CharField(max_length=80, blank=True)
    ase = models.CharField(max_length=80, blank=True)
    udm = models.CharField(max_length=80, blank=True)
    rdm = models.CharField(max_length=80, blank=True)
    nsm = models.CharField(max_length=80, blank=True)
    nsdm = models.CharField(max_length=80, blank=True)
    vp_sales = models.CharField(max_length=80, blank=True)
    distributor = models.CharField(max_length=80, blank=True)
    distributor_code = models.CharField(max_length=50, blank=True)
    sub_program = models.CharField(max_length=80, blank=True)
    bdm = models.CharField(max_length=80, blank=True)

    udf1 = models.CharField(max_length=80, blank=True)
    udf2 = models.CharField(max_length=80, blank=True)

    aw_code = models.CharField(max_length=80, blank=True)
    aw_name = models.CharField(max_length=80, blank=True)

    #ase_user_name = models.CharField(max_length=80, blank=True)

    rsm = models.CharField(max_length=80, blank=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    personal_email = models.EmailField(null=True, blank=True)
    mobile_no = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, default='India', blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)

    secrete_otp = models.CharField(max_length=10, blank=True, null=True)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserKyc(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    mobile_no = models.CharField(max_length=12, blank=True, null=True)
    secondary_no = models.CharField(max_length=12, blank=True, null=True)
    aadhar_no = models.CharField(max_length=15, blank=True, null=True)
    pan_no = models.CharField(max_length=15, blank=True, null=True)
    gst_no = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, default='India', blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.first_name

class BritanniaPayoutYearMaster(models.Model):
    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.britannia_program_name


class RetailerPayout(models.Model):
    britannia_payout_year_master = models.ForeignKey(BritanniaPayoutYearMaster, on_delete=models.SET_NULL, blank=True,
                                                   null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)

    po = models.CharField(max_length=256, null=True, blank=True)
    regular = models.CharField(max_length=256, null=True, blank=True)
    exception = models.CharField(max_length=256, null=True, blank=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)
    amount = models.FloatField(default=0, null=True, blank=True)
    utr = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    bank_name = models.CharField(max_length=256, null=True, blank=True)
    account_no = models.CharField(max_length=30, null=True, blank=True)

    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)

    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)

    remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

class BritanniaSaleYearMaster(models.Model):
    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.britannia_program_name



class SalesData(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    britannia_sale_year_master = models.ForeignKey(BritanniaSaleYearMaster, on_delete=models.SET_NULL, blank=True, null=True)
    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)
    overall_mtd = models.CharField(max_length=15, null=True, blank=True, help_text='In lakhs')
    biscuit_mtd = models.CharField(max_length=15, null=True, blank=True)
    crdal_mtd = models.CharField(max_length=15, null=True, blank=True)
    unique_line_mtd = models.CharField(max_length=15, null=True, blank=True)
    focus_sale1 = models.CharField(max_length=15, null=True, blank=True)
    focus_sale2 = models.CharField(max_length=15, null=True, blank=True)
    cheese = models.CharField(max_length=15, null=True, blank=True)
    ghee = models.CharField(max_length=15, null=True, blank=True)
    visibility = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class TrendAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, help_text='Store Retailer', blank=True, null=True)
    week = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    store_id = models.CharField(max_length=10, null=True, blank=True)
    benchmark = models.TextField(null=True, blank=True)
    biscuit = models.CharField(max_length=80, null=True, blank=True)
    britannia = models.CharField(max_length=80, null=True, blank=True)
    parle = models.CharField(max_length=80, null=True, blank=True)
    sunfeast = models.CharField(max_length=80, null=True, blank=True)
    britannia_sos = models.CharField(max_length=80, null=True, blank=True)
    other = models.CharField(max_length=80, null=True, blank=True)

    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class BritanniaTargetYearMaster(models.Model):
    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return self.britannia_program_name


class BritanniaTarget(models.Model):
    STATE_CHOICE = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    )

    RESION_CHOICE = (
        ('Reason for changing the targets - ACE CLUB', 'Reason for changing the targets - ACE CLUB'),
        ('Retailer started purchasing from other Source', 'Retailer started purchasing from other Source'),
        ('Municipal Work in Progress', 'Municipal Work in Progress'),

        ('Retailer sale has gone Down', 'Retailer sale has gone Down'),
        ('Festival Season', 'Festival Season'),
        ('Want to Increase Target', 'Want to Increase Target'),
        ('Store permanently Closed', 'Store permanently Closed'),
        ('Store temporarily closed', 'Store temporarily closed'),
    )
    britannia_target_year_master = models.ForeignKey(BritanniaTargetYearMaster, on_delete=models.CASCADE, null=True,
                                                     blank=True)
    status = models.CharField(max_length=50, choices=STATE_CHOICE, blank=True, null=True)
    reason = models.CharField(max_length=256, choices=RESION_CHOICE, blank=True, null=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True, blank=True)  # should be foreign key

    user = models.ForeignKey(User, on_delete=models.SET_NULL, help_text='Retailer', blank=True, null=True)

    bcradl_target = models.CharField(max_length=80, help_text=' BCRADL Target', blank=True, null=True)
    biscuit_target = models.CharField(max_length=80, help_text='Biscuit Target', blank=True, null=True)
    cradl_target = models.CharField(max_length=80, help_text='CRADL Target', blank=True, null=True)
    unqiue_target = models.CharField(max_length=80, help_text='Unqiue Lines Target', blank=True, null=True)
    ghee_target = models.CharField(max_length=80, help_text='Ghee Target', blank=True, null=True)
    focus_target1 = models.CharField(max_length=80, help_text='Focus Target1', blank=True, null=True)
    focus_target2 = models.CharField(max_length=80, help_text='Focus Target2', blank=True, null=True)
    cheese = models.CharField(max_length=80, help_text='Cheese', blank=True, null=True)
    cheese_ulpo = models.CharField(max_length=80, help_text='Cheese ULPO', blank=True, null=True)
    visibility = models.CharField(max_length=80, help_text='Visibility', blank=True, null=True)
    over_all = models.CharField(max_length=15, help_text='Over All', blank=True, null=True)
    power_brand = models.CharField(max_length=80, help_text='Power Brand', blank=True, null=True)
    focus_brand = models.CharField(max_length=80, help_text='Focus Brand', blank=True, null=True)

    bcrda = models.CharField(max_length=80, help_text='BCRDA', blank=True, null=True)

    phasing = models.CharField(max_length=80, help_text='Phasing', blank=True, null=True)

    ulpr = models.CharField(max_length=80, help_text='ULPR', blank=True, null=True)

    app_eco_retention = models.CharField(max_length=80, help_text='App ECO Retention', blank=True, null=True)

    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)

    inserted_by = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)

    inserted_by_role = models.CharField(max_length=30, null=True, blank=True)

    date = models.DateField(help_text='Inserted Date', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class BritanniaPointYearMaster(models.Model):
    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.britannia_program_name

class BritanniaPoint(models.Model):
    status = models.CharField(max_length=100, blank=True, null=True)

    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)

    britannia_point_year_master = models.ForeignKey(BritanniaPointYearMaster, on_delete=models.SET_NULL,
                                                    help_text='Britannia Point Year Master', blank=True, null=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, help_text='Retailer', blank=True, null=True)
    payout = models.FloatField(default=0, help_text='Payout in Rs')
    utr_no = models.CharField(max_length=80, help_text='UTR number or Credit note number', blank=True, null=True)
    bank_name = models.CharField(max_length=256, blank=True, null=True)
    account_no = models.CharField(max_length=30, blank=True, null=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)
    remark = models.CharField(max_length=256, blank=True, null=True)
    bpu_remark = models.CharField(max_length=256, blank=True, null=True, help_text='BPU Remark')
    date = models.DateField(blank=True, null=True, help_text='Insert Date')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class BritanniaDate(models.Model):
    bad_id = models.CharField(max_length=10, blank=True, null=True)
    bad_ase_date = models.DateTimeField(editable=True, blank=True, null=True)
    bad_asm_date = models.DateTimeField(editable=True, blank=True, null=True)
    bad_rsm_date = models.DateTimeField(editable=True, blank=True, null=True)
    bad_approval_date = models.DateTimeField(editable=True, blank=True, null=True)
    bad_bpn_id = models.CharField(max_length=10, blank=True, null=True)

    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)

    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class BritanniaUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, help_text='User Name', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    britannia_program = models.ForeignKey(BritanniaProgram, on_delete=models.CASCADE, null=True, blank=True)
    britannia_program_name = models.CharField(max_length=30, null=True, blank=True)
    login_user = models.CharField(max_length=15, help_text='Inserted By', blank=True, null=True)
    login_role = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class SmsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    template = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=5, null=True, blank=True)
    api_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile
