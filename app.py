 #!/usr/bin/python

from flask import Flask, request, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

#Inky imports
import tweepy
import datetime
import os

from inky import InkyWHAT

from PIL import Image, ImageFont, ImageDraw
from font_source_serif_pro import SourceSerifProSemibold
from font_source_sans_pro import SourceSansProSemibold

# Get the current path
PATH = os.path.dirname(__file__)

status = 'true'
client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAEENhQEAAAAACq94yYIo%2B7Sg48evVMepjpxflEM%3Dd6zLmM12lShZhzFFkipjNMlOgjg6144NascYjjXtq5npAUIPXs")

app = Flask(__name__)   # Create an instance of flask called "app"
executors = {
    'default': ThreadPoolExecutor(16),
    'processpool': ProcessPoolExecutor(4)
}

sched = BackgroundScheduler(timezone='Asia/Seoul', executors=executors)

@app.route("/")         # This is our default handler, if no path is given
def my_form():
    global status
    print(status)
    return render_template('index.html', status = status)

@app.route('/process', methods=['POST'])
def process():
    global status
    if status == 'false':
        return jsonify({'error' : 'Missing data!'})
    text = request.form['text']
    print(text)
    status = 'false'
    processed_text = text.upper()
    inkyprint(processed_text)
    status = 'true'
    return jsonify({'error' : 'Missing data!'})

# This function will take a quote as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that quote with newlines to fit into the space required.

def reflow_quote(quote, width, font):
    words = quote.split(" ")
    reflowed = '"'
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n  " + word

    reflowed = reflowed.rstrip() + '"'
    return reflowed

def inkyprint(message):
    # Set up the correct display and scaling factors
    inky_display = InkyWHAT('red')
    inky_display.set_border(inky_display.WHITE)

    # inky_display.set_rotation(180)
    w = inky_display.WIDTH
    h = inky_display.HEIGHT

    # Create a new canvas to draw on
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    # Load the fonts
    font_size = 24
    author_font = ImageFont.truetype(SourceSerifProSemibold, font_size)
    quote_font = ImageFont.truetype(SourceSansProSemibold, font_size)

    # The amount of padding around the quote. Note that
    # a value of 30 means 15 pixels padding left and 15
    # pixels padding right.
    #
    # Also define the max width and height for the quote.
    padding = 50
    max_width = w - padding
    max_height = h - padding - author_font.getsize("ABCD ")[1]
    below_max_length = False

    reflowed = reflow_quote(message, max_width, quote_font)
    p_w, p_h = quote_font.getsize(reflowed)  # Width and height of quote
    p_h = p_h * (reflowed.count("\n") + 1)   # Multiply through by number of lines

    # x- and y-coordinates for the top left of the quote
    quote_x = (w - max_width) / 2
    quote_y = ((h - max_height) + (max_height - p_h)) / 2

    # x- and y-coordinates for the top left of the author
    author_x = quote_x
    author_y = quote_y + p_h

    # Draw red rectangles top and bottom to frame quote
    draw.rectangle((padding / 4, padding / 4, w - (padding / 4), quote_y - (padding / 4)), fill=inky_display.RED)
    draw.rectangle((padding / 4, author_y + (padding / 4) + 5, w - (padding / 4), h - (padding / 4)), fill=inky_display.RED)

    # Add some white hatching to the red rectangles to make
    # it look a bit more interesting
    hatch_spacing = 12
    for x in range(0, 2 * w, hatch_spacing):
        draw.line((x, 0, x - w, h), fill=inky_display.WHITE, width=3)

    # Write our quote and author to the canvas
    draw.multiline_text((quote_x, quote_y), reflowed, fill=inky_display.BLACK, font=quote_font, align="left")
    print(reflowed)

    # Display the completed canvas on Inky wHAT
    inky_display.set_image(img)
    inky_display.show()

