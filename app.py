import random
import secrets
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

quotes = {
    "Trump": {
        "real": [
            "I'm the best thing that's ever happened to the Republican Party.",
            "Nobody respects women more than I do. Nobody.",
            "I have a great relationship with the blacks.",
            "Wind is a very deceiving thing. It's very deceiving.",
            "I know more about ISIS than the generals do, believe me.",
        ],
        "fake": [
            "I invented the internet. Google thanked me.",
            "The pyramids were built to store Trump steaks.",
            "I've read every book ever written. Twice.",
            "Climate change is just the Earth sweating from excitement.",
        ]
    },
    "Keanu": {
        "real": [
            "The simple act of paying attention can take you a long way.",
            "Every struggle in your life has shaped you into the person you are today.",
            "None of us are getting out of here alive, so please stop treating yourself like an afterthought.",
            "Multi-culture is the real culture of the world.",
        ],
        "fake": [
            "I once meditated for 48 hours straight on a bus to nowhere.",
            "The Matrix is just a documentary of my real life.",
            "I don't eat food. I absorb happiness directly from strangers.",
            "Time is a flat circle, and I am its circumference.",
        ]
    },
    "Elon": {
        "real": [
            "When something is important enough, you do it even if the odds are not in your favor.",
            "Failure is an option here. If things are not failing, you are not innovating enough.",
            "I think it's very important to have a feedback loop.",
            "Life is too short for long-term grudges.",
        ],
        "fake": [
            "I personally built the first Tesla with my bare hands in a Walmart parking lot.",
            "Mars is just Earth's backup drive. I'm the IT guy.",
            "I communicate exclusively via meme for efficiency.",
            "Money is just compressed freedom. I have a lot of freedom.",
        ]
    }
}

PERSON_DISPLAY = {
    "Trump": "Donald Trump",
    "Keanu": "Keanu Reeves",
    "Elon": "Elon Musk",
}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    citation = None
    person_display = None
    score = session.get("score", {"correct": 0, "total": 0})

    if request.method == "POST":
        action = request.form.get("action")

        if action == "select_person":
            selected_person = request.form.get("person")
            if selected_person in quotes:
                real = random.choice([True, False])
                pool = quotes[selected_person]["real" if real else "fake"]
                citation = random.choice(pool)
                session["current_quote"] = citation
                session["current_real"] = real
                session["current_person"] = selected_person

        elif action == "guess":
            citation = session.get("current_quote")
            real = session.get("current_real")
            selected_person = session.get("current_person")
            guess = request.form.get("guess")

            if citation and real is not None and guess in ("True", "False"):
                correct = (guess == "True") == real
                result = "Korrekt!" if correct else "Forkert! Det var {}.".format(
                    "sandt" if real else "falsk"
                )
                score["total"] += 1
                if correct:
                    score["correct"] += 1
                session["score"] = score
                session.pop("current_quote", None)
                session.pop("current_real", None)
                session.pop("current_person", None)

        elif action == "reset":
            session.clear()
            score = {"correct": 0, "total": 0}

        if not citation and not result:
            selected_person = session.get("current_person")
            citation = session.get("current_quote")

        if selected_person := session.get("current_person"):
            person_display = PERSON_DISPLAY.get(selected_person, selected_person)

    return render_template(
        "index.html",
        citation=citation,
        result=result,
        person_display=person_display,
        score=score,
        persons=PERSON_DISPLAY,
    )

if __name__ == "__main__":
    app.run(debug=True)
