"""
K–2 Sight Word Flashcard App  (v3 – condensed + floral + large sentence)
=========================================================================
Run with:
    pip install streamlit
    streamlit run app.py
"""

import random
import streamlit as st

# ── Dolch Word Lists ────────────────────────────────────────────────

DOLCH_KINDERGARTEN = [
    "a","and","away","big","blue","can","come","down",
    "find","for","funny","go","help","here","I","in",
    "is","it","jump","little","look","make","me","my",
    "not","one","play","red","run","said","see","the",
    "three","to","two","up","we","where","yellow","you",
]

DOLCH_FIRST_GRADE = [
    "after","again","an","any","as","ask","by","could",
    "every","fly","from","give","going","had","has","her",
    "him","his","how","just","know","let","live","may",
    "of","old","once","open","over","put","round","some",
    "stop","take","thank","them","then","think","walk",
    "were","when","with",
]

KINDERGARTEN_SENTENCES: dict[str, list[str]] = {
    "a":["I see a dog.","We got a cat.","She has a hat.","He fed a pig."],
    "and":["You and I run.","Mom and Dad sit.","Cat and dog play.","Red and blue mix."],
    "away":["The cat ran away.","Run away from rain.","He went far away.","Birds fly away fast."],
    "big":["I see a big dog.","That is a big box.","We have a big bed.","Look at the big sun."],
    "blue":["The sky is blue.","I like blue pens.","We see blue fish.","My hat is blue."],
    "can":["I can hop fast.","We can play now.","You can help me.","She can run far."],
    "come":["Come sit with me.","Please come here.","Can you come play?","Come look at this."],
    "down":["Sit down on it.","The cat ran down.","Go down the hill.","We look down here."],
    "find":["Can you find me?","I find my hat.","Help me find it.","We find red bugs."],
    "for":["This is for you.","A hat for Dad.","We look for Mom.","One for me, please."],
    "funny":["That dog is funny.","You are so funny.","We see funny fish.","He told a funny one."],
    "go":["Let us go play.","We go to bed.","I go up the hill.","Can we go now?"],
    "help":["Please help me now.","I help my mom.","Can you help Dad?","We help at home."],
    "here":["Come sit here.","I am over here.","Look here at me.","Put it here, please."],
    "I":["I like to play.","I see a cat.","I run so fast.","I sit with Mom."],
    "in":["The dog is in bed.","Sit in the box.","We play in mud.","Look in the bag."],
    "is":["The cat is big.","Mom is at home.","It is fun here.","My dog is red."],
    "it":["Look at it go.","I like it a lot.","Can you see it?","We play with it."],
    "jump":["I jump up high.","We jump and play.","Can you jump far?","The frog can jump."],
    "little":["I see a little bug.","My little cat naps.","A little fish swims.","We pet the little dog."],
    "look":["Look at the sun.","We look for bugs.","Look at my dog.","Can you look here?"],
    "make":["We make a big fort.","I make my bed.","Let us make art.","Can you make one?"],
    "me":["Come play with me.","Help me find it.","Look at me jump.","Give it to me."],
    "my":["This is my dog.","I love my mom.","My hat is red.","Where is my bag?"],
    "not":["I am not sad.","It is not big.","We do not run.","That is not red."],
    "one":["I see one dog.","We have one cat.","Pick one for me.","Just one more, please."],
    "play":["We play in mud.","Can you play now?","I play with my dog.","Let us play a lot."],
    "red":["My hat is red.","I like red jam.","The red bug hops.","We see red fish."],
    "run":["I run so fast.","We run and play.","Can the dog run?","Run to the big tree."],
    "said":["Mom said to go.","He said sit here.","Dad said come now.","She said look up."],
    "see":["I see a big cat.","We see red birds.","Can you see me?","Look and see it."],
    "the":["I pet the dog.","We see the sun.","Run to the tree.","The cat sat down."],
    "three":["I see three cats.","We have three hats.","Look at three bugs.","Three fish swim here."],
    "to":["We go to bed.","Run to the tree.","Come to my home.","I like to play."],
    "two":["I see two dogs.","We have two cats.","Two birds fly up.","Pick two for me."],
    "up":["I jump up high.","Look up at birds.","We go up the hill.","The cat ran up."],
    "we":["We play and run.","Can we go now?","We like the sun.","We sit with Dad."],
    "where":["Where is my hat?","Where did it go?","Where do you sit?","Where is the dog?"],
    "yellow":["I see a yellow sun.","My yellow hat is big.","The yellow bus is here.","We like yellow birds."],
    "you":["I like you a lot.","Can you see me?","You are my pal.","Where did you go?"],
}

