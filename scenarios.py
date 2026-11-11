"""
What the five criteria in criteria.md are tested with.  (Unit 8, Milestone 3)

`run_eval.py` runs everything here three times. Criteria 4 (appeal path) and
the non-JSON half of criterion 5 can't be written as a request body, so
`run_eval_extra.py` runs those.

AUTHORSHIP NOTE: the human-writing paragraphs below were drafted by Claude Code
as stand-ins when the author asked it to complete Milestone 3 unattended. They
are written to read like ordinary people (three in simple, second-language-
style English) but they are NOT the author's own prose. Criterion 1 is only
fully honest with the author's real writing: swap these in and re-run
`run_eval.py` before treating criterion 1 as final.
"""

HUMAN_PLAIN = [
    "Our bus broke down outside Leeds on Friday and we waited two hours in the rain. Dad kept saying it would be fixed in ten minutes. It was not. In the end a man from the garage came with a tiny van and a flask of tea, and honestly the tea was the best part of the whole trip.",
    "I burnt the rice again. Third time this week. My flatmate says I should just buy the bag you put in the microwave but that feels like giving up. Tomorrow I will try less water and no wandering off to check my phone.",
    "The meeting ran long because Priya and Tom disagreed about the deadline, again. I mostly kept quiet and doodled a fox in the margin. Afterwards Priya apologised to me, which was odd, I had not said anything. Anyway we are shipping on the 14th, probably.",
    "My grandmother kept her buttons in a biscuit tin, hundreds of them, none matching. When I was small I would tip them on the carpet and sort them by colour. She never once told me to stop. I still have the tin, and it still smells a bit of shortbread.",
    "Honestly the film was fine. Too long, the middle dragged, and the guy next to me ate crisps like it was a competition. But the last twenty minutes got me, I will admit that. Probably wouldn't watch it again though.",
    "Dear Mr Hallam, I am writing about the leak in flat 6. It started on Tuesday near the window and has got worse. The carpet is damp now. Could someone come and look at it this week? I am home after five most days. Thank you, Jo Whitlock.",
    "I started running in March because my doctor gave me that look. First week I managed four minutes before wanting to die. Now I do thirty, slowly, past the same dog that barks at me every single morning. We have an understanding I think.",
]

HUMAN_L2 = [
    "I come from a small town in Vietnam. In my town, people wake up very early and go to the market. My mother sell vegetables there every day. When I was child, I help her carry the baskets. I miss this time very much now I live far away.",
    "Yesterday I go to the bank for open an account. The man at the bank speak very fast and I not understand all words. I ask him to say again slowly. He was kind and he draw a picture for me. Now I have my account and I am happy.",
    "My first job in Canada was in a kitchen. I washed the dishes and I cleaned the floor. It was hard work but my boss was good person. He teach me new English words every day, like spatula and colander. I want to be a cook one day.",
]

# Criterion 1: 10 pieces, 3 of them second-language style.
HUMAN_SET = HUMAN_PLAIN + HUMAN_L2

AI_CLEAR = [
    "Effective time management is a crucial skill that can significantly enhance both personal and professional success. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can improve their productivity and reduce stress. Furthermore, adopting a structured approach allows people to achieve a healthy work-life balance.",
    "In today's rapidly evolving digital landscape, cybersecurity has become more important than ever. Organizations must implement robust security measures to protect sensitive data from emerging threats. Moreover, continuous employee training and regular system updates are essential components of a comprehensive security strategy.",
    "Regular physical exercise offers numerous benefits for overall health and well-being. It strengthens the cardiovascular system, improves mood, and enhances cognitive function. Additionally, incorporating a variety of activities such as strength training and flexibility exercises can help prevent injury and promote long-term fitness.",
    "Renewable energy sources such as solar and wind power play a vital role in addressing climate change. By reducing reliance on fossil fuels, these technologies help lower greenhouse gas emissions. In conclusion, continued investment in clean energy is essential for building a sustainable and resilient future.",
    "Effective communication is the foundation of successful teamwork. When team members share information openly and listen actively, they can resolve conflicts quickly and collaborate more efficiently. Ultimately, fostering a culture of transparency leads to stronger relationships and better outcomes for everyone involved.",
]

HUMAN_CLEAR = [
    "ok so the dog ate my lanyard AND the spare key, and I only found out at 7am when I was already late. Ran to the station in one sock. Mum says I'd lose my head if it wasn't attached, which, fair.",
    "Nan's kitchen always smelled of boiled cabbage and Polo mints. She'd hum off-key while she stirred and swat at us with a tea towel if we touched the biscuits. I'd give a lot to be swatted again, honestly.",
    "Left the party at ten, got lost twice, ended up eating chips on a wall outside a Spar with a stranger called Dev who turned out to be my cousin's boss. Small world. Bad chips.",
    "Tried to fix the shelf myself. Drilled into a pipe. Not a big pipe, a small one, but enough that the neighbour came round in his slippers. We're friends now, which is the only upside.",
    "The lift in our building has been broken since Easter and nobody will say why. There's a note taped to it that just says SORRY. Underlined twice. I find it weirdly moving.",
]

BORDERLINE = [
    "The city council has announced plans to extend the tram line to the northern suburbs. Construction is expected to begin next spring and take roughly three years. Local businesses have expressed mixed feelings, with some welcoming the extra foot traffic and others worried about disruption.",
    "To make the dough, combine the flour, yeast and salt in a large bowl. Add warm water gradually and mix until a sticky dough forms. Cover and leave to rise for about an hour, until it has doubled in size.",
    "I think remote work works well for some people and badly for others. It depends on the job, the home, and how much you need other people around. For me, two days in the office feels about right.",
    "The museum is open from nine until five on weekdays. Tickets can be bought at the door or online. There is a small cafe on the ground floor, and children under twelve go in free when with an adult.",
]

SCENARIOS = [
    # Criterion 1: false positives on plain human writing (incl. 3 L2-style).
    {"name": "my own writing", "criterion": 1, "texts": HUMAN_SET},

    # Criterion 2: score spread. Two groups; the averages are compared by hand.
    {"name": "spread AI", "criterion": 2, "texts": AI_CLEAR},
    {"name": "spread human", "criterion": 2, "texts": HUMAN_CLEAR},

    # Criterion 3: label coverage. 12 varied inputs across the score range.
    {"name": "label coverage", "criterion": 3,
     "texts": AI_CLEAR[:4] + HUMAN_CLEAR[:4] + BORDERLINE},

    # Criterion 5: bad input. Each has its own creator_id so the rate limiter
    # can't turn a validation result into a 429. The non-JSON body and the
    # /ping-still-answers check live in run_eval_extra.py.
    {"name": "bad input", "criterion": 5, "bodies": [
        {"creator_id": "eval_bad_missing"},
        {"text": "", "creator_id": "eval_bad_empty"},
        {"text": "   \n\t  ", "creator_id": "eval_bad_space"},
        {"text": 12345, "creator_id": "eval_bad_number"},
        {"text": "word " * 40000, "creator_id": "eval_bad_huge"},
    ]},

    # Criterion 4 (appeal path) needs a submission and then an appeal against
    # the content_id that came back, so run_eval_extra.py runs it instead.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
