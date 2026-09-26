import re

INTENT_TO_LEVEL = {
    'VISIT': 'high',
    'SCHEDULING': 'high',
    'AVAILABILITY': 'high',
    'DIRECT_PURCHASE_INTENT': 'high',
    'DIRECT_RENT_INTENT': 'high',
    'CONTACT_ATTEMPT': 'high',
    'PRICE': 'medium',
    'CONDOMINIUM': 'medium',
    'IPTU': 'medium',
    'FINANCING': 'medium',
    'FGTS': 'medium',
    'DOWN_PAYMENT': 'medium',
    'LOCATION': 'medium',
    'BEDROOMS': 'medium',
    'AREA': 'medium',
    'GARAGE': 'medium',
    'PROPERTY_FEATURE': 'medium',
    'PHOTOS': 'low',
    'GENERIC_INFO': 'low',
}

LEVEL_ORDER = {'not_lead': 0, 'low': 1, 'medium': 2, 'high': 3}

PATTERNS = [
    ('SCHEDULING', r'\b(agendar|marcar|agenda|hor[aá]rio|pode ver amanh[aã])\b'),
    ('VISIT', r'\b(visita|visitar|conhecer o im[oó]vel)\b'),
    ('AVAILABILITY', r'\b(ainda.*dispon[ií]vel|est[aá].*dispon[ií]vel|disponibilidade)\b'),
    ('DIRECT_PURCHASE_INTENT', r'\b(quero comprar|pretendo comprar|tenho interesse|interesse em comprar)\b'),
    ('DIRECT_RENT_INTENT', r'\b(quero alugar|pretendo alugar|interesse em alugar)\b'),
    ('CONTACT_ATTEMPT', r'\b(tentei contato|ningu[eé]m respondeu|j[aá] mandei mensagem)\b'),
    ('CONDOMINIUM', r'\b(condom[ií]nio)\b'),
    ('IPTU', r'\b(iptu)\b'),
    ('FINANCING', r'\b(financi|financiamento|financia)\w*\b'),
    ('FGTS', r'\bfgts\b'),
    ('DOWN_PAYMENT', r'\b(entrada|sinal)\b'),
    ('PRICE', r'\b(valor|pre[cç]o|quanto custa|mensal)\b'),
    ('BEDROOMS', r'\b(quarto|quartos|su[ií]te|su[ií]tes)\b'),
    ('AREA', r'\b(metragem|m2|m²|metros quadrados)\b'),
    ('GARAGE', r'\b(garagem|vaga|vagas)\b'),
    ('LOCATION', r'\b(fica onde|localiza[cç][aã]o|bairro|perto da praia|proximidade)\b'),
    ('PHOTOS', r'\b(foto|fotos|planta|tabela)\b'),
    ('PROPERTY_FEATURE', r'\b(andar|piscina|profundidade)\b'),
    ('GENERIC_INFO', r'\b(mais informa[cç][oõ]es|saber mais|qual o contato|informa[cç][aã]o)\b'),
]

EXCLUDE_ONLY_EMOJI = re.compile(r'^[\W_]+$', re.UNICODE)
EXCLUDE_MENTION_ONLY = re.compile(r'^\s*@[-._a-zA-Z0-9]+\s*$', re.UNICODE)


def qualify(intents):
    levels = [INTENT_TO_LEVEL[i] for i in intents if i in INTENT_TO_LEVEL]
    return max(levels, key=lambda item: LEVEL_ORDER[item]) if levels else 'not_lead'


def analyze_comment(text):
    original = text or ''
    normalized = original.strip().lower()

    if not normalized:
        return {'is_lead': False, 'intents': [], 'qualification': 'not_lead', 'confidence': 1.0, 'exclusion_reason': 'Comentario vazio'}
    if EXCLUDE_MENTION_ONLY.match(normalized):
        return {'is_lead': False, 'intents': [], 'qualification': 'not_lead', 'confidence': 0.99, 'exclusion_reason': 'Marcacao generica'}
    if EXCLUDE_ONLY_EMOJI.match(normalized) and not any(char.isalnum() for char in normalized):
        return {'is_lead': False, 'intents': [], 'qualification': 'not_lead', 'confidence': 0.99, 'exclusion_reason': 'Emoji/sem texto comercial'}

    intents = []
    evidence = []
    for intent, pattern in PATTERNS:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if match:
            intents.append(intent)
            evidence.append(match.group(0))

    # Elogios simples sem sinais comerciais nao viram lead.
    if not intents:
        return {
            'is_lead': False,
            'intents': [],
            'qualification': 'not_lead',
            'confidence': 0.85,
            'evidence': [],
            'exclusion_reason': 'Sem sinal comercial reconhecido',
        }

    level = qualify(intents)
    confidence = 0.96 if level == 'high' else 0.91 if level == 'medium' else 0.84
    return {
        'is_lead': level != 'not_lead',
        'intents': intents,
        'qualification': level,
        'confidence': confidence,
        'evidence': evidence,
        'exclusion_reason': '',
    }
