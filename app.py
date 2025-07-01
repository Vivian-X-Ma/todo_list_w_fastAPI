
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_items():
    try:
        response = requests.get(f"{API_URL}/items")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch items")
            return []
    except:
        st.error("Cannot connect to backend")
        return []


def create_item(name, text, is_done):
    try:
        item_data = {
            "name": name,
            "text": text,
            "is_done": is_done
        }

        response = requests.post(f"{API_URL}/items", json=item_data)
        if response.status_code == 200:
            st.success("Item created successfully")
        else:
            st.error("Failed to create item")
    except:
        st.error("Cannot connect to backend")
        
def update_item(name, text, is_done, id):
    try:
        item_data = {
            "name": name,
            "text": text,
            "is_done": is_done
        }
        response = requests.put(f"{API_URL}/items/{id}", json=item_data)
        if response.status_code == 200:
            print("success")
            return True
        else:
            print("fail")
            return False
    except:
        st.error("cannot connect")
        return False

def delete_item(id):
    try: 
        response = requests.delete(f"{API_URL}/items/{id}")
        if response.status_code == 200:
            print("success")
            return True
        else:
            print("fail")
            return False
    except:
        st.error("cannot connect")
        return False

        
st.title("Item Manager")

# Display items
items = get_items()
for item in items:
    st.write(f"Name: {item['name']}")
    st.write(f"Text: {item['text']}")
    st.write(f"Done: {item['is_done']}")
    st.write("---")
    # st.checkbox(label, value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible", width="content")



st.header("Add New Item")

with st.form("add_item"):
    name = st.text_input("Task")
    text = st.text_area("Description")
    is_done = st.checkbox("Done")
    submit = st.form_submit_button("Add Task")

    if submit:
        if name and text:
            create_item(name, text, is_done)
            st.rerun() # Refresh page
        else:
            st.error("Fill in all fields")


st.header("Timer")

st.select_slider("Timer Length")
st.select_slider("Break Length")

st.write(f"25:00")

st.columns(spec, *, gap="small", vertical_alignment="top", border=False)
st.form_submit_button("Start")
st.form_submit_button("End")
st.form_submit_button("Reset")


