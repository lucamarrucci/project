# app.py
import streamlit as st, pandas as pd, os
from datetime import date
from model import training_value

DATA_DIR=os.path.join(os.path.dirname(__file__),"data")
ATHLETES=os.path.join(DATA_DIR,"athletes.csv")
REPORTS=os.path.join(DATA_DIR,"reports.csv")
os.makedirs(DATA_DIR,exist_ok=True)
if not os.path.exists(ATHLETES):
    pd.DataFrame(columns=["athlete_id","name","squad"]).to_csv(ATHLETES,index=False)
if not os.path.exists(REPORTS):
    pd.DataFrame(columns=["athlete_id","date","duration_min","rpe","swim_meters","high_intensity_meters","gym_volume_kg","sleep_hours","sleep_quality_1_5","fatigue_1_10","stress_1_10","mood_1_10","quality_note","tv"]).to_csv(REPORTS,index=False)

athletes=pd.read_csv(ATHLETES)
reports=pd.read_csv(REPORTS)

st.sidebar.title("SplashCoach Club")
role=st.sidebar.radio("Chi sei?",["Allenatore","Atleta"])

if role=="Allenatore":
    st.title("👨‍🏫 Allenatore")
    with st.form("add"):
        name=st.text_input("Nome atleta")
        squad=st.text_input("Squadra","Assoluti")
        if st.form_submit_button("Aggiungi") and name:
            new_id=str(int(athletes["athlete_id"].max())+1 if not athletes.empty else 1)
            athletes=pd.concat([athletes,pd.DataFrame([{"athlete_id":new_id,"name":name,"squad":squad}])],ignore_index=True)
            athletes.to_csv(ATHLETES,index=False)
            st.success(f"Aggiunto {name}")
    st.dataframe(athletes)

    st.subheader("Report ricevuti")
    if not reports.empty: st.dataframe(reports)

else:
    st.title("🏊 Atleta")
    if athletes.empty: st.warning("Nessun atleta ancora"); st.stop()
    pick=st.selectbox("Chi sei?",athletes["athlete_id"],format_func=lambda i:f"{i} - {athletes.loc[athletes['athlete_id']==i,'name'].values[0]}")
    with st.form("rep"):
        d=st.date_input("Data",value=date.today())
        dur=st.number_input("Minuti",0,240,120)
        rpe=st.slider("RPE",1,10,6)
        swim=st.number_input("Metri nuoto",0,15000,4000,step=100)
        hi=st.number_input("Metri HI",0,5000,800,step=50)
        gym=st.number_input("Palestra kg",0,20000,0,step=100)
        sleep=st.number_input("Ore sonno",0.0,12.0,7.5,step=0.5)
        q_sleep=st.slider("Qualità sonno",1,5,4)
        fat=st.slider("Fatica",1,10,5)
        stress=st.slider("Stress",1,10,5)
        mood=st.slider("Umore",1,10,6)
        qual=st.slider("Qualità percepita",0.0,1.0,0.5,step=0.1)
        if st.form_submit_button("Invia"):
            row={"athlete_id":str(pick),"date":str(d),"duration_min":dur,"rpe":rpe,"swim_meters":swim,"high_intensity_meters":hi,"gym_volume_kg":gym,"sleep_hours":sleep,"sleep_quality_1_5":q_sleep,"fatigue_1_10":fat,"stress_1_10":stress,"mood_1_10":mood,"quality_note":qual}
            row["tv"]=training_value(row)
            reports=pd.concat([reports,pd.DataFrame([row])],ignore_index=True)
            reports.to_csv(REPORTS,index=False)
            st.success(f"Report inviato! TV={row['tv']}")
    st.subheader("Storico")
    me=reports[reports["athlete_id"]==str(pick)]
    st.dataframe(me)
