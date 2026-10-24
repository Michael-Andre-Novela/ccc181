# Demo: join-queue form, from issue to merged PR

The finished code is in `my-app/` next to this file. It changes four files and adds one new one:

| File | Change |
|---|---|
| `app.py` | Tickets now have a name; new `/join` route (GET + POST); ticket page finds the position or returns 404 |
| `templates/join.html` | **New.** The form |
| `templates/index.html` | "Join the queue" button, names in the list |
| `templates/ticket.html` | "You are number N in the queue" |
| `static/css/style.css` | Button, form and error styles |

## 1. Open the issue (GitHub, Issues tab, New issue)

- **Title:** Student can join the queue from their phone
- **Description:**
  > As a student, I want to join the queue remotely so that I can wait in class.
  > **Done when:** the student sees their position after joining.
- **Labels:** `feature`, `Must` · **Assignee:** you · **Milestone:** MVP

Note the number GitHub gives it. The steps below use **#1**.

## 2. Branch from an up-to-date main

```
git switch main
git pull origin main
git switch -c feature/join-queue
```

## 3. Commit 1: give tickets a name and a position

In `app.py`:
- Change `TICKETS` to a list of dictionaries (`{"number": 12, "name": "Ana"}`, ...).
- Update the `ticket()` route to loop with `enumerate`, render the ticket and position, and `abort(404)` if it isn't found.
- Add `abort` to the import.

```
from flask import Flask, abort, render_template   # add abort

@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number`
```

- Then update `templates/index.html` (use `t.number` and `t.name`) and `templates/ticket.html`.

**Show in the browser:** `/queue/12` says "You are number 1". Then `/queue/99` gives a 404.


```
git status
git diff
git add app.py templates/index.html templates/ticket.html
git commit -m "Show ticket owner and queue position"
```



## 4. Commit 2: add the form

In `app.py`, add `redirect`, `request` and `url_for` to the import and add the `join()` route. Create `templates/join.html`, add the button to `index.html`, and add the CSS.

### a. `app.py`: the import

```python
from flask import Flask, abort, redirect, render_template, request, url_for
```

- `request` holds what the browser sent, including the submitted form.
- `redirect` sends the browser to a different URL.
- `url_for` builds that URL from a function name, the same way it does in templates.

### b. `app.py`: the `join()` route

Add it below `ticket()`:

```python
@app.route("/join", methods=["GET", "POST"])
def join():
    # GET: show the empty form. POST: the form was submitted.
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template("join.html", error="Please enter your name.")

        number = TICKETS[-1]["number"] + 1 if TICKETS else 1
        TICKETS.append({"number": number, "name": name})
        # Redirect after POST so refreshing the page doesn't join twice.
        return redirect(url_for("ticket", ticket_id=number))

    return render_template("join.html")
```

How it works, line by line:
- **`methods=["GET", "POST"]`**: routes only accept GET by default. Without POST here, submitting the form gives "405 Method Not Allowed".
- **`request.method`**: `"GET"` when you open the page, `"POST"` when you submit the form.
- **`request.form.get("name", "")`** reads the input whose `name="name"`. `.get` with a default gives `""` instead of crashing if it's missing. `.strip()` removes spaces, so a name of only spaces counts as blank.
- **`if not name`**: show the form again with an error message.
- **`TICKETS[-1]["number"] + 1`**: the last ticket's number plus one. The `if TICKETS else 1` handles an empty queue.
- **`TICKETS.append(...)`** adds the new ticket to the end of the list.
- **`redirect(url_for("ticket", ticket_id=number))`** sends the browser to the new ticket's page, for example `/queue/15`.
- **The last `return`** only runs for GET and shows the empty form.

### c. `templates/join.html` (new file)

```
{% extends "base.html" %}

{% block title %}Join the queue · ClinicQ{% endblock %}

{% block content %}
  <h2>Join the queue</h2>

  {% if error %}
    <p class="error">{{ error }}</p>
  {% endif %}

  {# method="post" sends the form to the same URL as a POST request #}
  <form method="post" class="join-form">
    <label for="name">Your name</label>
    <input id="name" name="name" type="text" autofocus>
    <button type="submit">Get a ticket</button>
  </form>

  <p><a href="{{ url_for('index') }}">&larr; Back to the queue</a></p>
{% endblock %}
```

- **`method="post"`** makes the browser send a POST. With no `action`, it goes to the same URL, `/join`.
- **`name="name"`** on the input is the key that `request.form.get("name")` reads. The `id` and `for` only link the label to the box.
- **`{% if error %}`** shows the message only when the route passed one. On a GET, `error` is undefined, so nothing shows.

### d. `templates/index.html`: the button

Add this line above the `<h2>Tickets in the queue</h2>` heading:

```
<p><a class="button" href="{{ url_for('join') }}">Join the queue</a></p>
```

### e. `static/css/style.css`: add at the end

```css
/* Join-queue form */
.button, .join-form button {
  display: inline-block;
  background: var(--teal);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font: inherit;
  text-decoration: none;
  cursor: pointer;
}

.join-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 320px;
}

.join-form input {
  padding: 0.5rem;
  border: 1px solid #C9C4B8;
  border-radius: 6px;
  font: inherit;
}

.error { color: var(--orange); font-weight: 600; }
```

### f. Commit

```
git add app.py templates/join.html templates/index.html static/css/style.css
git commit -m "Add join-queue form"
```

**Show in the browser:**
1. Click **Join the queue** (a GET request shows the empty form).
2. Submit with no name: the error appears.
3. Submit "Dina": you're sent to `/queue/15`, "number 4 in the queue".
4. Go back to `/`: Dina is in the list.

## 5. Push and open the PR

```
git push -u origin feature/join-queue
```

On GitHub, click **Compare & pull request**:
- **Title:** Add join-queue form
- **Description:** what changed, then `Closes #1`

Show the **Files changed** tab, and leave a review comment on a line to show how feedback works.

## 6. Merge and sync

Click **Merge pull request**, then show that issue #1 closed automatically.

```
git switch main
git pull origin main
git log --oneline
```

## Talking points

- **GET vs POST:** the same URL does two jobs. `methods=["GET", "POST"]` allows both, and `request.method` tells them apart.
- **`request.form["name"]`** reads the input whose `name="name"`.
- **Redirect after POST:** without it, refreshing the page would submit the form again and add a duplicate ticket.
- **Auto-escaping:** type `<b>hi</b>` as a name. It shows as text, not bold.
- **Data in memory:** restart the server and the new tickets are gone. That is why the app needs a database (you will set this up later on your own applications).
