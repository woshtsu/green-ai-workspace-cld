from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta

import os
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'evidencias')) + os.sep
F = 'C:/Windows/Fonts/'


def font(n, s):
    return ImageFont.truetype(F + n, s)


fr, fb = font('arial.ttf', 15), font('arialbd.ttf', 15)
fs, fsb = font('arial.ttf', 12), font('arialbd.ttf', 12)
f9 = font('arial.ttf', 9)
ft = font('arialbd.ttf', 26)
fsub = font('arial.ttf', 15)


def d(s):
    return date(2026, int(s[3:5]), int(s[0:2]))


COL = {'PMV1': ('#2563EB', '#DBEAFE'), 'PMV2': ('#059669', '#D1FAE5'), 'PMV3': ('#EA580C', '#FFEDD5')}
R = []


def pmv(k, t):
    R.append(('pmv', k, t))


def spr(k, t):
    R.append(('spr', k, t))


def act(k, i, t, r, a, b, cierre=False):
    R.append(('act', k, i, t, r, a, b, cierre))


pmv('PMV1', 'PMV1 — Viabilidad técnica y pipeline de datos (Semanas 1–6)')
spr('PMV1', 'Sprint 1: 25 Ago – 05 Sep 2026')
act('PMV1', '1.1', 'Project Charter aprobado', 'J', '25/08', '28/08')
act('PMV1', '1.2', 'Arquitectura de alto nivel definida', 'R', '25/08', '28/08')
act('PMV1', '1.3', 'Cluster Kubernetes desplegado (minikube/k3s/kind)', 'L', '31/08', '04/09')
act('PMV1', '1.4', 'EDT/WBS definida y backlog priorizado', 'T', '31/08', '05/09')
spr('PMV1', 'Sprint 2: 08 Sep – 19 Sep 2026')
act('PMV1', '2.1', 'Prometheus + Node Exporter + cAdvisor configurados', 'L', '08/09', '11/09')
act('PMV1', '2.2', 'Grafana conectado con dashboard básico', 'R', '08/09', '11/09')
act('PMV1', '2.3', 'Workloads sintéticos diseñados (baja/media/alta/pico)', 'G', '14/09', '18/09')
act('PMV1', '2.4', 'Prueba de Concepto (PoC) predictiva ejecutada', 'G', '14/09', '19/09')
spr('PMV1', 'Sprint 3: 22 Sep – 03 Oct 2026')
act('PMV1', '3.1', 'Pipeline ETL operativo (extracción → limpieza → carga)', 'R', '22/09', '25/09')
act('PMV1', '3.2', 'Dataset versionado (≥ 2 semanas de observación)', 'R', '22/09', '29/09')
act('PMV1', '3.3', 'Modelo baseline (media móvil / ARIMA) entrenado', 'G', '28/09', '01/10')
act('PMV1', '3.4', 'MAE y RMSE del baseline registrados en MLflow', 'G', '01/10', '02/10')
act('PMV1', '3.5', 'CIERRE PMV1: Sprint Review + Retrospectiva', 'T', '03/10', '03/10', True)
pmv('PMV2', 'PMV2 — Solución predictiva y motor de recomendaciones (Semanas 7–12)')
spr('PMV2', 'Sprint 4: 06 Oct – 17 Oct 2026')
act('PMV2', '4.1', 'Análisis exploratorio de datos (EDA) completado', 'G', '06/10', '09/10')
act('PMV2', '4.2', 'Random Forest Regressor entrenado y comparado', 'G', '06/10', '13/10')
act('PMV2', '4.3', 'XGBoost Regressor entrenado y comparado', 'G', '13/10', '16/10')
act('PMV2', '4.4', 'Métricas de modelos comparadas en MLflow', 'G', '16/10', '17/10')
spr('PMV2', 'Sprint 5: 20 Oct – 31 Oct 2026')
act('PMV2', '5.1', 'Modelo predictivo seleccionado (precisión ≥ 90 %)', 'G', '20/10', '23/10')
act('PMV2', '5.2', 'Motor de recomendaciones con Policy Engine operativo', 'R', '20/10', '27/10')
act('PMV2', '5.3', 'API de predicción FastAPI con latencia < 2 s', 'R', '27/10', '30/10')
act('PMV2', '5.4', 'Módulo de aprobación humana (Recommendation-Only)', 'R', '30/10', '31/10')
spr('PMV2', 'Sprint 6: 03 Nov – 14 Nov 2026')
act('PMV2', '6.1', 'Dashboard Grafana con predicciones en tiempo real', 'R', '03/11', '06/11')
act('PMV2', '6.2', 'Paneles de eficiencia energética (kWh, Wh/request)', 'G', '03/11', '07/11')
act('PMV2', '6.3', 'Sistema de alertas de anomalías y riesgo SLA', 'R', '09/11', '12/11')
act('PMV2', '6.4', 'CO2e: diseño preliminar (implementación = trabajo futuro)', 'G', '12/11', '13/11')
act('PMV2', '6.5', 'CIERRE PMV2: Sprint Review + Retrospectiva', 'T', '14/11', '14/11', True)
pmv('PMV3', 'PMV3 — Proceso de software, calidad y documento final (Semanas 13–14)')
spr('PMV3', 'Sprint 7: 17 Nov – 23 Nov 2026')
act('PMV3', '7.1', 'Proceso de desarrollo documentado (flujo Git test→main, PR)', 'R', '17/11', '19/11')
act('PMV3', '7.2', 'Proceso de calidad: Ola 2 del plan FURPS+/OWASP', 'G', '17/11', '21/11')
act('PMV3', '7.3', 'Proceso de CI/CD documentado (GitHub Actions + Render)', 'L/R', '18/11', '21/11')
act('PMV3', '7.4', 'Gestión del proceso en Trello (PMVn-HUxx, dailies, DoD)', 'J', '17/11', '20/11')
act('PMV3', '7.5', 'CIERRE SPRINT 7: Sprint Review + Retrospectiva', 'T', '23/11', '23/11', True)
spr('PMV3', 'Sprint 8: 24 Nov – 30 Nov 2026')
act('PMV3', '8.1', 'Ola 3 de calidad y re-medición FURPS+/OWASP', 'G', '24/11', '27/11')
act('PMV3', '8.2', 'Métricas del proceso (DoD, HU por sprint, hallazgos)', 'J', '24/11', '26/11')
act('PMV3', '8.3', 'Documento final: guía de uso y manual de instalación', 'R/L', '25/11', '28/11')
act('PMV3', '8.4', 'Video de sustentación según lista de cotejo', 'T', '27/11', '29/11')
act('PMV3', '8.5', 'CIERRE PMV3: Sprint Review + Retrospectiva + Sustentación', 'T', '30/11', '30/11', True)

