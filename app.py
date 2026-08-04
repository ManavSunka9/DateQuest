import base64
import json
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from streamlit.errors import StreamlitSecretNotFoundError


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="DateQuest ❤️",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------
try:
    with open("style.css", encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True,
        )
except FileNotFoundError:
    st.error("style.css could not be found.")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
default_values = {
    "page": "home",
    "food": None,
    "selected_date": date.today() + timedelta(days=1),
    "selected_time": "19:00",
}

for state_name, default_value in default_values.items():
    if state_name not in st.session_state:
        st.session_state[state_name] = default_value


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def change_page(page_name):
    st.session_state.page = page_name
    st.rerun()


def format_time(time_text):
    return datetime.strptime(
        time_text,
        "%H:%M",
    ).strftime("%I:%M %p")


def reset_app():
    st.session_state.page = "home"
    st.session_state.food = None
    st.session_state.selected_date = (
        date.today() + timedelta(days=1)
    )
    st.session_state.selected_time = "19:00"
    st.rerun()


def apply_page_background(image_filename):
    image_path = Path("assets") / image_filename

    if not image_path.exists():
        return

    encoded_image = base64.b64encode(
        image_path.read_bytes()
    ).decode()

    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(255, 250, 252, 0.18),
                        rgba(255, 240, 247, 0.22)
                    ),
                    url("data:image/png;base64,{encoded_image}");

                background-size: cover;
                background-position: center top;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            @media screen and (max-width: 600px) {{
                .stApp {{
                    background-position: center top;
                    background-attachment: scroll;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# PAGE BACKGROUNDS
# --------------------------------------------------
page_backgrounds = {
    "home": "home-background.png",
    "food": "food-background.png",
    "schedule": "schedule-background.png",
    "confirmed": "confirmed-background.png",
}

current_background = page_backgrounds.get(
    st.session_state.page
)

if current_background:
    apply_page_background(current_background)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------
if st.session_state.page == "home":

    st.markdown(
        """
<div class="hero">
    <div class="heart-icon">💖</div>
    <h1>Will you go on a date with me?</h1>
    <p class="subtitle">I promise it'll be cute ✨</p>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "YES 💗",
        key="yes_button",
        use_container_width=True,
        type="primary",
    ):
        change_page("food")

    components.html(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0,
        maximum-scale=1.0, user-scalable=no"
    >

    <style>
        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        html,
        body {
            width: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: transparent;

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Arial,
                sans-serif;
        }

        #button-area {
            position: relative;
            width: 100%;
            height: 280px;
            overflow: hidden;
        }

        #no-button {
            position: absolute;
            top: 18px;
            left: calc(50% - 63px);

            width: 126px;
            min-height: 58px;
            padding: 9px 7px;

            border: none;
            border-radius: 17px;

            background: linear-gradient(
                135deg,
                #8e8e9a,
                #a8a8b2
            );

            color: white;
            font-size: 15px;
            font-weight: 750;
            line-height: 1.1;
            text-align: center;

            box-shadow:
                0 8px 20px rgba(100, 100, 115, 0.18);

            cursor: pointer;
            touch-action: none;
            user-select: none;
            -webkit-user-select: none;
            -webkit-touch-callout: none;

            transition:
                left 0.13s ease,
                top 0.13s ease;
        }
    </style>
</head>

<body>
    <div id="button-area">
        <button id="no-button" type="button">
            NO 😭
        </button>
    </div>

    <script>
        const noButton =
            document.getElementById("no-button");

        const buttonArea =
            document.getElementById("button-area");

        const messages = [
            "NO 😭",
            "Are you sure? 🥺",
            "Please? 💔",
            "Think again 😭",
            "Don't do this 🥹",
            "Choose YES! ❤️",
            "Wrong button 😂",
            "Not happening! 💕",
            "Nice try 😏",
            "Still NO? 🥲",
            "Just say YES 💖",
            "You can't catch me 😜"
        ];

        let attempts = 0;
        let recentlyMoved = false;


        function moveNoButton(event) {
            if (event) {
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
            }

            if (recentlyMoved) {
                return false;
            }

            recentlyMoved = true;

            const maximumX = Math.max(
                buttonArea.clientWidth -
                noButton.offsetWidth,
                0
            );

            const maximumY = Math.max(
                buttonArea.clientHeight -
                noButton.offsetHeight,
                0
            );

            const currentX = noButton.offsetLeft;
            const currentY = noButton.offsetTop;

            let newX = currentX;
            let newY = currentY;
            let tries = 0;

            do {
                newX = Math.random() * maximumX;
                newY = Math.random() * maximumY;
                tries += 1;
            }
            while (
                Math.hypot(
                    newX - currentX,
                    newY - currentY
                ) < 100 &&
                tries < 30
            );

            noButton.style.left = `${newX}px`;
            noButton.style.top = `${newY}px`;

            attempts += 1;

            noButton.textContent =
                messages[attempts % messages.length];

            noButton.style.pointerEvents = "none";

            window.setTimeout(function () {
                noButton.style.pointerEvents = "auto";
                recentlyMoved = false;
            }, 450);

            return false;
        }


        noButton.addEventListener(
            "mouseenter",
            moveNoButton,
            true
        );

        noButton.addEventListener(
            "pointerdown",
            moveNoButton,
            true
        );

        noButton.addEventListener(
            "pointerup",
            function (event) {
                event.preventDefault();
                event.stopPropagation();
            },
            true
        );

        noButton.addEventListener(
            "touchstart",
            moveNoButton,
            {
                passive: false,
                capture: true
            }
        );

        noButton.addEventListener(
            "touchend",
            function (event) {
                event.preventDefault();
                event.stopPropagation();
            },
            {
                passive: false,
                capture: true
            }
        );

        noButton.addEventListener(
            "click",
            function (event) {
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();

                if (!recentlyMoved) {
                    moveNoButton(event);
                }

                return false;
            },
            true
        );

        noButton.addEventListener(
            "contextmenu",
            function (event) {
                event.preventDefault();
            }
        );

        noButton.addEventListener(
            "dragstart",
            function (event) {
                event.preventDefault();
            }
        );
    </script>
</body>
</html>
""",
        height=290,
        scrolling=False,
    )


# --------------------------------------------------
# FOOD PAGE
# --------------------------------------------------
elif st.session_state.page == "food":

    st.markdown(
        """
<div class="page-heading">
    <div class="page-emoji">🍽️</div>
    <h1>What are we feeling?</h1>
    <p>Choose what you'd like to eat 💕</p>
</div>
""",
        unsafe_allow_html=True,
    )

    food_options = [
        ("🍕 Pizza", "Pizza 🍕"),
        ("🍣 Sushi", "Sushi 🍣"),
        ("🍔 Burgers", "Burgers 🍔"),
        ("🍜 Ramen", "Ramen 🍜"),
        ("🍝 Pasta", "Pasta 🍝"),
        ("🌮 Tacos", "Tacos 🌮"),
    ]

    first_column, second_column = st.columns(
        2,
        gap="small",
    )

    for index, (button_label, food_value) in enumerate(
        food_options
    ):
        chosen_column = (
            first_column
            if index % 2 == 0
            else second_column
        )

        with chosen_column:
            if st.button(
                button_label,
                key=f"food_{index}",
                use_container_width=True,
            ):
                st.session_state.food = food_value
                st.rerun()

    if st.session_state.food:
        selected_food = st.session_state.food

        food_preview = (
            '<div class="selection-card">'
            "<span>You chose</span>"
            f"<strong>{selected_food}</strong>"
            "</div>"
        )

        st.markdown(
            food_preview,
            unsafe_allow_html=True,
        )

        if st.button(
            "Continue 💖",
            key="continue_food",
            use_container_width=True,
            type="primary",
        ):
            change_page("schedule")

    st.markdown(
        '<div class="small-space"></div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "← Go back",
        key="back_home",
        use_container_width=True,
    ):
        st.session_state.food = None
        change_page("home")


# --------------------------------------------------
# DATE AND TIME PAGE
# --------------------------------------------------
elif st.session_state.page == "schedule":

    st.markdown(
        """
<div class="page-heading schedule-heading">
    <div class="page-emoji">🗓️</div>
    <h1>When are you free?</h1>
    <p>Choose our date and time ✨</p>
</div>
""",
        unsafe_allow_html=True,
    )

    selected_date = st.date_input(
        "Pick a date",
        value=st.session_state.selected_date,
        min_value=date.today(),
        format="DD/MM/YYYY",
        key="date_picker",
    )

    time_options = []

    for hour in range(10, 24):
        time_options.append(f"{hour:02d}:00")
        time_options.append(f"{hour:02d}:30")

    current_time = st.session_state.selected_time

    if current_time not in time_options:
        current_time = "19:00"

    selected_time = st.selectbox(
        "Pick a time",
        options=time_options,
        index=time_options.index(current_time),
        format_func=format_time,
        key="time_picker",
    )

    st.session_state.selected_date = selected_date
    st.session_state.selected_time = selected_time

    formatted_date = selected_date.strftime(
        "%A, %d %B %Y"
    )

    formatted_time = format_time(selected_time)

    preview_html = (
        '<div class="date-preview-card">'
        '<div class="preview-row">'
        '<span class="preview-icon">🗓️</span>'
        f"<strong>{formatted_date}</strong>"
        "</div>"
        '<div class="preview-row">'
        '<span class="preview-icon">⏰</span>'
        f"<strong>{formatted_time}</strong>"
        "</div>"
        "</div>"
    )

    st.markdown(
        preview_html,
        unsafe_allow_html=True,
    )

    if st.button(
        "Confirm our date 💖",
        key="confirm_date",
        use_container_width=True,
        type="primary",
    ):
        change_page("confirmed")

    if st.button(
        "← Change the food",
        key="back_food",
        use_container_width=True,
    ):
        change_page("food")


# --------------------------------------------------
# CONFIRMATION PAGE
# --------------------------------------------------
elif st.session_state.page == "confirmed":

    formatted_date = (
        st.session_state.selected_date.strftime(
            "%A, %d %B %Y"
        )
    )

    formatted_time = format_time(
        st.session_state.selected_time
    )

    selected_food = st.session_state.food

    st.balloons()

    st.markdown(
        """
<div class="final-heading">
    <div class="celebration-emoji">💖</div>
    <h1>It's a date!</h1>
    <p>I can't wait ✨</p>
</div>
""",
        unsafe_allow_html=True,
    )

    confirmation_html = (
        '<div class="final-card">'
        '<div class="final-row">'
        '<span class="final-icon">🍽️</span>'
        "<div>"
        "<small>Food</small>"
        f"<strong>{selected_food}</strong>"
        "</div>"
        "</div>"
        '<div class="final-row">'
        '<span class="final-icon">🗓️</span>'
        "<div>"
        "<small>Date</small>"
        f"<strong>{formatted_date}</strong>"
        "</div>"
        "</div>"
        '<div class="final-row">'
        '<span class="final-icon">⏰</span>'
        "<div>"
        "<small>Time</small>"
        f"<strong>{formatted_time}</strong>"
        "</div>"
        "</div>"
        "</div>"
    )

    st.markdown(
        confirmation_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------
    # PREPARE PLAN
    # --------------------------------------------------
    plan_text = (
        "It's a date! 💖\n\n"
        f"🍽️ Food: {selected_food}\n"
        f"🗓️ Date: {formatted_date}\n"
        f"⏰ Time: {formatted_time}\n\n"
        "See you then! ✨"
    )

    # --------------------------------------------------
    # GET WEB3FORMS SECRET SAFELY
    # --------------------------------------------------
    try:
        web3forms_access_key = st.secrets[
            "WEB3FORMS_ACCESS_KEY"
        ]
    except (KeyError, StreamlitSecretNotFoundError):
        web3forms_access_key = None

    # --------------------------------------------------
    # COPY AND EMAIL BUTTON
    # --------------------------------------------------
    if web3forms_access_key:
        access_key_json = json.dumps(
            web3forms_access_key
        )

        plan_json = json.dumps(plan_text)

        email_button_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <style>
        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        html,
        body {
            width: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: transparent;

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Arial,
                sans-serif;
        }

        .send-area {
            width: 100%;
            padding: 5px 0;
            text-align: center;
        }

        #send-plan-button {
            width: 100%;
            min-height: 60px;
            padding: 12px 18px;

            border: none;
            border-radius: 18px;

            background: linear-gradient(
                135deg,
                #f05b8a,
                #ed76a0
            );

            color: white;
            font-size: 17px;
            font-weight: 750;

            box-shadow:
                0 9px 22px rgba(255, 79, 135, 0.26);

            cursor: pointer;
            touch-action: manipulation;

            transition:
                transform 0.15s ease,
                opacity 0.15s ease;
        }

        #send-plan-button:hover {
            transform: translateY(-2px);
        }

        #send-plan-button:active {
            transform: scale(0.98);
        }

        #send-plan-button:disabled {
            cursor: default;
            opacity: 0.75;
            transform: none;
        }

        #send-result {
            min-height: 24px;
            margin: 10px 0 0;

            color: #684d58;
            font-size: 14px;
            font-weight: 650;
        }
    </style>
