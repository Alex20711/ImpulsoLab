"""ImpulsoLab en la web: ejecutar con `streamlit run app.py`."""
from __future__ import annotations

import base64
import json
from pathlib import Path

import streamlit as st

from physicslab import PhysicsInputError, Scenario, SimulationInput, simulate
from physicslab.models import SimulationResult, StageResult
from physicslab.reporting import equations, fmt, physical_explanation, stage_summary
from physicslab.storage import get_storage
from physicslab.visualization import make_comparison_figure, make_motion_figure

st.set_page_config(page_title="ImpulsoLab | Física interactiva", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
  :root {color-scheme:dark}
  .stApp {background: radial-gradient(ellipse at 70% 0%, #142D44 0%, #081623 38%, #071320 100%); color: #EBF6FF;}
  [data-testid="stSidebar"] {background: #0D2132; border-right: 1px solid #2B475B;}
  .block-container {max-width: 1250px; padding-top: 1.3rem; padding-bottom: 4rem;}
  h1,h2,h3 {letter-spacing: -.035em; color: #EAF6FF !important;}
  h2 {font-weight: 760 !important;}
  [data-testid="stMetric"] {background: #10283A; border: 1px solid #2A4A5C; border-radius: 13px; padding: 18px 18px 12px;}
  [data-testid="stMetricLabel"] {color: #A8C3D3;}
  [data-testid="stMetricValue"] {color: #7EE5DE; font-weight: 750;}
  [data-testid="stForm"] {border-radius: 18px; border: 1px solid #345269; background: rgba(16, 37, 53, .64); padding: 1.45rem;}
  button[kind="primary"] {background: #20A99F !important; border-color: #64EBDF !important; color: #04272A !important; font-weight: 800 !important;}
  div[data-testid="stTabs"] button[aria-selected="true"] {color: #73E7DF !important;}
  .eyebrow {letter-spacing:.15em;font-size:.73rem;color:#82BEBE;font-weight:750;text-transform:uppercase}
  .impact-note {background:#102738;border-left:3px solid #F7B26B;border-radius:9px;padding:12px 16px;color:#CBDDE6;margin:.55rem 0 1.2rem}
  .foot-note {color:#8DAABD;font-size:.83rem;margin-top:1rem}
  [data-testid="stAlert"] {border-radius: 12px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def show_banner() -> None:
    path = Path(__file__).resolve().parent / "assets" / "banner.svg"
    src = base64.b64encode(path.read_bytes()).decode("ascii")
    st.markdown(f'<img alt="ImpulsoLab: ilustración educativa de arma, proyectil y blanco" style="display:block;width:100%;border-radius:17px;border:1px solid #345165;margin-bottom:1rem" src="data:image/svg+xml;base64,{src}" />', unsafe_allow_html=True)


def show_stage(stage: StageResult, key: str) -> None:
    st.subheader(stage.name)
    entries = []
    for b in stage.bodies:
        entries.append({
            "Cuerpo": b.name,
            "m (kg)": round(b.mass_kg, 7),
            "v inicial (m/s)": round(b.initial_velocity_m_s, 6),
            "v final (m/s)": round(b.final_velocity_m_s, 6),
            "p inicial (kg·m/s)": round(b.initial_momentum_kg_m_s, 6),
            "p final (kg·m/s)": round(b.final_momentum_kg_m_s, 6),
            "J (N·s)": round(b.impulse_n_s, 6),
            "Ec inicial (J)": round(b.initial_kinetic_energy_j, 6),
            "Ec final (J)": round(b.final_kinetic_energy_j, 6),
            "ΔEc (J)": round(b.kinetic_energy_change_j, 6),
            "F promedio (N)": None if b.average_force_n is None else round(b.average_force_n, 6),
        })
    st.dataframe(entries, hide_index=True, use_container_width=True, key=f"tbl_{key}")
    for text in stage_summary(stage):
        st.markdown("- " + text)
    with st.expander(f"¿Por qué sucede esto? · {stage.name}"):
        for paragraph in stage.interpretation:
            st.write(paragraph)


def show_result(result: SimulationResult, *, key: str) -> None:
    p = result.parameters
    st.markdown(f'<div class="eyebrow">Resultado calculado · {p.scenario.label}</div>', unsafe_allow_html=True)
    st.caption(f"Estudiante: {p.student_id}  ·  Fecha UTC: {result.created_at_utc}  ·  ID: {result.id[:8]}")
    a, b, c, d = st.columns(4)
    a.metric("Retroceso del arma", f"{fmt(result.launch.bodies[1].final_velocity_m_s)} m/s")
    b.metric("Impulso del proyectil", f"{fmt(result.impact.bodies[0].impulse_n_s)} N·s")
    c.metric("Momento total tras choque", f"{fmt(result.impact.final_total_momentum_kg_m_s)} kg·m/s")
    d.metric("Energía cinética transformada", f"{fmt(max(0, -result.impact.kinetic_energy_change_j))} J")

    st.markdown("### Visualización por etapas")
    st.caption("Usa Reproducir o la línea de etapas. No es una simulación temporal a escala: las flechas señalan sentido y muestran las velocidades reales calculadas.")
    st.plotly_chart(make_motion_figure(result), use_container_width=True, key=f"scene_{key}", config={"displaylogo": False, "scrollZoom": False})
    st.markdown("### Antes y después de la colisión")
    st.plotly_chart(make_comparison_figure(result), use_container_width=True, key=f"compare_{key}", config={"displaylogo": False})

    st.markdown("### Datos de entrada")
    values = [
        ("Masa del proyectil", f"{fmt(p.projectile_mass_kg)} kg"),
        ("Masa del arma", f"{fmt(p.firearm_mass_kg)} kg"),
        ("Velocidad del proyectil al salir del arma", f"{fmt(p.muzzle_speed_m_s)} m/s"),
        ("Masa del blanco", "Barrera fija" if p.target_mass_kg is None else f"{fmt(p.target_mass_kg)} kg"),
        ("Velocidad inicial del blanco", "No aplica" if p.target_mass_kg is None else f"{fmt(p.target_speed_m_s)} m/s"),
        ("Velocidad final introducida del proyectil", "No aplica" if p.projectile_exit_speed_m_s is None else f"{fmt(p.projectile_exit_speed_m_s)} m/s"),
        ("Coeficiente de restitución", ("1 (elástico)" if p.scenario == Scenario.ELASTIC else "No aplica") if p.restitution is None else fmt(p.restitution)),
        ("Duración del choque", "Desconocida" if p.contact_time_s is None else f"{fmt(p.contact_time_s)} s"),
    ]
    st.dataframe([{"Variable": a, "Valor": b} for a, b in values], hide_index=True, use_container_width=True, key=f"data_{key}")

    st.markdown("### Ecuaciones y cálculos")
    st.latex(r"p = m\,v \qquad J=\Delta p=m(v_f-v_i)")
    st.latex(r"E_c=\frac{1}{2}mv^2 \qquad F_{\mathrm{prom}}=\frac{J}{\Delta t}")
    st.latex(r"v_{\mathrm{arma}}=-\frac{m_b}{m_a}v_b")
    if p.scenario != Scenario.INDIVIDUAL:
        st.latex(r"m_bu_b+m_tu_t=m_bv_b+m_tv_t")
        st.latex(r"e=\frac{v_t-v_b}{u_b-u_t}")
        st.latex(r"v_b=\frac{(m_b-em_t)u_b+(1+e)m_tu_t}{m_b+m_t}")
        st.latex(r"v_t=\frac{(1+e)m_bu_b+(m_t-em_b)u_t}{m_b+m_t}")
    else:
        st.latex(r"J_{\mathrm{barrera}\rightarrow\mathrm{proyectil}}=m_b(v_f-v_i)")
    shot = result.launch.bodies[1]
    bullet = result.impact.bodies[0]
    st.code(
        f"Disparo: v_arma = -({fmt(p.projectile_mass_kg)} / {fmt(p.firearm_mass_kg)}) · {fmt(p.muzzle_speed_m_s)} = {fmt(shot.final_velocity_m_s)} m/s\n"
        f"Impacto: J_proyectil = {fmt(p.projectile_mass_kg)} · ({fmt(bullet.final_velocity_m_s)} - {fmt(bullet.initial_velocity_m_s)}) = {fmt(bullet.impulse_n_s)} N·s\n"
        f"Impacto: Ec_i = {fmt(result.impact.initial_total_kinetic_energy_j)} J  →  Ec_f = {fmt(result.impact.final_total_kinetic_energy_j)} J\n"
        f"ΔEc = {fmt(result.impact.kinetic_energy_change_j)} J\n"
        + ("F_prom = J/Δt: sin tiempo de contacto, no se calcula." if p.contact_time_s is None else
           f"F_prom, proyectil = {fmt(bullet.impulse_n_s)} / {fmt(p.contact_time_s)} = {fmt(bullet.average_force_n)} N"),
        language="text",
    )

    show_stage(result.launch, f"{key}_launch")
    show_stage(result.impact, f"{key}_impact")
    st.markdown("### Interpretación y leyes de conservación")
    for explanation in physical_explanation(result):
        st.markdown("- " + explanation)
    for warning in result.warnings:
        st.warning(warning)
    with st.expander("Supuestos físicos y límites del modelo", expanded=False):
        for assumption in result.assumptions:
            st.markdown("- " + assumption)

    st.download_button(
        "Descargar informe de datos (JSON)",
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2).encode("utf-8"),
        file_name=f"impulsolab_{result.id[:8]}.json", mime="application/json", key=f"down_{key}",
    )


show_banner()
with st.sidebar:
    st.markdown('<div class="eyebrow">CONFIGURACIÓN DE LABORATORIO</div>', unsafe_allow_html=True)
    st.write("**Identificación del estudiante**")
    student = st.text_input("Nombre o código", value="Estudiante demo", max_chars=60, label_visibility="collapsed", help="El historial se consulta por esta identificación. No es un sistema de autenticación.").strip()
    st.markdown("**Selecciona un escenario**")
    scenario = st.radio("Escenarios", list(Scenario), format_func=lambda x: x.label, label_visibility="collapsed")
    st.divider()
    st.info("Eje horizontal: **+** hacia la derecha, **−** hacia la izquierda. Las velocidades y magnitudes se expresan en el Sistema Internacional.")
    st.caption("Python + Streamlit + Plotly · Modelo educativo 1D")

try:
    store = get_storage(st.secrets)
    is_remote_storage = store.__class__.__name__ == "SupabaseHistory"
except Exception as error:
    st.error(f"No se pudo inicializar el historial: {error}")
    st.stop()

simulation_tab, history_tab, learning_tab = st.tabs(["🎯 Simulador", "🗂️ Historial", "📘 Fundamentos"])
with simulation_tab:
    st.markdown('<div class="eyebrow">01  /  DEFINIR PARÁMETROS</div>', unsafe_allow_html=True)
    st.markdown("## Configura el disparo y el impacto")
    st.markdown('<div class="impact-note">El disparo y el impacto se calculan como <b>dos etapas diferentes</b>. En choques entre dos cuerpos, el blanco puede moverse libremente; en el impacto individual, la barrera está anclada.</div>', unsafe_allow_html=True)
    with st.form("simulation_form", clear_on_submit=False):
        st.markdown("**Etapa A — Lanzamiento del proyectil y retroceso del arma**")
        c1, c2, c3 = st.columns(3)
        with c1:
            mb = st.number_input("Masa del proyectil (kg)", min_value=0.000001, max_value=1e8, value=0.02, format="%.6f", help="Masa positiva, en kilogramos")
        with c2:
            mg = st.number_input("Masa del arma (kg)", min_value=0.000001, max_value=1e8, value=2.0, format="%.4f")
        with c3:
            vb = st.number_input("Velocidad de salida (m/s)", min_value=0.000001, max_value=2999999., value=30.0, format="%.4f", help="Velocidad del proyectil respecto del suelo, no relativa al cañón")
        st.markdown("**Etapa B — Interacción con el blanco**")
        mt = None
        vt = 0.
        vf = None
        e = None
        if scenario == Scenario.INDIVIDUAL:
            st.caption("Barrera fija e impenetrable: indica si el proyectil se detiene (0) o rebota (valor negativo).")
            vf = st.number_input("Velocidad final del proyectil (m/s; ≤ 0)", max_value=0.0, value=0.0, format="%.4f")
        else:
            c4, c5 = st.columns(2)
            with c4:
                mt = st.number_input("Masa del blanco móvil (kg)", min_value=0.000001, max_value=1e8, value=0.4, format="%.6f")
            with c5:
                vt = st.number_input("Velocidad inicial del blanco (m/s)", min_value=-2999999., max_value=2999999., value=0.0, format="%.4f", help="Negativa si el blanco va hacia el proyectil")
            if scenario == Scenario.ELASTIC:
                st.caption("Choque elástico: e = 1. Las velocidades finales se calculan automáticamente; no se solicitan.")
            else:
                e = st.slider("Coeficiente de restitución e · 0 = unión de los cuerpos", 0.0, 0.99, value=0.35, step=0.01)
        known_time = st.checkbox("Conozco el tiempo de contacto del choque", value=True)
        dt = st.number_input("Duración del contacto Δt (s)", min_value=0.000000001, max_value=1e6, value=0.02, format="%.6f", disabled=not known_time)
        submit = st.form_submit_button("Calcular y guardar simulación", type="primary", use_container_width=True)
    if submit:
        try:
            params = SimulationInput(
                student_id=student, scenario=scenario, projectile_mass_kg=mb, firearm_mass_kg=mg,
                muzzle_speed_m_s=vb, target_mass_kg=mt, target_speed_m_s=vt,
                projectile_exit_speed_m_s=vf, restitution=e,
                contact_time_s=dt if known_time else None,
            )
            calculated = simulate(params)
            st.session_state["last_simulation"] = calculated
            try:
                store.save(calculated)
                st.success("Simulación calculada y registrada en el historial.")
            except (OSError, RuntimeError) as exc:
                st.error(f"El cálculo se completó, pero no pudo guardarse el historial: {exc}")
        except PhysicsInputError as exc:
            st.error(f"Parámetros inválidos: {exc}")
    result = st.session_state.get("last_simulation")
    if result is not None and result.parameters.student_id == student:
        st.divider()
        show_result(result, key="latest")
    elif not submit:
        st.info("Introduce los parámetros y pulsa **Calcular y guardar simulación** para mostrar los resultados y la animación.")

with history_tab:
    st.markdown("## Historial por estudiante")
    if not is_remote_storage:
        st.warning("Se está utilizando SQLite local. En Streamlit Community Cloud este almacenamiento puede desaparecer tras reinicios o despliegues. Para persistencia web configura Supabase (consulta el README).")
    st.caption("Consulta simulaciones guardadas usando la identificación escrita en la barra lateral. Esta identificación no es una contraseña.")
    if not student:
        st.info("Escribe una identificación válida en la barra lateral.")
    else:
        try:
            records = store.list_by_student(student, 100)
            if not records:
                st.info("Todavía no hay simulaciones registradas para esta identificación.")
            else:
                st.dataframe([
                    {"Fecha UTC": r.created_at_utc, "Escenario": r.parameters.scenario.label,
                     "Momento final total (kg·m/s)": round(r.impact.final_total_momentum_kg_m_s, 5),
                     "ΔEc (J)": round(r.impact.kinetic_energy_change_j, 5), "ID": r.id[:8]}
                    for r in records
                ], hide_index=True, use_container_width=True)
                selected_id = st.selectbox("Consultar una simulación anterior", options=[r.id for r in records],
                    format_func=lambda id_: next(f"{r.created_at_utc} · {r.parameters.scenario.label} · {r.id[:8]}" for r in records if r.id == id_))
                selected = next(r for r in records if r.id == selected_id)
                show_result(selected, key=f"history_{selected.id}")
        except (RuntimeError, OSError, ValueError) as exc:
            st.error(f"Error al consultar historial: {exc}")

with learning_tab:
    st.markdown("## Fundamentos y límites")
    st.markdown(r"""
    **Momento lineal** (kg·m/s): \(p=mv\). Tiene signo y representa la cantidad de movimiento en una dirección.

    **Impulso** (N·s): \(J=\Delta p\). Es el resultado de una fuerza actuando durante un intervalo, no el momento de un objeto.

    **Fuerza promedio** (N): \(F_{prom}=J/\Delta t\). Si desconocemos el tiempo de contacto, el impulso no basta para determinarla.

    **Energía cinética** (J): \(E_c=\tfrac12mv^2\). Es no negativa; no distingue el sentido de desplazamiento.

    **Disparo y retroceso:** el conjunto arma–proyectil parte del reposo. Idealmente, la cantidad de movimiento total es cero tanto antes como inmediatamente después del disparo, aunque la energía cinética aumenta gracias a la energía química.

    **Choque elástico:** los dos cuerpos libres conservan momento total y energía cinética total.

    **Choque inelástico:** los cuerpos libres conservan el momento total, pero parte de la energía cinética se transforma. Con \(e=0\) se supone que quedan unidos.

    **Barrera fija:** el proyectil como subsistema recibe impulso externo. Para recuperar la conservación del momento habría que considerar también el muro, su soporte y la Tierra.
    """)
    st.info("Esta herramienta es conceptual y académica. No calcula trayectorias balísticas, perforación, lesiones, rendimiento de armas ni condiciones reales de disparo.")
    st.markdown("### Ecuaciones incluidas")
    for expression in equations(simulate(SimulationInput("Estudiante demo", Scenario.INELASTIC, .02, 2., 30., .4, 0., restitution=.35))):
        st.code(expression, language="text")
    st.markdown("### Publicación y persistencia")
    st.write("Publica este repositorio en GitHub y despliégalo con Streamlit Community Cloud. GitHub Pages **no ejecuta Python**. El historial será permanente en web solo cuando se configure un servicio de almacenamiento externo como Supabase.")
