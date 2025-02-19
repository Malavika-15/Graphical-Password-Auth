import cv2
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random  # For some basic "animation"
from flask import Flask, jsonify, request
import threading

USER_DATA_FILE = "users.json"

# Initialize Flask app
app = Flask(__name__)

# Load user data from file
def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to file
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Flask route for user registration
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username')
    users = load_users()
    
    if not username or username in users:
        return jsonify({'status': 'error', 'message': 'Invalid or existing username'}), 400
    
    users[username] = {"method": "none", "data": []}
    save_users(users)
    return jsonify({'status': 'success', 'message': 'Registration successful'})

# Flask route for user login
@app.route('/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    users = load_users()
    
    if username not in users:
        return jsonify({'status': 'error', 'message': 'Username not found'}), 400
    
    return jsonify({'status': 'success', 'message': 'Login successful'})

# Function to run Flask app
def run_flask():
    app.run(host='0.0.0.0', port=5000)  # Accessible from any machine on the network

class GraphicalPasswordAuth:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphical Password Authentication")

        # --- Full Screen ---
        self.root.attributes("-fullscreen", True)  # Set to True for fullscreen

        # --- Load Background Image ---
        try:
            self.bg_image = Image.open("india.jpg")  # Replace "background.jpg"
            self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            self.bg_photo = None
            print("Background image 'india.jpg' not found!")

        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Load Users ---
        self.username = None
        self.user_pattern = []
        self.cued_points = []
        self.users = load_users()

        # --- Styling ---
        self.title_font = ("Comic Sans Ms", 36, "bold")
        self.button_font = ("Comic Sans Ms", 16, "bold")
        self.label_font = ("Comic Sans Ms", 14)
        self.primary_color = "darkred"  # Background color
        self.secondary_color = "#5e60e2"  # Button color
        self.text_color = "white"
        self.shadow_color = "rgba(105, 18, 18, 0.616)"  # Simulated shadow color

        # --- Load Transparent Background Image for Glassy Effect ---
        try:
            self.transparent_bg_image = Image.open("india.jpg")  # Replace with your transparent image
            self.transparent_bg_image = self.transparent_bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
            self.transparent_bg_photo = ImageTk.PhotoImage(self.transparent_bg_image)
        except FileNotFoundError:
            self.transparent_bg_photo = None
            print("Transparent background image 'india.jpg' not found!")

        # --- Glassy Container (Simulated with Transparency) ---
        self.main_frame = tk.Frame(root, bd=2, relief=tk.SOLID)
        if self.transparent_bg_photo:
            self.main_frame.config(bg="#80bfff") #To allow transparency to be seen
            self.main_frame.bg_label = tk.Label(self.main_frame, image=self.transparent_bg_photo, borderwidth=0)  # Create label for bg
            self.main_frame.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place it on the frame
        else:
            self.main_frame.config(bg="#80bfff") #If fails just choose BG color

        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.6, relheight=0.6)  # Placed at center

        # --- UI Elements with Styling ---
        title_label = tk.Label(self.main_frame, text="Graphical Password Authentication",
                            font=self.title_font, bg=self.primary_color, fg=self.text_color, padx=20, pady=20)
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30), padx=30, sticky="ew")

        # Button style configuration
        button_style = {
            'padx': 30,
            'pady': 12,
            'font': self.button_font,
            'bg': '#5e60e2',  # Background color
            'fg': 'white',     # Text color
            'relief': tk.RAISED,
            'borderwidth': 0,
            'highlightthickness': 0,
            'activebackground': '#4f54d4',  # Darker shade for active state
            'activeforeground': 'white'
        }

        # Create buttons with hover effect
        self.register_button = tk.Button(self.main_frame, text="Register", command=self.register_user, **button_style)
        self.register_button.grid(row=1, column=0, pady=15, padx=(30, 10), sticky="ew")

        self.login_button = tk.Button(self.main_frame, text="Login", command=self.login_user, **button_style)
        self.login_button.grid(row=1, column=1, pady=15, padx=(10, 30), sticky="ew")

        # Add hover effect
        def on_enter(button):
            button.config(bg='#e94e77')  # Darker shade on hover

        def on_leave(button):
            button.config(bg='#5e60e2')  # Original shade when not hovered

        self.register_button.bind("<Enter>", lambda e: on_enter(self.register_button))
        self.register_button.bind("<Leave>", lambda e: on_leave(self.register_button))
        self.login_button.bind("<Enter>", lambda e: on_enter(self.login_button))
        self.login_button.bind("<Leave>", lambda e: on_leave(self.login_button))

        # --- Animation (Simple) ---
        self.animate_title()


        root.bind("<Escape>", self.exit_fullscreen)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def animate_title(self):
        colors = ["#007acc", "#00a3cc"]  # Add more colours for animation
        current_color = colors[random.randint(0, len(colors) - 1)]
        title_label = self.main_frame.winfo_children()[0]  # Access title Label from the main frame
        title_label.config(bg=current_color)
        self.root.after(2000, self.animate_title)  # Change the 2000 to change animation speed

    # ------------------- REGISTER MODULE -------------------
    def register_user(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("User Registration")
        reg_window.attributes("-fullscreen", True)  # Fullscreen
        reg_window.transient(self.root)

        # Semi transparent BG using a label with the transparent BG image
        reg_window.config(bg="#80bfff")
        if self.transparent_bg_photo:
            reg_window.bg_label = tk.Label(reg_window, image=self.transparent_bg_photo, borderwidth=0)  # Create label for bg
            reg_window.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place it on the frame

        reg_frame = tk.Frame(reg_window, bg="#80bfff")
        reg_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(reg_frame, text="Enter Username:", bg="#80bfff", font=self.label_font, fg=self.text_color).pack(pady=15)
        self.username_entry_reg = tk.Entry(reg_frame, font=self.label_font, bg="white", fg="black")
        self.username_entry_reg.pack(pady=5, padx=30)

        def proceed_reg():
            username = self.username_entry_reg.get()
            if not username or username in self.users:
                messagebox.showerror("Error", "Invalid or existing username")
                return
            self.username = username
            reg_window.destroy()
            self.choose_auth_method(is_register=True)

        proceed_button_style = {'padx': 20, 'pady': 8, 'font': self.button_font,
                                'bg': self.secondary_color, 'fg': self.text_color, 'relief': tk.RAISED, 'borderwidth': 2}
        tk.Button(reg_frame, text="Proceed", command=proceed_reg, **proceed_button_style).pack(pady=20)

    # ------------------- LOGIN MODULE -------------------
    def login_user(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("User Login")
        login_window.attributes("-fullscreen", True)  # Fullscreen
        login_window.transient(self.root)

        # Semi transparent BG using a label with the transparent BG image
        login_window.config(bg="#80bfff")
        if self.transparent_bg_photo:
            login_window.bg_label = tk.Label(login_window, image=self.transparent_bg_photo, borderwidth=0)  # Create label for bg
            login_window.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place it on the frame

        login_frame = tk.Frame(login_window, bg="#80bfff")
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(login_frame, text="Enter Username:", bg="#80bfff", font=self.label_font, fg=self.text_color).pack(pady=15)
        self.username_entry_login = tk.Entry(login_frame, font=self.label_font, bg="white", fg="black")
        self.username_entry_login.pack(pady=5, padx=30)

        def proceed_login():
            username = self.username_entry_login.get()
            if username not in self.users:
                messagebox.showerror("Error", "Username not found")
                return
            self.username = username
            login_window.destroy()
            self.choose_auth_method(is_register=False)

        proceed_button_style = {'padx': 20, 'pady': 8, 'font': self.button_font,
                                'bg': self.secondary_color, 'fg': self.text_color, 'relief': tk.RAISED, 'borderwidth': 2}
        tk.Button(login_frame, text="Proceed", command=proceed_login, **proceed_button_style).pack(pady=20)

    # ------------------- CHOOSE AUTHENTICATION TYPE -------------------
    def choose_auth_method(self, is_register):
        auth_window = tk.Toplevel(self.root)
        auth_window.title("Select Authentication Method")
        auth_window.attributes("-fullscreen", True)  # Fullscreen
        auth_window.transient(self.root)

        # Semi transparent BG using a label with the transparent BG image
        auth_window.config(bg="#80bfff")
        if self.transparent_bg_photo:
            auth_window.bg_label = tk.Label(auth_window, image=self.transparent_bg_photo, borderwidth=0)  # Create label for bg
            auth_window.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place it on the frame

        auth_frame = tk.Frame(auth_window, bg="#80bfff")
        auth_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        method_button_style = {'padx': 20, 'pady': 10, 'font': self.button_font,
                                'bg': self.secondary_color, 'fg': self.text_color, 'relief': tk.RAISED, 'borderwidth': 2}

        tk.Button(auth_frame, text="Recognition-Based",
                  command=lambda: self.recognition_based(is_register), **method_button_style).pack(pady=15)
        tk.Button(auth_frame, text="Recall-Based (Pattern)",
                  command=lambda: self.recall_based(is_register), **method_button_style).pack(pady=15)
        tk.Button(auth_frame, text="Cued Recall-Based",
                  command=lambda: self.cued_recall_based(is_register), **method_button_style).pack(pady=15)

    # ------------------- RECOGNITION-BASED AUTH -------------------
    def recognition_based(self, is_register):
        images = ["france.jpg", "hongkong.jpg", "malaysia.jpg", "norway.jpg","singapore.jpg","switz1.jpg","antartica.jpg","australia.jpg","china.jpg","germany.jpg","japan.jpg","seoul.jpg"]
        top = tk.Toplevel(self.root)
        top.title("Select Images")
        top.attributes("-fullscreen", True)  # Fullscreen
        top.transient(self.root)

        # Semi transparent BG using a label with the transparent BG image
        top.config(bg="#80bfff")
        if self.transparent_bg_photo:
            top.bg_label = tk.Label(top, image=self.transparent_bg_photo, borderwidth=0)  # Create label for bg
            top.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place it on the frame
        recog_frame = tk.Frame(top, bg="#80bfff")
        recog_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        selected_images_session = []
        image_buttons = {}  # Store button references for highlighting

        def select_image(img):
            if img in selected_images_session:
                selected_images_session.remove(img)
                image_buttons[img].config(relief=tk.RAISED)  # Remove highlight
            else:
                selected_images_session.append(img)
                image_buttons[img].config(relief=tk.SUNKEN)  # Highlight

        frame = tk.Frame(recog_frame, bg="#80bfff")
        frame.pack(pady=20)

        # Create a grid layout for images
        for index, img in enumerate(images):
            img_obj = Image.open(img).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img_obj)
            btn = tk.Button(frame, image=img_tk, command=lambda i=img: select_image(i), relief=tk.RAISED)
            btn.image = img_tk
            btn.grid(row=index // 4, column=index % 4, padx=10, pady=10)  # Change 4 to the number of columns you want
            image_buttons[img] = btn  # Store the button reference

        def confirm_selection():
            if is_register:
                if not selected_images_session:
                    messagebox.showerror("Error", "Please select at least one image.")
                    return
                self.users[self.username] = {"method": "recognition", "data": selected_images_session}
                save_users(self.users)
                messagebox.showinfo("Success", "Registration Complete!")
            else:
                stored_images = self.users[self.username]["data"]
                if selected_images_session == stored_images:
                    messagebox.showinfo("Success", "Login Successful!")
                else:
                    messagebox.showerror("Error", "Password was incorrect. Login unsuccessful.")
            top.destroy()

        confirm_button_style = {'padx': 20, 'pady': 8, 'font': self.button_font,
                                'bg': self.secondary_color, 'fg': self.text_color, 'relief': tk.RAISED, 'borderwidth': 2}
        tk.Button(recog_frame, text="Confirm", command=confirm_selection, **confirm_button_style).pack(pady=20)

    # ------------------- RECALL-BASED AUTH -------------------
    def recall_based(self, is_register):
        # Create a Toplevel window
        top = tk.Toplevel(self.root)
        top.title("Draw a Pattern")
        top.attributes("-fullscreen", True)  # Make it fullscreen
        top.transient(self.root)

        # Semi transparent BG using a label with the transparent BG image
        top.config(bg="#80bfff")
        if self.transparent_bg_photo:
            top.bg_label = tk.Label(top, image=self.transparent_bg_photo, borderwidth=0)  # Create label for bg
            top.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place it on the frame

        canvas_frame = tk.Frame(top, bg="#80bfff")  # To hold canvas for better layout
        canvas_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        canvas = tk.Canvas(canvas_frame, width=400, height=400, bg="white", highlightthickness=0, borderwidth=2, relief=tk.SUNKEN)
        canvas.pack(pady=10)

        drawn_pattern = []
        drawing = False

        def start_drawing(event):
            nonlocal drawing
            drawing = True
            drawn_pattern.append((event.x, event.y))

        def draw(event):
            nonlocal drawing
            if drawing:
                x, y = event.x, event.y
                drawn_pattern.append((x, y))
                canvas.create_oval(x-4, y-4, x+4, y+4, fill=self.primary_color, outline=self.primary_color)

        def stop_drawing(event):
            nonlocal drawing
            drawing = False

        def distance(p1, p2):
            return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

        def compare_patterns(pattern1, pattern2, tolerance=20):
            if len(pattern1) != len(pattern2):
                                return False

            total_distance = 0
            for i in range(len(pattern1)):
                total_distance += distance(pattern1[i], pattern2[i])

            average_distance = total_distance / len(pattern1)
            return average_distance <= tolerance

        def confirm_pattern():
            if is_register:
                if not drawn_pattern:  # Check if any drawing occurred
                    messagebox.showerror("Error", "Please draw a pattern.")
                    return
                self.users[self.username] = {"method": "recall", "data": drawn_pattern}
                save_users(self.users)
                messagebox.showinfo("Success", "Registration Complete!")
            else:
                stored_pattern = self.users[self.username]["data"]
                if compare_patterns(drawn_pattern, stored_pattern):
                    messagebox.showinfo("Success", "Login Successful!")
                else:
                    messagebox.showerror("Error", "Password was incorrect. Login unsuccessful.")
            top.destroy()

        canvas.bind("<ButtonPress-1>", start_drawing)
        canvas.bind("<B1-Motion>", draw)
        canvas.bind("<ButtonRelease-1>", stop_drawing)

        confirm_button_style = {'padx': 20, 'pady': 8, 'font': self.button_font,
                                'bg': self.secondary_color, 'fg': self.text_color, 'relief': tk.RAISED, 'borderwidth': 2}
        tk.Button(canvas_frame, text="Confirm", command=confirm_pattern, **confirm_button_style).pack(pady=20)

    # ------------------- CUED RECALL-BASED AUTH -------------------
    def cued_recall_based(self, is_register):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not file_path:
            return

        top = tk.Toplevel(self.root)
        top.title("Click on Secret Points")
        top.attributes("-fullscreen", True)  # Fullscreen
        top.transient(self.root)

        # Semi transparent BG using a label with the transparent BG image
        top.config(bg="#80bfff")
        if self.transparent_bg_photo:
            top.bg_label = tk.Label(top, image=self.transparent_bg_photo, borderwidth=0)  # Create label for bg
            top.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place it on the frame
        cue_frame = tk.Frame(top, bg="#80bfff")
        cue_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        try:
            image = cv2.imread(file_path)
            image = cv2.resize(image, (500, 500))  # Increased Size
            img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            img_tk = ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            top.destroy()
            return

        label = tk.Label(cue_frame, image=img_tk, borderwidth=2, relief=tk.SUNKEN)
        label.image = img_tk
        label.pack(pady=10)

        cued_points_session = []

        def on_click(event):
            x, y = event.x, event.y
            cued_points_session.append((x, y))
            print(f"Clicked at: {x}, {y}")
            label.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="red")

        label.bind("<Button-1>", on_click)

        def distance(p1, p2):
            return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

        def compare_points(points1, points2, tolerance=20):
            print("Comparing points...")
            print("User Points:", points1)
            print("Stored Points:", points2)

            if not points1 or not points2:
                print("One of the points lists is empty")
                return False

            if len(points1) != len(points2):
                print("Number of points does not match")
                return False

            total_distance = 0
            for i in range(len(points1)):
                total_distance += distance(points1[i], points2[i])

            average_distance = total_distance / len(points1)
            print("Average Distance:", average_distance)
            print("Tolerance:", tolerance)
            return average_distance <= tolerance

        def confirm_points():
            if is_register:
                if not cued_points_session:
                    messagebox.showerror("Error", "Please click on the image to select points.")
                    return
                self.users[self.username] = {"method": "cued", "data": cued_points_session}
                save_users(self.users)
                messagebox.showinfo("Success", "Registration Complete!")
            else:
                stored_points = self.users[self.username]["data"]

                print("Stored Points (Raw):", stored_points)

                try:
                    stored_points = [tuple(map(float, point)) for point in stored_points]
                except Exception as e:
                    print(f"Error converting stored points: {e}")
                    messagebox.showerror("Error", "Error loading stored data. Data might be corrupted.")
                    return

                print("Stored Points (Converted):", stored_points)

                if compare_points(cued_points_session, stored_points):
                    messagebox.showinfo("Success", "Login Successful!")
                else:
                    messagebox.showerror("Error", "Password was incorrect. Login unsuccessful.")
            top.destroy()

        confirm_button_style = {'padx': 20, 'pady': 8, 'font': self.button_font,
                                'bg': self.secondary_color, 'fg': self.text_color, 'relief': tk.RAISED, 'borderwidth': 2}
        tk.Button(cue_frame, text="Confirm", command=confirm_points, **confirm_button_style).pack(pady=20)

# Run the application
if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run Tkinter application
    root = tk.Tk()
    app = GraphicalPasswordAuth(root)
    root.mainloop()