</head>

<body>
    <div class="send-area">
        <button id="send-plan-button" type="button">
            📋 Copy plan & email me 💌
        </button>

        <p id="send-result"></p>
    </div>

    <script>
        const accessKey = __ACCESS_KEY__;
        const plan = __PLAN__;

        const button =
            document.getElementById("send-plan-button");

        const result =
            document.getElementById("send-result");


        async function copyPlan() {
            try {
                if (
                    navigator.clipboard &&
                    window.isSecureContext
                ) {
                    await navigator.clipboard.writeText(plan);
                    return true;
                }

                const temporaryTextArea =
                    document.createElement("textarea");

                temporaryTextArea.value = plan;
                temporaryTextArea.style.position = "fixed";
                temporaryTextArea.style.opacity = "0";

                document.body.appendChild(
                    temporaryTextArea
                );

                temporaryTextArea.focus();
                temporaryTextArea.select();

                const copied =
                    document.execCommand("copy");

                temporaryTextArea.remove();

                return copied;

            } catch (error) {
                return false;
            }
        }


        async function emailPlan() {
            const response = await fetch(
                "https://api.web3forms.com/submit",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },

                    body: JSON.stringify({
                        access_key: accessKey,
                        subject:
                            "💖 A DateQuest plan was confirmed!",
                        from_name: "DateQuest",
                        name: "DateQuest guest",
                        message: plan
                    })
                }
            );

            const responseData = await response.json();

            if (!response.ok || !responseData.success) {
                throw new Error(
                    responseData.message ||
                    "The email could not be sent."
                );
            }
        }


        button.addEventListener(
            "click",
            async function () {
                if (button.disabled) {
                    return;
                }

                button.disabled = true;
                button.textContent =
                    "Sending our plan... 💌";

                result.textContent = "";

                const copied = await copyPlan();

                try {
                    await emailPlan();

                    button.textContent =
                        "Plan sent! 💖";

                    if (copied) {
                        result.textContent =
                            "Copied and emailed successfully ✨";
                    } else {
                        result.textContent =
                            "Email sent successfully 💌";
                    }

                } catch (error) {
                    button.disabled = false;

                    button.textContent =
                        "📋 Copy plan & email me 💌";

                    if (copied) {
                        result.textContent =
                            "Plan copied, but the email failed. Please try again.";
                    } else {
                        result.textContent =
                            "Something went wrong. Please try again.";
                    }
                }
            }
        );
    </script>
</body>
</html>
"""

        email_button_html = email_button_html.replace(
            "__ACCESS_KEY__",
            access_key_json,
        ).replace(
            "__PLAN__",
            plan_json,
        )

        components.html(
            email_button_html,
            height=115,
            scrolling=False,
        )

    else:
        st.warning(
            "The email service has not been configured."
        )

    if st.button(
        "Start again 💕",
        key="start_again",
        use_container_width=True,
    ):
        reset_app()