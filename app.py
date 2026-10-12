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
            "I have the best words.",
            "Part of the beauty of me is that I am very rich.",
            "I'm like, really smart. And a very stable genius!",
            "My fingers are long and beautiful, as, it has been well documented, are various other parts of my body.",
            "I've always had a great relationship with science. I understand it better than most scientists.",
        ],
        "fake": [
            "I invented the internet. Google thanked me.",
            "The pyramids were built to store Trump steaks.",
            "I've read every book ever written. Twice.",
            "Climate change is just the Earth sweating from excitement.",
            "I can speak 47 languages. I just choose not to.",
            "I personally invented the cheeseburger. McDonald's knows it.",
            "My hair is actually alive. It whispers strategy to me.",
            "I once arm-wrestled a shark. The shark apologized.",
            "The sun rises earlier when I'm awake. It wants to see me.",
            "I've been to space. Didn't tell anyone. Very impressive up there.",
            "Sharks are fake news. Nobody has ever actually seen one.",
            "I don't sleep. I just close my eyes and negotiate.",
            "I once bench-pressed the Statue of Liberty. She was grateful.",
            "I invented the concept of winning. Nobody had done it before me.",
            "The moon asked me to build a resort there. We're still negotiating.",
        ]
    },
    "Keanu": {
        "real": [
            "The simple act of paying attention can take you a long way.",
            "Every struggle in your life has shaped you into the person you are today.",
            "None of us are getting out of here alive, so please stop treating yourself like an afterthought.",
            "Multi-culture is the real culture of the world.",
            "Grief changes shape, but it never ends.",
            "I'm at the point in my life where I just want to be happy.",
            "It's fun to be hopelessly in love. It's dangerous, but it's fun.",
            "Sometimes enemies are our best teachers.",
        ],
        "fake": [
            "I once meditated for 48 hours straight on a bus to nowhere.",
            "The Matrix is just a documentary of my real life.",
            "I don't eat food. I absorb happiness directly from strangers.",
            "Time is a flat circle, and I am its circumference.",
            "I have never aged. I simply refuse.",
            "Every morning I wake up and choose to be breathtaking.",
            "I communicate with dogs telepathically. They always agree with me.",
            "Neo was based on me. The Wachowskis still owe me royalties.",
        ]
    },
    "Elon": {
        "real": [
            "When something is important enough, you do it even if the odds are not in your favor.",
            "Failure is an option here. If things are not failing, you are not innovating enough.",
            "I think it's very important to have a feedback loop.",
            "Life is too short for long-term grudges.",
            "Work like hell. I mean you just have to put in 80 to 100 hour weeks every week.",
            "I think it is possible for ordinary people to choose to be extraordinary.",
            "People work better when they know what the goal is and why.",
            "If you get up in the morning and think the future is going to be better, it is a bright day.",
        ],
        "fake": [
            "I personally built the first Tesla with my bare hands in a Walmart parking lot.",
            "Mars is just Earth's backup drive. I'm the IT guy.",
            "I communicate exclusively via meme for efficiency.",
            "Money is just compressed freedom. I have a lot of freedom.",
            "I bought Twitter because the memes weren't loading fast enough.",
            "I named my child X Æ A-12 as a typo. It felt right.",
            "Sleep is for people who haven't optimized their schedule.",
            "I have solved every problem except boredom. I'm working on it.",
        ]
    },
    "Pope": {
        "real": [
            "Who am I to judge?",
            "The Lord never tires of forgiving. It is we who tire of asking for forgiveness.",
            "You cannot fully understand yourself if you do not listen to others.",
            "Corruption is not an act, it is a condition — a condition of the soul.",
            "Tenderness is not weakness; it is fortitude.",
            "A little bit of mercy makes the world less cold and more just.",
            "The Earth, our home, is beginning to look more and more like an immense pile of filth.",
            "Do not be men and women of sadness.",
            "We must not be afraid of dialogue.",
        ],
        "fake": [
            "I once beat a cardinal at arm wrestling. God willed it.",
            "Heaven has a VIP section. I have the list.",
            "I tried pizza for the first time last week. I've been making a huge mistake.",
            "Confession is basically free therapy. Spread the word.",
            "I Googled myself once. It was humbling.",
            "The Pope-mobile gets surprisingly good mileage for its size.",
            "God invented coffee. Of that I am completely certain.",
            "I have never lost a prayer. Not once.",
        ]
    },
    "Dalai": {
        "real": [
            "The purpose of our lives is to be happy.",
            "My religion is very simple. My religion is kindness.",
            "Remember that sometimes not getting what you want is a wonderful stroke of luck.",
            "If you think you are too small to make a difference, try sleeping with a mosquito.",
            "The more you are motivated by love, the more fearless and free your action will be.",
            "Do not let the behavior of others destroy your inner peace.",
            "Love and compassion are necessities, not luxuries. Without them, humanity cannot survive.",
            "Happiness is not something ready-made. It comes from your own actions.",
            "An open heart is an open mind.",
        ],
        "fake": [
            "I have never lost a staring contest. Not once.",
            "Enlightenment tastes like warm yak butter tea. I would know.",
            "Reincarnation is just nature's way of doing a software update.",
            "I once meditated for so long that I accidentally invented a new color.",
            "I have watched every episode of The Office. Twice. Very instructive.",
            "The key to enlightenment is excellent posture.",
            "I once forgot what day it was. It was the most peaceful week of my life.",
            "I laugh at everything. It is cheaper than therapy and more effective.",
        ]
    },
    "Churchill": {
        "real": [
            "I am fond of pigs. Dogs look up to us. Cats look down on us. Pigs treat us as equals.",
            "The best argument against democracy is a five-minute conversation with the average voter.",
            "I may be drunk, Miss, but in the morning I will be sober and you will still be ugly.",
            "A fanatic is one who can't change his mind and won't change the subject.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "You have enemies? Good. That means you've stood up for something, sometime in your life.",
            "Courage is what it takes to stand up and speak; courage is also what it takes to sit down and listen.",
            "History will be kind to me, for I intend to write it.",
            "We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields.",
        ],
        "fake": [
            "I once punched a horse. It apologized.",
            "History will be kind to me, for I intend to write it — and also burn the other drafts.",
            "A good cigar is like a good speech: nobody wants it to end, but everyone is relieved when it does.",
            "I have defeated armies, nations, and my doctor's advice. In that order.",
            "I have never lost a game of chess. I simply choose not to play.",
            "My greatest battle was with my tailor. He still hasn't recovered.",
            "A good night's sleep is for people without enough whiskey.",
            "I once gave a speech so powerful that three enemy generals switched sides mid-sentence.",
        ]
    },
    "Napoleon": {
        "real": [
            "Never interrupt your enemy when he is making a mistake.",
            "Impossible is a word found only in the dictionary of fools.",
            "In politics, stupidity is not a handicap.",
            "A leader is a dealer in hope.",
            "The reason most people fail instead of succeed is they trade what they want most for what they want at the moment.",
            "Four hostile newspapers are more to be feared than a thousand bayonets.",
            "A soldier will fight long and hard for a bit of colored ribbon.",
            "The battlefield is a scene of constant chaos. The winner will be the one who controls that chaos.",
            "You don't reason with intellectuals. You shoot them.",
        ],
        "fake": [
            "I am not short. Everyone else is simply too tall.",
            "I once looked in a mirror and the mirror flinched.",
            "Every great empire begins with a good pastry. Mine began with a croissant.",
            "History is written by the victors. I wrote mine in advance, just to be safe.",
            "My greatest regret is not inventing the baguette. Someone else got there first.",
            "I once conquered a room just by entering it. The room never fully recovered.",
            "Height is a state of mind. In my mind I am enormous.",
            "I have never lost a battle I actually cared about. The others were practice.",
        ]
    },
    "Tesla": {
        "real": [
            "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration.",
            "The scientists of today think deeply instead of clearly. One must be sane to think clearly, but one can think deeply and be quite insane.",
            "I don't care that they stole my idea. I care that they don't have any of their own.",
            "Be alone, that is the secret of invention; be alone, that is when ideas are born.",
            "Of all things, I liked books best.",
            "The present is theirs; the future, for which I really worked, is mine.",
            "Our virtues and our failings are inseparable, like force and matter.",
            "The day science begins to study non-physical phenomena, it will make more progress in one decade than in all previous centuries.",
            "Let the future tell the truth and evaluate each one according to his work and accomplishments.",
        ],
        "fake": [
            "I once stared at a lightbulb for six hours. It blinked first.",
            "Sleep is just charging. I prefer to stay at 1%.",
            "Pigeons are my closest friends. Humans are mostly background noise.",
            "I have held a lightning bolt in my bare hands. It felt like shaking hands with God.",
            "I once powered an entire city with my mind. Nobody believed me. They were right.",
            "Lightning is just the sky winking at me.",
            "I have never shaken hands with Edison. My standards are too high.",
            "I invented a machine that could hear the thoughts of cats. The results were troubling.",
        ]
    },
    "Wilde": {
        "real": [
            "I can resist everything except temptation.",
            "We are all in the gutter, but some of us are looking at the stars.",
            "I am not young enough to know everything.",
            "To lose one parent may be regarded as a misfortune; to lose both looks like carelessness.",
            "The truth is rarely pure and never simple.",
            "Always forgive your enemies; nothing annoys them so much.",
            "A cynic is a man who knows the price of everything and the value of nothing.",
            "Consistency is the last refuge of the unimaginative.",
            "The only way to get rid of a temptation is to yield to it.",
        ],
        "fake": [
            "I once attended my own funeral just to critique the floral arrangements.",
            "Fashion is a form of ugliness so intolerable that we have to alter it every six months.",
            "I have nothing to declare except my genius — and also this suitcase full of velvet.",
            "A man who moralizes is usually a hypocrite, and a woman who moralizes is invariably plain.",
            "I once attended a party so dull I left before I arrived.",
            "My wardrobe costs more than most countries' GDP. I regret nothing.",
            "I have never met a bore I couldn't out-bore.",
            "The only thing worse than being talked about is not being talked about — unless they are boring about it.",
        ]
    }
}

PERSON_DISPLAY = {
    "Trump": "Donald Trump",
    "Keanu": "Keanu Reeves",
    "Elon": "Elon Musk",
    "Pope": "Pave Frans",
    "Dalai": "Dalai Lama",
    "Churchill": "Winston Churchill",
    "Napoleon": "Napoleon Bonaparte",
    "Tesla": "Nikola Tesla",
    "Wilde": "Oscar Wilde",
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
