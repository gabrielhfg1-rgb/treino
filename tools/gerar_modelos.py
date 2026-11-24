"""Gera templates.json: a biblioteca de modelos de treino do app.

Cada divisão (Full body, AB, ABC, ABCD, ABCDE, Push/Pull/Legs) é montada para
3 objetivos (emagrecer, massa magra, hipertrofia). O objetivo muda séries,
repetições, descanso e cardio. Os vídeos são os mesmos já conferidos no app.

Uso:  python tools/gerar_modelos.py
"""
import json, os

Y = 'https://www.youtube.com/watch?v='
SM = 'SkeletMotion · '

# (rótulo, id do YouTube, duração em segundos)
V = {
 'SR': [(SM+'erros no supino','jwQW5vdo_1Q',33),('Barra livre','WwXS2TeFmeg',65),('Halteres','SWVO95XzxKg',66),('Smith','qpGlwaXwrHE',60)],
 'SI': [(SM+'supino inclinado','qoFa4IAh2aA',28),('Halteres','F4Q1g2z8MWM',58),('Barra','oZjIQN0YMX0',61),('Smith','D_h6XI_YxhA',57)],
 'CR': [('Máquina (voador)','1D9x_U6PkY8',56),('Crossover','j9dk50rAd1w',49),('Halteres no banco','ITbQH-1HYZI',67)],
 'TP': [(SM+'tríceps pulley','14Ix96dxXIQ',36),('Polia com barra reta','9cmeOVHOjck',17),('Polia com barra V','k4Rl9WksA5o',47),('Polia com corda','GtHahe5XOwE',46)],
 'TF': [(SM+'extensão acima da cabeça','hpS-aXn6Jyg',28),('Halter com as duas mãos','hMY9E-qy20k',44),('Halter com uma mão','UHzfoMytaCg',55),('Polia com corda','mmWQ2ArLZzE',17)],
 'TT': [('Barra W','AY0kcO-tx30',59)],
 'PF': [(SM+'puxada frontal','khYdpqwBIug',25),('Polia, pegada aberta','Xn-fIQw08q4',51),('Barra fixa','e0_JPPnPNXo',57),('Polia com triângulo','SIyWK5Uy1yM',53)],
 'RC': [('Barra livre','z6DDVvZKlVo',52),('Smith','YBbuote_idg',53),('Halter (serrote)','JE3XUqMyHXo',50)],
 'RB': [(SM+'remada sentada','9Jcc4XmkUPI',12),('Polia com triângulo','WxkMoxuMSho',55),('Máquina articulada','Gg_EGNPg-cs',48),('Halter (serrote)','EUisRaNkCd4',58)],
 'RU': [('Halter no banco (serrote)','JE3XUqMyHXo',50),('Polia (uma mão)','L2O3Hp8wemk',85),(SM+'variações de remada','cFX2mKBeE50',21)],
 'RD': [('Barra reta','yopIHJ-jr3w',57),('Barra W','017j7Gbxipo',54),('Polia baixa','2eeOSoAJdD4',50),(SM+'4 variações de rosca','MmuCimOgUrk',11)],
 'RM': [('Halteres','UZCzZJ0_2jg',43),('Polia com corda','GVMsv9kiRVo',11),('Banco Scott','xDaBywsDams',51),(SM+'4 variações de rosca','MmuCimOgUrk',11)],
 'AG': [(SM+'agachamento','WbjUXlFsTM0',27),('Barra livre','WLw3eRGkM5U',77),('Smith','mhu6HkDYvlw',68),('Hack','fr9DVLm6-3A',83)],
 'LP': [('Leg press 45°','eg2R_x8uMxQ',56),('Hack','fr9DVLm6-3A',83),('Afundo com halteres (sem máquina)','6Zz_RG0EHFE',65)],
 'MF': [('Mesa flexora','LuoeM8mY6UU',45),('Flexora em pé','AqALAGcDvcI',15),('Stiff com halteres (sem máquina)','XlGjQYUN4RQ',58)],
 'CE': [('Cadeira extensora','lmK4wsg8GAM',58),('Caneleira','YzKurnaoxW0',15),('Caneleira, uma perna','jBeEbcE7uG0',15)],
 'ST': [('Halteres','XlGjQYUN4RQ',58)],
 'AF': [('Halteres','6Zz_RG0EHFE',65)],
 'PT': [('Máquina em pé','opT3f__p12U',15),('No leg press','aPhesY3Z0RI',61),('Máquina sentado','Bx6elAOgxMI',58),('Degrau (sem máquina)','cklp_Xh5V8M',14)],
 'EP': [('No solo','BWmflYDhajM',59),('Banco com barra','0_PXXzmK0Yc',33)],
 'DE': [('Halteres','Nu1lKrS-Vvw',61),('Barra','o2LfBH1I8r8',50),('Máquina','xxr4_cPZfF0',40),(SM+'ombro com halteres','6Nczm3cBTV0',23)],
 'EL': [(SM+'elevação lateral na polia','rCvZu_py04w',24),('Halteres','qDAoUOmdbi4',58),('Polia (as duas mãos)','kiGnl8yRwTw',69),('Polia (uma mão)','lKY3r_a5XcQ',75)],
 'EF': [('Halteres','jhxLYSm_P-k',56),('Anilha','i0wc7uppDfw',49),('Polia','PEaXaQpmEpE',124),(SM+'3 exercícios de ombro','Sr6YMhPM7YI',17)],
 'PR': [('Prancha no solo','39v8Wz4CYuI',100),('Erros comuns','XDy7ACqq2KI',214)],
 'AI': [('No solo','MD4u2PANvmM',15),('Reverso no banco ou solo','8yUEzqy10F4',14),('Nas paralelas','2k4gSkfjnGE',9),(SM+'4 exercícios de abdômen','DOZeCJrnKiw',13)],
 'PL': [('Prancha lateral','Yc_p9WHjRI0',18),('Joelho apoiado (mais fácil)','Yf3Qv35jDDY',11),('Outra demonstração','BBjQgvzMZO8',33)],
 'BI': [('No solo','apmprS8H1MY',13),('Outra demonstração','o4gmaMTeQ2M',16)],
 'LS': [('Superman no solo','9LsIwRS8nwQ',15),('Versão iniciante','_kY519rZBR4',10),('Banco romano','hfFVbXJ5UvQ',51),(SM+'hiperextensão no banco','eDWc7jxLWhk',19)],
}