FIRST_GRADE_SENTENCES: dict[str, list[str]] = {
    "after":["We play after the rain stops.","The dog naps after his walk.","I eat lunch after math class.","Come find me after you look."],
    "again":["Read the story to me again.","Can we play that game again?","She sang the song again today.","Try to jump the rope again."],
    "an":["I ate an apple at lunch.","She drew an egg on paper.","We found an old shell outside.","He picked an orange from the tree."],
    "any":["Do you have any blue crayons?","We do not have any pets.","Are there any books on the shelf?","She did not pick any flowers."],
    "as":["She is as tall as her mom.","Run as fast as you can.","The cat sat as still as stone.","He smiled as the sun came up."],
    "ask":["Please ask your teacher for help.","I will ask Mom if we can go.","Did you ask him his name?","You should ask before you take it."],
    "by":["The school is by the park.","We walked by the old bridge.","She sat by her best friend.","The birds flew by our window."],
    "could":["We could play outside after lunch.","She could hear the birds singing.","They could not find the lost ball.","I could see the moon from bed."],
    "every":["We read a book every night.","She smiles at every new friend.","He runs every morning before school.","I brush my teeth every day."],
    "fly":["We saw birds fly over the lake.","The kite can fly very high.","I wish I could fly like birds.","Bees fly from flower to flower."],
    "from":["I got a letter from Grandma.","The ball rolled from the hill.","We walked home from the park.","She came from across the street."],
    "give":["Please give me your pencil.","They give food to the birds.","I will give this book to Mom.","Can you give the dog a treat?"],
    "going":["We are going to the store.","She is going home after school.","They are going to swim today.","I am going to read my book."],
    "had":["We had fun at the park today.","She had a red hat on her head.","They had three cats at home.","I had milk and toast for lunch."],
    "has":["She has a new pair of shoes.","The dog has a long brown tail.","My friend has two baby brothers.","He has a book about the stars."],
    "her":["She put her coat on the hook.","Give the book back to her.","I walked with her to the park.","Her dog likes to dig in sand."],
    "him":["I gave the ball back to him.","Tell him to come inside now.","She helped him tie his shoes.","We asked him to play with us."],
    "his":["He left his hat on the bus.","The boy ate his lunch at school.","His dog sits by the front door.","She found his missing red crayon."],
    "how":["Do you know how to draw a cat?","Show me how to tie my shoes.","I wonder how birds learn to fly.","Tell me how you made that cake."],
    "just":["I just saw a rabbit in the yard.","We just got home from the store.","She just started reading that book.","He just turned seven years old."],
    "know":["I know how to ride a bike.","Do you know where the park is?","They know the way back home.","We know all the words to that song."],
    "let":["Please let me help you carry that.","Let the cat come back inside.","Will you let us play outside?","Mom let me stay up a bit late."],
    "live":["We live near a big green park.","Birds live in nests in the trees.","They live on a quiet little street.","I want to live by the sea."],
    "may":["You may pick one treat from here.","May I borrow your blue pencil?","She may come with us to the park.","We may see the sunrise from here."],
    "of":["She has a bag of red apples.","I drank a cup of warm milk.","We saw a lot of fish today.","He ate a piece of bread."],
    "old":["The old tree has big long branches.","She reads an old book every night.","We found an old coin in the dirt.","That old dog sleeps all day long."],
    "once":["I once saw a fox near the creek.","She visits her grandma once a week.","We once had a fish named Bubbles.","He once ran all the way to school."],
    "open":["Please open the window for fresh air.","Can you open this jar for me?","She will open her gift after lunch.","We open our books to page ten."],
    "over":["The ball went over the tall fence.","Birds fly over the lake at dawn.","Come over to my house after school.","She jumped over the puddle on the path."],
    "put":["Please put your shoes by the door.","He put the book back on the shelf.","She put a flower in her hair.","I put my lunch in my backpack."],
    "round":["The ball is big and round.","We walked round the pond at school.","She drew a round face with a smile.","The moon looks full and round tonight."],
    "some":["May I have some water, please?","We picked some flowers in the garden.","She gave me some of her grapes.","There are some birds on the fence."],
    "stop":["Please stop running in the hallway.","The bus will stop at the next corner.","We need to stop and look both ways.","He did not stop to rest at all."],
    "take":["Please take your coat when you leave.","I will take the dog for a walk.","Can you take this to your teacher?","She wants to take her time drawing."],
    "thank":["I want to thank you for your help.","We should thank the teacher for the trip.","She wrote a thank you note today.","Please thank him for the nice gift."],
    "them":["I gave the crayons back to them.","Tell them to meet us at the park.","We played with them after school today.","She helped them clean up the room."],
    "then":["We ate lunch and then went outside.","First read the book, then draw a picture.","He woke up and then brushed his teeth.","She ran fast and then sat to rest."],
    "think":["I think the answer is seven.","Do you think it will rain today?","She stopped to think before she spoke.","We think this game is really fun."],
    "walk":["We walk to school on sunny days.","The dog loves to walk in the park.","She takes a walk every morning.","I like to walk by the creek."],
    "were":["They were happy to see us today.","We were late to school this morning.","The flowers were blooming in the garden.","Her shoes were muddy from the rain."],
    "when":["Tell me when you are ready to go.","We sing a song when the bell rings.","She smiles when her friends wave hello.","I feel happy when the sun is out."],
    "with":["I like to draw with bright colors.","She played with her friends after lunch.","Come sit with us at the big table.","He shared his lunch with a new friend."],
}

