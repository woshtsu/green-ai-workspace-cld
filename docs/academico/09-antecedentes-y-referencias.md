# Antecedentes y referencias (ISO 690-2, sistema numérico)

Fuente: los 9 artículos de `guias/articulos/`. Fichas elaboradas por Antigravity CLI (encargo 04, Claude
Sonnet 4.6, solo lectura); Claude verificó en el texto las cifras de Khan (87,48 %), Verdecchia (13–115 %) y
Sharma (45 %/71 %). **Error del informe entregado:** citó a Khan et al. con «precisión ≈ 87,48 % (RMSE ≈ 12,5 %)».
El 87,48 % es la **mejora del algoritmo de clustering TSSAP sobre AP** al estimar estados energéticos, no la
precisión de la predicción de carga. El RMSE de 12,5 % no aparece en el texto convertido.

## 1. Fichas resumidas (cifras con su origen en el artículo)
| # | Referencia corta | Tipo | Datos | Método | Resultado citado (origen) | Uso |
|---|---|---|---|---|---|---|
| A1 | Khan et al., 2022 (FGCS) | Revista, revisada por pares | Bitbrains fastStorage (1 250 VM, 30 d, 5 min) y Rnd (500 VM, 90 d) | LR, Ridge, ARD, Elastic Net, **GRU**; clustering TSSAP | GRU con el menor RMSE en todas las variables; TSSAP supera a AP en 87,48 % (§8.2) | **Antecedente ML** de predicción de carga |
| A2 | Ji et al., 2021 (SUSCOM) | Revista | Trazas reales (nombre no consta) | **MM-GRU** multivariable y multipaso + scheduling + refrigeración | Mejora de la utilización y el consumo (cifra exacta no consta en la conversión) | **Antecedente ML** clave (predicción → decisión) |
| A3 | Sharma y Garg, 2020 (SUSCOM) | Revista | CloudSim; ~18 M instancias generadas con GA | ANN de dos niveles (AGEN) | Consumo −45 % (carga pesada) / −71 % (ligera); makespan −59/−64 % (resumen) | **Antecedente ML** (simulación) |
| A4 | Malekloo et al., 2018 (SUSCOM) | Revista | CloudSim (sintético) | ACO multiobjetivo (MACO) | Superior a FFD, DVFS y otros (cifras propias no extraídas) | Antecedente de energía y SLA |
| A5 | Ali, 2026 (Discover AI) | Revista | Revisión de 40 publicaciones + simulación | DVFS, consolidación, SDN + IA | Hasta −50 % de energía con < 9 % de degradación (resumen; simulado) | Antecedente de energía |
| A6 | Verdecchia et al., 2023 (WIREs) | **Revisión sistemática** | 98 estudios (2015–2022) | SLR (Kitchenham) | Ahorros reportados del 13 % al 115 %; el 76 % se publicó desde 2020 | **Marco Green AI** |
| A7 | Bolón-Canedo et al., 2024 (Neurocomputing) | Revisión | — | Narrativa: *green-in* y *green-by* AI | Entrenar GPT-3 ≈ 1 287 MWh; las herramientas de carbono subestiman (§4) | Marco Green AI |
| A8 | d'Orgeval et al., 2026 (Applied Energy) | Revista | Ecoinvent, PEP/PCF | LCA (ISO 14040/44) de IA generativa | Hasta −60 % de huella con renovables y equipo reacondicionado (citado, §1.3) | Marco (costo de la IA) |
| A9 | Cruzes, 2025 (TechRxiv) | **Preprint, NO revisado** | — | Encuesta tutorial | PUE de ~2,0 (2010) a ~1,55; hyperscale ≈ 1,1 | Solo contexto; citar con cautela |
Fuera de la carpeta (citadas en el trabajo previo; **verificar antes de usar**): Ullah, Bilal y Yoon 2023
(Computer Networks, BiLSTM); Awad, Leivadeas y Awad 2023 (Computer Networks); Rao y Li 2025 (J. Grid
Computing); Morales Romero 2024 (tesis UTP, nacional); Arellanos-Tafur et al. 2025 (LACCEI); IEA 2025; ISO/IEC
21031:2024.

## 2. Cumplimiento de lo exigido
- Lista de cotejo U3 (ind. 3): **3 antecedentes de integración con ML** de fuentes válidas → **A1, A2, A3**
  (Elsevier/ScienceDirect).
- `informeFinal.md`: «2 en español y 1 en inglés». **No hay antecedentes en español en la carpeta.** Buscar dos
  en SciELO, ALICIA o el Repositorio UC (p. ej. tesis peruanas de eficiencia energética de data centers;
  Morales Romero 2024 es candidata).
- Lineamientos S2: 7 fuentes (internacional, nacional y local), Q1/Q2, de los últimos 5 años. A3 (2020) y A4
  (2018) superan los 5 años; preferir A1, A2, A5 y A6–A8.

