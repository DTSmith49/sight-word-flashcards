"""
K–2 Sight Word Flashcard App  (v2 – mobile-optimised)
======================================================
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

# ── Sentences (no prefix needed — grade is tracked separately) ──────

KINDERGARTEN_SENTENCES: dict[str, list[str]] = {
    "a":      ["I see a dog.","We got a cat.","She has a hat.","He fed a pig."],
    "and":    ["You and I run.","Mom and Dad sit.","Cat and dog play.","Red and blue mix."],
    "away":   ["The cat ran away.","Run away from rain.","He went far away.","Birds fly away fast."],
    "big":    ["I see a big dog.","That is a big box.","We have a big bed.","Look at the big sun."],
    "blue":   ["The sky is blue.","I like blue pens.","We see blue fish.","My hat is blue."],
    "can":    ["I can hop fast.","We can play now.","You can help me.","She can run far."],
    "come":   ["Come sit with me.","Please come here.","Can you come play?","Come look at this."],
    "down":   ["Sit down on it.","The cat ran down.","Go down the hill.","We look down here."],
    "find":   ["Can you find me?","I find my hat.","Help me find it.","We find red bugs."],
    "for":    ["This is for you.","A hat for Dad.","We look for Mom.","One for me, please."],
    "funny":  ["That dog is funny.","You are so funny.","We see funny fish.","He told a funny one."],
    "go":     ["Let us go play.","We go to bed.","I go up the hill.","Can we go now?"],
    "help":   ["Please help me now.","I help my mom.","Can you help Dad?","We help at home."],
    "here":   ["Come sit here.","I am over here.","Look here at me.","Put it here, please."],
    "I":      ["I like to play.","I see a cat.","I run so fast.","I sit with Mom."],
    "in":     ["The dog is in bed.","Sit in the box.","We play in mud.","Look in the bag."],
    "is":     ["The cat is big.","Mom is at home.","It is fun here.","My dog is red."],
    "it":     ["Look at it go.","I like it a lot.","Can you see it?","We play with it."],
    "jump":   ["I jump up high.","We jump and play.","Can you jump far?","The frog can jump."],
    "little": ["I see a little bug.","My little cat naps.","A little fish swims.","We pet the little dog."],
    "look":   ["Look at the sun.","We look for bugs.","Look at my dog.","Can you look here?"],
    "make":   ["We make a big fort.","I make my bed.","Let us make art.","Can you make one?"],
    "me":     ["Come play with me.","Help me find it.","Look at me jump.","Give it to me."],
    "my":     ["This is my dog.","I love my mom.","My hat is red.","Where is my bag?"],
    "not":    ["I am not sad.","It is not big.","We do not run.","That is not red."],
    "one":    ["I see one dog.","We have one cat.","Pick one for me.","Just one more, please."],
    "play":   ["We play in mud.","Can you play now?","I play with my dog.","Let us play a lot."],
    "red":    ["My hat is red.","I like red jam.","The red bug hops.","We see red fish."],
    "run":    ["I run so fast.","We run and play.","Can the dog run?","Run to the big tree."],
    "said":   ["Mom said to go.","He said sit here.","Dad said come now.","She said look up."],
    "see":    ["I see a big cat.","We see red birds.","Can you see me?","Look and see it."],
    "the":    ["I pet the dog.","We see the sun.","Run to the tree.","The cat sat down."],
    "three":  ["I see three cats.","We have three hats.","Look at three bugs.","Three fish swim here."],
    "to":     ["We go to bed.","Run to the tree.","Come to my home.","I like to play."],
    "two":    ["I see two dogs.","We have two cats.","Two birds fly up.","Pick two for me."],
    "up":     ["I jump up high.","Look up at birds.","We go up the hill.","The cat ran up."],
    "we":     ["We play and run.","Can we go now?","We like the sun.","We sit with Dad."],
    "where":  ["Where is my hat?","Where did it go?","Where do you sit?","Where is the dog?"],
    "yellow": ["I see a yellow sun.","My yellow hat is big.","The yellow bus is here.","We like yellow birds."],
    "you":    ["I like you a lot.","Can you see me?","You are my pal.","Where did you go?"],
}

FIRST_GRADE_SENTENCES: dict[str, list[str]] = {
    "after":  ["We play after the rain stops.","The dog naps after his walk.","I eat lunch after math class.","Come find me after you look."],
    "again":  ["Read the story to me again.","Can we play that game again?","She sang the song again today.","Try to jump the rope again."],
    "an":     ["I ate an apple at lunch.","She drew an egg on paper.","We found an old shell outside.","He picked an orange from the tree."],
    "any":    ["Do you have any blue crayons?","We do not have any pets.","Are there any books on the shelf?","She did not pick any flowers."],
    "as":     ["She is as tall as her mom.","Run as fast as you can.","The cat sat as still as stone.","He smiled as the sun came up."],
    "ask":    ["Please ask your teacher for help.","I will ask Mom if we can go.","Did you ask him his name?","You should ask before you take it."],
    "by":     ["The school is by the park.","We walked by the old bridge.","She sat by her best friend.","The birds flew by our window."],
    "could":  ["We could play outside after lunch.","She could hear the birds singing.","They could not find the lost ball.","I could see the moon from bed."],
    "every":  ["We read a book every night.","She smiles at every new friend.","He runs every morning before school.","I brush my teeth every day."],
    "fly":    ["We saw birds fly over the lake.","The kite can fly very high.","I wish I could fly like birds.","Bees fly from flower to flower."],
    "from":   ["I got a letter from Grandma.","The ball rolled from the hill.","We walked home from the park.","She came from across the street."],
    "give":   ["Please give me your pencil.","They give food to the birds.","I will give this book to Mom.","Can you give the dog a treat?"],
    "going":  ["We are going to the store.","She is going home after school.","They are going to swim today.","I am going to read my book."],
    "had":    ["We had fun at the park today.","She had a red hat on her head.","They had three cats at home.","I had milk and toast for lunch."],
    "has":    ["She has a new pair of shoes.","The dog has a long brown tail.","My friend has two baby brothers.","He has a book about the stars."],
    "her":    ["She put her coat on the hook.","Give the book back to her.","I walked with her to the park.","Her dog likes to dig in sand."],
    "him":    ["I gave the ball back to him.","Tell him to come inside now.","She helped him tie his shoes.","We asked him to play with us."],
    "his":    ["He left his hat on the bus.","The boy ate his lunch at school.","His dog sits by the front door.","She found his missing red crayon."],
    "how":    ["Do you know how to draw a cat?","Show me how to tie my shoes.","I wonder how birds learn to fly.","Tell me how you made that cake."],
    "just":   ["I just saw a rabbit in the yard.","We just got home from the store.","She just started reading that book.","He just turned seven years old."],
    "know":   ["I know how to ride a bike.","Do you know where the park is?","They know the way back home.","We know all the words to that song."],
    "let":    ["Please let me help you carry that.","Let the cat come back inside.","Will you let us play outside?","Mom let me stay up a bit late."],
    "live":   ["We live near a big green park.","Birds live in nests in the trees.","They live on a quiet little street.","I want to live by the sea."],
    "may":    ["You may pick one treat from here.","May I borrow your blue pencil?","She may come with us to the park.","We may see the sunrise from here."],
    "of":     ["She has a bag of red apples.","I drank a cup of warm milk.","We saw a lot of fish today.","He ate a piece of bread."],
    "old":    ["The old tree has big long branches.","She reads an old book every night.","We found an old coin in the dirt.","That old dog sleeps all day long."],
    "once":   ["I once saw a fox near the creek.","She visits her grandma once a week.","We once had a fish named Bubbles.","He once ran all the way to school."],
    "open":   ["Please open the window for fresh air.","Can you open this jar for me?","She will open her gift after lunch.","We open our books to page ten."],
    "over":   ["The ball went over the tall fence.","Birds fly over the lake at dawn.","Come over to my house after school.","She jumped over the puddle on the path."],
    "put":    ["Please put your shoes by the door.","He put the book back on the shelf.","She put a flower in her hair.","I put my lunch in my backpack."],
    "round":  ["The ball is big and round.","We walked round the pond at school.","She drew a round face with a smile.","The moon looks full and round tonight."],
    "some":   ["May I have some water, please?","We picked some flowers in the garden.","She gave me some of her grapes.","There are some birds on the fence."],
    "stop":   ["Please stop running in the hallway.","The bus will stop at the next corner.","We need to stop and look both ways.","He did not stop to rest at all."],
    "take":   ["Please take your coat when you leave.","I will take the dog for a walk.","Can you take this to your teacher?","She wants to take her time drawing."],
    "thank":  ["I want to thank you for your help.","We should thank the teacher for the trip.","She wrote a thank you note today.","Please thank him for the nice gift."],
    "them":   ["I gave the crayons back to them.","Tell them to meet us at the park.","We played with them after school today.","She helped them clean up the room."],
    "then":   ["We ate lunch and then went outside.","First read the book, then draw a picture.","He woke up and then brushed his teeth.","She ran fast and then sat to rest."],
    "think":  ["I think the answer is seven.","Do you think it will rain today?","She stopped to think before she spoke.","We think this game is really fun."],
    "walk":   ["We walk to school on sunny days.","The dog loves to walk in the park.","She takes a walk every morning.","I like to walk by the creek."],
    "were":   ["They were happy to see us today.","We were late to school this morning.","The flowers were blooming in the garden.","Her shoes were muddy from the rain."],
    "when":   ["Tell me when you are ready to go.","We sing a song when the bell rings.","She smiles when her friends wave hello.","I feel happy when the sun is out."],
    "with":   ["I like to draw with bright colors.","She played with her friends after lunch.","Come sit with us at the big table.","He shared his lunch with a new friend."],
}

# ── Helper ──────────────────────────────────────────────────────────

def generate_deck(grade: str, n: int) -> list[dict[str, str]]:
    """Return n shuffled flashcard dicts for the chosen grade."""
    word_list = DOLCH_KINDERGARTEN if grade == "Kindergarten" else DOLCH_FIRST_GRADE
    sentences  = KINDERGARTEN_SENTENCES if grade == "Kindergarten" else FIRST_GRADE_SENTENCES
    chosen = random.sample(word_list, min(n, len(word_list)))
    return [
        {"word": w, "sentence": random.choice(sentences.get(w, [f"I see {w}."]))}
        for w in chosen
    ]

# ── Page config ─────────────────────────────────────────────────────
# "centered" keeps content in a comfortable reading column on all devices
st.set_page_config(
    page_title="Sight Word Flashcards",
    page_icon="📖",
    layout="centered",          # ← was "wide" (bad on mobile)
)

# ── CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

/* ── Base ─────────────────────────────────────── */
html, body, .stApp {
    font-family: 'Nunito', sans-serif;
    background: #f0f4ff;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 520px !important;   /* constrain to phone-friendly width */
    margin: 0 auto;
}

/* ── Title ────────────────────────────────────── */
.app-header {
    text-align: center;
    margin-bottom: 0.25rem;
}
.app-title {
    font-size: clamp(1.3rem, 5vw, 1.8rem);
    font-weight: 800;
    color: #1e3a8a;
    margin: 0;
}
.app-subtitle {
    font-size: clamp(0.8rem, 3vw, 0.95rem);
    color: #64748b;
    margin: 0.1rem 0 1rem;
}

/* ── Controls ─────────────────────────────────── */
.controls-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin-bottom: 0.75rem;
}

/* ── Card ─────────────────────────────────────── */
.flashcard {
    width: 100%;
    min-height: clamp(200px, 45vw, 280px);
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: clamp(1.2rem, 5vw, 2.5rem) clamp(1rem, 4vw, 2rem);
    margin: 0.75rem 0;
    user-select: none;
    transition: box-shadow 0.2s ease, transform 0.15s ease;
    animation: cardIn 0.3s ease;
}
@keyframes cardIn {
    from { opacity: 0; transform: scale(0.96); }
    to   { opacity: 1; transform: scale(1); }
}
.flashcard:active { transform: scale(0.98); }

/* Word side — indigo */
.card-word {
    background: linear-gradient(135deg, #3730a3 0%, #4f46e5 100%);
    box-shadow: 0 6px 24px rgba(79,70,229,0.35);
}
/* Sentence side — warm amber */
.card-sentence {
    background: linear-gradient(135deg, #b45309 0%, #f59e0b 100%);
    box-shadow: 0 6px 24px rgba(245,158,11,0.35);
}

.card-word-text {
    font-size: clamp(3rem, 14vw, 5rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    text-align: center;
    letter-spacing: -0.01em;
}
.card-hint {
    font-size: clamp(0.7rem, 2.5vw, 0.85rem);
    color: rgba(255,255,255,0.65);
    margin-top: 1rem;
}
.card-grade-badge {
    font-size: clamp(0.65rem, 2.5vw, 0.8rem);
    font-weight: 700;
    color: rgba(255,255,255,0.8);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.card-sentence-text {
    font-size: clamp(1.2rem, 5vw, 1.7rem);
    font-weight: 600;
    color: #ffffff;
    line-height: 1.55;
    text-align: center;
}

/* ── Progress bar label ───────────────────────── */
.progress-label {
    text-align: center;
    font-size: 0.82rem;
    font-weight: 600;
    color: #475569;
    margin-bottom: 0.2rem;
}

/* ── Done banner ──────────────────────────────── */
.done-banner {
    text-align: center;
    background: linear-gradient(135deg,#059669,#10b981);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    color: white;
    font-size: clamp(1rem, 4vw, 1.25rem);
    font-weight: 700;
    margin: 1rem 0;
    animation: cardIn 0.4s ease;
}

/* ── Buttons ──────────────────────────────────── */
div.stButton > button {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    border-radius: 12px;
    font-size: clamp(0.85rem, 3vw, 1rem);
    padding: 0.5rem 0;
}

/* ── Mobile breakpoint ────────────────────────── */
@media (max-width: 480px) {
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    .flashcard { min-height: 180px; }
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="app-title">📖 Sight Word Flashcards</div>
  <div class="app-subtitle">Dolch Kindergarten &amp; 1st-Grade Lists</div>
</div>
""", unsafe_allow_html=True)