# ── Helper ──────────────────────────────────────────────────────────

def generate_deck(grade: str, n: int) -> list[dict[str, str]]:
    word_list = DOLCH_KINDERGARTEN if grade == "Kindergarten" else DOLCH_FIRST_GRADE
    sentences  = KINDERGARTEN_SENTENCES if grade == "Kindergarten" else FIRST_GRADE_SENTENCES
    chosen = random.sample(word_list, min(n, len(word_list)))
    return [
        {"word": w, "sentence": random.choice(sentences.get(w, [f"I see {w}."]))}
        for w in chosen
    ]

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(page_title="Sight Word Flashcards", page_icon="🌸", layout="centered")

# ── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

/* ── Floral SVG background ─────────────────────────────────────────
   Inline SVG pattern: repeating daisies + leaves, soft pastel tones  */
html, body, .stApp {
    font-family: 'Nunito', sans-serif;
    background-color: #fdf6ff;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3C!-- stem --%3E%3Cline x1='60' y1='120' x2='60' y2='72' stroke='%23a8d5a2' stroke-width='2.5'/%3E%3C!-- leaves --%3E%3Cellipse cx='48' cy='90' rx='10' ry='5' fill='%23b8e0b2' transform='rotate(-30 48 90)'/%3E%3Cellipse cx='72' cy='85' rx='10' ry='5' fill='%23b8e0b2' transform='rotate(30 72 85)'/%3E%3C!-- petals --%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fbc4d7'/%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fbc4d7' transform='rotate(45 60 60)'/%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fce4b0' transform='rotate(90 60 60)'/%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fce4b0' transform='rotate(135 60 60)'/%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fbc4d7' transform='rotate(180 60 60)'/%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fbc4d7' transform='rotate(225 60 60)'/%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fce4b0' transform='rotate(270 60 60)'/%3E%3Cellipse cx='60' cy='52' rx='6' ry='12' fill='%23fce4b0' transform='rotate(315 60 60)'/%3E%3C!-- center --%3E%3Ccircle cx='60' cy='60' r='8' fill='%23fde68a'/%3E%3Ccircle cx='60' cy='60' r='4' fill='%23f59e0b'/%3E%3C/svg%3E");
    background-size: 120px 120px;
}

