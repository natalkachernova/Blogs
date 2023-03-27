from flask import render_template, request
from blog import app
from blog.models import Entry
from blog.forms import EntryForm
from . import db


@app.route("/")
def index():
	all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
	return render_template("homepage.html", all_posts=all_posts)

@app.route("/post/<int:entry_id>", methods=["GET", "POST"])
def add_edit_entry(entry_id):
    errors = None
    if (entry_id != 0):
        #Якщо Id не дорівнює 0, то відбувається редагування
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj = entry)
        form_header = "Редагування публікації"
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()
            else:
                errors = form.errors
            all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
            return render_template("homepage.html", all_posts=all_posts)
    else:                           
        #Якщо Id 0, то - додавання
        print(entry_id)
        form = EntryForm()
        form_header = "Нова публікація"
        if request.method == 'POST':
            if form.validate_on_submit():
                entry = Entry(
                    title = form.title.data,
                    body = form.body.data,
                    is_published = form.is_published.data
                )
                db.session.add(entry)
                db.session.commit()
            else:
                errors = form.errors
            all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
            return render_template("homepage.html", all_posts=all_posts)
    return render_template("entry_form.html", form=form, errors=errors, form_header=form_header)