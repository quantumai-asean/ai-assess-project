import enum
import streamlit as st
import toml
import psycopg
from psycopg import errors
import os
from google.cloud.firestore_v1.base_query import FieldFilter

def generate_enum(enumClass, enumDict):
    """
    Generates python code for an Enum
    """

    enum_template = """
@unique
class {enumClass}(enum.Enum):
{enumBody}
"""

    enumBody = '\n'.join([f"    {name} = '{value}'" for (name,value) in enumDict.items()])

    return enum_template.format(enumClass=enumClass,enumBody=enumBody)


def streamlit_session_states_init():
    if 'confs' not in st.session_state:
        try:
            #https://docs.python.org/3.11/library/tomllib.html#module-tomllib
            #with open("frontend/configs.toml", "rb") as f:
            #    confs = tomllib.load(f)
            #    st.session_state.confs = confs
            st.session_state.confs = toml.load("frontend/configs.toml") 
        except Exception as e:
            st.error(e)
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
        st.session_state.show_user_register  = False
        st.session_state.show_user_login  = False

        #mode card page
        #st.session_state.modelcard_showassessment = False
        #st.session_state.modelcard_showmodelcard = False

        st.session_state.modelcardpage_states = {'mc_registration_input': None, 
                                                 'mc_modelcard': None, 
                                                 'mc_mctoolkit': None, 
                                                 'sm_RunAssessment': False,
                                                 'sm_showassessment': False,
                                                 'sm_showmodelcard': False,
                                                 'sm_registration_page_cnt' : 0
                                                 }



"""
def psql_database_interface(qry:str="", configs: dict = None, action: str = "update"):
    try:
        assert action in {"query","update"}, f"invalid action {action}"
        conn_str = f"host={configs['host']} port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
        q = None
        with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(qry)
                # Make the changes to the database persistent
                if action == "query":
                    #q = cur.fetchone()
                    q = cur.fetchall()
                else:
                    q = True
            conn.commit()
    except Exception as e:
        print(e)
        return False
    return q
"""

def psql_database_interface(qry:str="", configs: dict = None, action: str = "update"):
    assert action in {"query","update"}, f"invalid action {action}"
    q = None
    # first try
    try:
        conn_str = f"host={configs['host']} port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
        conn = psycopg.connect(conn_str)
    except:
        try:
            conn_str = f"host=localhost port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
            conn = psycopg.connect(conn_str)
        except Exception as e:
            print(e)
            return False
    #print(conn_str)
    try:
        cur = conn.cursor()
        cur.execute(qry)
        # Make the changes to the database persistent
        if action == "query":
            #q = cur.fetchone()
            q = cur.fetchall()
        else:
            q = True
        conn.commit()
    except Exception as e:
        print(e)
        return False
    #print(q)
    return q


def gcp_firestore_add_data(collection, document_id:str, document_data:dict):
    """
    https://cloud.google.com/firestore/docs/manage-data/add-data?_gl=1*uodbo1*_up*MQ..&gclid=CjwKCAjwt-OwBhBnEiwAgwzrUoDaTxawX9iiZ0rCWSkFZhtD_jgWEowgC15d0bQJGqBzBfmgmR1UbxoCKjoQAvD_BwE&gclsrc=aw.ds
    """
    from google.cloud import firestore
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.session_state.confs['gcp']['secret']
    db = firestore.Client(st.session_state.confs['gcp']['project_id'])
    db.collection(collection).document(document_id).set(document_data) #this will add new row 

def gcp_firestore_get_data(collection, document_id:str):
    """
    https://cloud.google.com/firestore/docs/query-data/get-data?_gl=1*sor8kr*_up*MQ..&gclid=CjwKCAjwt-OwBhBnEiwAgwzrUoDaTxawX9iiZ0rCWSkFZhtD_jgWEowgC15d0bQJGqBzBfmgmR1UbxoCKjoQAvD_BwE&gclsrc=aw.ds
    """
    from google.cloud import firestore
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.session_state.confs['gcp']['secret']
    db = firestore.Client(st.session_state.confs['gcp']['project_id'])
    doc = db.collection(collection).document(document_id).get().to_dict()  
    return doc


def gcp_firestore_query_multiple(collection, filter:FieldFilter):
    """
    https://cloud.google.com/firestore/docs/query-data/queries?_gl=1*1ps3v9p*_up*MQ..&gclid=CjwKCAjwt-OwBhBnEiwAgwzrUoDaTxawX9iiZ0rCWSkFZhtD_jgWEowgC15d0bQJGqBzBfmgmR1UbxoCKjoQAvD_BwE&gclsrc=aw.ds#execute_a_query
    """
    from google.cloud import firestore
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.session_state.confs['gcp']['secret']
    db = firestore.Client(st.session_state.confs['gcp']['project_id'])
    docs = db.collection(collection).where(filter=filter).stream()
    return [doc.to_dict() for doc in docs]







def scroll_to_top(var):
    st.components.v1.html(
        f"""
            <p>{var}</p>
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
        """,
        height=0
    )


