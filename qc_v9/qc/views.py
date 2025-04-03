import gspread
import pandas as pd
from django.shortcuts import render
import json
import os
from google.oauth2.service_account import Credentials
# Create your views here.

# def my_view(request):
#     sheet_data = fetch_google_sheet_data()  # دریافت داده‌های شیت گوگل
#     return render(request, 'index.html', {'sheet_data': sheet_data})


def fetch_google_sheet_data():
    # اتصال به Google Sheet
    gc = gspread.service_account(filename='credentials.json')  # فایل JSON کلید سرویس را جایگزین کنید
    sheet = gc.open_by_key('1qP7c5J_c27tgPZ1eHffAsaL2rNYwHfwkPpxkEjaB0ds')  # جایگزین با ID شیت گوگل شما
    worksheet = sheet.get_worksheet(1)  # اولین برگه (Sheet) شیت گوگل
    data = worksheet.get_all_records()  # دریافت تمام داده‌ها
    return data



# def render_second_column_with_sum_pandas(request):
#     # اتصال به Google Sheets
#     gc = gspread.service_account(filename='credentials.json')
#     sheet = gc.open_by_key('1qP7c5J_c27tgPZ1eHffAsaL2rNYwHfwkPpxkEjaB0ds')
#     worksheet = sheet.get_worksheet_by_id(1393451510)  # اولین شیت

#     # دریافت تمام داده‌ها به‌صورت DataFrame
#     data = worksheet.get_all_values()
#     df = pd.DataFrame(data)

#     # نمایش اطلاعات
#     print(df)

#     # بررسی اینکه حداقل دو ستون وجود داشته باشد
#     if len(df.columns) < 2:
#         return render(request, 'second_column_sum.html', {'second_column': [], 'total_sum': 0})

#     # حذف هدر و تبدیل مقادیر ستون دوم به عدد
#     try:
#         df[18] = pd.to_numeric(df[18], errors='coerce')  # ستون دوم
#         numeric_values = df[18].dropna()  # حذف مقادیر غیرعددی
#         total_sum = numeric_values.sum()
#     except Exception as e:
#         numeric_values = []
#         total_sum = 0

#     # ارسال داده‌ها به قالب
#     return render(request, 'test.html', {
#         'second_column': numeric_values.tolist(),
#         'total_sum': total_sum,
#     })

    