# ── Session state defaults (single source of truth) ─────────────────
DEFAULTS: dict = {"grade": "Kindergarten", "num_words": 20, "index": 0, "flipped": False, "deck": None}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v
if st.session_state.deck is None:
    st.session_state.deck = generate_deck("Kindergarten", 20)

# ── Controls ─────────────────────────────────────────────────────────
grade = st.selectbox(
    "Grade level",
    ["Kindergarten", "1st Grade"],
    index=0 if st.session_state.grade == "Kindergarten" else 1,
    label_visibility="visible",
)
max_words = len(DOLCH_KINDERGARTEN if grade == "Kindergarten" else DOLCH_FIRST_GRADE)
num_words = st.slider("Words this session", min_value=5, max_value=max_words,
                      value=min(st.session_state.num_words, max_words))

if st.button("🔀 Generate New Deck", use_container_width=True, type="primary"):
    st.session_state.deck    = generate_deck(grade, num_words)
    st.session_state.index   = 0
    st.session_state.flipped = False
    st.session_state.grade   = grade
    st.session_state.num_words = num_words
    st.rerun()

# ── Card area ────────────────────────────────────────────────────────
deck = st.session_state.deck
idx  = st.session_state.index
card = deck[idx]
total = len(deck)
done  = (idx == total - 1) and st.session_state.flipped

