
from flask import Flask, request, redirect
from urllib.parse import urlparse, quote
import secrets

app = Flask(__name__)

links = {}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        original = request.form["url"].strip()
        parsed = urlparse(original)

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return "Please enter a valid http or https URL.", 400

        code = secrets.token_urlsafe(8)

        # Make the URL gloriously inefficient
        nonsense = "this-link-is-extremely-long-and-unnecessarily-complicated-" * 3

        links[code] = original
        long_url = request.host_url + "go/" + nonsense + code

        return f"""
        <h1>Congratulations! Your URL is now worse.</h1>
        <p>Original: {len(original)} characters</p>
        <p>New: {len(long_url)} characters</p>
        <p><a href="/go/{nonsense}{code}">Test your new link</a></p>
        <textarea rows="5" cols="70" readonly>{long_url}</textarea>
        """

    return """
    <h1>Negative-Sum Link Shortener</h1>
    <p>Why make links shorter when you can make them worse?</p>
    <form method="POST">
        <input name="url" type="url"
               placeholder="https://hackclub.com" required>
        <button>Make My URL Worse</button>
    </form>
    """

@app.route("/go/<path:slug>")
def go(slug):
    code = slug[-11:]
    original = links.get(code)

    if not original:
        return "Link not found", 404

    return redirect(original)

if __name__ == "__main__":
    app.run(debug=True)
