import hashlib
from django.core.management.base import BaseCommand
from leads.models import Classification, Comment, Profile, Publication
from leads.services.qualification import analyze_comment


DEMO_ROWS = [
    ('56 sem', '@talitamabrito', 'Triplex', 'Pitangueiras', 'Venda', 'Gostaria de marcar uma visita.'),
    ('81 sem', '@jully.queiroz', 'Triplex', 'Pitangueiras', 'Venda', 'Gostaria de mais informações'),
    ('82 sem', '@dandj26', 'Triplex', 'Pitangueiras', 'Venda', 'Boa tarde, todas as fotos estão aí ou tem mais? Se sim, poderia me enviar'),
    ('33 sem', '@ss.international.br', 'Casa', 'Pitangueiras', 'Venda', 'Perfeito. Qual a profundidade da piscina? E o valor do condomínio?'),
    ('38 sem', '@jessica_souza_m91', 'Casa', 'Pitangueiras', 'Venda', 'Ainda tá disponível?'),
    ('69 sem', '@vancbittencourt', 'Casa', 'Pitangueiras', 'Venda', 'Qual o contato para saber informações'),
    ('69 sem', '@roselimarquesdafonseca', 'Casa', 'Pitangueiras / próximo à praia', 'Venda', 'Sou de SP e pretendo comprar uma casa em Salvador para morar. Gostei muito dessa casa, vc poderia mandar mais fotos, a casa é perto da praia, dá pra ir andando.'),
    ('69 sem', '@consullessa', 'Casa', 'Pitangueiras', 'Venda', 'Gostaria de saber mais informações'),
    ('61w', '@beel.rodriigues', 'Imóvel', 'Praia de Ipitanga', 'Venda', 'Ainda está disponível?'),
    ('64w', '@jannerosa50', 'Imóvel', 'Praia de Ipitanga', 'Venda', 'Fica onde'),
    ('4d', '@almada_97', 'Apartamento 2 quartos', 'Costa Azul', 'Locação', 'Pode ver amanhã?'),
    ('4d', '@almada_97', 'Apartamento 2 quartos', 'Costa Azul', 'Locação', 'Tenho interesse'),
    ('6d', '@ana_dosreis', 'Apartamento 2 quartos', 'Costa Azul', 'Locação', '2822,00? Mensal?'),
    ('1w', '@ludmila.l.leite', 'Apartamento', 'Aquárius/Pituba', 'Locação', 'Qual o valor para locação?'),
    ('1w', '@gabisbonadio', 'Apartamento mobiliado', 'Ondina', 'Locação', 'Está disponível?'),
    ('1w', '@angelaaraujoa2a2', 'Apartamento', 'Jardim Apipema/Ondina', 'Venda', 'São quantos quartos?'),
    ('1w', '@renammarques', 'Apartamento', 'Jardim Apipema/Ondina', 'Venda', 'Projeto impecável! 👏 Gostaria de saber o valor desse investimento.'),
    ('1w', '@lualeluia', 'Apartamento', 'Armação / Residencial Cidade de Ituberá', 'Venda', 'Qual o andar?'),
    ('1w', '@lualeluia', 'Apartamento', 'Armação / Residencial Cidade de Ituberá', 'Venda', 'Gostaria de agendar uma visita nesse imóvel. Cidade de Ituberá.'),
    ('8w', '@nivearigaud', 'Imóvel anunciado', 'Região não informada', 'Venda', 'Quero comprar. To de olho aqui.'),
    ('3 min', '@odilon_rodrigo', 'Imóvel anunciado', 'Região não informada', '', 'Tem Fotos ?'),
    ('10 h', '@katherinegalo_', 'Imóvel anunciado', 'Região não informada', '', 'Qual o valor do condomínio'),
    ('1h', '@lucysales23', 'Imóvel anunciado', 'Região não informada', '', 'Mais informações'),
    ('4h', '@terezada_silvaqueiroz', 'Imóvel anunciado', 'Região não informada', '', 'Qual a metragem'),
]


class Command(BaseCommand):
    help = 'Carrega os 24 leads de referencia para testar a interface do ChaveRadar.'

    def handle(self, *args, **options):
        profile, _ = Profile.objects.get_or_create(
            handle='@demo_imobiliaria',
            defaults={'display_name': 'Imobiliaria Demo', 'source_type': 'manual'},
        )
        created = 0
        for index, (date_display, user, property_type, region, transaction, text) in enumerate(DEMO_ROWS, start=1):
            permalink = f'https://www.instagram.com/p/chaveradar-demo-{index:02d}/'
            publication, _ = Publication.objects.get_or_create(
                profile=profile,
                permalink=permalink,
                defaults={
                    'media_type': 'POST',
                    'property_type': property_type,
                    'property_region': region,
                    'transaction_type': transaction,
                },
            )
            raw_key = '|'.join([profile.handle, permalink, user, text, date_display])
            fingerprint = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
            comment, was_created = Comment.objects.get_or_create(
                fingerprint=fingerprint,
                defaults={
                    'publication': publication,
                    'username': user,
                    'display_name': '',
                    'text_original': text,
                    'displayed_date_original': date_display,
                    'source_type': 'manual',
                },
            )
            if not was_created:
                continue
            result = analyze_comment(text)
            Classification.objects.create(
                comment=comment,
                is_lead=result['is_lead'],
                intents=result.get('intents', []),
                qualification=result['qualification'],
                evidence=result.get('evidence', []),
                confidence=result.get('confidence'),
                exclusion_reason=result.get('exclusion_reason', ''),
                review_status='pending' if result['is_lead'] else 'auto',
                classifier_version='0.2.2',
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Dados de demonstracao carregados. Novos comentarios: {created}.'))
