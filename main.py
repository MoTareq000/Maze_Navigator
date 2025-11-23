# app.py
import streamlit as st
import time
from PIL import Image
from maze_generator import generate_maze
from search_algorithms import bfs_steps, a_star_steps
from helpers import plot_maze

# --- load and pre-resize images (use relative paths if possible) ---
# Adjust sizes if they look too big/small. Agent should be ~ 40-80 px depending on grid.
agent_img = Image.open(r"unnamed-removebg-preview.png").convert("RGBA")
agent_img_resized = agent_img.resize((48, 48))   # try 48, change if needed

goal_img = Image.open(r"Gemini_Generated_Image_2kex3o2kex3o2kex-removebg-preview.png").convert("RGBA")
goal_img_resized = goal_img.resize((36, 36))     # try 36

img_found = Image.open(r"ChatGPT Image Nov 23, 2025, 09_37_53 PM.png").convert("RGBA")
img_notfound = Image.open(r"Gemini_Generated_Image_6yywac6yywac6yyw-removebg-preview.png").convert("RGBA")

st.title("Help Jinx Find the Magical coin")

# --- controls ---
maze_size = st.slider("Maze Size", 5, 25, 10)
wall_prob = st.slider("Wall Probability", 0.05, 0.45, 0.25)
algo_choice = st.selectbox("Choose Algorithm", ["BFS", "A*"])
speed = st.slider("Animation Speed (s)", 0.01, 0.5, 0.08)

# Use unique keys for duplicate buttons if any
start_button = st.button("Start Search", key="start_btn")
if st.button("Reset Maze", key="reset_btn"):
    st.rerun()

# --- generate maze and goal ONCE ---
maze, goal_pos = generate_maze(maze_size, maze_size, wall_prob)
st.write(f"Maze generated — goal at {goal_pos}")

# placeholders
placeholder = st.empty()
cost_display = st.empty()

# run only when start pressed
if start_button:
    # create generator with explicit goal
    if algo_choice == "BFS":
        generator = bfs_steps(maze, start=(0,0), goal=goal_pos)
    else:
        generator = a_star_steps(maze, start=(0,0), goal=goal_pos)

    path_found = None
    start_time = time.time()

    for path, cost, visited in generator:
        
        fig = plot_maze(
             maze,paths=[path],
            visited_nodes_list=[visited],
            agent_img=agent_img_resized,
            goal_img=goal_img_resized,
            goal_pos=goal_pos
        )
        placeholder.pyplot(fig)
        cost_display.text(f"Current cost: {cost}")
        time.sleep(speed)

        # mark path_found if generator reached goal (generator yields final path when it sees goal)
        # safe way: if last node equals goal_pos then this is the final found path
        if path and path[-1] == goal_pos:
            path_found = path

    elapsed = time.time() - start_time
    st.info(f"Time taken: {elapsed:.2f} seconds")

    if path_found and path_found[-1] == goal_pos:
        placeholder.image(img_found, use_container_width=True)
        st.balloons()
        st.success("Jinx found the magical coin 🎉")
    else:
        placeholder.image(img_notfound, use_container_width=True)
        st.error("Jinx did not find magical coin 😞")