def render_sum(request):
    # خواندن `credentials.json` از متغیر محیطی
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    # ساختن کرنشیال‌ها برای gspread
    creds = Credentials.from_service_account_info(credentials_info)

    # مقداردهی gspread
    gc = gspread.authorize(creds)

    # باز کردن Google Sheet
    sheet = gc.open_by_key('1EOwhcDI9fcEwrziOzeNPDDeLFU5slQulwLJHItLPMGQ')

    # اتصال به Google Sheets
    # gc = gspread.service_account(filename='credentials.json')
    # sheet = gc.open_by_key('1xk2lKmvnefpKTArUNG_HxOGwJeI9yzlE2oMnjtJfFTU')
    # worksheet = sheet.get_worksheet_by_id(1393451510) # اولین شیت

    # sheet = gc.open_by_key('1RKMqT_wsR_dNKyNV27GmHt4BbTcM6xpC2pSL6_GW0g4')
    # sheet = gc.open_by_key('1EOwhcDI9fcEwrziOzeNPDDeLFU5slQulwLJHItLPMGQ')
    worksheet = sheet.get_worksheet_by_id(1393451510) # اولین شیت

    # دریافت تمام داده‌ها به صورت DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)

    # بررسی اینکه حداقل هشت ستون وجود داشته باشد
    if len(df.columns) < 2:
        return render(request, 'sum.html', {'shahrzad_values': [], 'total_sum': 0})

    # حذف هدر و نامگذاری ستون‌ها
    df.columns = df.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df = df[1:]  # حذف ردیف هدر

    # فیلتر کردن ردیف‌هایی که نام "شهرزاد" دارند (ستون دوم)
    shahrzad_df = df[df.iloc[:, 0].str.strip() == 'شهرزاد']  # فیلتر بر اساس نام در ستون دوم
    arian_df = df[df.iloc[:, 0].str.strip() == 'آرین']  # فیلتر بر اساس نام در ستون دوم
    mohamad_df = df[df.iloc[:, 0].str.strip() == 'محمد']  # فیلتر بر اساس نام در ستون دوم

    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع
    shahrzad_df.iloc[:, 18] = pd.to_numeric(shahrzad_df.iloc[:, 18], errors='coerce')  # تبدیل به عدد
    total_sum_shahrzad = shahrzad_df.iloc[:, 18].sum()  # محاسبه مجموع
    
    arian_df.iloc[:, 18] = pd.to_numeric(arian_df.iloc[:, 18], errors='coerce')  # تبدیل به عدد
    total_sum_arian =arian_df.iloc[:, 18].sum()  # محاسبه مجموع
    
    mohamad_df.iloc[:, 18] = pd.to_numeric(mohamad_df.iloc[:, 18], errors='coerce')  # تبدیل به عدد
    total_sum_mohamad = mohamad_df.iloc[:, 18].sum()  # محاسبه مجموع

     # شمارش ردیف‌هایی که نام "شهرزاد" دارند (ستون دوم)
    shahrzad_count = df[df.iloc[:, 0].str.strip() == 'شهرزاد'].shape[0]  # تعداد ردیف‌ها
    
    arian_count = df[df.iloc[:, 0].str.strip() == 'آرین'].shape[0]  # تعداد ردیف‌ها
   
    mohamad_count = df[df.iloc[:, 0].str.strip() == 'محمد'].shape[0]  # تعداد ردیف‌ها

    # شمارش تعداد True در ستون پنجم
    work_sample_count_shahrzad = shahrzad_df.iloc[:, 12].str.strip().str.lower().value_counts().get('true', 0)  # شمارش تعداد True

    work_sample_count_arian = arian_df.iloc[:, 12].str.strip().str.lower().value_counts().get('true', 0)  # شمارش تعداد True

    work_sample_count_mohamad = mohamad_df.iloc[:, 12].str.strip().str.lower().value_counts().get('true', 0)  # شمارش تعداد True

    work_sample_rate_shahrzad = (work_sample_count_shahrzad/shahrzad_count)*100
  
    work_sample_rate_arian = (work_sample_count_arian/arian_count)*100
   
    work_sample_rate_mohamad = (work_sample_count_mohamad/mohamad_count)*100

    # تعداد هر رشته
    ortodensi_count = df[df.iloc[:, 3].str.strip() == 'ارتودنسی'].shape[0]  # تعداد ردیف‌ها
    asaboravan_count = df[df.iloc[:, 3].str.strip() == 'اعصاب و روان'].shape[0]  # تعداد ردیف‌ها
    orolozh_count = df[df.iloc[:, 3].str.strip() == 'اورولوژی'].shape[0]  # تعداد ردیف‌ها
    poost_count = df[df.iloc[:, 3].str.strip() == 'پوست، مو و زیبایی'].shape[0]  # تعداد ردیف‌ها
    taghzie_count = df[df.iloc[:, 3].str.strip() == 'تغذیه'].shape[0]  # تعداد ردیف‌ها
    ortopedi_count = df[df.iloc[:, 3].str.strip() == 'ارتوپدی فنی'].shape[0]  # تعداد ردیف‌ها
    jarahomomi_count = df[df.iloc[:, 3].str.strip() == 'جراح عمومی'].shape[0]  # تعداد ردیف‌ها
    fakosoorat_count = df[df.iloc[:, 3].str.strip() == 'جراح فک و صورت'].shape[0]  # تعداد ردیف‌ها
    lase_count = df[df.iloc[:, 3].str.strip() == 'جراح لثه'].shape[0]  # تعداد ردیف‌ها
    cheshm_count = df[df.iloc[:, 3].str.strip() == 'چشم پزشکی'].shape[0]  # تعداد ردیف‌ها
    dandoon_count = df[df.iloc[:, 3].str.strip() == 'دندانپزشک عمومی'].shape[0]  # تعداد ردیف‌ها
    ravanshenas_count = df[df.iloc[:, 3].str.strip() == 'روانشناسی'].shape[0]  # تعداد ردیف‌ها
    zanan_count = df[df.iloc[:, 3].str.strip() == 'زنان و زایمان'].shape[0]  # تعداد ردیف‌ها
    omoomi_count = df[df.iloc[:, 3].str.strip() == 'عمومی'].shape[0]  # تعداد ردیف‌ها
    govaresh_count = df[df.iloc[:, 3].str.strip() == 'گوارش'].shape[0]  # تعداد ردیف‌ها
    ghalb_count = df[df.iloc[:, 3].str.strip() == 'قلب و عروق'].shape[0]  # تعداد ردیف‌ها
    goosh_count = df[df.iloc[:, 3].str.strip() == 'گوش و حلق و بینی'].shape[0]  # تعداد ردیف‌ها
    norolozh_count = df[df.iloc[:, 3].str.strip() == 'نورولوژی'].shape[0]  # تعداد ردیف‌ها
    endodantix_count = df[df.iloc[:, 3].str.strip() == 'تخصص درمان ریشه (اندودانتیکس)'].shape[0]  # تعداد ردیف‌ها

    # تعداد امضا های هر شخص
    shahrzad_sign_count = shahrzad_df.iloc[:, 15].str.strip().str.lower().value_counts().get('true', 0)
    arian_sign_count = arian_df.iloc[:, 15].str.strip().str.lower().value_counts().get('true', 0)
    mohamad_sign_count = mohamad_df.iloc[:, 15].str.strip().str.lower().value_counts().get('true', 0)
   
    # تعداد کل امضاها
    sign_count = df.iloc[:, 15].str.strip().str.lower().value_counts().get('true', 0)
    all_doctor = shahrzad_count + arian_count + mohamad_count
    not_sign_count = all_doctor - sign_count

    # تعداد tag های هر شخص
    shahrzad_tag_count = shahrzad_df.iloc[:, 10].str.strip().str.lower().value_counts().get('true', 0)
    arian_tag_count = arian_df.iloc[:, 10].str.strip().str.lower().value_counts().get('true', 0)
    mohamad_tag_count = mohamad_df.iloc[:, 10].str.strip().str.lower().value_counts().get('true', 0)
   
    # تعداد کل tag ها
    tag_count = df.iloc[:, 10].str.strip().str.lower().value_counts().get('true', 0)
    all_doctor = shahrzad_count + arian_count + mohamad_count
    not_tag_count = all_doctor - tag_count

    # کل افرها
    total_offer = total_sum_shahrzad + total_sum_arian + total_sum_mohamad

    # تعداد خدمات غیر فعال
    active_count = df.iloc[:, 16].str.strip().str.lower().value_counts().get('true', 0)
    all_doctor = shahrzad_count + arian_count + mohamad_count
    not_active_count = all_doctor - active_count

    # تعداد pdp های هر شخص
    shahrzad_pdp_count = shahrzad_df.iloc[:, 11].str.strip().str.lower().value_counts().get('true', 0)
    arian_pdp_count = arian_df.iloc[:, 11].str.strip().str.lower().value_counts().get('true', 0)
    mohamad_pdp_count = mohamad_df.iloc[:, 11].str.strip().str.lower().value_counts().get('true', 0)

    # تعداد عکس های هر شخص
    shahrzad_df.iloc[:, 20] = pd.to_numeric(shahrzad_df.iloc[:, 20], errors='coerce')  # تبدیل به عدد
    total_ax_shahrzad = shahrzad_df.iloc[:, 20].sum()  # محاسبه مجموع
    
    arian_df.iloc[:, 20] = pd.to_numeric(arian_df.iloc[:, 20], errors='coerce')  # تبدیل به عدد
    total_ax_arian =arian_df.iloc[:, 20].sum()  # محاسبه مجموع

    mohamad_df.iloc[:, 20] = pd.to_numeric(mohamad_df.iloc[:, 20], errors='coerce')  # تبدیل به عدد
    total_ax_mohamad = mohamad_df.iloc[:, 20].sum()  # محاسبه مجموع

    # تعداد فیلم های هر شخص
    shahrzad_df.iloc[:, 19] = pd.to_numeric(shahrzad_df.iloc[:, 19], errors='coerce')  # تبدیل به عدد
    total_film_shahrzad = shahrzad_df.iloc[:, 19].sum()  # محاسبه مجموع
    
    arian_df.iloc[:, 19] = pd.to_numeric(arian_df.iloc[:, 19], errors='coerce')  # تبدیل به عدد
    total_film_arian =arian_df.iloc[:, 19].sum()  # محاسبه مجموع
    
    mohamad_df.iloc[:, 19] = pd.to_numeric(mohamad_df.iloc[:, 19], errors='coerce')  # تبدیل به عدد
    total_film_mohamad = mohamad_df.iloc[:, 19].sum()  # محاسبه مجموع

    # تعداد پزرشک های هر شخص که قرارداد ارسال کردند
    shahrzad_contract_count = shahrzad_df.iloc[:, 14].str.strip().str.lower().value_counts().get('true', 0)
    not_contract_shahrzad_count = shahrzad_count - shahrzad_contract_count
    arian_contract_count = arian_df.iloc[:, 14].str.strip().str.lower().value_counts().get('true', 0)
    not_contract_arian_count = arian_count - arian_contract_count
    mohamad_contract_count = mohamad_df.iloc[:, 14].str.strip().str.lower().value_counts().get('true', 0)
    not_contract_mohamad_count = mohamad_count - mohamad_contract_count

    # تعداد پزشکانی که نمونه کار دادند
    docsendws_count = df.iloc[:, 12].str.strip().str.lower().value_counts().get('true', 0)
    all_doctor = shahrzad_count + arian_count + mohamad_count
    not_docsendws_count = all_doctor - docsendws_count

    # تعداد پزشکانی که خدماتشون فعال شده
    docactivity_count = df.iloc[:, 16].str.strip().str.lower().value_counts().get('true', 0)
    all_doctor = shahrzad_count + arian_count + mohamad_count
    not_docactivity_count = all_doctor - docactivity_count

    # ارسال داده‌ها به قالب
    return render(request, 'index.html', {
        'shahrzad_values': shahrzad_df.iloc[:, 8].dropna().tolist(),  # مقادیر عددی
        'total_sum_shahrzad': total_sum_shahrzad,
        'shahrzad_count': shahrzad_count,
        'work_sample_count_shahrzad': work_sample_count_shahrzad,
        'work_sample_rate_shahrzad': round(work_sample_rate_shahrzad),
        'total_ax_shahrzad' : total_ax_shahrzad,
        'total_film_shahrzad' : total_film_shahrzad,
        'shahrzad_contract_count' : shahrzad_contract_count,
        'not_contract_shahrzad_count' : not_contract_shahrzad_count,

        'arian_values': arian_df.iloc[:, 8].dropna().tolist(),  # مقادیر عددی
        'total_sum_arian': total_sum_arian,
        'arian_count': arian_count,
        'work_sample_count_arian': work_sample_count_arian,
        'work_sample_rate_arian': round(work_sample_rate_arian),
        'total_ax_arian' : total_ax_arian,
        'total_film_arian' : total_film_arian,
        'arian_contract_count' : arian_contract_count,
        'not_contract_arian_count' : not_contract_arian_count,

        'mohamad_values': mohamad_df.iloc[:, 8].dropna().tolist(),  # مقادیر عددی
        'total_sum_mohamad': total_sum_mohamad,
        'mohamad_count': mohamad_count,
        'work_sample_count_mohamad': work_sample_count_mohamad,
        'work_sample_rate_mohamad': round(work_sample_rate_mohamad),
        'total_ax_mohamad' : total_ax_mohamad,
        'total_film_mohamad' : total_film_mohamad,
        'mohamad_contract_count' : mohamad_contract_count,
        'not_contract_mohamad_count' : not_contract_mohamad_count,

        'ortodensi_count' : ortodensi_count,
        'asaboravan_count' : asaboravan_count,
        'orolozh_count' : orolozh_count,
        'poost_count' : poost_count,
        'taghzie_count' : taghzie_count,
        'ortopedi_count'  : ortopedi_count,
        'jarahomomi_count' : jarahomomi_count,
        'fakosoorat_count' : fakosoorat_count,
        'lase_count' : lase_count,
        'cheshm_count' : cheshm_count,
        'dandoon_count' : dandoon_count,
        'ravanshenas_count' : ravanshenas_count,
        'zanan_count' : zanan_count,
        'omoomi_count' : omoomi_count,
        'govaresh_count' : govaresh_count,
        'ghalb_count' : ghalb_count,
        'goosh_count' : goosh_count,
        'norolozh_count' : norolozh_count,
        'endodantix_count' : endodantix_count,

        'shahrzad_sign_count' : shahrzad_sign_count,
        'arian_sign_count' : arian_sign_count,
        'mohamad_sign_count' : mohamad_sign_count,

        'sign_count' : sign_count,
        'not_sign_count' : not_sign_count,

        'tag_count' : tag_count,
        'not_tag_count' : not_tag_count,

        'total_offer' : int(total_offer),

        'not_active_count' : int(not_active_count),

        'shahrzad_pdp_count' : shahrzad_pdp_count,
        'arian_pdp_count' : arian_pdp_count,
        'mohamad_pdp_count' : mohamad_pdp_count,

        'docsendws_count' : docsendws_count,
        'not_docsendws_count' : not_docsendws_count,

        'docactivity_count' : docactivity_count,
        'not_docactivity_count' : not_docactivity_count,
    })