/* Frosted panel so content is readable over the pattern */
.block-container {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    border-radius: 24px;
    padding: 1.2rem 1rem 1.5rem !important;
    max-width: 500px !important;
    margin: 1rem auto !important;
}

/* ── Title ──────────────────────────────────────────────────────── */
.app-title {
    text-align: center;
    font-size: clamp(1.2rem, 5vw, 1.6rem);
    font-weight: 800;
    color: #6b21a8;
    margin: 0 0 0.1rem;
}
.app-subtitle {
    text-align: center;
    font-size: clamp(0.75rem, 3vw, 0.88rem);
    color: #9333ea;
    margin: 0 0 0.8rem;
}

/* ── Compact controls row ───────────────────────────────────────── */
/* Grade selector + Generate sit side by side; slider below */
.compact-controls {
    display: flex;
    gap: 0.5rem;
    align-items: flex-end;
    margin-bottom: 0.4rem;
}

/* ── Progress ───────────────────────────────────────────────────── */
.progress-label {
    text-align: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: #7c3aed;
    margin: 0.5rem 0 0.15rem;
}
/* Make Streamlit progress bar thicker + purple */
div[data-testid="stProgressBar"] > div {
    height: 10px !important;
    border-radius: 999px;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #a855f7, #6366f1) !important;
    border-radius: 999px;
}