# chave: (nome, tipo, dica). tipo: comp = multiarticular, iso = isolado, core, coreT = core por tempo
X = {
 'SR': ('Supino reto','comp','Escápulas encaixadas e pés firmes no chão. Desça a barra até o meio do peito, controlando a descida.'),
 'SI': ('Supino inclinado','comp','Banco entre 30° e 45°. Cotovelos levemente abaixo da linha dos ombros.'),
 'CR': ('Crucifixo','iso','Cotovelos levemente flexionados. Aperte o peito no final do movimento.'),
 'TP': ('Tríceps pulley','iso','Cotovelos colados ao corpo; só o antebraço se mexe.'),
 'TF': ('Tríceps francês','iso','Cotovelos apontando para cima, sem abrir para os lados.'),
 'TT': ('Tríceps testa','iso','Desça a barra em direção à testa sem mexer os cotovelos.'),
 'PF': ('Puxada frontal','comp','Puxe a barra até o alto do peito, levando os cotovelos para baixo e para trás.'),
 'RC': ('Remada curvada','comp','Coluna neutra e tronco inclinado. Puxe a barra em direção ao umbigo.'),
 'RB': ('Remada baixa','comp','Peito aberto. Não balance o tronco para puxar.'),
 'RU': ('Remada unilateral','iso','Cada lado. Costas retas, puxe o cotovelo em direção ao quadril.'),
 'RD': ('Rosca direta','iso','Cotovelos parados ao lado do corpo. Desça devagar.'),
 'RM': ('Rosca martelo','iso','Pegada neutra, com as palmas viradas uma para a outra.'),
 'AG': ('Agachamento','comp','Joelhos acompanham a ponta dos pés. Desça mantendo a coluna neutra.'),
 'LP': ('Leg press','comp','Lombar apoiada no banco o tempo todo. Não trave os joelhos em cima.'),
 'MF': ('Mesa flexora','iso','Quadril colado no banco.'),
 'CE': ('Cadeira extensora','iso','Segure 1 segundo no alto.'),
 'ST': ('Stiff','comp','Joelhos levemente flexionados; desça o tronco com a coluna reta, sentindo atrás da coxa.'),
 'AF': ('Afundo','comp','Cada perna. Tronco reto, o joelho de trás desce em direção ao chão.'),
 'PT': ('Panturrilha','iso','Amplitude completa: desça bem o calcanhar e suba até a ponta dos pés.'),
 'EP': ('Elevação pélvica','iso','Suba o quadril contraindo os glúteos e segure 1 segundo em cima.'),
 'DE': ('Desenvolvimento','comp','Não arqueie a lombar. Suba até quase encostar um halter no outro.'),
 'EL': ('Elevação lateral','iso','Suba até a altura dos ombros, com os cotovelos levemente flexionados.'),
 'EF': ('Elevação frontal','iso','Suba até a linha dos ombros, sem balançar o tronco.'),
 'PR': ('Prancha','coreT','Corpo em linha reta, abdômen e glúteos contraídos. Não deixe o quadril cair.'),
 'AI': ('Abdominal infra','core','Suba o quadril com o abdômen, sem dar impulso com as pernas.'),
 'PL': ('Prancha lateral','coreT','Cada lado. Quadril alto, corpo em linha reta.'),
 'BI': ('Abdominal bicicleta','core','Cada lado. Leve o cotovelo em direção ao joelho oposto, sem puxar o pescoço.'),
 'LS': ('Lombar (superman)','core','Deitado de barriga para baixo, eleve braços e pernas juntos, sem dar tranco.'),
}