def compose_saKeyFactorUserAnswer (key_factormodel):
  answers = []
  for att1, val1 in key_factormodel.items():
    for att2, val2 in val1.items():
      answers.append(val2)
  return answers

def calculate_KeyFactor_RiskStats(user_keyfactor_model, ai_keyfactor_model: None):
    user_risk = [0 for _ in range(6)]
    ai_risk = []
    for att1, val1 in user_keyfactor_model.items():
        for att2, val2 in val1.items():
            user_risk[ val2['predicted_risk'] ] += 1
    
    if ai_keyfactor_model:
        ai_risk = [0 for _ in range(6)]
        for ai_rv in st.session_state.manual_assessment_keyfactor_ai_review:
            ai_risk[ ai_rv['Risk'] ] += 1
    
    return user_risk, ai_risk

def calculate_KeyFactor_RiskStats_lumped(user_keyfactor_model, ai_keyfactor_model: None):
    user_risk = [0 for _ in range(6)]
    ai_risk = []
    for att1, val1 in user_keyfactor_model.items():
        for att2, val2 in val1.items():
            user_risk[ val2['predicted_risk'] ] += 1
    
    if ai_keyfactor_model:
        ai_risk = [0 for _ in range(6)]
        for ai_rv in st.session_state.manual_assessment_keyfactor_ai_review['Risk']:
            ai_risk[ ai_rv ] += 1
    
    return user_risk, ai_risk

def draw_KeyFactor_DonutChart (user_keyfactor_model, ai_keyfactor_model: None):
    import matplotlib.pyplot as plt
    from src.enums import RISK_LEVEL
    import numpy as np
    from model_card_toolkit.utils.graphics import figure_to_base64str
    #user_risk, ai_risk = calculate_KeyFactor_RiskStats(user_keyfactor_model, ai_keyfactor_model)
    user_risk, ai_risk = calculate_KeyFactor_RiskStats_lumped(user_keyfactor_model, ai_keyfactor_model)
    #from https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
    
    def get_average_risk(ra):
        c = 0
        i = 0
        sum = 0
        for r in ra:
            c+=r
            sum = i * r
            i+=1
        return sum/c


    def draw_legends(wedges_, ax_, avgR):
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")
        for i, p in enumerate(wedges_):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax_.annotate(RISK_LEVEL[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)
            # Calculate center coordinates
            center_x, center_y = 0.0, 0.0  # Adjust as needed
            # Draw the red box
            #red_box = plt.Rectangle((center_x - 0.15, center_y - 0.01), 0.3, 0.2, color='red')
            #ax_.add_patch(red_box)
            ax_.text(center_x, center_y + 0.1, 'Avg Risk', horizontalalignment='center')
            if avgR<2:
                color = "green"
            elif avgR>=2 and avgR<3.5: 
                color = "yellow"
            else:
                color = "red"
            ax_.text(center_x, center_y - 0.15, f"{avgR:.1f}", horizontalalignment='center', color=color, fontsize="large")

    figU, axU = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedgesU, texts = axU.pie(user_risk, wedgeprops=dict(width=0.5), startangle=-40)
    axU.set_title("User Self-Assessment Risk Distribution")
    draw_legends(wedgesU, axU, get_average_risk(user_risk))

    figAI, axAI = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedgesAI, texts = axAI.pie(ai_risk, wedgeprops=dict(width=0.5), startangle=-40)
    axAI.set_title("AI Assessment Risk Distribution")
    draw_legends(wedgesAI, axAI, get_average_risk(ai_risk))


    return figure_to_base64str(figU.figure), figure_to_base64str(figAI.figure)
        
    





def calculate_risk_points(model):
    #str_properties = {attr: value for attr, value in model.items() if 'risk_rating'==attr}
    #print('check prop:', str_properties)

    total_risks = {'risk_rating':0, 'revised_risk_rating':0}

    for _, value1 in model.items():
        for attr2, value2 in value1.items():
            if attr2 == 'risk_rating':
                total_risks["risk_rating"]  += value2
            elif attr2 == 'revised_risk_rating':
                total_risks["revised_risk_rating"] += value2

    return total_risks      




#drawing pie chart
#single: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
#nested pie chart: https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html
# https://www.geeksforgeeks.org/donut-chart-using-matplotlib-in-python/


def demo_donut_with_box():
    import matplotlib.pyplot as plt

    # Create a donut chart (you'll need your actual data here)
    labels = ['A', 'B', 'C', 'D']
    sizes = [20, 30, 25, 25]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})

    # Calculate center coordinates
    center_x, center_y = 0.5, 0.5  # Adjust as needed

    # Draw the red box
    red_box = plt.Rectangle((center_x - 0.05, center_y - 0.05), 0.1, 0.1, color='red')
    ax.add_patch(red_box)

    # Add text next to the box
    plt.text(center_x + 0.1, center_y, 'Hello, World!', color='white')

    # Set aspect ratio to make it a donut chart
    ax.set_aspect('equal')

    plt.show()


    
    