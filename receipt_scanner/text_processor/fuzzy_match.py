from rapidfuzz import process, fuzz

def normalize_and_match_unit(unit):
    KNOWN_UNITS = ['lb', 'g', 'kg', 'oz', 'ml', 'l', 'ea']
    unit = unit.lower()
    KNOWN_UNITS_LOWER = [u.lower() for u in KNOWN_UNITS]
    match, score, _ = process.extractOne(unit, KNOWN_UNITS_LOWER, scorer=fuzz.ratio)

    return match if score >= 50 else unit