# como cada objetivo prescreve cada tipo de exercício: (séries, repetições, descanso em s)
GOALS = {
 'emagrecer': {
   'nome': 'Emagrecer',
   'comp': (3,'12–15',60), 'iso': (3,'15',45), 'core': (3,'15–20',30), 'coreT': (3,'30–45 s',30),
   'cardio': ('30–40 min', 'Caminhada rápida, bike ou elíptico, logo depois da musculação. Ritmo em que dá para falar frases curtas.'),
   'tips': ['Descanso curto (30 a 60 s) mantém o coração acelerado e gasta mais energia.',
            'Use cargas que permitam completar as repetições com boa técnica; a última repetição deve ser difícil.',
            'Cardio todos os dias de treino, depois da musculação. Aumente 5 min a cada 2 semanas até 40 min.',
            'Quem emagrece é a dieta: o treino preserva os músculos enquanto você perde gordura.',
            'Durma 7 a 8 horas e beba bastante água.'],
 },
 'massa': {
   'nome': 'Massa magra',
   'comp': (4,'8–12',90), 'iso': (3,'10–12',60), 'core': (3,'12–15',45), 'coreT': (3,'30–60 s',45),
   'cardio': ('15–20 min', 'Leve a moderado, depois da musculação: ajuda a manter a gordura baixa sem atrapalhar o ganho de músculo.'),
   'tips': ['Objetivo: ganhar músculo sem ganhar muita gordura (recomposição corporal).',
            'Quando fizer o máximo de repetições em todas as séries, aumente a carga.',
            'Coma proteína em todas as refeições (cerca de 1,6 a 2 g por kg de peso por dia).',
            'Cardio leve e curto, só para saúde e controle de gordura.',
            'Durma 7 a 8 horas: o músculo cresce no descanso.'],
 },
 'hipertrofia': {
   'nome': 'Hipertrofia',
   'comp': (4,'6–10',120), 'iso': (4,'8–12',75), 'core': (3,'12–15',60), 'coreT': (3,'45–60 s',60),
   'cardio': None,
   'tips': ['Foco em força e volume: cargas pesadas nos exercícios principais, descanso de 2 min.',
            'Progressão: tente subir carga ou repetições toda semana, sem perder a técnica.',
            'Termine as séries perto da falha (sobrando 1 a 2 repetições).',
            'Coma um pouco acima do que gasta, com bastante proteína; sem isso o músculo não cresce.',
            'Cardio opcional: 10 a 15 min leves, 2 a 3 vezes por semana, para a saúde do coração.'],
 },
}