## 3. Discusión propuesta (ind. 6: comparar los resultados de cada PMV con los antecedentes)
| Aspecto | Green AI | A1 Khan 2022 | A2 Ji 2021 | A3 Sharma 2020 | Lectura honesta |
|---|---|---|---|---|---|
| Datos | Telemetría **simulada**, 5 min | Trazas reales Bitbrains, 5 min | Trazas reales | Simulación CloudSim | Misma cadencia que A1; A1 y A2 usan datos reales y nosotros no |
| Modelo | RF y XGBoost (árboles) frente a baselines | GRU (recurrente) | MM-GRU | ANN | Usamos modelos de menor costo computacional (*green-in AI*, A6/A7). Las RNN son trabajo futuro |
| Resultado de predicción | MAE 3,22 pp a 15 min (−30 % frente a persistencia) | GRU con el menor RMSE frente a modelos lineales | Mejora frente a otras técnicas | — | Coincide en la tendencia (el ML supera a los baselines), **no en magnitud**: datos y métricas distintos |
| Energía | Solo estimación (∫P dt); sin ahorro reclamado | Habilita la consolidación (E-states) | Optimización conjunta con refrigeración | −45 %/−71 % en simulación | Los ahorros de A3–A5 son simulados. A6 muestra el rango 13–115 %: Green AI no debe prometer cifras sin medir |
| Decisión | Solo recomendación con política explicable | Consolidación automática | Scheduling y migración | Scheduler | Diferencia de diseño: supervisión humana por restricciones institucionales |
**PMV1** (observabilidad) frente a A1/A2: mismas variables de entrada (CPU y memoria a 5 min); nuestra serie es
simulada.

## 4. Referencias (formato ISO 690 numérico; confirmar con la guía de estilo de la biblioteca UC)
[1] KHAN, T., TIAN, W., ILAGER, S. y BUYYA, R. Workload forecasting and energy state estimation in cloud data
centres: ML-centric approach. *Future Generation Computer Systems*. 2022, vol. 128, pp. 320–332. ISSN 0167-739X.
DOI 10.1016/j.future.2021.10.019.

[2] JI, K., ZHANG, F., CHI, C., SONG, P., ZHOU, B., MARAHATTA, A. y LIU, Z. A joint energy efficiency
optimization scheme in data centers. *Sustainable Computing: Informatics and Systems*. 2021, vol. 32,
art. 100596. DOI 10.1016/j.suscom.2021.100596.

[3] SHARMA, M. y GARG, R. AGEN: ANN based energy-efficient scheduler for cloud data centers. *Sustainable
Computing: Informatics and Systems*. 2020, vol. 26, art. 100373. DOI 10.1016/j.suscom.2020.100373.

[4] MALEKLOO, M.-H., KARA, N. y EL BARACHI, M. An energy efficient and SLA compliant approach for resource
allocation and consolidation in cloud computing environments. *Sustainable Computing: Informatics and
Systems*. 2018, vol. 17, pp. 9–24. DOI 10.1016/j.suscom.2018.02.001.

[5] ALI, Q. I. Intelligent energy governance in solar-powered data centers: a multi-stage framework for
sustainable operation and AI-driven optimization. *Discover Artificial Intelligence*. 2026, vol. 6, art. 124.
DOI 10.1007/s44163-025-00823-7.

[6] VERDECCHIA, R., SALLOU, J. y CRUZ, L. A systematic review of Green AI. *WIREs Data Mining and Knowledge
Discovery*. 2023, vol. 13, art. e1507. DOI 10.1002/widm.1507.

[7] BOLÓN-CANEDO, V., MORÁN-FERNÁNDEZ, L., CANCELA, B. y ALONSO-BETANZOS, A. A review on green artificial
intelligence. *Neurocomputing*. 2024, vol. 599, art. 128096. DOI 10.1016/j.neucom.2024.128096.

[8] D'ORGEVAL, A., SHEEHAN, S., AVENAS, Q., ASSOUMOU, E. y SESSA, V. Life cycle assessment of artificial
intelligence in data centers: comparative study of generative AI models, cloud architectures, and mitigation
strategies. *Applied Energy*. 2026, vol. 406, art. 127288. DOI 10.1016/j.apenergy.2025.127288.

[9] CRUZES, S. Data centers in the age of AI: a tutorial survey on infrastructure, sustainability, and emerging
challenges [preprint]. *TechRxiv*. 2025. DOI 10.36227/techrxiv.176158592.23065552/v1.

[10] INTERNATIONAL ENERGY AGENCY. *Energy and AI* [en línea]. París: IEA, 2025 [consulta: fecha de acceso].
Disponible en: URL oficial (completar).

[11] ISO/IEC. *ISO/IEC 21031:2024 Information technology — Software Carbon Intensity (SCI) specification*.
Ginebra: ISO, 2024.
Pendiente: nombres completos de los autores si la guía UC los exige, el número (issue) de cada revista y las
fechas de consulta de las fuentes en línea.
