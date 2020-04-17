import re

# zahlen oder ein # plus zahl am beginn
import sys

title_starting_numbers = r"^#?[\d_-]*(.*)"
title_starting_single_char = r"^[a-dA-D]\s(.*)"

challenge_starts_numbers = r"^\d+\s?-(.*)"


def normalize_title(s):
    normalized_a = re.findall(title_starting_numbers, s.strip())
    normalized_b = normalized_a[0].strip().replace('_', ' ')
    if re.match(title_starting_single_char, normalized_b):
        normalized_c = re.findall(title_starting_single_char, normalized_b)
        return normalized_c[0].strip()
    else:
        return normalized_b


def normalize_challenge(s):
    if re.match(challenge_starts_numbers, s):
        normalized = re.findall(challenge_starts_numbers, s)
        return normalized[0].strip()
    else:
        return s


if __name__ == '__main__':

    print(normalize_challenge("48 - hilfsmittel"))

    titles = ["01_096_Lebensmittel-Matching_ErsatzKompass",
              "034_nachbarschaftshilfe_karmakurier",
              "#1_019_d_e-learning Digitale Schule",
              "06_Medizingeräteherstellung_Medprint",
              "Lake COVID",
              "1_019_e-learning_eedu_elearning_portal_mit_aufgaben",
              "01_006_Medizingeräteherstellung_DIY-Beatmungsgerät",
              "0024_Krankenhäuser_Corina",
              "1_016_LokaleUnternehmen_WirVonHier",
              "01_017_Supermarkt Status_SafeMarket",
              "31_Digitale_Krankheits-Anamnese_SymptomTracker",
              "04_Verteilung von HelferInnen - we.help",
              "16_lokaleUnternehmen_lokaler-kaufen",
              "1_039_d_staatlichekommunikation_BevölkerungUndBehördenApp",
              "1_036_d_Grenzkontrollen – fastbordercrossing.org",
              "08_PANDOA Virus Tracker",
              "1_16_D_lokaleunternehmen_GET IT!",
              "029_Landwirtschaft_ErnteErfolg",
              "#EveryoneCounts - Das Social Distancing Dashboard",
              "09_e-Anträge_AutomatisierteFörderantragsstellung",
              "1_19_0065_1508_ e-learning_Die Virtuelle Schule",
              "46_Gamification_CouchTree, deine App zum hinpflanzen",
              "1_026_580_Virtuelles Klassenzimmer",
              "NEXT-Bedroom",
              "21_Krisenkommunikation_CheckDenFakt",
              "www. 48hFörderung.org zur fin Unterstützung in 48h Solounter",
              "01_011_Infektionsfallübermittlung_TrackCovidCluster",
              "009_eAnträge_wir-bleiben-liqui.de",
              "01_034_Nachbarschaftshilfe_NahundGern!",
              "01_004_VerteilungVonHelferInnen_Projekt_HelferApp",
              "1_001_a_lebensmittel-matching_HelpingHands",
              "1_008_corona_tracking_CoroNow-Contact tracking via Bluetooth",
              "1_016_dgE-Krisengeld",
              "17_SupermarktStatus_SuTi",
              "023-1344_GenerelleKommunikation_GHH Corona Chatbot",
              "1_018_mental_health_pallia_gemeinsamgehen",
              "1_017_Supermarkt-Status_Klopaphere",
              "#1_003_arbeiterinnenverteilung_helpKRANKENHAUS",
              "1_035_bedingungsloses_grundeinkommen",
              "019_e-Learning_Homeschooling_für_benachteiligte_Familien",
              "1_018_mental_health_Konfliktlotse",
              "012_a_social-distancing_PortalAR - Virtuelles Reisen",
              "024_Krankenhäuser_DeutschlandweitesIntensivbettenmanagement",
              "016_LokaleUnternehmen_stubenshopper",
              "008_CoronaTracking_Gretel",
              "1_06_Medizingeräteherstellung_print4health",
              "1_016_a_lokale_unternehmen_LokalKauf",
              "05_a_hilfsmittelverteilung MediSupply",
              "01_e-learning_EDUmentoring.de",
              "019_e-learning_ROOMIE – digitales Klassenzimmer",
              "#1_018_mental_health_coaching_fuer_alle_Ayouto_HilfeFürDich",
              "01_010_analogeunterstützung_hilfstelefon",
              "11_Infektionsfall-Übermittlung_CoV-erage",
              "1_019_d-e-learning_508_eLearning_Bananasplit",
              "1_002_d_tauschplattformen_CivicTechHub",
              "11_Infektionsfall-Übermittlung_Sick Or Not]",
              "Ein ganz normaler Titel"]

    normalized_titles = []
    for title in titles:
        normalized_titles.append(normalize_title(title))

    normalized_titles.sort()
    for title in normalized_titles:
        print(title)
