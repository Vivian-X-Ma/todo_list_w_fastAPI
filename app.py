import streamlit as st
import requests
import time
import re

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
            return True
        else:
            st.error("Failed to create item")
            return False
    except:
        st.error("Cannot connect to backend")
        return False
        
def update_item(name, text, is_done, id):
    try:
        item_data = {
            "name": name,
            "text": text,
            "is_done": is_done
        }
        response = requests.put(f"{API_URL}/items/{id}", json=item_data)
        if response.status_code == 200:
            return True
        else:
            st.error("Failed to update item")
            return False
    except:
        st.error("Cannot connect to backend")
        return False

def delete_item(id):
    try: 
        response = requests.delete(f"{API_URL}/items/{id}")
        if response.status_code == 200:
            return True
        else:
            st.error("Failed to delete item")
            return False
    except:
        st.error("Cannot connect to backend")
        return False

# Configure page
st.set_page_config(page_title="Pomodoro Timer", layout="wide")

st.title("Pomodoro Timer")

# Session state initialization
if 'timer_length' not in st.session_state:
    st.session_state['timer_length'] = 25
if 'timer_seconds' not in st.session_state:
    st.session_state['timer_seconds'] = st.session_state['timer_length'] * 60
if 'timer_running' not in st.session_state:
    st.session_state['timer_running'] = False
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = time.time()

# Show slider only when not running
if not st.session_state['timer_running']:
    timer_length = st.slider(
        'Set timer (minutes)',
        min_value=1,
        max_value=90,
        value=st.session_state['timer_length'],
        key='timer_length_slider'
    )
    # Only update timer if the slider value changed
    if timer_length != st.session_state['timer_length']:
        st.session_state['timer_length'] = timer_length
        st.session_state['timer_seconds'] = timer_length * 60
        st.rerun()  # Immediate update for slider changes

# Timer display
minutes = st.session_state['timer_seconds'] // 60
seconds = st.session_state['timer_seconds'] % 60
timer_str = f"{minutes:02d}:{seconds:02d}"

# Use a placeholder for the timer to avoid layout shifts
timer_placeholder = st.empty()
timer_placeholder.markdown(
    f"<h1 style='text-align: center; font-size: 72px; font-family: monospace;'>{timer_str}</h1>",
    unsafe_allow_html=True
)

# Timer controls
col1, col2, col3 = st.columns(3)
with col1:
    start_button = st.button("Start", key="start_timer", use_container_width=True)
with col2:
    end_button = st.button("End", key="end_timer", use_container_width=True)
with col3:
    reset_button = st.button("Reset", key="reset_timer", use_container_width=True)

# Handle button clicks
if start_button:
    st.session_state['timer_running'] = True
    st.session_state['last_update'] = time.time()
    st.rerun()

if end_button:
    st.session_state['timer_running'] = False
    st.rerun()

if reset_button:
    st.session_state['timer_seconds'] = st.session_state['timer_length'] * 60
    st.session_state['timer_running'] = False
    st.rerun()

# Countdown logic with better timing
if st.session_state['timer_running'] and st.session_state['timer_seconds'] > 0:
    current_time = time.time()
    if current_time - st.session_state['last_update'] >= 1.0:
        st.session_state['timer_seconds'] -= 1
        st.session_state['last_update'] = current_time
        st.rerun()  # Keep the timer updating smoothly
elif st.session_state['timer_running'] and st.session_state['timer_seconds'] <= 0:
    st.session_state['timer_running'] = False
    st.balloons()  # Celebration when timer ends
    st.success("Time's up!")
    st.rerun()  # Update to show timer ended

# Add some spacing
st.markdown("---")

st.title("Task Manager")

# Display items with better formatting
items = get_items()
if items:
    for i, item in enumerate(items):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                status = "✅" if item['is_done'] else "⏳"
                st.markdown(f"**{status} {item['name']}**")
                if item['text']:
                    st.markdown(f"*{item['text']}*")
            
            with col2:
                if st.button("Toggle", key=f"toggle_{item.get('id', i)}"):
                    if update_item(item['name'], item['text'], not item['is_done'], item.get('id')):
                        st.rerun()
            
            with col3:
                if st.button("Delete", key=f"delete_{item.get('id', i)}"):
                    if delete_item(item.get('id')):
                        st.rerun()
            
            st.markdown("---")
else:
    st.info("No tasks yet. Add one below!")

st.header("Add New Task")

# Use a form to prevent duplicate submissions
with st.form("add_item_form", clear_on_submit=True):
    name = st.text_input("Task Name")
    text = st.text_area("Description (optional)")
    is_done = st.checkbox("Mark as completed")
    submit_button = st.form_submit_button("Add Task", use_container_width=True)

    if submit_button:
        if name.strip():  # Only require task name
            if create_item(name.strip(), text.strip(), is_done):
                st.rerun()
        else:
            st.error("Please enter a task name")


# st.title("Pomodoro Timer")

# # Session state initialization
# if 'timer_length' not in st.session_state:
#     st.session_state['timer_length'] = 25
# if 'timer_seconds' not in st.session_state:
#     st.session_state['timer_seconds'] = st.session_state['timer_length'] * 60
# if 'timer_running' not in st.session_state:
#     st.session_state['timer_running'] = False

# # Show slider only when not running
# if not st.session_state['timer_running']:
#     timer_length = st.slider(
#         'Set timer (minutes)',
#         min_value=1,
#         max_value=90,
#         value=st.session_state['timer_length'],
#         key='timer_length_slider'
#     )

# # Format and display the timer
# minutes = st.session_state['timer_seconds'] // 60
# seconds = st.session_state['timer_seconds'] % 60
# timer_str = f"{minutes:02d}:{seconds:02d}"
# st.markdown(
#     f"<h1 style='text-align: center; font-size: 72px;'>{timer_str}</h1>",
#     unsafe_allow_html=True
# )

# left, middle, right = st.columns(3, vertical_alignment="bottom")
# start = left.button("Start", use_container_width=True)
# end = middle.button("End", use_container_width=True)
# reset = right.button("Reset", use_container_width=True)

# if start:
#     st.session_state['timer_running'] = True
# if end:
#     st.session_state['timer_running'] = False
# if reset:
#     st.session_state['timer_seconds'] = st.session_state['timer_length'] * 60
#     st.session_state['timer_running'] = False

# # Countdown logic
# if st.session_state['timer_running'] and st.session_state['timer_seconds'] > 0:
#     time.sleep(1)
#     st.session_state['timer_seconds'] -= 1
#     st.rerun()

# st.title("Item Manager")

# # Display items
# items = get_items()
# for item in items:
#     st.write(f"Name: {item['name']}")
#     st.write(f"Text: {item['text']}")
#     st.write(f"Done: {item['is_done']}")
#     st.write("---")
#     # st.checkbox(label, value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible", width="content")

# st.header("Add New Item")

# with st.form("add_item"):
#     name = st.text_input("Task")
#     text = st.text_area("Description")
#     is_done = st.checkbox("Done")
#     submit = st.form_submit_button("Add Task")

#     if submit:
#         if name and text:
#             create_item(name, text, is_done)
#             st.rerun() # Refresh page
#         else:
#             st.error("Fill in all fields")