/* ── Flashcard ──────────────────────────────────────────────────── */
.flashcard {
    width: 100%;
    min-height: clamp(190px, 42vw, 260px);
    border-radius: 22px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: clamp(1.2rem, 5vw, 2rem) clamp(1rem, 4vw, 1.8rem);
    margin: 0.6rem 0 0.5rem;
    user-select: none;
    animation: cardIn 0.28s ease;
}
@keyframes cardIn {
    from { opacity:0; transform:scale(0.95) translateY(6px); }
    to   { opacity:1; transform:scale(1)    translateY(0);   }
}
.card-word {
    background: linear-gradient(135deg, #3730a3 0%, #6366f1 100%);
    box-shadow: 0 8px 28px rgba(99,102,241,0.4);
}
.card-sentence {
    background: linear-gradient(135deg, #92400e 0%, #f59e0b 100%);
    box-shadow: 0 8px 28px rgba(245,158,11,0.4);
}
.card-word-text {
    font-size: clamp(3.2rem, 15vw, 5.5rem);
    font-weight: 800;
    color: #fff;
    line-height: 1.05;
    text-align: center;
}
/* ── LARGE sentence text (key fix) ─────────────────────────────── */
.card-sentence-text {
    font-size: clamp(1.6rem, 6.5vw, 2.2rem);   /* ← was 1.2–1.7rem, now 1.6–2.2rem */
    font-weight: 700;
    color: #fff;
    line-height: 1.5;
    text-align: center;
}
.card-badge {
    font-size: clamp(0.65rem, 2.5vw, 0.78rem);
    font-weight: 700;
    color: rgba(255,255,255,0.75);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.card-hint {
    font-size: clamp(0.65rem, 2vw, 0.78rem);
    color: rgba(255,255,255,0.55);
    margin-top: 0.8rem;
}

/* ── Flip button — visually dominant ───────────────────────────── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    border: none !important;
    color: #fff !important;
    font-size: clamp(0.9rem, 3.5vw, 1.05rem) !important;
    font-weight: 800 !important;
    border-radius: 14px !important;
    padding: 0.55rem 0 !important;
}

/* Nav + secondary buttons */
div.stButton > button {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    border-radius: 12px;
    font-size: clamp(0.82rem, 3vw, 0.95rem);
}

/* ── Completion banner ──────────────────────────────────────────── */
.done-banner {
    text-align: center;
    background: linear-gradient(135deg, #059669, #34d399);
    border-radius: 16px;
    padding: 1rem;
    color: #fff;
    font-size: clamp(0.95rem, 4vw, 1.15rem);
    font-weight: 800;
    margin: 0.75rem 0 0;
    animation: cardIn 0.4s ease;
}

/* ── Mobile ─────────────────────────────────────────────────────── */
@media (max-width: 420px) {
    .block-container { border-radius: 0 !important; margin: 0 auto !important; }
    .flashcard { min-height: 170px; }
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div class="app-title">🌸 Sight Word Flashcards</div>
<div class="app-subtitle">Dolch Kindergarten &amp; 1st-Grade Lists</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────
DEFAULTS = {"grade": "Kindergarten", "num_words": 20, "index": 0, "flipped": False, "deck": None}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v
if st.session_state.deck is None:
    st.session_state.deck = generate_deck("Kindergarten", 20)

# ── Condensed controls: grade + button on one row, slider below ───────
ctrl_left, ctrl_right = st.columns([3, 2], gap="small")
with ctrl_left:
    grade = st.selectbox(
        "Grade",
        ["Kindergarten", "1st Grade"],
        index=0 if st.session_state.grade == "Kindergarten" else 1,
        label_visibility="collapsed",
    )
with ctrl_right:
    gen_clicked = st.button("🔀 New Deck", use_container_width=True, type="primary")

max_words = len(DOLCH_KINDERGARTEN if grade == "Kindergarten" else DOLCH_FIRST_GRADE)
num_words = st.slider(
    "Words", min_value=5, max_value=max_words,
    value=min(st.session_state.num_words, max_words),
    label_visibility="collapsed",
)

if gen_clicked:
    st.session_state.deck      = generate_deck(grade, num_words)
    st.session_state.index     = 0
    st.session_state.flipped   = False
    st.session_state.grade     = grade
    st.session_state.num_words = num_words
    st.rerun()

# ── Card display ──────────────────────────────────────────────────────
deck  = st.session_state.deck
idx   = st.session_state.index
card  = deck[idx]
total = len(deck)

# Progress bar
st.markdown(f'<div class="progress-label">Card {idx+1} of {total}</div>', unsafe_allow_html=True)
st.progress((idx + 1) / total)

grade_badge = "🌱 Kindergarten" if st.session_state.grade == "Kindergarten" else "⭐ 1st Grade"

if st.session_state.flipped:
    st.markdown(f"""
    <div class="flashcard card-sentence">
        <div class="card-badge">{grade_badge}</div>
        <div class="card-sentence-text">{card['sentence']}</div>
        <div class="card-hint">tap · flip to word</div>
    </div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="flashcard card-word">
        <div class="card-word-text">{card['word']}</div>
        <div class="card-hint">tap · flip to sentence</div>
    </div>""", unsafe_allow_html=True)

# ── Flip button (full width, most prominent) ──────────────────────────
flip_label = "🔄 Show Word" if st.session_state.flipped else "🔄 Show Sentence"
if st.button(flip_label, use_container_width=True, type="primary"):
    st.session_state.flipped = not st.session_state.flipped
    st.rerun()

# ── Prev / Next on one row ────────────────────────────────────────────
prev_col, next_col = st.columns(2, gap="small")
with prev_col:
    if st.button("⬅ Prev", use_container_width=True, disabled=(idx == 0)):
        st.session_state.index  -= 1
        st.session_state.flipped = False
        st.rerun()
with next_col:
    if st.button("Next ➡", use_container_width=True, disabled=(idx >= total - 1)):
        st.session_state.index  += 1
        st.session_state.flipped = False
        st.rerun()

# ── Completion ────────────────────────────────────────────────────────
if idx == total - 1:
    st.markdown("""
    <div class="done-banner">🎉 Deck complete! Tap New Deck to play again.</div>
    """, unsafe_allow_html=True)
    st.balloons()
