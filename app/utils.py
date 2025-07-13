from jhora.horoscope.chart import charts, dosha, raja_yoga, yoga
from jhora.horoscope.dhasa.graha import vimsottari
from jhora.horoscope.match import compatibility
from jhora.horoscope.prediction import general
from jhora.panchanga import drik
from jhora.utils import julian_day_number

def get_julian_day(data):
    return julian_day_number((data.year, data.month, data.day), (data.hour, data.minute, data.second))

def get_place(data):
    return drik.Place("",data.latitude, data.longitude, data.timezone)

def get_afflictions(data):
    jd = get_julian_day(data)
    place = get_place(data)
    return dosha.get_dosha_details(jd, place, language=data.language)

def get_compatibility(data):
    ak = compatibility.Ashtakoota(
        boy_nakshatra_number=data.male_nak_num,
        boy_paadham_number=data.male_nak_pada,
        girl_nakshatra_number=data.female_nak_num,
        girl_paadham_number=data.female_nak_pada,
        method=data.method
        )
    return ak

def get_daily_calendar(data):
    jd = get_julian_day(data)
    place = get_place(data)
    tamil_date = drik.tamil_solar_month_and_date_from_jd(jd,place)
    moon_rise = drik.moonrise(jd, place)
    moon_set = drik.moonset(jd, place)
    sun_rise = drik.sunrise(jd, place)
    sun_set = drik.sunset(jd, place)
    rahu_kala = drik.trikalam(jd, place, option='raahu kaalam')
    gulika_kala = drik.trikalam(jd, place, option='gulikai')
    yamaganda_kala = drik.trikalam(jd, place, option='yamagandam')
    tithi = drik.tithi(jd,place)
    rasi = drik.raasi(jd, place)
    nakshatra = drik.nakshatra(jd, place)
    karana= drik.karana(jd, place)
    masa = drik.lunar_month(jd, place)
    ritu = drik.ritu(masa[0])
    abhijit_muhurta = drik.abhijit_muhurta(jd, place)    
    day_length = drik.day_length(jd, place)
    night_length = drik.night_length(jd, place)
    nitya_yoga = drik.yogam(jd, place)
    elapsed_year = drik.elapsed_year(jd,masa[0])
    kali_year = elapsed_year[0]    
    result = {
        "kali": kali_year,
        "date": tamil_date,
        "sun": [sun_rise, sun_set],
        "moon": [moon_rise, moon_set],
        "day": day_length,
        "night": night_length,
        "ritu": ritu,
        "rasi": rasi,
        "nakshatra": nakshatra,
        "tithi": tithi,
        "karana": karana,
        "yoga": nitya_yoga,
        "rahu": rahu_kala,
        "gulika": gulika_kala,
        "yamaganda": yamaganda_kala,
        "abhijit": abhijit_muhurta,
    }
    return result

def get_divisional_chart(data):
    d_number = int(data.chart_num[1:])
    jd = get_julian_day(data)
    place = get_place(data)
    ayanamsa = data.ayanamsa
    gulika = drik.upagraha_longitude((data), (data.hour,data.minute,data.second), place, planet_index=6, ayanamsa_mode=ayanamsa, divisional_chart_factor=d_number)
    chart = charts.divisional_chart(jd, place, ayanamsa_mode=ayanamsa, divisional_chart_factor=d_number)
    retrograde_planets = drik.planets_in_retrograde(jd, place)
    asc = chart[0][1]
    return { chart, retrograde_planets, asc, gulika }

def get_general_predictions(data):
    jd = get_julian_day(data)
    place = get_place(data)
    return general.get_prediction_details(jd, place, language=data.language)

def get_nakshatra(data):
    jd = get_julian_day(data)
    place = get_place(data)
    return drik.nakshatra(jd, place)

def get_planet_combinations(data):
    d_number = 1
    jd = get_julian_day(data)
    place = get_place(data)
    all_yoga = yoga.get_yoga_details_for_all_charts(jd, place, divisional_chart_factor=d_number, language=data.language)
    all_raja_yoga = raja_yoga.get_raja_yoga_details_for_all_charts(jd, place, divisional_chart_factor=d_number, language=data.language)
    return { raja_yoga: all_raja_yoga[0], yoga: all_yoga[0] }

def get_planet_periods(data):
    jd = get_julian_day(data)
    place = get_place(data)
    dasha = {}
    if data.name.lower() == "vimshottari":
        dasha = get_vimsottari_dasha(jd, place)
    return dasha

def get_planet_positions(data):
    return get_divisional_chart(data)

def get_vimsottari_dasha(jd, place):    
    dasha = vimsottari.vimsottari_mahadasa(jd, place)
    bhukthi = vimsottari.get_vimsottari_dhasa_bhukthi(jd, place)
    return { dasha, bhukthi }
