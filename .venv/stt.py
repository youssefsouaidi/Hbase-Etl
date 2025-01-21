import streamlit as st
import happybase
import pandas as pd

# Connexion à HBase
def connect_hbase():
    return happybase.Connection('localhost')

def get_all_data(table, limit=None):
    rows = table.scan(limit=limit)
    data = []
    for key, row in rows:
        row_data = {"row_key": key.decode('utf-8')}
        for col, value in row.items():
            row_data[col.decode('utf-8')] = value.decode('utf-8')
        data.append(row_data)
    return pd.DataFrame(data).fillna("")

def add_data(table, row_key, data):
    table.put(row_key, {k.encode('utf-8'): v.encode('utf-8') for k, v in data.items()})

def update_data(table, row_key, column, new_value):
    table.put(row_key, {column.encode('utf-8'): new_value.encode('utf-8')})

def get_versions(table, row_key, column, max_versions=3):
    return table.cells(row_key, column, versions=max_versions)

def delete_data(table, row_key):
    table.delete(row_key)

def main():
    st.set_page_config(page_title="HBase CRUD Application", page_icon="🔍", layout="wide")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image("logo.png", width=200)

    with col2:
        st.markdown(
            """
            <style>
                .title-container {
                    text-align: center;
                    font-family: 'Courier New', monospace;  /* Police pour un alignement parfait */
                    padding: 20px;
                    letter-spacing: 2px;  /* Espacement uniforme entre les lettres */
                }
                .title-part-red {
                    color: red;
                    font-size: 55px;  /* Taille de police ajustée */
                    font-weight: bold;
                    display: inline-block;
                    text-transform: uppercase;  /* Tous les caractères en majuscules */
                }
                .title-part-black {
                    color: black;
                    font-size: 55px;  /* Taille de police ajustée */
                    font-weight: bold;
                    display: inline-block;
                    text-transform: uppercase;  /* Tous les caractères en majuscules */
                }
            </style>
            <div class="title-container">
                <span class="title-part-red">HBase</span>
                <span class="title-part-black">CRUD</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        with col3:
         st.image("logo.png", width=200)

    st.markdown("---")

    conn = connect_hbase()
    table = conn.table('userdata')

    st.sidebar.title("Navigation")
    action = st.sidebar.radio("Choisissez une action", ["Afficher les données", "Ajouter", "Mettre à jour/chercher_rowkey", "Supprimer"])

    if action == "Afficher les données":
        st.markdown("### 🔍 Afficher les données")
        limit = st.slider("Nombre de lignes à afficher", min_value=1, max_value=10000, value=10, step=1)
        data = get_all_data(table, limit=limit)
        st.write("Données actuelles :")
        st.dataframe(data)

    elif action == "Ajouter":
        st.markdown("### ➕ Ajouter une nouvelle donnée")
        with st.form("Ajouter une ligne"):
            row_key = st.text_input("Row Key", "")
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("Prénom")
                last_name = st.text_input("Nom")
                email = st.text_input("Email")
                phone = st.text_input("Téléphone")

            with col2:
                username = st.text_input("Nom d'utilisateur")
                street = st.text_input("Rue")
                post_code = st.text_input("Code postal")
                dob = st.text_input("Date de naissance")

            submitted = st.form_submit_button("Ajouter")
            if submitted:
                if row_key:
                    data = {
                        "info:first_name": first_name,
                        "info:last_name": last_name,
                        "contact:email": email,
                        "contact:phone": phone,
                        "contact:username": username,
                        "address:street": street,
                        "address:post_code": post_code,
                        "info:dob": dob,
                    }
                    data = {k: v for k, v in data.items() if v}  # Supprime les champs vides
                    try:
                        add_data(table, row_key, data)
                        st.success(f"Données ajoutées pour la ligne : {row_key}")
                    except Exception as e:
                        st.error(f"Erreur lors de l'ajout : {e}")
                else:
                    st.error("La Row Key est obligatoire.")

    elif action == "Mettre à jour/chercher_rowkey":
        st.markdown("### 🛠️ Mise à jour et recherche d'une donnée")
        row_key = st.text_input("Row Key à chercher", "")
        if row_key:
            data = table.row(row_key.encode('utf-8'))
            if data:
                st.write(f"Données actuelles pour la ligne **{row_key}** :")
                st.json({k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()})

                col1, col2 = st.columns(2)

                with col1:
                    available_columns = [k.decode('utf-8') for k in data.keys()]
                    col_to_update = st.selectbox("Colonne à mettre à jour", available_columns)

                with col2:
                    new_value = st.text_input("Nouvelle valeur")

                if st.button("Mettre à jour"):
                    try:
                        update_data(table, row_key, col_to_update, new_value)
                        st.success(f"Colonne {col_to_update} mise à jour avec succès.")
                    except Exception as e:
                        st.error(f"Erreur lors de la mise à jour : {e}")

                if st.button("Afficher les versions"):
                    try:
                        versions = get_versions(table, row_key.encode('utf-8'), col_to_update.encode('utf-8'))
                        if versions:
                            st.write(f"Versions disponibles pour **{col_to_update}** :")
                            for i, version in enumerate(versions):
                                st.write(f"Version {i + 1}: {version.decode('utf-8')}")
                        else:
                            st.warning("Aucune version disponible pour cette colonne.")
                    except Exception as e:
                        st.error(f"Erreur lors de la récupération des versions : {e}")
            else:
                st.error("Row Key introuvable.")

    elif action == "Supprimer":
        st.markdown("### ❌ Supprimer une donnée")
        row_key = st.text_input("Row Key à supprimer", "")
        if st.button("Supprimer"):
            try:
                delete_data(table, row_key)
                st.success(f"Ligne {row_key} supprimée avec succès.")
            except Exception as e:
                st.error(f"Erreur lors de la suppression : {e}")

if __name__ == "__main__":
    main()
