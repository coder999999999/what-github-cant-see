# What GitHub Can't See

> An art project. If you're here because the graph caught your eye,
> that's the piece working. See [ABOUT.md](./ABOUT.md) for the plain
> version.

---

I've been watching something happen.

People are gaming the graph. Quietly, then less quietly. A friend with
a cron job. A colleague with an agent. A stranger on the leaderboard
with a contribution history that doesn't quite add up if you look
twice. None of it new, exactly. But the volume is new. The ease is
new. The indifference is new.

At the same time, I kept thinking about all the work that has never
been on GitHub at all.

The review comment that talked someone out of a bad abstraction.
The meeting you made ten minutes shorter. The doc you wrote so three
people wouldn't have to ask. The incident that didn't happen because
you caught it first. The junior you unblocked on a Tuesday afternoon.
The refactor you chose not to do. The scope you cut. The thing you
said no to. The hour you spent staring at a wall until the answer
showed up.

None of it is here. None of it is on any graph. All of it is the job.

So I made this. Partly as a piece. Partly as research — I wanted to
find out whether it was even possible. Whether a single person, on a
laptop, in an afternoon, could convincingly fake the thing an entire
industry treats as evidence. The answer turned out to be yes, easily,
and that answer is most of what the repo is about.

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Nutrition Facts
  Serving size: 1 contribution graph (52 weeks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Amount per serving

  Commits ............................ 126,000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                  % Daily Value *

  Real work ................................ 0%
  Performative output .................. 4,200%
  Reviewed PRs ............................. 0%
  Mentored juniors ......................... 0%
  Said "no" to bad ideas ................... 0%
  Whiteboarded until it made sense ......... 0%
  Caught an incident before it paged ....... 0%
  Deleted more lines than added ............ 0%
  Wrote the doc so nobody had to ask ....... 0%
  Listened ................................. 0%
  Stayed late to explain it again .......... 0%
  Rubber-ducked a teammate ................. 0%
  Cut scope ................................ 0%
  Changed your mind in public .............. 0%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  * Percent Daily Values are based on a career
    that actually produces something. Your
    career may vary.

  Ingredients:
    python, cron, subprocess, a little grief.

  Contains: no real work.
  May contain traces of: things I wanted to
  say out loud but couldn't find the form for.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## The piece

Every green square on this profile for 2024 and 2025 came from this
repository. A script wrote them in under a minute. On those two
years, the lit squares spell **CODER** across the graph — one word,
twice, in the calendar.

There is no product here. No library. No cleverness hidden in the
diffs. The commit history is the artwork. The README is the
placard. The graph is the canvas. That's the whole thing.

## What I was thinking about while making it

Two quiet facts, sitting next to each other.

**One.** It is now trivial to fake the thing we pretend is a
measurement. I did this with a script on a laptop in the time it
takes to make coffee. Other people are doing far more than this,
faster, with agents, every day. The graph was already a thin
signal. It's becoming a decoration.

**Two.** The work I am proudest of in my career mostly doesn't live
on any graph. It lives in conversations, in the things I didn't ship,
in the people who didn't have to ask twice, in the bugs that never
reached production, in the ideas I helped shape that have someone
else's name on them. A graph cannot hold any of that. It was never
built to.

The piece is the gap between those two things. A wall of green that
means nothing, in front of a whole career that means everything, and
no instrument on this site that can tell them apart.

## How to read the graph on my profile

The shape on the graph is what a tool can see.
The space off the graph is what a tool cannot.

Both are me.

---

## What's in here

- `marks.txt` — a single line, overwritten by each commit
- `draw.py`   — the script that produced the history
- `ABOUT.md`  — plain-language notes for anyone who needs them
- this README — the only writing in the repo that took time

---

*The graph is public.
The labor mostly isn't.
Sometimes the labor isn't anything at all.*