def inkybbc():
    global status
    if status == 'true':
        #Get the the latest 5 tweets from BBC (only using 2-3 depending on tweet height
        user_id = 5402612
        response = client.get_users_tweets(user_id, max_results=5)

        # By default, only the ID and text fields of each Tweet will be returned
        tweetone = response.data[0].text
        tweetone = tweetone.replace("\n", " ")
        tweettwo = response.data[1].text
        tweettwo = tweettwo.replace("\n", " ")
        tweetthree = response.data[2].text
        tweetthree = tweetthree.replace("\n", " ")

        # Set up the correct display and scaling factors
        inky_display = InkyWHAT('red')
        inky_display.set_border(inky_display.WHITE)

        # inky_display.set_rotation(180)
        w = inky_display.WIDTH
        h = inky_display.HEIGHT

        # Create a new canvas to draw on
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)

        # Load the fonts
        font_size = 14
        update_font = ImageFont.truetype(SourceSerifProSemibold, font_size)
        tweet_font = ImageFont.truetype(SourceSerifProSemibold, font_size)
        quote_font = ImageFont.truetype(SourceSansProSemibold, font_size)

        # The amount of padding around the quote. Note that
        # a value of 30 means 15 pixels padding left and 15
        # pixels padding right.
        #
        # Also define the max width and height for the quote.
        padding = 50
        max_width = w - padding
        max_height = h - padding
        below_max_length = False

        reflowedtweetone = reflow_quote(tweetone, max_width, quote_font)
        p_w, tweetone_h = quote_font.getsize(reflowedtweetone)  # Width and height of quote
        tweetone_h = tweetone_h * (reflowedtweetone.count("\n") + 2)   # Multiply through by number of lines

        reflowedtweettwo = reflow_quote(tweettwo, max_width, quote_font)
        p_w, tweettwo_h = quote_font.getsize(reflowedtweettwo)  # Width and height of quote
        tweettwo_h = tweettwo_h * (reflowedtweettwo.count("\n") + 2)   # Multiply through by number of lines

        reflowedtweetthree = reflow_quote(tweetthree, max_width, quote_font)
        p_w, tweetthree_h = quote_font.getsize(reflowedtweetthree)  # Width and height of quote
        tweetthree_h = tweetthree_h * (reflowedtweetthree.count("\n") + 1)   # Multiply through by number of lines

        p_h = tweetone_h + tweettwo_h + tweetthree_h

        tweets = reflowedtweetone + "\n \n" + reflowedtweettwo + "\n \n" + reflowedtweetthree

        # x- and y-coordinates for the top left of the quote
        quote_x = (w - max_width) / 2
        quote_y = ((h - max_height) + (max_height - p_h)) / 2

        # x- and y-coordinates for the top left of the author
        author_x = quote_x
        author_y = quote_y + p_h

        # Draw red rectangles top and bottom to frame quote
        draw.rectangle((padding / 4, padding / 4, w - (padding / 4), quote_y - (padding / 4)), fill=inky_display.RED)
        draw.rectangle((padding / 4, author_y + (padding / 4) + 5, w - (padding / 4), h - (padding / 4)), fill=inky_display.RED)

        # Add some white hatching to the red rectangles to make
        # it look a bit more interesting
        hatch_spacing = 12
        for x in range(0, 2 * w, hatch_spacing):
            draw.line((x, 0, x - w, h), fill=inky_display.WHITE, width=3)

        # Write our quote and author to the canvas
        draw.multiline_text((quote_x, quote_y), tweets, fill=inky_display.BLACK, font=quote_font, align="left")

        # slip the updated date in
        now = datetime.datetime.now()
        tweet_update = "Updated: " + now.strftime("%d-%m-%y %H:%M")
        draw.text((250,285), tweet_update, inky_display.RED, update_font)

        # Display the completed canvas on Inky wHAT
        inky_display.set_image(img)
        inky_display.show()
    if status == 'false':
        print("Unable to run BBC task")

@app.cli.command()
def inkytest():
    inky_display = InkyWHAT('red')
    inky_display.set_border(inky_display.WHITE)
    img = Image.open(os.path.join(PATH, "HappyB.png"))
    inky_display.set_image(img)
    inky_display.show()

sched.add_job(inkybbc, 'interval', seconds=3600)

# If we're running this script directly, this portion executes. The Flask
#  instance runs with the given parameters. Note that the "host=0.0.0.0" part
#  is essential to telling the system that we want the app visible to the
#  outside world.
if __name__ == "__main__":
    sched.start()
    app.run(host='0.0.0.0', port=5000)