# income def
def income_def(request):
    # خواندن `credentials.json` از متغیر محیطی
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    # ساختن کرنشیال‌ها برای gspread
    creds = Credentials.from_service_account_info(credentials_info)

    # مقداردهی gspread
    gc = gspread.authorize(creds)

    # باز کردن Google Sheet
    sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')

    # اتصال به Google Sheets
    # gc = gspread.service_account(filename='credentials.json')
    # sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')
    worksheet = sheet.get_worksheet_by_id(232137112) # اولین شیت
    worksheet2 = sheet.get_worksheet_by_id(0) # اولین شیت

    # دریافت تمام داده‌ها به صورت DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)
    data2 = worksheet2.get_all_values()
    df2 = pd.DataFrame(data2)

    # بررسی اینکه حداقل هشت ستون وجود داشته باشد
    if len(df.columns) < 2:
        return render(request, 'sum.html', {'sum_values': [], 'total_sum': 0})

    # حذف هدر و نامگذاری ستون‌ها
    df.columns = df.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df = df[1:]  # حذف ردیف هدر
    df2.columns = df2.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df2 = df2[1:]  # حذف ردیف هدر

    # فیلتر کردن ردیف‌هایی که نام "سارا" دارند در شیت درامد (ستون دوم)
    sanam_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
    sara_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
    elahe_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
    mohamad_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم

    # فیلتر کردن ردیف‌هایی که نام "سارا" دارند در شیت جایگاه (ستون دوم)
    sanam_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
    sara_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
    elahe_df_place = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
    mohamad_df_place = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم

    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع در شیت درامد
    sanam_df.iloc[:, 13] = pd.to_numeric((sanam_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sanam = sanam_df.iloc[:, 13].sum()  # محاسبه مجموع
    
    sara_df.iloc[:, 13] = pd.to_numeric((sara_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sara =sara_df.iloc[:, 13].sum()  # محاسبه مجموع
    
    elahe_df.iloc[:, 13] = pd.to_numeric((elahe_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_elahe = elahe_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_df.iloc[:, 13] = pd.to_numeric((mohamad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_mohamad = mohamad_df.iloc[:, 13].sum()  # محاسبه مجموع

    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع در شیت جایگاه
    sanam_df_place.iloc[:, 14] = pd.to_numeric((sanam_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sanam_place = sanam_df_place.iloc[:, 14].sum()  # محاسبه مجموع
    
    sara_df_place.iloc[:, 14] = pd.to_numeric((sara_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sara_place =sara_df_place.iloc[:, 14].sum()  # محاسبه مجموع
    
    elahe_df_place.iloc[:, 14] = pd.to_numeric((elahe_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_elahe_place = elahe_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_df_place.iloc[:, 14] = pd.to_numeric((mohamad_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_mohamad_place = mohamad_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد هر فرد از شیت جایگاه و درامد 
    sum_income_place_sanam = total_sum_sanam + total_sum_sanam_place
    sum_income_place_sara = total_sum_sara + total_sum_sara_place
    sum_income_place_elahe = total_sum_elahe + total_sum_elahe_place
    sum_income_place_mohamad = total_sum_mohamad + total_sum_mohamad_place


    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند در شیت درامد
    sanam_month_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_month_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_month_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_month_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند در شیت جایگاه
    sanam_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت درامد
    sanam_month_df.iloc[:, 13] = pd.to_numeric((sanam_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sanam = sanam_month_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_month_df.iloc[:, 13] = pd.to_numeric((sara_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sara = sara_month_df.iloc[:, 13].sum()  # محاسبه مجموع
    
    elahe_month_df.iloc[:, 13] = pd.to_numeric((elahe_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_elahe = elahe_month_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_month_df.iloc[:, 13] = pd.to_numeric((mohamad_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_mohamad = mohamad_month_df.iloc[:, 13].sum()  # محاسبه مجموع

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    sanam_month_df_place.iloc[:, 14] = pd.to_numeric((sanam_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sanam_place = sanam_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    sara_month_df_place.iloc[:, 14] = pd.to_numeric((sara_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sara_place = sara_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع
    
    elahe_month_df_place.iloc[:, 14] = pd.to_numeric((elahe_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_elahe_place = elahe_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_month_df_place.iloc[:, 14] = pd.to_numeric((mohamad_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_mohamad_place = mohamad_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد از شیت جایگاه و درامد هر فرد
    sum_month_income_place_sanam = sum_month_sanam + sum_month_sanam_place
    sum_month_income_place_sara = sum_month_sara + sum_month_sara_place
    sum_month_income_place_elahe = sum_month_elahe + sum_month_elahe_place
    sum_month_income_place_mohamad = sum_month_mohamad + sum_month_mohamad_place

    # درامد هر ماه از شیت درامد
    farvardin_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'فروردین')]
    farvardin_income_df.iloc[:, 13] = pd.to_numeric((farvardin_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    farvardin_income = farvardin_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    ordibehesht_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'اردیبهشت')]
    ordibehesht_income_df.iloc[:, 13] = pd.to_numeric((ordibehesht_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    ordibehesht_income = ordibehesht_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    khordad_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'خرداد')]
    khordad_income_df.iloc[:, 13] = pd.to_numeric((khordad_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    khordad_income = khordad_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    tir_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'تیر')]
    tir_income_df.iloc[:, 13] = pd.to_numeric((tir_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    tir_income = tir_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    mordad_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'مرداد')]
    mordad_income_df.iloc[:, 13] = pd.to_numeric((mordad_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    mordad_income = mordad_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    shahrivar_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'شهریور')]
    shahrivar_income_df.iloc[:, 13] = pd.to_numeric((shahrivar_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    shahrivar_income = shahrivar_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    mehr_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'مهر')]
    mehr_income_df.iloc[:, 13] = pd.to_numeric((mehr_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    mehr_income = mehr_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    aban_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'آبان')]
    aban_income_df.iloc[:, 13] = pd.to_numeric((aban_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    aban_income = aban_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    azar_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'آذر')]
    azar_income_df.iloc[:, 13] = pd.to_numeric((azar_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    azar_income = azar_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    dey_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'دی')]
    dey_income_df.iloc[:, 13] = pd.to_numeric((dey_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    dey_income = dey_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    bahman_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'بهمن')]
    bahman_income_df.iloc[:, 13] = pd.to_numeric((bahman_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    bahman_income = bahman_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    esfand_income_df = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 2].str.strip() == 'اسفند')]
    esfand_income_df.iloc[:, 13] = pd.to_numeric((esfand_income_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    esfand_income = esfand_income_df.iloc[:, 13].sum()  # محاسبه مجموع

    # درامد هر ماه از شیت جایگاه
    farvardin_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'فروردین')]
    farvardin_place_df.iloc[:, 14] = pd.to_numeric((farvardin_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    farvardin_place = farvardin_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    ordibehesht_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'اردیبهشت')]
    ordibehesht_place_df.iloc[:, 14] = pd.to_numeric((ordibehesht_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    ordibehesht_place = ordibehesht_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    khordad_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'خرداد')]
    khordad_place_df.iloc[:, 14] = pd.to_numeric((khordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    khordad_place = khordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    tir_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'تیر')]
    tir_place_df.iloc[:, 14] = pd.to_numeric((tir_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    tir_place = tir_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mordad_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'مرداد')]
    mordad_place_df.iloc[:, 14] = pd.to_numeric((mordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    mordad_place = mordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    shahrivar_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'شهریور')]
    shahrivar_place_df.iloc[:, 14] = pd.to_numeric((shahrivar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    shahrivar_place = shahrivar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mehr_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'مهر')]
    mehr_place_df.iloc[:, 14] = pd.to_numeric((mehr_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    mehr_place = mehr_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    aban_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'آبان')]
    aban_place_df.iloc[:, 14] = pd.to_numeric((aban_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    aban_place = aban_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    azar_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'آذر')]
    azar_place_df.iloc[:, 14] = pd.to_numeric((azar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    azar_place = azar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    dey_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'دی')]
    dey_place_df.iloc[:, 14] = pd.to_numeric((dey_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    dey_place = dey_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    bahman_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'بهمن')]
    bahman_place_df.iloc[:, 14] = pd.to_numeric((bahman_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    bahman_place = bahman_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    esfand_place_df = df2[(df2.iloc[:, 4].str.strip() == 'DONE') & (df2.iloc[:, 2].str.strip() == 'اسفند')]
    esfand_place_df.iloc[:, 14] = pd.to_numeric((esfand_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    esfand_place = esfand_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد از شیت جایگاه و درامد هر ماه
    sum_income_place_farvardin = farvardin_income + farvardin_place
    sum_income_place_ordibehesht = ordibehesht_income + ordibehesht_place
    sum_income_place_khordad = khordad_income + khordad_place
    sum_income_place_tir = tir_income + tir_place
    sum_income_place_mordad = mordad_income + mordad_place
    sum_income_place_shahrivar = shahrivar_income + shahrivar_place
    sum_income_place_mehr = mehr_income + mehr_place
    sum_income_place_aban = aban_income + aban_place
    sum_income_place_azar = azar_income + azar_place
    sum_income_place_dey = dey_income + dey_place
    sum_income_place_bahman = bahman_income + bahman_place
    sum_income_place_esfand = esfand_income + esfand_place


    # پندینگ و دان و کنسلی و تمام دکتر های هر شخص
    sanam_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها
    sara_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها
    elahe_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها
    mohamad_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    sanam_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها
    sara_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها
    elahe_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها
    mohamad_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    sanam_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها
    sara_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها
    elahe_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها
    mohamad_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    sanam_count = df[df.iloc[:, 3].str.strip() == 'sanam'].shape[0]  # تعداد ردیف‌ها
    sara_count = df[df.iloc[:, 3].str.strip() == 'sara'].shape[0]  # تعداد ردیف‌ها
    elahe_count = df[df.iloc[:, 3].str.strip() == 'elahe'].shape[0]  # تعداد ردیف‌ها
    mohamad_count = df[df.iloc[:, 3].str.strip() == 'mohammad'].shape[0]  # تعداد ردیف‌ها


    # درصد موفقیت هر شخص
    success_rate_sanam = (sanam_done_count / sanam_count)* 100
    success_rate_sara = (sara_done_count / sara_count)* 100
    success_rate_elahe = (elahe_done_count / elahe_count)* 100
    success_rate_mohamad = (mohamad_done_count / mohamad_count)* 100


    # محاسبات بخش هدر
    income_df = df[df.iloc[:, 4].str.strip() == 'DONE']
    income_df.iloc[:, 13] = pd.to_numeric(income_df.iloc[:, 13].str.replace(",", "").str.strip(), errors='coerce')
    total_sum_income = income_df.iloc[:, 13].sum()

    place_df = df2[df2.iloc[:, 4].str.strip() == 'DONE']
    place_df.iloc[:, 14] = pd.to_numeric(place_df.iloc[:, 14].str.replace(",", "").str.strip(), errors='coerce')
    total_sum_place = place_df.iloc[:, 14].sum()

    sum_income_place = f"{int(total_sum_income + total_sum_place):,}"

    # شمارش ردیف‌هایی که نام "pending" دارند (ستون 4)
    pending_count = df[df.iloc[:, 4].str.strip() == 'PENDING'].shape[0]  # تعداد ردیف‌ها


    # ارسال داده‌ها به قالب
    return render(request, 'income.html', {
        'total_sum_sanam': total_sum_sanam,
        'sum_month_sanam': sum_month_sanam,
        'sanam_pending_count': sanam_pending_count,
        'sanam_cancel_count': sanam_cancel_count,
        'sanam_count': sanam_count,
        'success_rate_sanam': success_rate_sanam,
        'sum_income_place_sanam': sum_income_place_sanam,
        'sum_month_income_place_sanam': sum_month_income_place_sanam,
        
        'total_sum_sara': total_sum_sara,
        'sum_month_sara': sum_month_sara,
        'sara_pending_count': sara_pending_count,
        'sara_cancel_count': sara_cancel_count,
        'sara_count': sara_count,
        'success_rate_sara': success_rate_sara,
        'sum_income_place_sara': sum_income_place_sara,
        'sum_month_income_place_sara': sum_month_income_place_sara,
       
        'total_sum_elahe': total_sum_elahe,
        'sum_month_elahe': sum_month_elahe,
        'elahe_pending_count': elahe_pending_count,
        'elahe_cancel_count': elahe_cancel_count,
        'elahe_count': elahe_count,
        'success_rate_elahe': success_rate_elahe,
        'sum_income_place_elahe': sum_income_place_elahe,
        'sum_month_income_place_elahe': sum_month_income_place_elahe,
        
        'total_sum_mohamad': total_sum_mohamad,
        'sum_month_mohamad': sum_month_mohamad,
        'mohamad_pending_count': mohamad_pending_count,
        'mohamad_cancel_count': mohamad_cancel_count,
        'mohamad_count': mohamad_count,
        'success_rate_mohamad': success_rate_mohamad,
        'sum_income_place_mohamad': sum_income_place_mohamad,
        'sum_month_income_place_mohamad': sum_month_income_place_mohamad,
        
        'total_sum_income': total_sum_income,
        'sum_income_place': sum_income_place,
        'pending_count': pending_count,
        'farvardin_income': farvardin_income,
        'ordibehesht_income': ordibehesht_income,
        'khordad_income': khordad_income,
        'tir_income': tir_income,
        'mordad_income': mordad_income,
        'shahrivar_income': shahrivar_income,
        'mehr_income': mehr_income,
        'aban_income': aban_income,
        'azar_income': azar_income,
        'dey_income': dey_income,
        'bahman_income': bahman_income,
        'esfand_income': esfand_income,
        'sum_income_place_farvardin': sum_income_place_farvardin,
        'sum_income_place_ordibehesht': sum_income_place_ordibehesht,
        'sum_income_place_khordad': sum_income_place_khordad,
        'sum_income_place_tir': sum_income_place_tir,
        'sum_income_place_mordad': sum_income_place_mordad,
        'sum_income_place_shahrivar': sum_income_place_shahrivar,
        'sum_income_place_mehr': sum_income_place_mehr,
        'sum_income_place_aban': sum_income_place_aban,
        'sum_income_place_azar': sum_income_place_azar,
        'sum_income_place_dey': sum_income_place_dey,
        'sum_income_place_bahman': sum_income_place_bahman,
        'sum_income_place_esfand': sum_income_place_esfand,
    })



# def top_result
def top_result_def(request):
    return render(request, 'top_result.html', {})


def mohammad_def(request):
    # خواندن `credentials.json` از متغیر محیطی
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    # ساختن کرنشیال‌ها برای gspread
    creds = Credentials.from_service_account_info(credentials_info)

    # مقداردهی gspread
    gc = gspread.authorize(creds)

    # باز کردن Google Sheet
    sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')
    # اتصال به Google Sheets
    # gc = gspread.service_account(filename='credentials.json')
    # sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')
    worksheet = sheet.get_worksheet_by_id(232137112) #  شیت درامد
    worksheet2 = sheet.get_worksheet_by_id(0) # شیت جایگاه 

    # دریافت تمام داده‌ها به صورت DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)
    data2 = worksheet2.get_all_values()
    df2 = pd.DataFrame(data2)


    # بررسی اینکه حداقل هشت ستون وجود داشته باشد
    if len(df.columns) < 2:
        return render(request, 'sum.html', {'sum_values': [], 'total_sum': 0})

    # حذف هدر و نامگذاری ستون‌ها
    df.columns = df.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df = df[1:]  # حذف ردیف هدر
    df2.columns = df2.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df2 = df2[1:]  # حذف ردیف هدر

    # فیلتر کردن ردیف‌هایی که نام "شهرزاد" دارند (ستون دوم)
    mohamad_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم

    # فیلتر کردن ردیف‌هایی که نام "سارا" دارند در شیت جایگاه (ستون دوم)
    mohamad_df_place = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
    
    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع
    mohamad_df.iloc[:, 13] = pd.to_numeric((mohamad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_mohamad = mohamad_df.iloc[:, 13].sum()  # محاسبه مجموع

    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع در شیت جایگاه
    mohamad_df_place.iloc[:, 14] = pd.to_numeric((mohamad_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_mohamad_place = mohamad_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد هر فرد طبق شیت درامد و جایگاه
    sum_income_place_mohamad = total_sum_mohamad + total_sum_mohamad_place

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند
    mohamad_month_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند در شیت جایگاه
    mohamad_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]

    # مجموع درامد افراد بر اساس ماه مورد نظر
    mohamad_month_df.iloc[:, 13] = pd.to_numeric((mohamad_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_mohamad = mohamad_month_df.iloc[:, 13].sum()  # محاسبه مجموع

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    mohamad_month_df_place.iloc[:, 14] = pd.to_numeric((mohamad_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_mohamad_place = mohamad_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد ماه مورد نظر از شیت جایگاه و درامد هر فرد
    sum_month_income_place_mohamad = sum_month_mohamad + sum_month_mohamad_place

    # تعداد دکتر های این ماه هر شخص
    mohamad_dr_count_this_month = df[(df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    # پندینگ و دان و کنسلی و تمام دکتر های هر شخص

    mohamad_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    mohamad_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    mohamad_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    mohamad_club_count = df[(df.iloc[:, 6].str.strip() == '💥') & (df.iloc[:, 3].str.strip() == 'mohammad')].shape[0]  # تعداد ردیف‌ها

    mohamad_count = df[df.iloc[:, 3].str.strip() == 'mohammad'].shape[0]  # تعداد ردیف‌ها

    # درصد موفقیت هر شخص
    success_rate_mohamad = (mohamad_done_count / mohamad_count)* 100

    # کنسلی هر شخص
    cancel_rate_mohamad = (mohamad_cancel_count / mohamad_count)* 100

    # پندینگ هر شخص
    pending_rate_mohamad = (mohamad_pending_count / mohamad_count)* 100

    # تمدید هر شخص
    club_rate_mohamad = (mohamad_club_count / mohamad_count)* 100

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت درامد
    mohamad_farvardin_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'فروردین') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_farvardin_df.iloc[:, 13] = pd.to_numeric((mohamad_farvardin_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_mohamad = mohamad_farvardin_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_ordibehesht_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'اردیبهشت') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_ordibehesht_df.iloc[:, 13] = pd.to_numeric((mohamad_ordibehesht_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_mohamad = mohamad_ordibehesht_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_khordad_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'خرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_khordad_df.iloc[:, 13] = pd.to_numeric((mohamad_khordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_mohamad = mohamad_khordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_tir_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'تیر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_tir_df.iloc[:, 13] = pd.to_numeric((mohamad_tir_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_mohamad = mohamad_tir_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_mordad_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'مرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_mordad_df.iloc[:, 13] = pd.to_numeric((mohamad_mordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_mohamad = mohamad_mordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_shahrivar_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'شهریور') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_shahrivar_df.iloc[:, 13] = pd.to_numeric((mohamad_shahrivar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_mohamad = mohamad_shahrivar_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_mehr_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'مهر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_mehr_df.iloc[:, 13] = pd.to_numeric((mohamad_mehr_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_mohamad = mohamad_mehr_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_aban_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'آبان') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_aban_df.iloc[:, 13] = pd.to_numeric((mohamad_aban_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_mohamad = mohamad_aban_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_azar_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'آذر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_azar_df.iloc[:, 13] = pd.to_numeric((mohamad_azar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_mohamad = mohamad_azar_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_dey_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'دی') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_dey_df.iloc[:, 13] = pd.to_numeric((mohamad_dey_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_mohamad = mohamad_dey_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_bahman_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'بهمن') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_bahman_df.iloc[:, 13] = pd.to_numeric((mohamad_bahman_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_mohamad = mohamad_bahman_df.iloc[:, 13].sum()  # محاسبه مجموع

    mohamad_esfand_df = df[(df.iloc[:, 3].str.strip() == 'mohammad') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_esfand_df.iloc[:, 13] = pd.to_numeric((mohamad_esfand_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_mohamad = mohamad_esfand_df.iloc[:, 13].sum()  # محاسبه مجموع

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    mohamad_farvardin_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'فروردین') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_farvardin_place_df.iloc[:, 14] = pd.to_numeric((mohamad_farvardin_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_mohamad_place = mohamad_farvardin_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_ordibehesht_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'اردیبهشت') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_ordibehesht_place_df.iloc[:, 14] = pd.to_numeric((mohamad_ordibehesht_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_mohamad_place = mohamad_ordibehesht_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_khordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'خرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_khordad_place_df.iloc[:, 14] = pd.to_numeric((mohamad_khordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_mohamad_place = mohamad_khordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_tir_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'تیر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_tir_place_df.iloc[:, 14] = pd.to_numeric((mohamad_tir_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_mohamad_place = mohamad_tir_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_mordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'مرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_mordad_place_df.iloc[:, 14] = pd.to_numeric((mohamad_mordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_mohamad_place = mohamad_mordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_shahrivar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'شهریور') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_shahrivar_place_df.iloc[:, 14] = pd.to_numeric((mohamad_shahrivar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_mohamad_place = mohamad_shahrivar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_mehr_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'مهر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_mehr_place_df.iloc[:, 14] = pd.to_numeric((mohamad_mehr_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_mohamad_place = mohamad_mehr_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_aban_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'آبان') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_aban_place_df.iloc[:, 14] = pd.to_numeric((mohamad_aban_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_mohamad_place = mohamad_aban_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_azar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'آذر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_azar_place_df.iloc[:, 14] = pd.to_numeric((mohamad_azar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_mohamad_place = mohamad_azar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_dey_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'دی') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_dey_place_df.iloc[:, 14] = pd.to_numeric((mohamad_dey_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_mohamad_place = mohamad_dey_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_bahman_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'بهمن') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_bahman_place_df.iloc[:, 14] = pd.to_numeric((mohamad_bahman_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_mohamad_place = mohamad_bahman_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    mohamad_esfand_place_df = df2[(df2.iloc[:, 3].str.strip() == 'mohammad') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    mohamad_esfand_place_df.iloc[:, 14] = pd.to_numeric((mohamad_esfand_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_mohamad_place = mohamad_esfand_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد از شیت جایگاه و درامد هر ماه
    sum_income_place_farvardin_mohamad = sum_farvardin_mohamad + sum_farvardin_mohamad_place
    sum_income_place_ordibehesht_mohamad = sum_ordibehesht_mohamad + sum_ordibehesht_mohamad_place
    sum_income_place_khordad_mohamad = sum_khordad_mohamad + sum_khordad_mohamad_place
    sum_income_place_tir_mohamad = sum_tir_mohamad + sum_tir_mohamad_place
    sum_income_place_mordad_mohamad = sum_mordad_mohamad + sum_mordad_mohamad_place
    sum_income_place_shahrivar_mohamad = sum_shahrivar_mohamad + sum_shahrivar_mohamad_place
    sum_income_place_mehr_mohamad = sum_mehr_mohamad + sum_mehr_mohamad_place
    sum_income_place_aban_mohamad = sum_aban_mohamad + sum_aban_mohamad_place
    sum_income_place_azar_mohamad = sum_azar_mohamad + sum_azar_mohamad_place
    sum_income_place_dey_mohamad = sum_dey_mohamad + sum_dey_mohamad_place
    sum_income_place_bahman_mohamad = sum_bahman_mohamad + sum_bahman_mohamad_place
    sum_income_place_esfand_mohamad = sum_esfand_mohamad + sum_esfand_mohamad_place

    # ارسال داده‌ها به قالب
    return render(request, 'mohammad.html', {
        'total_sum_mohamad': total_sum_mohamad,
        'sum_income_place_mohamad': sum_income_place_mohamad,
        'sum_month_mohamad': sum_month_mohamad,
        'sum_month_income_place_mohamad': sum_month_income_place_mohamad,
        'mohamad_pending_count': mohamad_pending_count,
        'mohamad_cancel_count': mohamad_cancel_count,
        'mohamad_count': mohamad_count,
        'success_rate_mohamad': success_rate_mohamad,
        'cancel_rate_mohamad': cancel_rate_mohamad,
        'pending_rate_mohamad': pending_rate_mohamad,
        'club_rate_mohamad': club_rate_mohamad,
        'mohamad_dr_count_this_month': mohamad_dr_count_this_month,

        'sum_farvardin_mohamad': sum_farvardin_mohamad,
        'sum_ordibehesht_mohamad': sum_ordibehesht_mohamad,
        'sum_khordad_mohamad': sum_khordad_mohamad,
        'sum_tir_mohamad': sum_tir_mohamad,
        'sum_mordad_mohamad': sum_mordad_mohamad,
        'sum_shahrivar_mohamad': sum_shahrivar_mohamad,
        'sum_mehr_mohamad': sum_mehr_mohamad,
        'sum_aban_mohamad': sum_aban_mohamad,
        'sum_azar_mohamad': sum_azar_mohamad,
        'sum_dey_mohamad': sum_dey_mohamad,
        'sum_bahman_mohamad': sum_bahman_mohamad,
        'sum_esfand_mohamad': sum_esfand_mohamad,

        'sum_income_place_farvardin_mohamad': sum_income_place_farvardin_mohamad,
        'sum_income_place_ordibehesht_mohamad': sum_income_place_ordibehesht_mohamad,
        'sum_income_place_khordad_mohamad': sum_income_place_khordad_mohamad,
        'sum_income_place_tir_mohamad': sum_income_place_tir_mohamad,
        'sum_income_place_mordad_mohamad': sum_income_place_mordad_mohamad,
        'sum_income_place_shahrivar_mohamad': sum_income_place_shahrivar_mohamad,
        'sum_income_place_mehr_mohamad': sum_income_place_mehr_mohamad,
        'sum_income_place_aban_mohamad': sum_income_place_aban_mohamad,
        'sum_income_place_azar_mohamad': sum_income_place_azar_mohamad,
        'sum_income_place_dey_mohamad': sum_income_place_dey_mohamad,
        'sum_income_place_bahman_mohamad': sum_income_place_bahman_mohamad,
        'sum_income_place_esfand_mohamad': sum_income_place_esfand_mohamad,

    })
    


def sara_def(request):
    # خواندن `credentials.json` از متغیر محیطی
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    # ساختن کرنشیال‌ها برای gspread
    creds = Credentials.from_service_account_info(credentials_info)

    # مقداردهی gspread
    gc = gspread.authorize(creds)

    # باز کردن Google Sheet
    sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')

    # اتصال به Google Sheets
    # gc = gspread.service_account(filename='credentials.json')
    # sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')
    worksheet = sheet.get_worksheet_by_id(232137112) # اولین شیت
    worksheet2 = sheet.get_worksheet_by_id(0) # شیت جایگاه 

    # دریافت تمام داده‌ها به صورت DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)
    data2 = worksheet2.get_all_values()
    df2 = pd.DataFrame(data2)


    # بررسی اینکه حداقل هشت ستون وجود داشته باشد
    if len(df.columns) < 2:
        return render(request, 'sum.html', {'sum_values': [], 'total_sum': 0})

    # حذف هدر و نامگذاری ستون‌ها
    df.columns = df.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df = df[1:]  # حذف ردیف هدر
    df2.columns = df2.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df2 = df2[1:]  # حذف ردیف هدر

    # فیلتر کردن ردیف‌هایی که نام "شهرزاد" دارند (ستون دوم)
    sara_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم

    # فیلتر کردن ردیف‌هایی که نام "سارا" دارند در شیت جایگاه (ستون دوم)
    sara_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
        
    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع
    sara_df.iloc[:, 13] = pd.to_numeric((sara_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sara = sara_df.iloc[:, 13].sum()  # محاسبه مجموع

    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع در شیت جایگاه
    sara_df_place.iloc[:, 14] = pd.to_numeric((sara_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sara_place = sara_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد هر فرد طبق شیت درامد و جایگاه
    sum_income_place_sara = total_sum_sara + total_sum_sara_place

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند
    sara_month_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند در شیت جایگاه
    sara_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]

    # مجموع درامد افراد بر اساس ماه مورد نظر
    sara_month_df.iloc[:, 13] = pd.to_numeric((sara_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sara = sara_month_df.iloc[:, 13].sum()  # محاسبه مجموع

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    sara_month_df_place.iloc[:, 14] = pd.to_numeric((sara_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sara_place = sara_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد ماه مورد نظر از شیت جایگاه و درامد هر فرد
    sum_month_income_place_sara = sum_month_sara + sum_month_sara_place

    # تعداد دکتر های این ماه هر شخص
    sara_dr_count_this_month = df[(df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها

    # پندینگ و دان و کنسلی و تمام دکتر های هر شخص

    sara_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها

    sara_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها

    sara_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها

    sara_club_count = df[(df.iloc[:, 6].str.strip() == '💥') & (df.iloc[:, 3].str.strip() == 'sara')].shape[0]  # تعداد ردیف‌ها

    sara_count = df[df.iloc[:, 3].str.strip() == 'sara'].shape[0]  # تعداد ردیف‌ها

    # درصد موفقیت هر شخص
    success_rate_sara = (sara_done_count / sara_count)* 100

    # کنسلی هر شخص
    cancel_rate_sara = (sara_cancel_count / sara_count)* 100

    # پندینگ هر شخص
    pending_rate_sara = (sara_pending_count / sara_count)* 100

    # تمدید هر شخص
    club_rate_sara = (sara_club_count / sara_count)* 100

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت درامد
    sara_farvardin_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'فروردین') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_farvardin_df.iloc[:, 13] = pd.to_numeric((sara_farvardin_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_sara = sara_farvardin_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_ordibehesht_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'اردیبهشت') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_ordibehesht_df.iloc[:, 13] = pd.to_numeric((sara_ordibehesht_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_sara = sara_ordibehesht_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_khordad_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'خرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_khordad_df.iloc[:, 13] = pd.to_numeric((sara_khordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_sara = sara_khordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_tir_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'تیر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_tir_df.iloc[:, 13] = pd.to_numeric((sara_tir_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_sara = sara_tir_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_mordad_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'مرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_mordad_df.iloc[:, 13] = pd.to_numeric((sara_mordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_sara = sara_mordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_shahrivar_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'شهریور') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_shahrivar_df.iloc[:, 13] = pd.to_numeric((sara_shahrivar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_sara = sara_shahrivar_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_mehr_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'مهر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_mehr_df.iloc[:, 13] = pd.to_numeric((sara_mehr_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_sara = sara_mehr_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_aban_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'آبان') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_aban_df.iloc[:, 13] = pd.to_numeric((sara_aban_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_sara = sara_aban_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_azar_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'آذر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_azar_df.iloc[:, 13] = pd.to_numeric((sara_azar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_sara = sara_azar_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_dey_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'دی') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_dey_df.iloc[:, 13] = pd.to_numeric((sara_dey_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_sara = sara_dey_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_bahman_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'بهمن') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_bahman_df.iloc[:, 13] = pd.to_numeric((sara_bahman_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_sara = sara_bahman_df.iloc[:, 13].sum()  # محاسبه مجموع

    sara_esfand_df = df[(df.iloc[:, 3].str.strip() == 'sara') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sara_esfand_df.iloc[:, 13] = pd.to_numeric((sara_esfand_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_sara = sara_esfand_df.iloc[:, 13].sum()  # محاسبه مجموع

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    sara_farvardin_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'فروردین') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_farvardin_place_df.iloc[:, 14] = pd.to_numeric((sara_farvardin_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_sara_place = sara_farvardin_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_ordibehesht_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'اردیبهشت') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_ordibehesht_place_df.iloc[:, 14] = pd.to_numeric((sara_ordibehesht_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_sara_place = sara_ordibehesht_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_khordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'خرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_khordad_place_df.iloc[:, 14] = pd.to_numeric((sara_khordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_sara_place = sara_khordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_tir_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'تیر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_tir_place_df.iloc[:, 14] = pd.to_numeric((sara_tir_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_sara_place = sara_tir_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_mordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'مرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_mordad_place_df.iloc[:, 14] = pd.to_numeric((sara_mordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_sara_place = sara_mordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_shahrivar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'شهریور') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_shahrivar_place_df.iloc[:, 14] = pd.to_numeric((sara_shahrivar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_sara_place = sara_shahrivar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_mehr_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'مهر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_mehr_place_df.iloc[:, 14] = pd.to_numeric((sara_mehr_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_sara_place = sara_mehr_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_aban_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'آبان') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_aban_place_df.iloc[:, 14] = pd.to_numeric((sara_aban_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_sara_place = sara_aban_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_azar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'آذر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_azar_place_df.iloc[:, 14] = pd.to_numeric((sara_azar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_sara_place = sara_azar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_dey_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'دی') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_dey_place_df.iloc[:, 14] = pd.to_numeric((sara_dey_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_sara_place = sara_dey_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_bahman_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'بهمن') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_bahman_place_df.iloc[:, 14] = pd.to_numeric((sara_bahman_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_sara_place = sara_bahman_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sara_esfand_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sara') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sara_esfand_place_df.iloc[:, 14] = pd.to_numeric((sara_esfand_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_sara_place = sara_esfand_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد از شیت جایگاه و درامد هر ماه
    sum_income_place_farvardin_sara = sum_farvardin_sara + sum_farvardin_sara_place
    sum_income_place_ordibehesht_sara = sum_ordibehesht_sara + sum_ordibehesht_sara_place
    sum_income_place_khordad_sara = sum_khordad_sara + sum_khordad_sara_place
    sum_income_place_tir_sara = sum_tir_sara + sum_tir_sara_place
    sum_income_place_mordad_sara = sum_mordad_sara + sum_mordad_sara_place
    sum_income_place_shahrivar_sara = sum_shahrivar_sara + sum_shahrivar_sara_place
    sum_income_place_mehr_sara = sum_mehr_sara + sum_mehr_sara_place
    sum_income_place_aban_sara = sum_aban_sara + sum_aban_sara_place
    sum_income_place_azar_sara = sum_azar_sara + sum_azar_sara_place
    sum_income_place_dey_sara = sum_dey_sara + sum_dey_sara_place
    sum_income_place_bahman_sara = sum_bahman_sara + sum_bahman_sara_place
    sum_income_place_esfand_sara = sum_esfand_sara + sum_esfand_sara_place

    # ارسال داده‌ها به قالب
    return render(request, 'sara.html', {
        'total_sum_sara': total_sum_sara,
        'sum_income_place_sara': sum_income_place_sara,
        'sum_month_sara': sum_month_sara,
        'sum_month_income_place_sara': sum_month_income_place_sara,
        'sara_pending_count': sara_pending_count,
        'sara_cancel_count': sara_cancel_count,
        'sara_count': sara_count,
        'success_rate_sara': success_rate_sara,
        'cancel_rate_sara': cancel_rate_sara,
        'pending_rate_sara': pending_rate_sara,
        'club_rate_sara': club_rate_sara,
        'sara_dr_count_this_month': sara_dr_count_this_month,

        'sum_farvardin_sara': sum_farvardin_sara,
        'sum_ordibehesht_sara': sum_ordibehesht_sara,
        'sum_khordad_sara': sum_khordad_sara,
        'sum_tir_sara': sum_tir_sara,
        'sum_mordad_sara': sum_mordad_sara,
        'sum_shahrivar_sara': sum_shahrivar_sara,
        'sum_mehr_sara': sum_mehr_sara,
        'sum_aban_sara': sum_aban_sara,
        'sum_azar_sara': sum_azar_sara,
        'sum_dey_sara': sum_dey_sara,
        'sum_bahman_sara': sum_bahman_sara,
        'sum_esfand_sara': sum_esfand_sara,

        'sum_income_place_farvardin_sara': sum_income_place_farvardin_sara,
        'sum_income_place_ordibehesht_sara': sum_income_place_ordibehesht_sara,
        'sum_income_place_khordad_sara': sum_income_place_khordad_sara,
        'sum_income_place_tir_sara': sum_income_place_tir_sara,
        'sum_income_place_mordad_sara': sum_income_place_mordad_sara,
        'sum_income_place_shahrivar_sara': sum_income_place_shahrivar_sara,
        'sum_income_place_mehr_sara': sum_income_place_mehr_sara,
        'sum_income_place_aban_sara': sum_income_place_aban_sara,
        'sum_income_place_azar_sara': sum_income_place_azar_sara,
        'sum_income_place_dey_sara': sum_income_place_dey_sara,
        'sum_income_place_bahman_sara': sum_income_place_bahman_sara,
        'sum_income_place_esfand_sara': sum_income_place_esfand_sara,
    })


def elahe_def(request):
    # خواندن `credentials.json` از متغیر محیطی
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    # ساختن کرنشیال‌ها برای gspread
    creds = Credentials.from_service_account_info(credentials_info)

    # مقداردهی gspread
    gc = gspread.authorize(creds)

    # باز کردن Google Sheet
    sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')

    # اتصال به Google Sheets
    # gc = gspread.service_account(filename='credentials.json')
    # sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')
    worksheet = sheet.get_worksheet_by_id(232137112) # اولین شیت
    worksheet2 = sheet.get_worksheet_by_id(0) # شیت جایگاه 

    # دریافت تمام داده‌ها به صورت DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)
    data2 = worksheet2.get_all_values()
    df2 = pd.DataFrame(data2)

    # بررسی اینکه حداقل هشت ستون وجود داشته باشد
    if len(df.columns) < 2:
        return render(request, 'sum.html', {'sum_values': [], 'total_sum': 0})

    # حذف هدر و نامگذاری ستون‌ها
    df.columns = df.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df = df[1:]  # حذف ردیف هدر
    df2.columns = df2.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df2 = df2[1:]  # حذف ردیف هدر

    # فیلتر کردن ردیف‌هایی که نام "شهرزاد" دارند (ستون دوم)
    elahe_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم

    # فیلتر کردن ردیف‌هایی که نام "سارا" دارند در شیت جایگاه (ستون دوم)
    elahe_df_place = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
      
    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع
    elahe_df.iloc[:, 13] = pd.to_numeric((elahe_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_elahe = elahe_df.iloc[:, 13].sum()  # محاسبه مجموع

    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع در شیت جایگاه
    elahe_df_place.iloc[:, 14] = pd.to_numeric((elahe_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_elahe_place = elahe_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد هر فرد طبق شیت درامد و جایگاه
    sum_income_place_elahe = total_sum_elahe + total_sum_elahe_place

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند
    elahe_month_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند در شیت جایگاه
    elahe_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]

    # مجموع درامد افراد بر اساس ماه مورد نظر
    elahe_month_df.iloc[:, 13] = pd.to_numeric((elahe_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_elahe = elahe_month_df.iloc[:, 13].sum()  # محاسبه مجموع

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    elahe_month_df_place.iloc[:, 14] = pd.to_numeric((elahe_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_elahe_place = elahe_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد ماه مورد نظر از شیت جایگاه و درامد هر فرد
    sum_month_income_place_elahe = sum_month_elahe + sum_month_elahe_place

    # تعداد دکتر های این ماه هر شخص
    elahe_dr_count_this_month = df[(df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها

    # پندینگ و دان و کنسلی و تمام دکتر های هر شخص

    elahe_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها

    elahe_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها

    elahe_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها

    elahe_club_count = df[(df.iloc[:, 6].str.strip() == '💥') & (df.iloc[:, 3].str.strip() == 'elahe')].shape[0]  # تعداد ردیف‌ها

    elahe_count = df[df.iloc[:, 3].str.strip() == 'elahe'].shape[0]  # تعداد ردیف‌ها

    # درصد موفقیت هر شخص
    success_rate_elahe = (elahe_done_count / elahe_count)* 100

    # کنسلی هر شخص
    cancele_rate_elahe = (elahe_cancel_count / elahe_count)* 100

    # پندینگ هر شخص
    pending_rate_elahe = (elahe_pending_count / elahe_count)* 100

    # تمدید هر شخص
    club_rate_elahe = (elahe_club_count / elahe_count)* 100

    # مجموع درامد افراد بر اساس ماه مورد نظر
    elahe_farvardin_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'فروردین') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_farvardin_df.iloc[:, 13] = pd.to_numeric((elahe_farvardin_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_elahe = elahe_farvardin_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_ordibehesht_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'اردیبهشت') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_ordibehesht_df.iloc[:, 13] = pd.to_numeric((elahe_ordibehesht_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_elahe = elahe_ordibehesht_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_khordad_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'خرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_khordad_df.iloc[:, 13] = pd.to_numeric((elahe_khordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_elahe = elahe_khordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_tir_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'تیر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_tir_df.iloc[:, 13] = pd.to_numeric((elahe_tir_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_elahe = elahe_tir_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_mordad_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'مرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_mordad_df.iloc[:, 13] = pd.to_numeric((elahe_mordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_elahe = elahe_mordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_shahrivar_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'شهریور') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_shahrivar_df.iloc[:, 13] = pd.to_numeric((elahe_shahrivar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_elahe = elahe_shahrivar_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_mehr_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'مهر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_mehr_df.iloc[:, 13] = pd.to_numeric((elahe_mehr_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_elahe = elahe_mehr_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_aban_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'آبان') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_aban_df.iloc[:, 13] = pd.to_numeric((elahe_aban_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_elahe = elahe_aban_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_azar_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'آذر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_azar_df.iloc[:, 13] = pd.to_numeric((elahe_azar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_elahe = elahe_azar_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_dey_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'دی') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_dey_df.iloc[:, 13] = pd.to_numeric((elahe_dey_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_elahe = elahe_dey_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_bahman_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'بهمن') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_bahman_df.iloc[:, 13] = pd.to_numeric((elahe_bahman_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_elahe = elahe_bahman_df.iloc[:, 13].sum()  # محاسبه مجموع

    elahe_esfand_df = df[(df.iloc[:, 3].str.strip() == 'elahe') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]
    elahe_esfand_df.iloc[:, 13] = pd.to_numeric((elahe_esfand_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_elahe = elahe_esfand_df.iloc[:, 13].sum()  # محاسبه مجموع
    
    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    elahe_farvardin_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'فروردین') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_farvardin_place_df.iloc[:, 14] = pd.to_numeric((elahe_farvardin_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_elahe_place = elahe_farvardin_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_ordibehesht_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'اردیبهشت') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_ordibehesht_place_df.iloc[:, 14] = pd.to_numeric((elahe_ordibehesht_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_elahe_place = elahe_ordibehesht_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_khordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'خرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_khordad_place_df.iloc[:, 14] = pd.to_numeric((elahe_khordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_elahe_place = elahe_khordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_tir_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'تیر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_tir_place_df.iloc[:, 14] = pd.to_numeric((elahe_tir_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_elahe_place = elahe_tir_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_mordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'مرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_mordad_place_df.iloc[:, 14] = pd.to_numeric((elahe_mordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_elahe_place = elahe_mordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_shahrivar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'شهریور') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_shahrivar_place_df.iloc[:, 14] = pd.to_numeric((elahe_shahrivar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_elahe_place = elahe_shahrivar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_mehr_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'مهر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_mehr_place_df.iloc[:, 14] = pd.to_numeric((elahe_mehr_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_elahe_place = elahe_mehr_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_aban_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'آبان') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_aban_place_df.iloc[:, 14] = pd.to_numeric((elahe_aban_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_elahe_place = elahe_aban_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_azar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'آذر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_azar_place_df.iloc[:, 14] = pd.to_numeric((elahe_azar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_elahe_place = elahe_azar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_dey_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'دی') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_dey_place_df.iloc[:, 14] = pd.to_numeric((elahe_dey_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_elahe_place = elahe_dey_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_bahman_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'بهمن') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_bahman_place_df.iloc[:, 14] = pd.to_numeric((elahe_bahman_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_elahe_place = elahe_bahman_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    elahe_esfand_place_df = df2[(df2.iloc[:, 3].str.strip() == 'elahe') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    elahe_esfand_place_df.iloc[:, 14] = pd.to_numeric((elahe_esfand_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_elahe_place = elahe_esfand_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد از شیت جایگاه و درامد هر ماه
    sum_income_place_farvardin_elahe = sum_farvardin_elahe + sum_farvardin_elahe_place
    sum_income_place_ordibehesht_elahe = sum_ordibehesht_elahe + sum_ordibehesht_elahe_place
    sum_income_place_khordad_elahe = sum_khordad_elahe + sum_khordad_elahe_place
    sum_income_place_tir_elahe = sum_tir_elahe + sum_tir_elahe_place
    sum_income_place_mordad_elahe = sum_mordad_elahe + sum_mordad_elahe_place
    sum_income_place_shahrivar_elahe = sum_shahrivar_elahe + sum_shahrivar_elahe_place
    sum_income_place_mehr_elahe = sum_mehr_elahe + sum_mehr_elahe_place
    sum_income_place_aban_elahe = sum_aban_elahe + sum_aban_elahe_place
    sum_income_place_azar_elahe = sum_azar_elahe + sum_azar_elahe_place
    sum_income_place_dey_elahe = sum_dey_elahe + sum_dey_elahe_place
    sum_income_place_bahman_elahe = sum_bahman_elahe + sum_bahman_elahe_place
    sum_income_place_esfand_elahe = sum_esfand_elahe + sum_esfand_elahe_place

    # ارسال داده‌ها به قالب
    return render(request, 'elahe.html', {
        'total_sum_elahe': total_sum_elahe,
        'sum_income_place_elahe': sum_income_place_elahe,
        'sum_month_elahe': sum_month_elahe,
        'sum_month_income_place_elahe': sum_month_income_place_elahe,
        'elahe_pending_count': elahe_pending_count,
        'elahe_cancel_count': elahe_cancel_count,
        'elahe_count': elahe_count,
        'success_rate_elahe': success_rate_elahe,
        'cancele_rate_elahe': cancele_rate_elahe,
        'pending_rate_elahe': pending_rate_elahe,
        'club_rate_elahe': club_rate_elahe,
        'elahe_dr_count_this_month': elahe_dr_count_this_month,

        'sum_farvardin_elahe': sum_farvardin_elahe,
        'sum_ordibehesht_elahe': sum_ordibehesht_elahe,
        'sum_khordad_elahe': sum_khordad_elahe,
        'sum_tir_elahe': sum_tir_elahe,
        'sum_mordad_elahe': sum_mordad_elahe,
        'sum_shahrivar_elahe': sum_shahrivar_elahe,
        'sum_mehr_elahe': sum_mehr_elahe,
        'sum_aban_elahe': sum_aban_elahe,
        'sum_azar_elahe': sum_azar_elahe,
        'sum_dey_elahe': sum_dey_elahe,
        'sum_bahman_elahe': sum_bahman_elahe,
        'sum_esfand_elahe': sum_esfand_elahe,

        'sum_income_place_farvardin_elahe': sum_income_place_farvardin_elahe,
        'sum_income_place_ordibehesht_elahe': sum_income_place_ordibehesht_elahe,
        'sum_income_place_khordad_elahe': sum_income_place_khordad_elahe,
        'sum_income_place_tir_elahe': sum_income_place_tir_elahe,
        'sum_income_place_mordad_elahe': sum_income_place_mordad_elahe,
        'sum_income_place_shahrivar_elahe': sum_income_place_shahrivar_elahe,
        'sum_income_place_mehr_elahe': sum_income_place_mehr_elahe,
        'sum_income_place_aban_elahe': sum_income_place_aban_elahe,
        'sum_income_place_azar_elahe': sum_income_place_azar_elahe,
        'sum_income_place_dey_elahe': sum_income_place_dey_elahe,
        'sum_income_place_bahman_elahe': sum_income_place_bahman_elahe,
        'sum_income_place_esfand_elahe': sum_income_place_esfand_elahe,
    })


def sanam_def(request):
    # خواندن `credentials.json` از متغیر محیطی
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    # ساختن کرنشیال‌ها برای gspread
    creds = Credentials.from_service_account_info(credentials_info)

    # مقداردهی gspread
    gc = gspread.authorize(creds)

    # باز کردن Google Sheet
    sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')

    # اتصال به Google Sheets
    # gc = gspread.service_account(filename='credentials.json')
    # sheet = gc.open_by_key('1xyIsK30g4OPlyRa4_VqfnKkFoPL-MYWR8AP8qR4_QHo')
    worksheet = sheet.get_worksheet_by_id(232137112) # اولین شیت
    worksheet2 = sheet.get_worksheet_by_id(0) # شیت جایگاه 

    # دریافت تمام داده‌ها به صورت DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)
    data2 = worksheet2.get_all_values()
    df2 = pd.DataFrame(data2)

    # بررسی اینکه حداقل هشت ستون وجود داشته باشد
    if len(df.columns) < 2:
        return render(request, 'sum.html', {'sum_values': [], 'total_sum': 0})

    # حذف هدر و نامگذاری ستون‌ها
    df.columns = df.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df = df[1:]  # حذف ردیف هدر
    df2.columns = df2.iloc[0]  # استفاده از اولین ردیف به عنوان هدر
    df2 = df2[1:]  # حذف ردیف هدر

    # فیلتر کردن ردیف‌هایی که نام "شهرزاد" دارند (ستون دوم)
    sanam_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم

    # فیلتر کردن ردیف‌هایی که نام "سارا" دارند در شیت جایگاه (ستون دوم)
    sanam_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 4].str.strip() == 'DONE')]  # فیلتر بر اساس نام در ستون دوم
      
    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع
    sanam_df.iloc[:, 13] = pd.to_numeric((sanam_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sanam = sanam_df.iloc[:, 13].sum()  # محاسبه مجموع

    # تبدیل مقادیر ستون هشتم به عدد و محاسبه مجموع در شیت جایگاه
    sanam_df_place.iloc[:, 14] = pd.to_numeric((sanam_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    total_sum_sanam_place = sanam_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد هر فرد طبق شیت درامد و جایگاه
    sum_income_place_sanam = total_sum_sanam + total_sum_sanam_place

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند
    sanam_month_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]

    # فیلتر کردن ردیف‌هایی که نام "محمد" و ماه "دی" دارند در شیت جایگاه
    sanam_month_df_place = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]

    # مجموع درامد افراد بر اساس ماه مورد نظر
    sanam_month_df.iloc[:, 13] = pd.to_numeric((sanam_month_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sanam = sanam_month_df.iloc[:, 13].sum()  # محاسبه مجموع

    # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    sanam_month_df_place.iloc[:, 14] = pd.to_numeric((sanam_month_df_place.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_month_sanam_place = sanam_month_df_place.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد ماه مورد نظر از شیت جایگاه و درامد هر فرد
    sum_month_income_place_sanam = sum_month_sanam + sum_month_sanam_place

    # تعداد دکتر های این ماه هر شخص
    sanam_dr_count_this_month = df[(df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها

    # پندینگ و دان و کنسلی و تمام دکتر های هر شخص

    sanam_pending_count = df[(df.iloc[:, 4].str.strip() == 'PENDING') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها

    sanam_cancel_count = df[(df.iloc[:, 4].str.strip() == 'CANCEL') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها

    sanam_done_count = df[(df.iloc[:, 4].str.strip() == 'DONE') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها

    sanam_club_count = df[(df.iloc[:, 6].str.strip() == '💥') & (df.iloc[:, 3].str.strip() == 'sanam')].shape[0]  # تعداد ردیف‌ها

    sanam_count = df[df.iloc[:, 3].str.strip() == 'sanam'].shape[0]  # تعداد ردیف‌ها

    # درصد موفقیت هر شخص
    success_rate_sanam = (sanam_done_count / sanam_count)* 100

    # کنسلی هر شخص
    cancele_rate_sanam = (sanam_cancel_count / sanam_count)* 100

    # پندینگ هر شخص
    pending_rate_sanam = (sanam_pending_count / sanam_count)* 100

    # تمدید هر شخص
    club_rate_sanam = (sanam_club_count / sanam_count)* 100

    # مجموع درامد افراد بر اساس ماه مورد نظر
    sanam_farvardin_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'فروردین') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_farvardin_df.iloc[:, 13] = pd.to_numeric((sanam_farvardin_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_sanam = sanam_farvardin_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_ordibehesht_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'اردیبهشت') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_ordibehesht_df.iloc[:, 13] = pd.to_numeric((sanam_ordibehesht_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_sanam = sanam_ordibehesht_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_khordad_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'خرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_khordad_df.iloc[:, 13] = pd.to_numeric((sanam_khordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_sanam = sanam_khordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_tir_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'تیر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_tir_df.iloc[:, 13] = pd.to_numeric((sanam_tir_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_sanam = sanam_tir_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_mordad_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'مرداد') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_mordad_df.iloc[:, 13] = pd.to_numeric((sanam_mordad_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_sanam = sanam_mordad_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_shahrivar_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'شهریور') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_shahrivar_df.iloc[:, 13] = pd.to_numeric((sanam_shahrivar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_sanam = sanam_shahrivar_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_mehr_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'مهر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_mehr_df.iloc[:, 13] = pd.to_numeric((sanam_mehr_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_sanam = sanam_mehr_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_aban_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'آبان') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_aban_df.iloc[:, 13] = pd.to_numeric((sanam_aban_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_sanam = sanam_aban_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_azar_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'آذر') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_azar_df.iloc[:, 13] = pd.to_numeric((sanam_azar_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_sanam = sanam_azar_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_dey_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'دی') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_dey_df.iloc[:, 13] = pd.to_numeric((sanam_dey_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_sanam = sanam_dey_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_bahman_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'بهمن') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_bahman_df.iloc[:, 13] = pd.to_numeric((sanam_bahman_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_sanam = sanam_bahman_df.iloc[:, 13].sum()  # محاسبه مجموع

    sanam_esfand_df = df[(df.iloc[:, 3].str.strip() == 'sanam') & (df.iloc[:, 2].str.strip() == 'اسفند') & (df.iloc[:, 4].str.strip() == 'DONE')]
    sanam_esfand_df.iloc[:, 13] = pd.to_numeric((sanam_esfand_df.iloc[:, 13]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_sanam = sanam_esfand_df.iloc[:, 13].sum()  # محاسبه مجموع

     # مجموع درامد افراد بر اساس ماه مورد نظر در شیت جایگاه
    sanam_farvardin_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'فروردین') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_farvardin_place_df.iloc[:, 14] = pd.to_numeric((sanam_farvardin_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_farvardin_sanam_place = sanam_farvardin_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_ordibehesht_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'اردیبهشت') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_ordibehesht_place_df.iloc[:, 14] = pd.to_numeric((sanam_ordibehesht_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_ordibehesht_sanam_place = sanam_ordibehesht_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_khordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'خرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_khordad_place_df.iloc[:, 14] = pd.to_numeric((sanam_khordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_khordad_sanam_place = sanam_khordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_tir_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'تیر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_tir_place_df.iloc[:, 14] = pd.to_numeric((sanam_tir_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_tir_sanam_place = sanam_tir_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_mordad_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'مرداد') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_mordad_place_df.iloc[:, 14] = pd.to_numeric((sanam_mordad_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mordad_sanam_place = sanam_mordad_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_shahrivar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'شهریور') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_shahrivar_place_df.iloc[:, 14] = pd.to_numeric((sanam_shahrivar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_shahrivar_sanam_place = sanam_shahrivar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_mehr_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'مهر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_mehr_place_df.iloc[:, 14] = pd.to_numeric((sanam_mehr_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_mehr_sanam_place = sanam_mehr_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_aban_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'آبان') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_aban_place_df.iloc[:, 14] = pd.to_numeric((sanam_aban_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_aban_sanam_place = sanam_aban_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_azar_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'آذر') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_azar_place_df.iloc[:, 14] = pd.to_numeric((sanam_azar_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_azar_sanam_place = sanam_azar_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_dey_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'دی') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_dey_place_df.iloc[:, 14] = pd.to_numeric((sanam_dey_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_dey_sanam_place = sanam_dey_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_bahman_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'بهمن') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_bahman_place_df.iloc[:, 14] = pd.to_numeric((sanam_bahman_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_bahman_sanam_place = sanam_bahman_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    sanam_esfand_place_df = df2[(df2.iloc[:, 3].str.strip() == 'sanam') & (df2.iloc[:, 2].str.strip() == 'اسفند') & (df2.iloc[:, 4].str.strip() == 'DONE')]
    sanam_esfand_place_df.iloc[:, 14] = pd.to_numeric((sanam_esfand_place_df.iloc[:, 14]).str.replace(",", ""), errors='coerce')  # تبدیل به عدد
    sum_esfand_sanam_place = sanam_esfand_place_df.iloc[:, 14].sum()  # محاسبه مجموع

    # مجموع درامد از شیت جایگاه و درامد هر ماه
    sum_income_place_farvardin_sanam = sum_farvardin_sanam + sum_farvardin_sanam_place
    sum_income_place_ordibehesht_sanam = sum_ordibehesht_sanam + sum_ordibehesht_sanam_place
    sum_income_place_khordad_sanam = sum_khordad_sanam + sum_khordad_sanam_place
    sum_income_place_tir_sanam = sum_tir_sanam + sum_tir_sanam_place
    sum_income_place_mordad_sanam = sum_mordad_sanam + sum_mordad_sanam_place
    sum_income_place_shahrivar_sanam = sum_shahrivar_sanam + sum_shahrivar_sanam_place
    sum_income_place_mehr_sanam = sum_mehr_sanam + sum_mehr_sanam_place
    sum_income_place_aban_sanam = sum_aban_sanam + sum_aban_sanam_place
    sum_income_place_azar_sanam = sum_azar_sanam + sum_azar_sanam_place
    sum_income_place_dey_sanam = sum_dey_sanam + sum_dey_sanam_place
    sum_income_place_bahman_sanam = sum_bahman_sanam + sum_bahman_sanam_place
    sum_income_place_esfand_sanam = sum_esfand_sanam + sum_esfand_sanam_place

    # ارسال داده‌ها به قالب
    return render(request, 'sanam.html', {
        'total_sum_sanam': total_sum_sanam,
        'sum_income_place_sanam': sum_income_place_sanam,
        'sum_month_sanam': sum_month_sanam,
        'sum_month_income_place_sanam': sum_month_income_place_sanam,
        'sanam_pending_count': sanam_pending_count,
        'sanam_cancel_count': sanam_cancel_count,
        'sanam_count': sanam_count,
        'success_rate_sanam': success_rate_sanam,
        'cancele_rate_sanam': cancele_rate_sanam,
        'pending_rate_sanam': pending_rate_sanam,
        'club_rate_sanam': club_rate_sanam,
        'sanam_dr_count_this_month': sanam_dr_count_this_month,

        'sum_farvardin_sanam': sum_farvardin_sanam,
        'sum_ordibehesht_sanam': sum_ordibehesht_sanam,
        'sum_khordad_sanam': sum_khordad_sanam,
        'sum_tir_sanam': sum_tir_sanam,
        'sum_mordad_sanam': sum_mordad_sanam,
        'sum_shahrivar_sanam': sum_shahrivar_sanam,
        'sum_mehr_sanam': sum_mehr_sanam,
        'sum_aban_sanam': sum_aban_sanam,
        'sum_azar_sanam': sum_azar_sanam,
        'sum_dey_sanam': sum_dey_sanam,
        'sum_bahman_sanam': sum_bahman_sanam,
        'sum_esfand_sanam': sum_esfand_sanam,
        
        'sum_income_place_farvardin_sanam': sum_income_place_farvardin_sanam,
        'sum_income_place_ordibehesht_sanam': sum_income_place_ordibehesht_sanam,
        'sum_income_place_khordad_sanam': sum_income_place_khordad_sanam,
        'sum_income_place_tir_sanam': sum_income_place_tir_sanam,
        'sum_income_place_mordad_sanam': sum_income_place_mordad_sanam,
        'sum_income_place_shahrivar_sanam': sum_income_place_shahrivar_sanam,
        'sum_income_place_mehr_sanam': sum_income_place_mehr_sanam,
        'sum_income_place_aban_sanam': sum_income_place_aban_sanam,
        'sum_income_place_azar_sanam': sum_income_place_azar_sanam,
        'sum_income_place_dey_sanam': sum_income_place_dey_sanam,
        'sum_income_place_bahman_sanam': sum_income_place_bahman_sanam,
        'sum_income_place_esfand_sanam': sum_income_place_esfand_sanam,
    })