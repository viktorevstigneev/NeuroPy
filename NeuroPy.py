from flask import Flask, Response, redirect, request, url_for, render_template
import time

app = Flask(__name__)


@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            for i in range(100):
                yield 'data: %s\n\n' % (i)
                time.sleep(1)  # an artificial delay

        return Response(events(), content_type='text/event-stream')
    return render_template('index.html')

@app.route('/hi')
def tryToWriteNeroNet():
  return render_template('tryToWriteNeroNet.html')
  
if __name__ == '__main__':
    app.run(debug =True)    