START = date(2026, 8, 25)
END = date(2026, 11, 30)
NW = 14


def status(r):
    k, i = r[1], r[2]
    if i == '6.5' or k == 'PMV3':
        return 'Planificado'
    if i.startswith('6.'):
        return 'En ejecución'
    return 'Completado'


def render(path, executed):
    rowh = 22
    top = 176
    cw = [40, 470, 48, 86, 86] + ([100] if executed else [])
    tw = sum(cw)
    W = tw + NW * 70 + 20
    H = top + len(R) * rowh + 70
    im = Image.new('RGB', (W, H), 'white')
    g = ImageDraw.Draw(im)
    g.rectangle((0, 0, W, 70), fill='#0B2545')
    g.text((20, 12), 'Green AI — Sistema Predictivo para Gestión Energética de Workloads Universitarios', font=ft, fill='white')
    if executed:
        sub = 'Diagrama Gantt de ejecución y seguimiento (corte 11/11/2026; lo posterior se muestra como planificado)'
    else:
        sub = 'Diagrama Gantt planificado del proyecto (calendario lectivo 25/08/2026 – 30/11/2026)'
    g.text((20, 44), sub, font=fsub, fill='#CBD5E1')
    g.text((20, 82), 'Responsables: J = Jhonny (PO)   G = Gina (SM-ML)   R = Ricardo (Dev)   L = Leonid (Infra)   T = Todo el equipo', font=fs, fill='#334155')
    if executed:
        g.rectangle((20, 108, 40, 120), fill='#2563EB')
        g.text((46, 106), 'Completado', font=fs, fill='#334155')
        g.rectangle((140, 108, 160, 120), fill='#F59E0B')
        g.text((166, 106), 'En ejecución', font=fs, fill='#334155')
        g.rectangle((270, 108, 290, 120), outline='#64748B', fill='white')
        g.text((296, 106), 'Planificado (posterior al 11/11/2026)', font=fs, fill='#334155')
    x0 = tw + 10
    g.rectangle((0, top - 40, W, top), fill='#1E3A5F')
    hs = ['ID', 'Actividad / Entregable', 'Resp.', 'Inicio', 'Fin'] + (['Estado'] if executed else [])
    x = 0
    for h, w in zip(hs, cw):
        g.text((x + 6, top - 28), h, font=fb, fill='white')
        x += w
    months = {}
    for wk in range(NW):
        ws = START + timedelta(days=7 * wk)
        months.setdefault(ws.strftime('%m'), []).append(wk)
    mn = {'08': 'Ago 2026', '09': 'Sep 2026', '10': 'Oct 2026', '11': 'Nov 2026'}
    for m, wks in months.items():
        g.text((x0 + wks[0] * 70 + 4, top - 40), mn[m], font=fsb, fill='#E2E8F0')
    for wk in range(NW):
        ws = START + timedelta(days=7 * wk)
        we = min(ws + timedelta(days=6), END)
        xx = x0 + wk * 70
        g.line((xx, top - 40, xx, H - 50), fill='#CBD5E1')
        g.text((xx + 4, top - 24), 'Sem %d' % (wk + 1), font=fsb, fill='white')
        g.text((xx + 4, top - 11), '%s-%s' % (ws.strftime('%d/%m'), we.strftime('%d/%m')), font=f9, fill='#CBD5E1')
    g.line((x0 + NW * 70, top - 40, x0 + NW * 70, H - 50), fill='#CBD5E1')

    def px(dt):
        return x0 + (dt - START).days * 10

    y = top
    for r in R:
        if r[0] == 'pmv':
            g.rectangle((0, y, W, y + rowh), fill=COL[r[1]][0])
            g.text((8, y + 3), r[2], font=fb, fill='white')
        elif r[0] == 'spr':
            g.rectangle((0, y, W, y + rowh), fill=COL[r[1]][1])
            g.text((8, y + 3), r[2], font=fb, fill='#0F172A')
        else:
            _, k, i, t, rs, a, b, cl = r
            g.line((0, y + rowh, W, y + rowh), fill='#E2E8F0')
            g.text((8, y + 4), i, font=fr, fill='#334155')
            g.text((cw[0] + 4, y + 4), t, font=fb if cl else fr, fill='#0F172A')
            xx = cw[0] + cw[1]
            for v, w in zip([rs, a + '/2026', b + '/2026'], cw[2:5]):
                g.text((xx + 8, y + 4), v, font=fr, fill='#334155')
                xx += w
            st = status(r)
            if executed:
                colr = {'Completado': '#15803D', 'En ejecución': '#B45309', 'Planificado': '#64748B'}[st]
                g.text((xx + 6, y + 4), st, font=fs, fill=colr)
            xa = px(d(a))
            xb = px(d(b)) + 10
            if cl:
                cx = px(d(b)) + 5
                cy = y + rowh // 2
                dc = '#2563EB' if (not executed or st == 'Completado') else '#64748B'
                g.polygon([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)], fill=dc)
            elif not executed:
                g.rectangle((xa, y + 4, xb, y + rowh - 4), fill=COL[k][0])
            elif st == 'Completado':
                g.rectangle((xa, y + 4, xb, y + rowh - 4), fill='#2563EB')
            elif st == 'En ejecución':
                g.rectangle((xa, y + 4, xb, y + rowh - 4), fill='#F59E0B')
            else:
                g.rectangle((xa, y + 4, xb, y + rowh - 4), fill='white', outline='#64748B', width=2)
        y += rowh
    if executed:
        hx = px(date(2026, 11, 11)) + 5
        g.line((hx, top, hx, y), fill='#DC2626', width=2)
        g.text((hx - 62, y + 4), 'Corte: 11/11/2026', font=fsb, fill='#DC2626')
    g.rectangle((0, H - 40, W, H), fill='#0B2545')
    g.text((20, H - 30), 'Universidad Continental | Proyecto Académico 2026 | PMV3 ajustado al cierre del periodo lectivo (30/11/2026): Sprint 7 (17–23/11) y Sprint 8 (24–30/11)', font=fs, fill='white')
    im.save(path)


render(OUT + 'gantt-planificado-2026-11.png', False)
render(OUT + 'gantt-ejecutado-2026-11.png', True)