# divisões: id, nome, resumo, nível, lista de (rótulo, foco, dias da semana, [exercícios])
SPLITS = [
 ('fullbody', 'Full body', 'Corpo todo em cada treino, alternando A e B. Ótimo para começar ou para quem tem pouco tempo.', 'Iniciante', [
   ('Treino A','Corpo todo',[1,5],['AG','SR','PF','DE','RD','TP','PR']),
   ('Treino B','Corpo todo',[3],['LP','SI','RB','EL','MF','PT','AI'])]),
 ('ab', 'AB · Superior e inferior', 'Parte de cima num dia, pernas no outro. 4 treinos por semana.', 'Iniciante a intermediário', [
   ('Treino A','Superior',[1,4],['SR','PF','SI','RB','DE','EL','RD','TP']),
   ('Treino B','Inferior',[2,5],['AG','LP','MF','CE','EP','PT','PR'])]),
 ('abc', 'ABC', 'Peito e tríceps, costas e bíceps, pernas e ombros. Repete a sequência na semana.', 'Intermediário', [
   ('Treino A','Peito + Tríceps',[1,4],['SR','SI','CR','TP','TF','AI']),
   ('Treino B','Costas + Bíceps',[2,5],['PF','RC','RB','RD','RM','LS']),
   ('Treino C','Pernas + Ombros',[3,6],['AG','LP','MF','CE','DE','EL','PT'])]),
 ('abcd', 'ABCD', 'Um grupo grande por dia, com ombros e abdômen separados. 4 treinos por semana.', 'Intermediário', [
   ('Treino A','Peito + Tríceps',[1],['SR','SI','CR','TP','TF']),
   ('Treino B','Costas + Bíceps',[2],['PF','RC','RU','RD','RM']),
   ('Treino C','Pernas',[4],['AG','LP','MF','CE','ST','PT']),
   ('Treino D','Ombros + Abdômen',[5],['DE','EL','EF','PR','AI','PL'])]),
 ('abcde', 'ABCDE', 'Um grupo muscular por dia, de segunda a sexta. Mais volume por músculo.', 'Intermediário a avançado', [
   ('Treino A','Peito',[1],['SR','SI','CR','PR']),
   ('Treino B','Costas',[2],['PF','RC','RB','RU','LS']),
   ('Treino C','Pernas',[3],['AG','LP','CE','MF','ST','PT']),
   ('Treino D','Ombros',[4],['DE','EL','EF','AI','PL']),
   ('Treino E','Braços',[5],['RD','RM','TP','TF','TT','BI'])]),
 ('ppl', 'Push · Pull · Legs', 'Empurrar, puxar e pernas, duas vezes por semana cada. 6 treinos por semana.', 'Avançado', [
   ('Push','Peito, ombros e tríceps',[1,4],['SR','SI','DE','EL','TP','TF']),
   ('Pull','Costas e bíceps',[2,5],['PF','RC','RB','RU','RD','RM']),
   ('Legs','Pernas e abdômen',[3,6],['AG','LP','MF','CE','EP','PT','PR'])]),
]

def exercise(key, goal, eid):
    name, kind, notes = X[key]
    sets, reps, rest = GOALS[goal][kind]
    vids = [{'label': l, 'url': Y + v, 'dur': d} for l, v, d in V[key]]
    return {'id': eid, 'name': name, 'sets': sets, 'reps': reps, 'rest': rest, 'load': '', 'notes': notes,
            'video': vids[0]['url'], 'videos': vids}

def badge(label):
    p = label.split()
    return (p[-1] if len(p) > 1 and len(p[-1]) <= 2 else label[:2]).upper()

templates = []
for sid, sname, sdesc, level, days in SPLITS:
    for gid, g in GOALS.items():
        pdays = []
        for di, (label, focus, wds, keys) in enumerate(days):
            dkey = f'{sid}-{gid}-{di}'
            exs = [exercise(k, gid, f'{dkey}-{i+1}') for i, k in enumerate(keys)]
            if g['cardio']:
                reps, note = g['cardio']
                exs.append({'id': f'{dkey}-c', 'name': 'Cardio', 'sets': 1, 'reps': reps, 'rest': 0, 'load': '', 'notes': note, 'video': ''})
            pdays.append({'id': f'd{di}', 'label': label, 'badge': badge(label), 'focus': focus, 'weekdays': wds, 'exercises': exs})
        per_week = sum(len(d[2]) for d in days)
        templates.append({
            'id': f'{sid}-{gid}', 'split': sname, 'goal': gid, 'goalName': g['nome'], 'level': level,
            'perWeek': per_week, 'desc': sdesc,
            'plan': {'name': f'{sname} · {g["nome"]}', 'days': pdays,
                     'guide': {'basics': [['Objetivo', g['nome']], ['Divisão', sname], ['Treinos por semana', str(per_week)], ['Nível', level]],
                               'tips': g['tips']}},
        })

out = os.path.join(os.path.dirname(__file__), '..', 'templates.json')
json.dump({'version': 1, 'goals': {k: v['nome'] for k, v in GOALS.items()}, 'templates': templates},
          open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(templates), 'modelos;', os.path.getsize(out) // 1024, 'KB')