# Progress
st.markdown(f'<div class="progress-label">Card {idx + 1} of {total}</div>', unsafe_allow_html=True)
st.progress((idx + 1) / total)

# Card HTML
grade_label = "🌱 Kindergarten" if st.session_state.grade == "Kindergarten" else "⭐ 1st Grade"
if st.session_state.flipped:
    card_html = f"""
    <div class="flashcard card-sentence">
        <div class="card-grade-badge">{grade_label}</div>
        <div class="card-sentence-text">{card['sentence']}</div>
        <div class="card-hint">tap · flip to word</div>
    </div>"""
else:
    card_html = f"""
    <div class="flashcard card-word">
        <div class="card-word-text">{card['word']}</div>
        <div class="card-hint">tap · flip to sentence</div>
    </div>"""

st.markdown(card_html, unsafe_allow_html=True)

# Flip button
flip_label = "🔄 Show Word" if st.session_state.flipped else "🔄 Show Sentence"
if st.button(flip_label, use_container_width=True):
    st.session_state.flipped = not st.session_state.flipped
    st.rerun()

# ── Navigation ───────────────────────────────────────────────────────
prev_col, next_col = st.columns(2, gap="small")
with prev_col:
    if st.button("⬅ Previous", use_container_width=True, disabled=(idx == 0)):
        st.session_state.index   -= 1
        st.session_state.flipped  = False
        st.rerun()
with next_col:
    if st.button("Next ➡", use_container_width=True, disabled=(idx >= total - 1)):
        st.session_state.index   += 1
        st.session_state.flipped  = False
        st.rerun()

# ── Completion banner ─────────────────────────────────────────────────
if idx == total - 1:
    st.markdown("""
    <div class="done-banner">
        🎉 You finished the deck! Tap Generate for a new one.
    </div>""", unsafe_allow_html=True)
    st.balloons()
